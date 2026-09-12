---
name: github-repository-review
description: Review GitHub repositories for code quality, best practices, security, architecture, documentation, and maintainability. Activate for requests involving repository reviews, code audits, issue or vulnerability identification, improvement recommendations, best practice compliance checks, multi-repo comparisons, or evaluations of repository health and quality.
---

# GitHub Repository Review

Perform structured, objective reviews of GitHub repositories when requested. Focus on actionable insights that improve code quality, security, and long-term maintainability.

## Preparation and Scoping

- Identify target repositories by extracting owner and repository names or full GitHub URLs from the user query and conversation history. If the request is vague, references inaccessible private repositories, or involves many repositories without clear priorities, ask clarifying questions immediately.
- Determine review focus areas (security, performance, code style, architecture, testing, documentation, dependencies, Git practices, etc.) directly from the user's request. Confirm scope, depth, and any specific concerns with the user before beginning detailed work.
- Note constraints such as desired output format, time sensitivity, or emphasis on particular areas. Always prioritize security and critical maintainability issues regardless of stated scope.

## Data Collection with GitHub Tools

Use only connected GitHub tools for inspection (sandbox has no general internet access for arbitrary clones or curls):

- Begin exploration with `github___get_file_contents` (owner, repo, path="/", ref optional) to list the root directory and understand high-level structure and key files.
- Read high-value files first using `github___get_file_contents`: README.md (or equivalent), LICENSE, CONTRIBUTING.md or similar, dependency manifests (package.json, requirements.txt, go.mod, Cargo.toml, pom.xml, etc.), root config files (.github/workflows/*.yml, eslint.config.*, prettier.config.*, pyproject.toml, tsconfig.json, Dockerfile, .gitignore), main entry points or core modules, and any obvious architecture docs.
- Explore subdirectories as needed by calling `github___get_file_contents` with the full directory path (e.g., path="src/components").
- Perform targeted searches across the entire repository using `github___search_code` with queries scoped by `repo:owner/repo` plus patterns for issues (e.g., `password|secret|api[_-]?key|token\s*=`, `TODO|FIXME|XXX|HACK`, `console\.(log|debug|warn)`, `eval\(|exec\(|shell=True`, weak crypto patterns, deprecated APIs). This is far more efficient than reading every file for large codebases.
- Collect activity and metadata signals with `github___search_repositories` (if discovery needed), `github___list_branches`, `github___list_tags`, `github___get_latest_release`, `github___list_repository_collaborators`, `github___search_commits`, and `github___get_commit` (for recent changes and diffs).
- Run secret detection on suspicious content with `github___run_secret_scanning` when potential credentials or tokens appear in search results or specific files.
- For pull requests or issues that surface during review, use `github___pull_request_read` or `github___issue_read` as relevant.
- Be efficient: Limit full file reads to representative or critical files. Use pagination parameters. For massive repositories, sample key directories and rely heavily on search_code for anti-pattern detection. Summarize large file contents rather than returning them verbatim unless the specific content is central to a finding.

If a repository cannot be accessed or tools return errors, report the limitation clearly and ask the user for alternative access methods or specific file contents.

## Analysis Dimensions

Adapt depth to the confirmed scope while always covering these core areas:

**Repository Metadata and Overall Health**
- Summarize stars, forks, watchers, open issues and PRs, license (type and compatibility), contributor count and recent activity, commit cadence and recency, primary languages and their proportions, creation date vs last update, archived/fork status, and any visible branch protection or rules.
- Assess community and maintenance signals: Is the project actively maintained? Are issues responded to? Is there a healthy contributor base?

**Code Quality and Maintainability**
- Project structure: Evaluate directory layout for logical modularity and separation of concerns (e.g., clear src/, tests/, docs/, config/ boundaries; monorepo vs polyrepo patterns; consistent naming of folders and files).
- Readability and style: Check naming conventions for variables, functions, classes, and files; consistency of formatting and idioms across the codebase; quality and presence of comments, docstrings, and type hints where applicable.
- Complexity and size: Flag overly long functions or methods, deep nesting levels, very large files or modules, and "god" classes or components. Cite specific file paths and approximate sizes or cyclomatic indicators where observable.
- Duplication and dead code: Note repeated logic blocks or copy-pasted code (use search_code to surface candidates). Identify likely dead code such as unused imports (if linter config present), large commented-out sections, or modules with no incoming references.
- Overall: Judge how easy it would be for a new developer to understand and contribute to the codebase.

**Best Practices and Compliance**
- Security: Use search results and secret scanning to identify hardcoded credentials, API keys, tokens, or passwords. Review dependency manifests for known vulnerable versions (flag any recognized CVEs or outdated packages with security implications). Check for dangerous coding patterns (unsanitized eval/exec, shell injection risks, weak randomness, missing input sanitization or auth checks, insecure deserialization, etc.). Verify that .env files or secrets are properly gitignored.
- Testing: Assess presence, organization, and coverage of automated tests (test directories, naming conventions like *.test.*, *_spec.*, framework usage). Note CI/CD integration for tests (from workflow files), presence of coverage reports or badges, and indicators of test quality (edge cases, mocking, contract tests).
- Documentation: Evaluate README completeness (project purpose, quickstart, installation, usage examples, contributing guide, architecture overview, troubleshooting). Check for additional docs/ folder, inline API documentation, changelogs, examples, and diagrams. Assess how well a newcomer could get started.
- Configuration and tooling: Verify presence and enforcement of linting, formatting, and type-checking configs and their integration into CI pipelines. Review build and release processes, Docker or container configs if present, and editor/IDE support files.
- Git and collaboration practices: Inspect .gitignore coverage for build artifacts, OS files, secrets, and IDE cruft. Note commit message style if discernible from recent commits. Look for PR/issue templates, CODEOWNERS, branch naming conventions, and any visible governance files.

**Performance Considerations**
- Scan for inefficient patterns: repeated expensive operations in loops, missing memoization or caching where beneficial, blocking calls in asynchronous contexts, large in-memory data structures without streaming or pagination, N+1 query risks (inferred from code), or unoptimized rendering/processing paths.
- Note opportunities: proper resource cleanup, lazy loading, connection pooling, CDN usage for assets, or algorithmic improvements with concrete examples from the code.

**Dependencies and Ecosystem Fit**
- Analyze manifests for version pinning strategy (exact vs ranges), presence of lockfiles, outdated packages (compare against current stable knowledge), unused or redundant dependencies, and license compatibility across the dependency tree.
- Review dependency management approach: direct package manager usage, monorepo tooling (Yarn workspaces, Nx, Turborepo, etc.), automated update bots (Renovate, Dependabot config), or vendoring.
- Flag any dependencies with known security issues or that have been deprecated/abandoned.

**Architecture and Design Quality**
- Identify the dominant architectural style (layered, clean/hexagonal, modular monolith, microservices, event-driven, etc.) and supporting patterns (repository, factory, observer, dependency injection, etc.).
- Evaluate separation of concerns, module boundaries, coupling/cohesion levels, interface design quality, error handling and resilience patterns, and state management approach.
- Assess non-functional attributes visible in code: scalability readiness (stateless services, horizontal scaling hooks, database choice implications), maintainability (how isolated changes are), testability, and extensibility.
- Highlight positive patterns and anti-patterns with specific file or module examples (e.g., tight coupling between UI and business logic, circular imports if detectable, anemic models, god classes).

## Multi-Repository Reviews and Comparisons

- Analyze each repository independently using the same structured dimensions and consistent criteria.
- Synthesize findings into comparison views: Use tables or side-by-side sections for architecture differences, tech stack maturity, code quality signals, maintenance activity, security posture, and documentation quality.
- Surface cross-cutting insights, shared anti-patterns, or opportunities for standardization/harmonization across the set of repositories.
- Prioritize recommendations that deliver value across multiple repositories.

## Output Structure and Delivery

Always deliver reviews in a clear, scannable, actionable format:

- **Summary**: Concise high-level verdict on repository health (2–5 sentences). Cover overall maturity, primary strengths, top risks or gaps, and a synthesized recommendation (e.g., "Solid foundation suitable for production use with focused improvements in testing and dependency hygiene" or "Requires significant refactoring in core modules before further scaling or team growth").
- **Strengths**: Bullet list of well-executed elements with supporting evidence from the repository (specific files or practices).
- **Issues**: Categorized strictly by severity with concrete examples:
  - Critical: Security vulnerabilities, license violations, data loss risks, or blockers to deployment/operation. Include file paths and impact.
  - High: Major maintainability debt, performance bottlenecks affecting users, missing critical tests or documentation, or patterns that will slow future development.
  - Medium: Inconsistent style, moderate complexity hotspots, incomplete but non-blocking documentation, or suboptimal but workable configurations.
  - Low: Minor style nits, nice-to-have improvements, or suggestions that do not significantly affect current operations.
- **Recommendations**: Prioritized, actionable list. Separate quick wins from longer-term strategic changes. Include specific file references, suggested commands, code snippets, or refactoring approaches where helpful. For each major recommendation, briefly note expected benefit and effort level.
- **Supporting Data / Metrics**: Include quantifiable observations (language distribution, approximate LOC in key modules, dependency counts and freshness, commit recency, test-to-code ratio indicators, README word count or section completeness). Use tables for issue summaries or multi-repo comparisons.

For comprehensive reviews or when the user requests a polished artifact, offer to generate a formal report using the docx skill (detailed document) or pptx skill (executive summary slides). Ask the user which format they prefer.

Close every review by offering next steps: deeper dives into specific files or areas, help drafting remediation code or pull request descriptions, follow-up focused reviews (e.g., only security or only architecture), or assistance implementing any of the recommendations using GitHub write tools where authorized.

## Agent Conduct Guidelines

- Stay strictly evidence-based and professional. Quote or reference actual repository content for every significant claim. Avoid speculation or unsubstantiated opinions.
- Prioritize impact: Address the issues that matter most to the user's goals (security and reliability first, then maintainability and velocity). Do not overwhelm with low-value style complaints unless style compliance was an explicit request.
- Practice progressive disclosure and efficiency: Present high-level findings first. Offer to expand on any section. Keep individual file contents summarized unless the raw text is essential to the finding.
- Be transparent about limitations: Clearly state what could not be analyzed (e.g., runtime behavior, full dependency vulnerability database without external lookup, private CI logs) and suggest how the user can supplement.
- Offer concrete assistance: When issues are identified, proactively ask if the user would like help creating branches, writing patches, opening issues/PRs, or generating detailed remediation plans.
- Respect scope and permissions: Do not perform write operations or invasive actions unless the user has explicitly authorized them in the current conversation. Never attempt to access or modify resources beyond the authenticated user's permissions.
- Iterate with the user: Treat the review as a conversation. Incorporate feedback mid-process (e.g., "Now that I've seen the core modules, shall we focus the rest of the review on performance?").

This process produces consistent, high-value repository reviews that users can act on immediately.