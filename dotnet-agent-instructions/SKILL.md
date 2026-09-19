---
name: dotnet-agent-instructions
description: Installs or updates project-level skill routing and self-review instructions for projects using this C#/.NET/MAUI skill collection. Use when adding the marked block to `AGENTS.md`, `CLAUDE.md`, or an explicitly named instruction file. Do not use to review or modify production code itself.
---

# .NET Agent Instructions

## Scope

Install a small project-level block that routes C#, .NET, and applicable MAUI changes to this
skill collection and requires a final self-review.

Preserve all existing project instructions. Never replace an entire instruction file.

## Target File

- Use an explicitly named target file when the user provides one.
- Otherwise update root `AGENTS.md` when it exists.
- If root `AGENTS.md` is absent but root `CLAUDE.md` exists, update `CLAUDE.md`.
- If neither exists, create root `AGENTS.md`.
- If both exist and the user did not choose, update only `AGENTS.md`.

## Install Workflow

1. Inspect the target file before changing it.
2. Add or update the marked `.NET Skill Routing and Self-Review` block.
3. Preserve unrelated instructions.
4. Do not infer Clean Architecture or DDD; only the project's main instructions can activate them.
5. Review the target-file diff before finalizing.

Prefer the bundled idempotent installer. Run it from the target repository root, resolving the
script path relative to this skill directory:

```bash
python /path/to/dotnet-agent-instructions/scripts/install-agent-instructions.py
```

Pass `--file CLAUDE.md` or another path when the user requests a specific target.

## Instruction Block

```md
<!-- dotnet-skills:self-review:start -->
## .NET Skill Routing and Self-Review

For C#, .NET, or .NET MAUI changes, apply the relevant skills while implementing. Review the final
diff against them and fix meaningful findings before finalizing.

- Clarify uncertain domain behavior first with `dotnet-domain-clarification`.
- Use `csharp-readable-code` for production C#.
- Use `dotnet-solid-review` for non-trivial design or implementation, responsibility boundaries,
  refactoring, explicit code/design reviews, and final self-review. Read its software-design
  principle reference and apply only principles relevant to the code.
- Use `dotnet-testing` for ordinary tests and `maui-ui-testing` for device/emulator UI tests.
- Use `dotnet-logging-exceptions` when logging or exceptions change.
- Use `maui-application` for MAUI presentation or platform code.
- Use `dotnet-clean-architecture` or `dotnet-ddd-architecture` only when the main project
  instructions explicitly activate that architecture.
- Keep cleanup scoped to the requested change.
- In self-review findings, name the applicable principle canonically. Do not enumerate principles
  without a material finding; a clean review may say that none was found.
<!-- dotnet-skills:self-review:end -->
```
