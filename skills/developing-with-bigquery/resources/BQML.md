# BigQuery ML (BQML) & AI Functions

Rules and syntax standards for BigQuery AI and Machine Learning functions.

## 1. Global Constraints

* **Connection ID**: Use `'DEFAULT'` for the `connection` argument in remote `CREATE MODEL` statements.
* **Dataset Creation**: Use `CREATE SCHEMA IF NOT EXISTS <project>.<dataset>;`.

## 2. Mandatory Function Routing

Function/Use Case         | Required Reference File
------------------------- | ----------------------------------------------
**AI.FORECAST**           | [ai-forecast.md](../../../skills/developing-with-bigquery/resources/ai-forecast.md)
**AI.EVALUATE**           | [ai-evaluate.md](../../../skills/developing-with-bigquery/resources/ai-evaluate.md)
**AI.GENERATE_TABLE**     | [ai-generate-table.md](../../../skills/developing-with-bigquery/resources/ai-generate-table.md)
**AI.GENERATE_EMBEDDING** | [ai-generate-embedding.md](../../../skills/developing-with-bigquery/resources/ai-generate-embedding.md)
**Remote Models**         | [remote-models.md](../../../skills/developing-with-bigquery/resources/remote-models.md)
**CONTRIBUTION_ANALYSIS** | [ml-contribution-analysis.md](../../../skills/developing-with-bigquery/resources/ml-contribution-analysis.md)
**VECTOR_SEARCH**         | [vector-search.md](../../../skills/developing-with-bigquery/resources/vector-search.md)

## 3. Mandatory Syntax Checks

* **Table-Valued Functions (TVFs)**: `AI.GENERATE_TABLE`, `AI.FORECAST`, `AI.EVALUATE`, and `AI.GENERATE_EMBEDDING` MUST be placed in the `FROM` clause.
* **Named Arguments**: `AI.FORECAST` and `AI.EVALUATE` require the `=>` operator for optional arguments.
* **The "Prompt" Alias**: For `AI.GENERATE_TABLE`, the input subquery must contain a column aliased as `prompt`.
* **Schema Quotes**: Ensure the `output_schema` string is enclosed in quotes.

## 4. Model Selection

* **Time-series**: `AI.FORECAST` uses **TimesFM** endpoints.
* **Generative**: `AI.GENERATE_TABLE` uses **Gemini** endpoints.
* **Freshness**: Prefer current models (e.g., `gemini-2.5-flash`) over deprecated ones.
