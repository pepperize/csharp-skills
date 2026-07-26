---
name: dotnet-clean-architecture
description: Applies Clean Architecture boundaries to .NET projects. Use only when the project's main instruction file explicitly states that it uses Clean Architecture, especially for use cases, ports, adapters, factories, or boundary refactors. Exclude every project without that explicit activation.
---

# .NET Clean Architecture

## Activation Guard

Before applying this skill, inspect the project's main instruction file such as `AGENTS.md`,
`CLAUDE.md`, or its documented equivalent.

Use this skill only when that file explicitly states that the project uses Clean Architecture.

If it does not:

- Say that `dotnet-clean-architecture` is not activated because the main project instructions do not explicitly state Clean Architecture.
- Do not introduce or show `UseCase`, `Port`, or `Adapter` classes or interfaces, even as examples.
- Continue using only the project's established structure and other applicable skills.

Do not infer activation from folders, existing type names, dependencies, task wording, or a user's
general mention of architecture.

## Boundaries

- Preserve clear boundaries between use cases, domain/application logic, ports, and adapters.
- Keep business rules out of technical adapters.
- Keep framework, transport, persistence, and client details out of application use cases.
- Direct dependencies toward the domain or application core.
- Make outer adapters depend on ports and application models rather than making the core depend on adapter types.

## Use Cases

- Let a use case orchestrate business flow and delegate technical concerns to ports or cohesive collaborators.
- Give a use case already-shaped application input.
- Keep request shape, syntax, binding, mutually required values, endpoint-specific enum support, and protocol status mapping at the controller, endpoint, or input-adapter boundary.
- Do not pass nullable parameter combinations into a use case to choose a request mode.
- Use separate PascalCase operations, a purpose-named command record/class, or a small input-adapter decision.
- Keep application/domain invariants in the core when every caller must satisfy them independently of transport.
- Do not let a use case accumulate unrelated creation, conversion, logging, key formatting, or client-specific work.
- Extract cohesive instance factories, selectors, policies, or publishers when orchestration becomes hard to read.

## Adapters And Clients

When each step is non-trivial, prefer this flow around a technical client:

`request factory -> awaited client call -> response-to-domain factory or mapper`

- Use instance collaborators and constructor injection.
- Keep a one-line response mapping inline when extraction would add no clarity.
- Keep transport/provider DTOs at the adapter boundary.
- Apply `dotnet-logging-exceptions` to client failure classification and recovery.

## Naming

- Prefer names that reveal an established architectural role: `UseCase`, `Port`, `Adapter`, `Factory`, `Policy`, `Selector`, or another project term.
- Use an `I`-prefixed C# interface only when an interface is warranted.
- Do not introduce a generic support type when a specific role is available.
- Apply `csharp-readable-code` to PascalCase, `Async` suffixes, nullability, and static-member restrictions.
