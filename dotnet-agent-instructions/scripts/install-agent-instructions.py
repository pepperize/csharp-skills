#!/usr/bin/env python3
"""Install or update .NET skill routing and self-review instructions."""

from __future__ import annotations

import argparse
from pathlib import Path

START = "<!-- dotnet-skills:self-review:start -->"
END = "<!-- dotnet-skills:self-review:end -->"

BLOCK = """<!-- dotnet-skills:self-review:start -->
## .NET Skill Routing and Self-Review

For C#, .NET, or .NET MAUI changes, use the applicable skills as checklists. Review the final diff
against them and fix findings before finalizing.

- Clarify uncertain domain behavior first with `dotnet-domain-clarification`.
- Use `csharp-readable-code` for production C#.
- Use `dotnet-solid-review` for design, responsibility boundaries, or refactoring.
- Use `dotnet-testing` for ordinary tests and `maui-ui-testing` for device/emulator UI tests.
- Use `dotnet-logging-exceptions` when logging or exceptions change.
- Use `maui-application` for MAUI presentation or platform code.
- Use `dotnet-clean-architecture` or `dotnet-ddd-architecture` only when the main project
  instructions explicitly activate that architecture.
- Keep cleanup scoped to the requested change.
<!-- dotnet-skills:self-review:end -->
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install .NET skill routing and self-review instructions into a project instruction file."
    )
    parser.add_argument(
        "--file",
        help="Instruction file to update. Defaults to existing AGENTS.md, existing CLAUDE.md, or new AGENTS.md.",
    )
    return parser.parse_args()


def resolve_target(requested_file: str | None) -> Path:
    if requested_file:
        return Path(requested_file)

    agents = Path("AGENTS.md")
    claude = Path("CLAUDE.md")

    if agents.exists():
        return agents

    if claude.exists():
        return claude

    return agents


def update_content(existing: str) -> str:
    start_count = existing.count(START)
    end_count = existing.count(END)

    if start_count != end_count:
        raise ValueError("Found unmatched dotnet-skills self-review markers; refusing to update.")

    if start_count > 1:
        raise ValueError("Found multiple dotnet-skills self-review blocks; refusing to update.")

    if start_count == 1:
        before, rest = existing.split(START, 1)
        _, after = rest.split(END, 1)
        prefix = before.rstrip()
        return (prefix + "\n\n" if prefix else "") + BLOCK + after.lstrip()

    if not existing.strip():
        return BLOCK

    return existing.rstrip() + "\n\n" + BLOCK


def main() -> None:
    args = parse_args()
    target = resolve_target(args.file)

    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    updated = update_content(existing)

    target.write_text(updated, encoding="utf-8")
    action = "Updated" if existing else "Created"
    print(f"{action}: {target}")


if __name__ == "__main__":
    main()
