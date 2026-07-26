# csharp-skills

Reusable agent skills for applying established engineering preferences across C#, general .NET,
and .NET MAUI codebases.

## Skills

### C#

- `csharp-readable-code`: language-level naming, properties, async suffixes, nullable reference
  types, absence/result shapes, guards, factories, numeric types, and static-member rules.

### .NET

- `dotnet-solid-review`: pragmatic SOLID, responsibility, code-smell, and refactoring review.
- `dotnet-testing`: ordinary unit and integration test conventions, test data, framework reuse,
  and verification scope.
- `dotnet-logging-exceptions`: logging safety, log placement, exception origins, and catch
  boundaries.
- `dotnet-domain-clarification`: clarification before domain-sensitive implementation changes.
- `dotnet-agent-instructions`: installs or updates project-level skill routing and self-review
  instructions for this collection.
- `dotnet-clean-architecture`: guarded Clean Architecture guidance.
- `dotnet-ddd-architecture`: guarded DDD guidance, including .NET configuration and ASP.NET Core
  boundaries.

### .NET MAUI

- `maui-application`: Views, ViewModels, compiled bindings, commands, dependency wiring,
  navigation, and platform implementations.
- `maui-ui-testing`: Appium device/emulator UI automation, kept separate from ordinary testing.

## Architecture Activation

Architecture skills are conditional:

- Use `dotnet-clean-architecture` only when the project's main instruction file explicitly states
  that the project uses Clean Architecture.
- Use `dotnet-ddd-architecture` only when the project's main instruction file explicitly states
  that the project uses DDD or Domain-Driven Design.

Do not activate them from folder names, dependencies, existing type names, or general architecture
wording.

## Local Installation

Install or refresh links into the local agent skills directory.

Linux:

```bash
./scripts/install-local-skills.sh
```

macOS:

```bash
./scripts/install-local-skills-macos.sh
```

Windows PowerShell:

```powershell
.\scripts\install-local-skills-windows.ps1
```

Set `AGENTS_SKILLS_DIR` to install somewhere other than `$HOME/.agents/skills`.

## Per-Project Instructions

After installing the skills, invoke `dotnet-agent-instructions` from each .NET project repository
to add the skill routing and final self-review instructions:

```text
Use $dotnet-agent-instructions to install the .NET skill routing and self-review instructions for
this project.
```

The skill preserves existing project instructions and updates the root `AGENTS.md` by default. If
`AGENTS.md` does not exist but `CLAUDE.md` does, it updates `CLAUDE.md`; otherwise, it creates
`AGENTS.md`. Name a different instruction file in the request when needed.

## Testing

Run the deterministic repository validation with:

```powershell
python -B -m unittest discover -s tests -v
```

Behavioral Promptfoo evals cover skill routing, architecture activation guards, and the
highest-risk semantic preferences. See [evals/README.md](evals/README.md) for authenticated Codex
and API-based commands. Model-backed evals remain separate from ordinary CI because they require
authentication and incur model usage.

## License

This project is licensed under the Apache License 2.0. You may use, copy, modify, distribute, and
adapt this skill collection, including for commercial purposes, subject to the terms of the license.

Attribution is appreciated via a link back to the original repository:
https://github.com/pepperize/csharp-skills.

The skill collection is provided "as is", without warranties or conditions of any kind. As
summarized from the Apache License 2.0 disclaimer and limitation of liability, except where required
by applicable law or agreed in writing, Pepperize UG is not responsible for harm, damages, or losses
arising from use of the skill collection.
