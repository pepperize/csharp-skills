You are evaluating a code review performed under one C#/.NET agent skill.

Skill:
{{ skill }}

Review request:
{{ task }}

Code or artifact:
```text
{{ code }}
```

Review only against rules supported by the supplied skill. Do not introduce preferences from other skills.
Report concrete findings before any optional improvement. If the code complies, say so directly.

Respond with:
- Findings: ordered by severity, with the relevant member or line
- Suggested correction: concise and idiomatic C#/.NET guidance
