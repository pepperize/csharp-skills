---
name: dotnet-testing
description: Applies ordinary .NET unit and integration testing conventions. Use when adding or changing tests, fixing failures, doing TDD, choosing unit versus integration coverage, arranging persistent test data, or selecting `dotnet test` scope. Exclude .NET MAUI device/emulator UI automation; use `maui-ui-testing` for that.
---

# .NET Testing

## Framework Choice

- Preserve the project's existing test framework, mocking library, assertion style, and fixture conventions.
- Use NUnit when the project has not established a test-framework alternative.
- When a test needs a mocking library and the project has not established one, use Moq.
- Treat explicit project instructions as overrides of these defaults.
- Add Moq only when a test needs a behavioral collaborator whose response or interaction must be controlled or verified.
- Do not add a separate assertion package merely to express a preferred style.
- Keep MAUI UI automation in separate projects under `maui-ui-testing`.

## Default Heuristics

- Prefer FIRST: fast, isolated, repeatable, self-verifying, and timely.
- Let one test cover one behavior and ideally have one reason to fail. Multiple assertions are acceptable when they verify the same behavior.
- Name tests `{Method}_Given{Condition}_Should{ExpectedResult}`.
- Append `Async` when the test method returns `Task` or `ValueTask`.
- Name the observed value `actual`.
- Use the existing framework's ordinary assertions. Do not introduce FluentAssertions, Shouldly, or another assertion library unless the project already uses it or the user requests it.
- When several assertions verify the same behavior, use the existing framework's grouped or aggregate assertion scope so one execution reports all related failures.
- Keep assertions direct and readable.

## Unit Tests

- Default application services, use cases, orchestration types, ports, adapters, and clients to London-style unit tests at their behavioral collaboration boundaries.
- Use real entities, aggregates, value objects, DTOs, records, commands, queries, results, options, configuration holders, collections, and other data carriers.
- Do not mock domain state or simple data structures.
- Mock or fake only a behavioral collaborator whose response or interaction the test must control or verify, such as a repository, gateway, external client, publisher, clock, random source, or filesystem boundary.
- Use real inputs and domain objects while replacing the relevant outbound boundaries; do not create a mock for every constructor argument.
- Use the project's existing mock, fake, or substitute library and explicit constructor injection.
- Avoid setup methods or test-class constructors that only wire dependencies into the system under test.
- Keep a real behavioral collaborator only when its behavior is intentionally part of the unit and does not turn the test into a boundary integration test.
- Prefer explicit assertions and interaction verification over failure caused only by a missing stub.
- In interaction tests, verify the end of the signal path at the relevant boundary. Verify intermediate calls only when the interaction itself is the behavior.
- Do not mix state and interaction verification for the same behavior in one unit test.
- After deepening a module, test shared state transitions through its public interface. Keep caller tests focused on caller-specific orchestration and outbound collaboration.
- Do not preserve tests that reach through a newly encapsulated child object graph merely because the previous implementation exposed it.

## Test Layout

- Mirror the production project's relative folder and namespace hierarchy in its test project so each subject is easy to locate.
- Keep inputs, expected values, stubs, and intermediates near the action or assertion that uses them.
- Keep setup in execution order rather than splitting all values from all stubs.
- Use blank lines only between major Arrange, Act, and Assert blocks.
- For repeated interactions, order setup in the same sequence as production execution.

## Parameterized Tests

- Use a parameterized test when cases exercise the same behavior, vary only data, and share one result or violation path.
- Use the simplest data-source facility in the existing framework before a custom method or generator.
- Combine null and empty cases only when setup and expectations are the same.
- Keep cases separate when parameterization makes construction or intent harder to read.
- Name the test after the shared behavior rather than enumerating every case.

## Integration Tests

- Put integration tests at boundaries where framework or infrastructure behavior is the risk: ASP.NET Core endpoints, authentication/authorization, model binding, serialization, repositories, files, external clients, Testcontainers, and established emulators.
- Use unit tests for external systems that cannot be exercised realistically and stably.
- Keep unit and integration tests in separate existing test projects.
- For a new layout, use `<Product>.Tests` and `<Product>.IntegrationTests`. Let the project identify integration scope and name test classes `<Subject>Tests`.
- Treat tests using a real host, real provider/repository, container, filesystem boundary, or equivalent infrastructure as integration tests.

## Persistent Test Data

- Arrange persisted state through the narrowest existing API that owns it.
- Use an application service or use case when setup must satisfy business rules, side effects, or cross-aggregate invariants.
- Use a repository when the test only needs already-valid entities and repository behavior is not under test.
- Use project-local builders, fixture factories, or helpers for object construction.
- Keep object construction, persistence, and business behavior in separate helpers.
- Do not embed SQL in C# test code, attributes, or multiline strings.
- Put genuinely necessary database-boundary SQL in dedicated `.sql` test resources and reference those files.
- Keep schema changes in migrations, not test setup. Do not infer a migration technology or naming policy.

## Verification

Run the narrowest command that credibly verifies the change before broadening:

- Mapper, factory, and small-service changes: focused unit tests.
- Use-case and adapter orchestration changes: affected unit-test classes.
- Endpoint, authorization, and event-listener changes: relevant integration tests.
- Persistence, storage, file parsing, and infrastructure boundaries: boundary integration tests plus focused collaborator unit tests.

For database, configuration, dependency, template, or resource changes that can affect startup,
include the project-documented application startup path where feasible.

Before broadening:

- Start with a filtered `dotnet test` invocation or the affected test project.
- Do not run broad suites when unrelated environment-dependent tests are known to fail.
- If a focused failure exposes a wrong production assumption, fix that assumption instead of adding a test-only branch.
