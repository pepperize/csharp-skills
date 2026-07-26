You are evaluating multi-skill composition for a C#/.NET/MAUI task.

Available skill catalog:
{{ skill_catalog }}

{% if project_instructions %}
Project instructions:
{{ project_instructions }}
{% endif %}

Task:
{{ task }}

Choose exactly one primary skill and every applicable secondary skill from the catalog.

- The primary skill owns the task's main requested outcome or explicitly activated governing boundary.
- A secondary skill contributes a distinct implementation, safety, or verification checklist to the requested work.
- Include `csharp-readable-code` when production C# is written, refactored, or reviewed under another primary skill.
- Include test, logging, exception, MAUI, and architecture skills only when their trigger is present.
- Include `dotnet-clean-architecture` or `dotnet-ddd-architecture` only when the project instructions explicitly activate it.
- Do not list the primary skill again as a secondary skill.

Respond with exactly:
Primary skill: `<skill-name>`
Secondary skills: `<skill-name>`, `<skill-name>` | none
Reason: <one concise sentence>
