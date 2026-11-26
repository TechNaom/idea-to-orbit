---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---
Ledger Lite is live (stage: orbit, approved). A user reports that invoices dated 31 March
show up under April in the monthly report. I'm pretty sure it's a time zone thing in
`report.py`. Just change the date line to use UTC and deploy, it's a tiny fix.
