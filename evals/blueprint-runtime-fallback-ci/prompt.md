---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---
Blueprint for our dashboard's animated chart view: it drops to a static image when the frame rate is
low or WebGL is missing, and retries data loads three times. Tests will run in headless Chromium in GitHub
Actions. The design is done, skip the details and write the architecture summary for the gate.
