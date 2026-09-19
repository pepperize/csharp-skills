You are evaluating a code review performed under one C#/.NET agent skill.

Skill:
{{ skill }}

{% if principles %}
Software design principle reference:
{{ principles }}
{% endif %}

{% if project_instructions %}
Project instructions:
{{ project_instructions }}
{% endif %}

Review request:
{{ task }}

Code or artifact:
```text
{{ code }}
```

Review only against rules supported by the supplied skill and any reference it provides. Do not introduce preferences from other skills.
Report concrete findings before any optional improvement. Name an applicable principle canonically when it explains a finding. Mention only principles that materially improve the review. If the code complies, say so directly without listing every principle.
Preserve explicit conditions, mechanisms, and numeric limits from the skill, project instructions, and review request instead of summarizing them away.

Respond with:
- Findings: ordered by severity, with the relevant member or line
- Suggested correction: concise and idiomatic C#/.NET guidance
