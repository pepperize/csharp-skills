---
name: dotnet-ddd-architecture
description: Applies Domain-Driven Design boundaries to .NET projects, including application/infrastructure placement, typed configuration, and ASP.NET Core adapter naming. Use only when the main project instructions explicitly state DDD or Domain-Driven Design. Exclude every project without that activation.
---

# .NET DDD Architecture

## Activation Guard

Before applying this skill, inspect the project's main instruction file such as `AGENTS.md`,
`CLAUDE.md`, or its documented equivalent.

Use this skill only when that file explicitly states that the project uses DDD or Domain-Driven
Design. Do not infer activation from folders, type names, dependencies, task wording, or a general
mention of domains.

When the guard is not satisfied, say that `dotnet-ddd-architecture` is not activated and do not
introduce DDD types or boundaries.

## Project Guidance

- Follow the project's own DDD rules and domain documentation first.
- Preserve clear responsibilities between domain concepts, application services, and infrastructure.
- Use `dotnet-domain-clarification` before changing an aggregate, entity, value object, repository, domain service, bounded-context term, or invariant whose rules are missing or unclear.
- Prefer anemic domain models with behavior primarily in services unless there is a strong reason to keep behavior on the entity itself.

## .NET Configuration

- Treat host, container, provider, and options configuration as infrastructure or composition-root code rather than domain/application code.
- Keep framework and third-party wiring focused at the composition boundary.
- Do not create project-owned static service-registration helpers; follow `csharp-readable-code`.
- Use a focused `<Thing>Options` type only for typed configuration binding.
- Keep options holders plain, represent optional values with nullable-reference-type annotations, and validate required values through the project's existing options validation mechanism.
- Keep a framework/provider-owned binding workaround local to infrastructure and document the exception at the affected type.
- Do not prescribe scanning, source generation, or a configuration library when the project has not chosen one.

## ASP.NET Core Boundaries

- Use folders and namespaces that expose a known frontend, backend, admin, or other application side when that distinction is meaningful.
- Do not hide side-specific endpoints or services in a neutral application namespace.
- Align application-layer names with existing route and UI vocabulary instead of inventing synonyms.
- Avoid vague `Public...` and `Admin...` type prefixes when a namespace or route term names the concept more clearly.
- Name controller actions or endpoint handlers mechanically from the HTTP verb, resource, and optional route action.
- Use PascalCase and append `Async` to project-owned `Task`/`ValueTask` handlers.
- Keep domain verbs in application services or use cases rather than endpoint names.

## Request Validation

- Treat HTTP request shape as an input-adapter concern.
- Validate required route/query/body values, mutually required values, syntax, model shape, endpoint-specific unsupported enum values, and HTTP status mapping through the project's established ASP.NET Core boundary mechanism.
- Translate web DTOs, query values, and generated API models into purpose-named application inputs before invoking application services.
- Do not pass nullable parameter combinations into application services to encode different request modes.
- Promote validation into domain/application code only when it is an invariant in the bounded context's language and every caller must satisfy it.
- Do not create a domain concept or domain exception solely for malformed HTTP input.
