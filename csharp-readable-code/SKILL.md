---
name: csharp-readable-code
description: Applies language-level C# readability rules. Use when writing, refactoring, or reviewing production C# types, abstractions, members, naming, properties, async APIs, nullable reference types, absence/result shapes, guards, factories, numeric types, or static members. Do not use for test style, logging policy, architecture, or MAUI UI concerns.
---

# C# Readable Code

## Default Style

- Prefer focused classes, explicit responsibilities, intention-revealing names, readable control flow, and minimal incidental complexity.
- Use design patterns only when they fit a current problem naturally.
- Replace broad utility classes that mix creation, mapping, conversion, logging, or key formatting with cohesive instance collaborators.
- Name a semantically important intermediate result when nesting non-trivial calls would obscure intent.
- Prefer simple words that non-native speakers can understand without looking them up.

## Members And Names

- Use PascalCase for types, properties, methods, and other project-owned public members.
- Represent state and accessors as properties. Do not create getter-like noun methods.
- Name boolean properties and predicates with `Is`, `Has`, `Can`, `Should`, or another phrase that reads as a state or question.
- Name operations with verb phrases. Do not repeat information already carried by the receiver, containing type, or return type unless it distinguishes variants at the call site.
- Append `Async` to project-owned methods that return `Task` or `ValueTask`. Preserve a different name only when a framework contract, interface, or override requires it.
- Classify each new or renamed member as a property, predicate, operation, or construction helper before accepting its name.

## Abstraction Discipline

- Prefer an existing production type when it already represents the data and behavior the caller needs.
- Introduce a class, interface, wrapper, adapter, or view model only for a current requirement that it uniquely owns: behavior, mutable state, an invariant, or non-trivial translation.
- Do not introduce a type that merely copies, renames, or forwards members of another type.
- Do not add members for anticipated future use. Every new production member must serve a current production caller or documented contract.
- Apply the deletion test: if removing the abstraction leaves callers equally simple and does not duplicate meaningful logic, remove it.
- Keep stable behavior over child state with the type that owns those children. Move repeated queries, selections, bulk operations, and child-event handling into it when those behaviors are shared across callers.
- Implement `IEnumerable<T>`, `IReadOnlyList<T>`, or another collection interface only when collection semantics are the type's primary responsibility. Otherwise expose purpose-named queries and operations, and name projections with different ordering explicitly.

## Static Members

- Do not introduce project-owned static methods. They hard-code a concrete implementation that ordinary proxy-based mocking frameworks cannot replace or verify, preventing London-style isolation of callers.
- Use external static APIs directly when they are stable, pure, and deterministic, such as `Math.Abs`.
- Put an external static API behind an injected boundary when it exposes I/O, time, randomness, mutable state, ambient context, service providers, or services.
- For trivial project-owned construction or transformation, use direct expressions or constructors. For non-trivial behavior, use an injected instance collaborator.
- Allow a project-owned static method only when a language, runtime, framework, generated-code, or third-party contract requires it. Keep such an entry point as thin wiring and move decisions into instance collaborators.
- Treat extension methods as static methods. Do not introduce project-owned extension methods to bypass this rule.

## Nullability And Result Shapes

- Enable and honor nullable reference types in new C# projects. In existing projects, follow the established nullable context and improve annotations within the requested scope.
- Return `T?` only when absence is expected, has one unambiguous meaning, and needs no failure details.
- Use the synchronous `Try...` pattern when callers primarily branch on whether a value was found and an `out` value expresses the successful result clearly.
- Use a purpose-named explicit result type when an expected failure has a reason, code, validation details, or multiple outcomes. Prefer this over an asynchronous tuple-shaped `Try` substitute.
- Return a non-null empty collection when there are no items.
- Use a nullable collection only when absence of the collection is a real named state distinct from an empty collection.
- Do not return `null`, `false`, or empty data to hide a failure. Model expected failure explicitly; allow unexpected exceptions to expose the defect at its origin.
- Do not use nullable parameters to select between operation modes. Resolve absence at the boundary, use separate operations, or pass a purpose-named input type.

## Guards

- Use explicit `if` guard clauses and throw a meaningful .NET exception where the invalid state originates.
- Keep transport, UI, and request-shape validation at the relevant boundary.
- Keep domain/application invariant checks in business logic when every caller must satisfy them.
- Do not add a defensive branch for a state that the domain or API contract cannot produce. Ask before weakening a stated invariant.

## Factories And Helpers

- When a class mainly creates one product, name it `<Product>Factory`.
- Name its main instance operation `Create` or `CreateAsync`.
- Prefer direct construction for a value object or record when a factory would only wrap an obvious constructor or fill one obvious member.
- Treat mutable objects whose lifecycle is wholly owned by the caller as constructed state rather than injectable services. Keep direct construction when the caller supplies runtime state to an object it exclusively owns.
- Extract construction into an injected factory when creation policy varies, repeats substantial decisions across callers, needs its own test seam, or ownership belongs outside the caller.
- Remove a helper that merely hides one obvious call unless it enforces an invariant or gives a repeated concept a useful name.

## Data Models And Immutability

- Prefer immutable types for value-like data, metadata, protocol bindings, and other models whose semantics do not require mutation.
- Establish immutable state through constructor parameters, `init`-only properties, or read-only fields.
- Do not expose mutable collections or mutable collaborators from an otherwise immutable type.

## Numeric Types

- Choose a numeric type from the semantic model across the full call chain, not from the first caller's local representation.
- Use `long` for genuinely 64-bit, accumulated, persisted, or contract-defined counts.
- Keep `int` for collection indexing, ordinary collection `Count` values, explicitly bounded domain values, and contracts that require it.
- Update a cohesive count/result model together rather than scattering narrowing or widening conversions downstream.
- Use `var` when the initializer makes the exact local type obvious and the type is not part of a contract, persistence shape, or overflow-sensitive operation.

## Production API Integrity

- Treat project-documented public type and member names and signatures as contracts. Do not rename or relocate them, or change their signatures, as incidental cleanup.
- After changing a signature or introducing a richer result, inspect production call sites before keeping compatibility members.
- Do not keep production constructors, methods, fallbacks, flags, or branches that exist only for tests.
- Keep paired public variants only when a production caller or external contract needs both, and identify that caller.
- Make tests use the production API and construct or mock collaborators explicitly.

## Required Self-Review

Before finalizing changed C# production code:

1. For every new production type, identify its current production callers and the responsibility it owns that no existing type owns.
2. Check whether an existing type already satisfies each new type's callers; remove pass-through types and types whose deletion leaves callers equally simple.
3. For every type that owns child state, inspect callers for repeated loops, filtering, member traversal, or child-event subscriptions that belong behind the type's interface.
4. Review every implemented collection interface and verify that collection semantics are the type's primary responsibility.
5. Review every new or renamed member against its member category and verify that each new member serves a current production caller or documented contract.
6. Check PascalCase, property usage, predicate phrasing, verb-led operations, and `Async` suffixes.
7. Review every static member and call; remove introduced project-owned static methods, allow direct stable pure external calls, and put external static I/O, time, randomness, state, context, or services behind an injected boundary.
8. Check each nullable annotation, empty collection, `Try...` operation, and explicit result against its intended semantics.
9. Remove helpers that only hide an obvious call.
10. Reject defensive handling for impossible states.
