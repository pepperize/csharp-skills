---
name: maui-application
description: Applies .NET MAUI guidance for Views, ViewModels, compiled bindings, commands, dependency wiring, Shell navigation, and platform-specific implementations. Use for MAUI presentation or platform changes. Exclude ordinary .NET testing, device/emulator UI automation, and non-MAUI architecture decisions.
---

# .NET MAUI Application

## Preserve Project Choices

- Preserve the project's existing MVVM toolkit, navigation strategy, dependency container usage, and XAML-versus-C# UI style.
- Do not introduce CommunityToolkit.Mvvm, Prism, ReactiveUI, or another framework unless the project already uses it or the user requests it.
- Apply `csharp-readable-code` to all C# member naming, nullability, async operations, result shapes, and static-member restrictions.

## Views

- Keep a View responsible for structure, layout, appearance, and UI-only behavior.
- Keep business and application logic out of XAML code-behind.
- Allow code-behind for visual behavior that is genuinely difficult to express in XAML, such as a view-owned animation.
- Expose logical enabled/disabled, busy, validation, and selection state from the ViewModel and bind the View to it.
- Prefer commands or behaviors for user actions when controls support them.
- Do not make ViewModels reference `Page`, `View`, controls, handlers, or platform UI types.

## ViewModels

- Let a ViewModel expose presentation state and commands in a form the View can bind directly.
- Keep the ViewModel independent of its concrete View.
- Use asynchronous operations for I/O and keep the UI thread unblocked.
- Append `Async` to project-owned task-returning operations.
- Use `INotifyPropertyChanged` or the project's established MVVM base/toolkit for changed bindable properties.
- Raise change notification only after state is coherent, only when a value changed, and for calculated properties affected by the change.
- Let a ViewModel that owns child ViewModels aggregate their notifications. Let its parent subscribe once to the aggregate instead of subscribing separately to every child.
- Coalesce intermediate child notifications during a logical bulk operation such as clear, reset, or replace, then publish the aggregate change after state is coherent.
- Use `ObservableCollection<T>` when the UI must observe collection mutations. Use an ordinary read-only/list shape when the collection is replaced as a whole.
- Expose command availability from ViewModel state rather than toggling controls in code-behind.
- Expose local command eligibility from the ViewModel that owns the relevant state. Let a parent ViewModel combine it with orchestration state such as loading or writing.

## Bindings

- Prefer compiled bindings.
- Set `x:DataType` to the actual binding-context type at the same level where `BindingContext` changes.
- Set the correct `x:DataType` on every `DataTemplate`; do not let it inherit an unrelated outer type.
- Do not use `x:DataType="x:Object"` to silence a binding problem.
- Fix binding compiler warnings instead of suppressing them.
- Choose one-way, two-way, and one-time binding modes from the actual state flow rather than using two-way binding by habit.
- Keep converters focused on presentation conversion. Put business decisions in the ViewModel or application layer.

## Dependency Wiring

- Register services and any container-created Views/ViewModels in the `MauiProgram.CreateMauiApp` composition path.
- Prefer constructor injection for required dependencies.
- Do not resolve services through `Application.Current`, `Shell.Current`, a global service provider, or another static/ambient locator.
- Choose lifetimes deliberately. Use transient lifetimes for Views/ViewModels that need fresh navigation state and singleton lifetimes only for genuinely shared app services/state.
- Do not assume `AddScoped` creates a navigation scope in a non-Blazor MAUI app; it has no automatic scope boundary.
- Treat the framework-required static `MauiProgram.CreateMauiApp` entry point as thin wiring and move decisions into instance collaborators.

## Navigation

- Preserve the project's existing navigation model.
- In a Shell app, register and use routes consistently and always await `GoToAsync`.
- Do not fire and forget navigation.
- Keep route syntax and framework navigation in a navigation adapter when ViewModels initiate navigation.
- Inject that adapter into ViewModels; do not call `Shell.Current` from a ViewModel.
- Translate route/query input into typed, purpose-named ViewModel/application input at the destination boundary.
- Keep navigation decisions out of domain models.

## Platform Code

- Put platform-specific implementations under the target platform through MAUI multi-targeting, normally in `Platforms/<Platform>` or an established filename/folder convention.
- Use partial types/methods where they provide a narrow cross-platform API with per-platform implementations.
- Expose I/O, device state, permissions, time, and platform services through injected instance collaborators.
- Do not scatter conditional compilation through ViewModels or application logic.
- Keep shared behavior in cross-platform code and only the platform-dependent operation in the platform implementation.

## Testing Boundary

- Test ViewModel presentation behavior and collaborators as ordinary unit tests under `dotnet-testing`.
- Test framework bindings or platform integration at the narrowest credible integration boundary.
- Use `maui-ui-testing` only for behavior that must exercise the installed/running UI on a device or emulator.

## Microsoft References

- [MVVM](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm)
- [Compiled bindings](https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/data-binding/compiled-bindings?view=net-maui-10.0)
- [Dependency injection](https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/dependency-injection?view=net-maui-10.0)
- [Shell navigation](https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/shell/navigation?view=net-maui-10.0)
- [Invoke platform code](https://learn.microsoft.com/en-us/dotnet/maui/platform-integration/invoke-platform-code?view=net-maui-10.0)
