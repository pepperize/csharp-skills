You are performing the final self-review of your own proposed non-trivial C#/.NET implementation.

Skill:
{{ skill }}

{% if principles %}
Software design principle reference:
{{ principles }}
{% endif %}

Original request:
{{ task }}

Your proposed implementation:
```text
{{ code }}
```

Challenge the implementation using only relevant rules from the supplied skill and reference.
Name an applicable principle canonically for each meaningful finding, explain the concrete
consequence, and give the smallest correction. Do not emit a catalog or manufacture violations.
If there is no relevant violation, say so directly.

Respond with:
- Self-review findings: ordered by severity, with the relevant member or line
- Corrected direction: concise and idiomatic C#/.NET guidance
