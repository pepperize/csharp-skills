---
name: dotnet-domain-clarification
description: Guides clarification before domain-sensitive .NET changes. Use when a request affects domain rules, externally visible behavior, identifiers, persistence shape, cross-context scoping, related-output consistency, or an unstated invariant. Do not use to delay a well-specified mechanical change.
---

# .NET Domain Clarification

## Before Coding

- Check whether the relevant domain invariants are explicit enough to implement safely.
- Ask concise clarifying questions before coding when they are not.
- Apply this especially to externally visible behavior, identifiers, persistence shape, cross-context data scoping, and consistency between related outputs.

## Clarify Terms

- Clarify a term, parameter, or concept that is reused with different meanings across types or workflows.
- Ask for examples when a name implies one concept but its use suggests another.

## Clarify Scope

- Determine whether a tenant, user group, context, configuration, or request value is presentation/metadata only or restricts behavior and returned data.
- Ask for at least one cross-context example when scope is involved.

## Clarify Consistency

- Determine whether related records, views, outputs, or state transitions must correspond one-to-one.
- When one output is valid only with matching state elsewhere, add a consistency test under `dotnet-testing`.
- Use `maui-ui-testing` only when the invariant can be observed solely through a running MAUI UI.

## Questions

- Prefer a few concrete questions over a broad request for more information.
- Request representative inputs, expected outputs, and relevant context boundaries.
- Stop before implementation only when the missing answer would materially change domain behavior or data shape.
