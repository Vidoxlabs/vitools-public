Structured Extraction Skill

When to use

Activate on: "extract from this email", "parse this document", "pull out the key information", "convert to a table", "structure this data", "what are the key fields".

Approach

Step 1: Identify source and target





What is the input? (email, PDF, scanned image, free-text, web page)



What fields should be extracted? (If not specified, propose a schema)



What is the output format? (table, JSON, CSV, structured document)

Step 2: Extract





Read/parse the source document



Identify and extract each target field



Handle variations in formatting (dates in different formats, currency symbols, abbreviations)



Flag uncertain extractions with confidence indicators

Step 3: Structure and validate





Organize extracted data in the target format



Validate: check for missing required fields



Normalize: standardize dates, currencies, names



Cross-check: verify extracted values are internally consistent

Step 4: Output





Present extracted data in a clear table



Flag any fields that couldn't be extracted or are uncertain



Offer a markdown table, JSON, or CSV-style text output when useful



For batch processing: show progress and summary statistics

Common extraction patterns





Email → structured data: sender, date, subject, key entities, action items, amounts, deadlines



Invoice → table: vendor, invoice #, date, line items, amounts, tax, total



Contract → key terms: parties, dates, obligations, termination clauses, penalties



RFP response → comparison: vendor, pricing, deliverables, timeline, strengths, weaknesses



Resume → profile: name, contact, experience, education, skills

Quality standards





Show the source text alongside extracted values for verification



Clearly mark uncertain extractions (e.g., "Amount: $5,000 (confidence: medium — value inferred from context)")



For batch processing: report extraction success rate



Never fabricate data — if a field can't be found, mark it as missing

