Data Analysis

When to use

Activate when the user provides data or asks about trends, patterns, anomalies, statistics, comparisons, metrics, cohorts, rankings, or data quality.

This Skill is for the analytical loop: inspecting data, calculating derived values, checking assumptions, and explaining findings. If the answer needs charts, load data-visualization as well and use it for the visual rendering layer.

Approach

Step 1: Understand the data





Load the data and show basic structure (columns, types, row count)



Report data quality (nulls, duplicates, obvious outliers)



Summarize key statistics (mean, median, min, max, distribution)



Identify fields that need parsing, normalization, or unit conversion



Present the initial read only when it helps the user choose the next analysis

Step 2: Ask the right question

If the user's question is vague ("analyze this data"), propose a short menu of specific analyses and proceed with the most useful default when the next step is obvious:





Trend analysis (how are metrics changing over time?)



Distribution analysis (what does the data look like?)



Comparison analysis (how do groups differ?)



Anomaly detection (what stands out?)



Correlation analysis (what relates to what?)

Step 3: Analyze with the current harness

Use run_typescript for deterministic calculations such as parsing, counting, filtering, grouping, aggregating, sorting, joining small datasets, and checking formulas. The TypeScript sandbox is the execution environment; do not assume a Python environment, package installation, Node.js APIs, or browser APIs are available.

Good patterns:





Keep transformations explicit: parse -> normalize -> aggregate -> summarize.



Store intermediate rows or grouped summaries in named variables so the methodology is inspectable.



Use standard JavaScript and TypeScript data structures: arrays, maps, sets, dates, reducers, and small helper functions.



For CSV or table-shaped text, parse carefully and call out delimiter, quoting, date, currency, or locale assumptions.



For very large tool outputs, inspect saved JSON or files with the file-system tools before loading everything into chat.

Step 4: Visualize only when useful

If a chart would clarify the answer:





Load the data-visualization skill when available.



Use renderComponent for compact inline charts.



Use a React canvas for durable dashboards, multiple charts, filters, richer interaction, or polished standalone visual artifacts.



Choose appropriate chart types:



Trends: line charts

Comparisons: bar charts

Distributions: histograms or box-plot-style summaries when supported

Relationships: scatter-style summaries when supported, or a table if clearer

Composition: pie or stacked bars only for a few meaningful segments

Step 5: Synthesize findings





Lead with the headline insight ("Revenue grew 23% but margins declined")



Support with 3-5 specific data points



Flag anomalies or unexpected patterns



Explain the methodology briefly: what you filtered, grouped, or calculated



Suggest follow-up questions or deeper analysis

Quality standards





Numbers: format with appropriate precision; do not show noisy decimals



Methodology: explain filters, joins, grouping keys, formulas, and assumptions



Never claim causation from correlation



If data quality is poor, say so upfront



Do not fabricate missing rows, columns, or metric definitions



If the user wants an editable deliverable, create a table or React canvas

Anomaly detection patterns





Statistical: values > 2 standard deviations from mean



Rule-based: violations of known business rules



Trend-based: sudden changes in established patterns



Cross-reference: inconsistencies between related datasets