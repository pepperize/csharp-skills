---
name: maui-ui-testing
description: Applies .NET MAUI device/emulator UI automation guidance with Appium. Use when adding, changing, running, or diagnosing tests that tap, type, navigate, or inspect a running MAUI app. Exclude ViewModel unit tests and ordinary .NET integration tests; use `dotnet-testing` for those.
---

# .NET MAUI UI Testing

## Boundary

- Keep UI automation in projects separate from ordinary unit and integration tests.
- Use UI tests for behavior that depends on real controls, binding, navigation, accessibility identifiers, platform rendering, or full user interaction.
- Keep business rules and ViewModel state transitions under `dotnet-testing` unless the risk exists only in the running UI.
- Preserve the project's existing UI automation stack.
- For a new MAUI UI automation setup, follow Microsoft's current Appium structure and NUnit sample unless project instructions specify otherwise.

## App Preparation

- Give every element that a test must locate a unique, stable `AutomationId`.
- Treat `AutomationId` as a test-automation contract; do not derive selectors from display text that can be localized or changed.
- Handle accessibility semantics separately; do not treat `AutomationId` as a substitute for semantic properties, accessible names, hints, or platform accessibility checks.
- Keep UI-test hooks limited to UI identification and platform launch requirements. Do not add production branches or alternate behavior for tests.
- Apply platform launch configuration required by the actual application id and target platform.

## Project Structure

- Keep shared cross-platform UI flows in shared test code.
- Keep Appium driver setup and genuinely platform-specific tests in platform-specific test projects.
- When creating the current Microsoft-documented layout, use a shared no-targets project linked into runnable Android, iOS, Windows, and/or Mac Catalyst test projects.
- Run a platform-specific project; the shared no-targets project is not independently runnable.
- Keep namespaces aligned where NUnit setup fixtures initialize drivers for linked shared tests.

## Test Design

- Exercise the app as a user would: locate a stable element, interact, and assert the visible result.
- Share a flow across platforms when the product behavior is cross-platform.
- Split a platform-specific test only when platform behavior or capabilities genuinely differ.
- Keep each UI test focused on one user-visible behavior and one coherent reason to fail.
- Capture diagnostics such as screenshots when they materially help diagnose a failure.
- Do not treat UI automation as a substitute for focused unit or boundary integration coverage.

## Execution

- Run against the intended app build on a reachable emulator, simulator, or physical device.
- Verify Appium, the platform driver, SDK/toolchain, app identifier, and deployed app before diagnosing test logic.
- Respect host constraints: iOS and Mac Catalyst require macOS; Windows UI automation requires Windows; Android can run on supported desktop hosts.
- For Android debug builds, account for Fast Deployment when configuring Appium reset behavior.
- Report which platform/build/device was exercised and any platform that was not run.

## Microsoft Reference

- [UI testing with Appium](https://learn.microsoft.com/en-us/dotnet/maui/deployment/ui-testing?view=net-maui-10.0)
- [Appium and NUnit sample](https://learn.microsoft.com/en-us/samples/dotnet/maui-samples/uitest-appium-nunit/)
