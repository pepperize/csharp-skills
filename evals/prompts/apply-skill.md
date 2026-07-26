You are evaluating whether a C#/.NET agent skill is followed.

Skill:
{{ skill }}

Task:
{{ task }}

{% if project_instructions %}
Project instructions:
{{ project_instructions }}
{% endif %}

{% if code %}
Code or artifact:
```text
{{ code }}
```
{% endif %}

Apply only rules supported by the skill and the supplied project instructions. Do not invent project constraints.
If the skill is not activated for this project, say so and do not introduce its patterns speculatively.

Respond with:
- Applicable rules: brief bullets
- Result: the requested code, review, questions, or recommendation
