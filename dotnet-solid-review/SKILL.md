---
name: dotnet-solid-review
description: Reviews general .NET production design for responsibilities, SOLID risks, code smells, and pragmatic refactoring. Use when designing, reviewing, or restructuring services, collaborators, interfaces, policies, factories, or adapters. Do not use for C# member naming/nullability, test style, or architecture rules that require explicit activation.
---

# .NET SOLID Review

## Scope And Precedence

- Treat SOLID and object-oriented rules as heuristics, not automatic mandates.
- Prefer maintainable, testable, intention-revealing local designs over pattern-heavy code, hypothetical abstractions, or premature optimization.
- Apply project conventions first.
- Use `csharp-readable-code` for language-level member naming, nullability, guards, factories, static members, and test-only production APIs.
- Use `dotnet-testing` for ordinary test design and `maui-ui-testing` for device/emulator UI automation.
- Use `dotnet-domain-clarification` before changing unclear domain-sensitive behavior.
- Use `dotnet-clean-architecture` and `dotnet-ddd-architecture` only when the main project instructions explicitly activate them. Do not move code across those boundaries as incidental cleanup.

## Review Workflow

1. Identify the required production behavior, root cause, responsibilities, contracts, and boundaries.
2. Locate the primary responsibility of each affected type and member.
3. Investigate mixed concerns and hidden assumptions that create real change, testability, or comprehension risk.
4. Prefer the smallest local or vertical-slice refactor that removes that risk without changing unrelated behavior.
5. Verify with the narrowest credible scope under `dotnet-testing`.

## SOLID Checks

### Single Responsibility

- Give a type one clear reason to change.
- Split a real mix of orchestration, mapping, transport, persistence, transactionality, caching, tracing, logging decisions, validation, and business policy.
- Keep related behavior together when splitting would scatter one cohesive concept.
- Keep a method at one clear abstraction level: orchestrate steps or perform focused work, rather than mixing framework calls, dependency traversal, transformation, and dense decisions.

### Open/Closed

- Add an extension point only when variation is real or emerging.
- Use explicit conditionals for simple stable rules.
- Use a policy, strategy, factory, or polymorphism when conditionals repeat, grow, or change independently.

### Liskov Substitution

- Make implementations of one interface honor the same accepted inputs, exception contract, and postconditions.
- Do not require callers to inspect concrete implementation types or handle unsupported ordinary operations.
- Judge inheritance by behavior, not shared structure. Prefer composition unless a framework contract or true substitutable hierarchy requires inheritance.

### Interface Segregation

- Keep interfaces and ports focused on what their callers need.
- Split an interface when implementations must stub, ignore, or reject unrelated members.
- Expose caller-needed behavior and semantics, not implementation structure.
- Follow the `I` prefix for a C# interface when the project does not establish another convention.

### Dependency Inversion

- Depend on a stable abstraction when concrete infrastructure would make business/application behavior hard to test or change.
- Prefer constructor injection for required collaborators.
- Avoid hidden construction, dependency lookup, ambient context, and global or static service access.
- Keep host, container, and framework wiring APIs at the composition boundary.
- Review single responsibility before hiding a constructor with many required collaborators.
- Do not add an interface merely to satisfy a principle. A stable, local, testable concrete collaborator can be appropriate.
- Keep framework, transport, persistence, and third-party details out of core behavior only where the activated project architecture requires that separation.

## Code-Smell Signals

Investigate these as risks, not proof:

- Long methods that hide decisions or phases.
- Large types with unrelated responsibilities.
- Long parameter lists that carry a repeated concept.
- Duplicated business knowledge, mappings, protocol rules, or decisions.
- Primitive obsession around identifiers, money, permissions, status, or other domain concepts.
- Repeated conditional logic over the same type, state, or capability.
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
- Use a design pattern only when it simplifies a current problem and matches project language.
- Remove duplicated knowledge, not merely similar-looking syntax.
- Wait for evidence before extracting a shared abstraction.
- Prefer executable vertical slices over horizontal foundation work unless the user requests foundation work.
- Treat Roslyn analyzer warnings and metrics as evidence to investigate, not automatic conclusions.
- Optimize only with evidence; inspect algorithms, data access, and boundaries before low-level tuning.
- Leave touched code clearer while keeping cleanup within the requested change.

## Review Output

Report findings in severity order with file and line references. For each finding, state:

- The concrete risk.
- The affected responsibility or SOLID principle.
- The smallest practical fix.
- The test impact under `dotnet-testing` or `maui-ui-testing`.
