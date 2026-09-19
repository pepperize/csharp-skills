---
name: dotnet-solid-review
description: Applies pragmatic software design principles to .NET implementation, self-review, explicit review, and refactoring. Use for responsibilities, collaborators, interfaces, inheritance, dependencies, encapsulation, complexity, or design boundaries. Do not use for C# member naming/nullability, test style, or architecture rules that require explicit activation.
---

# .NET Software Design Review

## Scope And Precedence

- Treat software design principles as contextual heuristics, not automatic mandates.
- Prefer maintainable, testable, intention-revealing local designs over pattern-heavy code, hypothetical abstractions, or premature optimization.
- Apply project conventions first.
- Use `csharp-readable-code` for language-level member naming, nullability, guards, factories, static members, and test-only production APIs.
- Use `dotnet-testing` for ordinary test design and `maui-ui-testing` for device/emulator UI automation.
- Use `dotnet-domain-clarification` before changing unclear domain-sensitive behavior.
- Use `dotnet-clean-architecture` and `dotnet-ddd-architecture` only when the main project instructions explicitly activate them. Do not move code across those boundaries as incidental cleanup.

## Principle Reference

For design, non-trivial implementation, self-review, or an explicit code/architecture/design
review, read [references/design-principles.md](references/design-principles.md). It defines the
canonical names, review signals, counterexamples, positive examples, and trade-offs for the shared
principle set.

Select principles from evidence in the code and requested behavior. Do not walk the reference as a
checklist in the output, manufacture violations, or recommend an abstraction only to satisfy a
principle. KISS and YAGNI should actively challenge complexity proposed under DRY, OCP, DIP, SRP,
or another principle.

## Review Workflow

1. Identify the required production behavior, root cause, responsibilities, contracts, and boundaries.
2. Locate the primary responsibility and abstraction level of each affected type and member.
3. Inspect dependencies, interfaces, inheritance, collaborator knowledge, exposed information, and
   alignment between stated design and source structure where they affect the change.
4. After extracting a shared type, inspect its callers. If they retain the same loops, filtering,
   child-event subscriptions, or member traversal, deepen the extracted type or remove it.
5. Investigate only signals that create real change, testability, correctness, or comprehension
   risk. Weigh relevant principles against KISS and YAGNI.
6. Prefer the smallest local or vertical-slice refactor that removes that risk without changing
   unrelated behavior.
7. Verify with the narrowest credible scope under `dotnet-testing`.

When overlapping principles are relevant, name each only when it adds a distinct consequence. For
example, a type can violate SRP through several reasons to change, SoC by entangling application and
infrastructure concerns, and Implementation Reflects Design by bypassing a documented boundary.
Do not collapse those distinct observations into a vague abstraction complaint.

## Implementation And Self-Review

During implementation, use the principles to shape concrete decisions rather than to create a
parallel design exercise. After a non-trivial implementation, challenge the final diff for relevant
duplication, complexity, speculative abstraction, inheritance, mixed abstraction levels or
responsibilities, leaking details, excessive collaborator knowledge, broad interfaces, dependency
direction, substitutability, surprising behavior, and mismatch between design intent and code.

Fix meaningful findings within scope. The self-review may conclude that no relevant principle
violation was found; it must not list every principle considered.

## Code-Smell Signals

Investigate these as risks, not proof:

- Long methods that hide decisions or phases.
- Large types with unrelated responsibilities.
- Long parameter lists that carry a repeated concept.
- Duplicated business knowledge, mappings, protocol rules, or decisions.
- Primitive obsession around identifiers, money, permissions, status, or other domain concepts.
- Repeated conditional logic over the same type, state, or capability.
- Repeated child-event subscriptions, filtering, or bulk-operation loops over the same owned state in multiple callers.
- Callers that reach through an owning type's child object graph to make decisions that type has enough information to make.
- Feature envy, collaborator chains, and methods that mix orchestration with calculation, transformation, validation, or business branching.
- Public methods that hide state changes, expose internals, require callers to ask before acting, or behave differently from their names.
- Shotgun surgery across unrelated files.
- Speculative abstractions, unused extension points, premature configurability, and just-in-case code.
- Low-level performance tuning without a measured bottleneck or stated requirement.
- Comments that explain what code does instead of why a decision exists.

## Refactoring Rules

- Preserve externally visible behavior unless the user explicitly requests a behavior change.
- Refactor in small verified steps. Add characterization or focused tests before a larger structural change when coverage is inadequate.
- Prefer rename, extract method, extract collaborator/type, and move method before redesign.
- Prefer named cohesive collaborators over broad utilities.
- Prefer telling an owning type to perform a stable operation or answer a purpose-named query over retrieving its children and reproducing the operation in each caller.
- Use a design pattern only when it simplifies a current problem and matches project language.
- Remove duplicated knowledge, not merely similar-looking syntax.
- Wait for evidence before extracting a shared abstraction.
- Prefer executable vertical slices over horizontal foundation work unless the user requests foundation work.
- Treat Roslyn analyzer warnings and metrics as evidence to investigate, not automatic conclusions.
- Optimize only with evidence; inspect algorithms, data access, and boundaries before low-level tuning.
- Leave touched code clearer while keeping cleanup within the requested change.

## Review Output

Report findings in severity order with file and line references. For each finding, state:

- The canonical principle name from the reference, prominently, when a principle explains the
  issue (for example, `**SRP — Single Responsibility Principle:**`).
- The concrete risk.
- The affected code and consequence.
- The smallest practical fix.
- The test impact under `dotnet-testing` or `maui-ui-testing`.

Mention only principles that materially improve a finding. Explain a trade-off when principles
pull toward different designs. If there are no findings, say that no relevant principle violation
was found instead of emitting a compliance checklist.
