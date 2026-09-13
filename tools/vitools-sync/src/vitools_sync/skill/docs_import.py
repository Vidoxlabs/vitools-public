"""
Documentation Importer for ViTools.

Fetches documentation from various sources (Context7, web URLs, etc.)
and generates concept cards and skills.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

from vitools_sync.paths import repo_root
from vitools_sync.skill.concept import create_concept_card, ConceptCardConfig, validate_concept_card_data
from vitools_sync.skill.create import create_skill_from_template, CreateSkillConfig
from vitools_sync.skill.validate import validate_skill


@dataclass
class DocsImportConfig:
    """Configuration for documentation import."""

    # Input
    url: Optional[str] = None  # URL to fetch documentation from
    file_path: Optional[Path] = None  # Local file path
    text: Optional[str] = None  # Raw text content

    # Processing options
    source: str = "web"  # Source type: web, context7, file
    extract_methods: bool = True  # Extract API methods/endpoints
    extract_examples: bool = True  # Extract usage examples
    generate_concept_card: bool = True  # Generate concept card
    generate_skill: bool = True  # Generate skill
    template: str = "api-integration"  # Template to use

    # Output
    output_dir: Optional[Path] = None  # Output directory
    dry_run: bool = False  # Don't create files


@dataclass
class ExtractedContent:
    """Content extracted from documentation."""

    title: str = ""
    description: str = ""
    methods: list[str] = field(default_factory=list)
    endpoints: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    parameters: list[str] = field(default_factory=list)
    authentication: str = ""
    rate_limits: str = ""
    evidence_url: str = ""


def extract_from_text(text: str, url: Optional[str] = None) -> ExtractedContent:
    """Extract structured content from documentation text."""
    content = ExtractedContent()
    content.evidence_url = url or ""

    # Extract title (first H1)
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if title_match:
        content.title = title_match.group(1).strip()

    # Extract description (first paragraph after title)
    desc_match = re.search(r"^#\s+.+$\s*\n\s*([^\n]+)", text, re.MULTILINE)
    if desc_match:
        content.description = desc_match.group(1).strip()

    # Extract code blocks as examples
    code_blocks = re.findall(r"```(?:\w*\n)?([\s\S]+?)```", text)
    for i, block in enumerate(code_blocks):
        cleaned = block.strip()
        if cleaned and len(cleaned) < 500:  # Only short examples
            content.examples.append(cleaned)

    # Extract HTTP methods (GET, POST, PUT, DELETE)
    methods = re.findall(r"\b(GET|POST|PUT|DELETE|PATCH)\b", text, re.IGNORECASE)
    content.methods = list(set(methods))

    # Extract endpoints (URL paths)
    endpoints = re.findall(r"(/[\w/\-]+)", text)
    content.endpoints = list(set(endpoints))

    # Extract authentication info
    auth_match = re.search(r"(authentication|auth|token|api key|bearer)", text, re.IGNORECASE)
    if auth_match:
        content.authentication = "Required (see documentation)"

    # Extract rate limit info
    rate_match = re.search(r"(rate limit|limit|throttle|quota)", text, re.IGNORECASE)
    if rate_match:
        content.rate_limits = "See documentation for details"

    return content


def fetch_from_url(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch content from a URL."""
    try:
        import urllib.request
        from urllib.error import URLError, HTTPError

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "ViTools-Docs-Importer/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8")
    except (URLError, HTTPError, ValueError) as e:
        print(f"Warning: Could not fetch URL {url}: {e}")
        return None


def fetch_from_context7(query: str, timeout: int = 30) -> Optional[str]:
    """Fetch documentation from Context7 MCP."""
    try:
        # Try to use Context7 MCP if available
        # This is a placeholder - actual implementation would use MCP client
        import subprocess
        result = subprocess.run(
            ["npx", "-y", "@upstash/context7-mcp", "--query", query],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass

    return None


def generate_from_docs(
    config: DocsImportConfig,
) -> dict:
    """
    Generate concept cards and skills from documentation.
    
    Args:
        config: Import configuration
    
    Returns:
        dict: Result with status and paths
    """
    repo = repo_root(config.output_dir)
    result = {
        "success": False,
        "content": None,
        "concept_card": None,
        "skill": None,
        "errors": [],
        "warnings": [],
    }

    try:
        # Fetch content
        content_text = None
        if config.url:
            content_text = fetch_from_url(config.url)
            if not content_text:
                result["warnings"].append(f"Could not fetch URL: {config.url}")
        elif config.file_path:
            if config.file_path.exists():
                content_text = config.file_path.read_text()
            else:
                result["errors"].append(f"File not found: {config.file_path}")
        elif config.text:
            content_text = config.text

        if not content_text:
            result["errors"].append("No content to process")
            return result

        result["content"] = content_text

        # Extract structured content
        extracted = extract_from_text(content_text, config.url)

        if not extracted.title:
            extracted.title = "Untitled Documentation"
        if not extracted.description:
            extracted.description = f"Documentation from {config.url or config.file_path or 'input'}"

        # Generate concept card
        if config.generate_concept_card:
            concept_config = ConceptCardConfig(
                name=re.sub(r"[^a-z0-9\-]", "-", extracted.title.lower()).strip("-"),
                domain="API Integrations" if config.template == "api-integration" else "Research",
                intent_patterns=[
                    f"use {extracted.title}",
                    f"interact with {extracted.title}",
                ],
                triggers=[
                    f"user needs {extracted.title} functionality",
                    f"user requests {extracted.title} operations",
                ],
                procedure_pattern=f"Use {extracted.title} API. Call methods. Return results.",
                description=extracted.description,
                evidence_urls=[config.url] if config.url else [],
                priority="medium",
                tags=["documentation", "api"],
            )

            if not config.dry_run:
                concept_result = create_concept_card(concept_config, repo)
                if concept_result["success"]:
                    result["concept_card"] = concept_result["path"]
                else:
                    result["warnings"].extend(concept_result.get("errors", []))
            else:
                result["concept_card"] = "[DRY RUN] Would create concept card"

        # Generate skill
        if config.generate_skill:
            skill_config = CreateSkillConfig(
                name=re.sub(r"[^a-z0-9\-]", "-", extracted.title.lower()).strip("-"),
                template=config.template,
                description=extracted.description,
                domain="API Integrations" if config.template == "api-integration" else "Research",
                summary=f"Use {extracted.title} for operations",
                triggers=[f"User needs {extracted.title} functionality"],
                inputs=["API client"] + extracted.endpoints[:5],
                outputs=["API responses", "Data", "Results"],
                procedure=f"Use {extracted.title} API. Make requests. Process responses.",
                guardrails=f"Validate inputs. Handle errors. {extracted.authentication or 'No authentication required.'}",
                good_examples="\n".join(extracted.examples[:2]),
                bad_examples="User: Request without validation\nOutput: Error or invalid data",
                verification=f"# Validate skill\nvitools-sync skill validate skills/{re.sub(r'[^a-z0-9\-]', '-', extracted.title.lower()).strip('-')}/SKILL.md",
                evidence_urls=[config.url] if config.url else [],
            )

            if not config.dry_run:
                skill_result = create_skill_from_template(
                    name=skill_config.name,
                    template=skill_config.template,
                    description=skill_config.description,
                    domain=skill_config.domain,
                    summary=skill_config.summary,
                    triggers=skill_config.triggers,
                    inputs=skill_config.inputs,
                    outputs=skill_config.outputs,
                    procedure=skill_config.procedure,
                    guardrails=skill_config.guardrails,
                    good_examples=skill_config.good_examples,
                    bad_examples=skill_config.bad_examples,
                    verification=skill_config.verification,
                    evidence_urls=skill_config.evidence_urls,
                )
                if skill_result["success"]:
                    result["skill"] = skill_result["skill_path"]
                else:
                    result["warnings"].extend(skill_result.get("errors", []))
            else:
                result["skill"] = "[DRY RUN] Would create skill"

        result["success"] = True

    except Exception as e:
        result["errors"].append(str(e))

    return result


def generate_from_context7(
    query: str,
    tool_name: Optional[str] = None,
    config: Optional[DocsImportConfig] = None,
) -> dict:
    """
    Generate concept card and skill from Context7 search.
    
    Args:
        query: Search query for Context7
        tool_name: Optional tool name to use
        config: Optional import configuration
    
    Returns:
        dict: Result with status and paths
    """
    if config is None:
        config = DocsImportConfig()

    config.source = "context7"
    config.url = f"context7:{query}"

    # Fetch from Context7
    content = fetch_from_context7(query)
    if not content:
        return {
            "success": False,
            "error": f"Could not fetch documentation for: {query}",
        }

    config.text = content
    return generate_from_docs(config)


def batch_generate_from_urls(
    urls: list[str],
    config_template: Optional[DocsImportConfig] = None,
) -> dict:
    """
    Generate skills from multiple documentation URLs.
    
    Args:
        urls: List of URLs to fetch and process
        config_template: Template configuration to use for each
    
    Returns:
        dict: Summary result
    """
    if config_template is None:
        config_template = DocsImportConfig()

    result = {
        "success": False,
        "total": len(urls),
        "generated": 0,
        "failed": 0,
        "results": {},
        "errors": [],
    }

    for url in urls:
        config = DocsImportConfig(
            url=url,
            source=config_template.source,
            extract_methods=config_template.extract_methods,
            extract_examples=config_template.extract_examples,
            generate_concept_card=config_template.generate_concept_card,
            generate_skill=config_template.generate_skill,
            template=config_template.template,
            output_dir=config_template.output_dir,
            dry_run=config_template.dry_run,
        )

        import_result = generate_from_docs(config)
        result["results"][url] = import_result

        if import_result["success"]:
            result["generated"] += 1
        else:
            result["failed"] += 1
            result["errors"].extend(import_result.get("errors", []))

    result["success"] = result["failed"] == 0
    return result
