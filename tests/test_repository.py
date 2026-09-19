from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TARGET_PREFIXES = ("csharp-", "dotnet-", "maui-")
EXPECTED_EVAL_CASES = 33
DESIGN_PRINCIPLES = (
    "DRY — Don’t Repeat Yourself",
    "KISS — Keep it simple, stupid",
    "FCoI — Favour Composition over Inheritance",
    "IOSP — Integration Operation Segregation Principle",
    "Single Level of Abstraction",
    "SRP — Single Responsibility Principle",
    "SoC — Separation of Concerns",
    "ISP — Interface Segregation Principle",
    "DIP — Dependency Inversion Principle",
    "LSP — Liskov Substitution Principle",
    "Principle of Least Astonishment",
    "Information Hiding Principle",
    "OCP — Open Closed Principle",
    "Tell, Don't Ask",
    "LoD — Law of Demeter",
    "Implementation Reflects Design",
    "YAGNI — You Ain’t Gonna Need It",
)


def skill_directories() -> tuple[Path, ...]:
    return tuple(
        sorted(
            path
            for path in ROOT.iterdir()
            if path.is_dir()
            and path.name.startswith(TARGET_PREFIXES)
            and (path / "SKILL.md").is_file()
        )
    )


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.DOTALL)
    if not match:
        raise AssertionError(f"Missing or invalid frontmatter: {path}")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            raise AssertionError(f"Invalid frontmatter line in {path}: {line}")
        values[key.strip()] = value.strip()
    return values


def parse_quoted_yaml_field(text: str, field: str) -> str:
    match = re.search(rf"^\s*{re.escape(field)}:\s*(\"(?:[^\"\\]|\\.)*\")\s*$", text, re.MULTILINE)
    if not match:
        raise AssertionError(f"Missing quoted YAML field: {field}")
    return json.loads(match.group(1))


def load_agent_installer():
    path = ROOT / "dotnet-agent-instructions" / "scripts" / "install-agent-instructions.py"
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("dotnet_agent_installer", path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot import installer: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SkillStructureTests(unittest.TestCase):
    def test_expected_skill_collection_exists(self) -> None:
        names = {path.name for path in skill_directories()}
        self.assertEqual(
            {
                "csharp-readable-code",
                "dotnet-agent-instructions",
                "dotnet-clean-architecture",
                "dotnet-ddd-architecture",
                "dotnet-domain-clarification",
                "dotnet-logging-exceptions",
                "dotnet-solid-review",
                "dotnet-testing",
                "maui-application",
                "maui-ui-testing",
            },
            names,
        )

    def test_skill_frontmatter_and_length(self) -> None:
        for skill_dir in skill_directories():
            with self.subTest(skill=skill_dir.name):
                skill_path = skill_dir / "SKILL.md"
                text = skill_path.read_text(encoding="utf-8")
                frontmatter = parse_frontmatter(skill_path)

                self.assertEqual({"name", "description"}, set(frontmatter))
                self.assertEqual(skill_dir.name, frontmatter["name"])
                self.assertRegex(frontmatter["name"], SKILL_NAME)
                self.assertIn("Use", frontmatter["description"])
                self.assertRegex(
                    frontmatter["description"],
                    r"Do not use|Exclude|Use only",
                    "Description must contain an explicit exclusion or activation guard",
                )
                self.assertLessEqual(len(text.splitlines()), 500)

    def test_openai_metadata_matches_each_skill(self) -> None:
        for skill_dir in skill_directories():
            with self.subTest(skill=skill_dir.name):
                metadata_path = skill_dir / "agents" / "openai.yaml"
                self.assertTrue(metadata_path.is_file())
                text = metadata_path.read_text(encoding="utf-8")
                display_name = parse_quoted_yaml_field(text, "display_name")
                short_description = parse_quoted_yaml_field(text, "short_description")
                default_prompt = parse_quoted_yaml_field(text, "default_prompt")

                self.assertTrue(display_name)
                self.assertGreaterEqual(len(short_description), 25)
                self.assertLessEqual(len(short_description), 64)
                self.assertIn(f"${skill_dir.name}", default_prompt)

    def test_no_templates_or_generated_python_artifacts(self) -> None:
        excluded_parts = {".git", ".idea"}
        placeholder_pattern = re.compile(
            re.escape("[" + "TODO") + "|" + "Structuring " + "This Skill"
        )
        for path in ROOT.rglob("*"):
            if any(part in excluded_parts for part in path.parts):
                continue
            self.assertNotEqual("__pycache__", path.name)
            self.assertNotEqual(".pyc", path.suffix)
            if path.is_file() and path.suffix in {".md", ".py", ".ps1", ".sh", ".yaml", ".yml"}:
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(placeholder_pattern.search(text))
                self.assertFalse(
                    any(line.endswith((" ", "\t")) for line in text.splitlines()),
                    f"Trailing whitespace: {path}",
                )

    def test_java_terminology_is_absent(self) -> None:
        forbidden = re.compile(
            r"\b(java|spring|junit|mockito|flyway|runtimeexception|bean validation|src/test)\b",
            re.IGNORECASE,
        )
        for skill_dir in skill_directories():
            with self.subTest(skill=skill_dir.name):
                text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                self.assertIsNone(forbidden.search(text))

    def test_design_principle_reference_is_complete(self) -> None:
        path = ROOT / "dotnet-solid-review" / "references" / "design-principles.md"
        text = path.read_text(encoding="utf-8")

        headings = tuple(re.findall(r"^### (.+)$", text, re.MULTILINE))
        self.assertEqual(DESIGN_PRINCIPLES, headings)

        for index, principle in enumerate(DESIGN_PRINCIPLES):
            with self.subTest(principle=principle):
                start = text.index(f"### {principle}")
                end = (
                    text.index(f"### {DESIGN_PRINCIPLES[index + 1]}")
                    if index + 1 < len(DESIGN_PRINCIPLES)
                    else text.index("## Relationships and Trade-offs")
                )
                section = text[start:end]
                for field in (
                    "**Intent:**",
                    "**Review signals:**",
                    "**Typical violation:**",
                    "**Do not apply mechanically:**",
                    "**Negative example**",
                    "**Positive example**",
                ):
                    self.assertIn(field, section)
                self.assertEqual(2, section.count("```csharp"))

        review_skill = (ROOT / "dotnet-solid-review" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("references/design-principles.md", review_skill)
        self.assertIn("explicit code/architecture/design", review_skill)
        self.assertIn("self-review", review_skill)


class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.installer = load_agent_installer()

    def test_documented_and_installed_blocks_match(self) -> None:
        skill_text = (
            ROOT / "dotnet-agent-instructions" / "SKILL.md"
        ).read_text(encoding="utf-8")
        match = re.search(
            r"```md\r?\n(<!-- dotnet-skills:self-review:start -->.*?"
            r"<!-- dotnet-skills:self-review:end -->)\r?\n```",
            skill_text,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        documented = match.group(1).replace("\r\n", "\n")
        installed = self.installer.BLOCK.rstrip().replace("\r\n", "\n")
        self.assertEqual(documented, installed)

    def test_block_update_is_idempotent_and_preserves_surrounding_text(self) -> None:
        before = "# Existing instructions\n"
        after = "\nFinal existing instruction.\n"
        existing = before + "\n" + self.installer.BLOCK + after

        updated = self.installer.update_content(existing)
        self.assertTrue(updated.startswith(before))
        self.assertTrue(updated.endswith("Final existing instruction.\n"))
        self.assertEqual(updated, self.installer.update_content(updated))

    def test_empty_content_receives_exact_block(self) -> None:
        self.assertEqual(self.installer.BLOCK, self.installer.update_content(""))

    def test_unmatched_markers_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.installer.update_content(self.installer.START)
        with self.assertRaises(ValueError):
            self.installer.update_content(self.installer.END)

    def test_duplicate_blocks_are_rejected(self) -> None:
        duplicate_blocks = self.installer.BLOCK + "\n" + self.installer.BLOCK

        with self.assertRaisesRegex(ValueError, "multiple"):
            self.installer.update_content(duplicate_blocks)

    def test_target_selection_order(self) -> None:
        original_directory = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                self.assertEqual(Path("AGENTS.md"), self.installer.resolve_target(None))

                Path("CLAUDE.md").touch()
                self.assertEqual(Path("CLAUDE.md"), self.installer.resolve_target(None))

                Path("AGENTS.md").touch()
                self.assertEqual(Path("AGENTS.md"), self.installer.resolve_target(None))
                self.assertEqual(
                    Path("CUSTOM.md"),
                    self.installer.resolve_target("CUSTOM.md"),
                )
            finally:
                os.chdir(original_directory)

    def test_local_install_manifests_match_skill_directories(self) -> None:
        expected = {path.name for path in skill_directories()}

        shell_text = (ROOT / "scripts" / "install-local-skills.sh").read_text(encoding="utf-8")
        shell_block = re.search(r"skills=\(\r?\n(.*?)\r?\n\)", shell_text, re.DOTALL)
        self.assertIsNotNone(shell_block)
        shell_names = {
            line.strip()
            for line in shell_block.group(1).splitlines()
            if line.strip()
        }

        powershell_text = (
            ROOT / "scripts" / "install-local-skills-windows.ps1"
        ).read_text(encoding="utf-8")
        powershell_block = re.search(
            r"\$skills = @\(\r?\n(.*?)\r?\n\)",
            powershell_text,
            re.DOTALL,
        )
        self.assertIsNotNone(powershell_block)
        powershell_names = set(
            re.findall(r'"((?:csharp|dotnet|maui)-[a-z0-9-]+)"', powershell_block.group(1))
        )

        self.assertEqual(expected, shell_names)
        self.assertEqual(expected, powershell_names)


class EvalHarnessTests(unittest.TestCase):
    def test_eval_catalog_matches_skill_descriptions(self) -> None:
        catalog_path = ROOT / "evals" / "skill-catalog.md"
        self.assertTrue(catalog_path.is_file())
        catalog = {
            name: description
            for name, description in re.findall(
                r"^- `([^`]+)`: (.+)$",
                catalog_path.read_text(encoding="utf-8"),
                re.MULTILINE,
            )
        }
        expected = {
            skill_dir.name: parse_frontmatter(skill_dir / "SKILL.md")["description"]
            for skill_dir in skill_directories()
        }
        self.assertEqual(expected, catalog)

    def test_eval_case_ids_and_references(self) -> None:
        case_root = ROOT / "evals" / "cases"
        case_files = tuple(sorted(case_root.rglob("*.yaml")))
        self.assertEqual(EXPECTED_EVAL_CASES, len(case_files))

        ids: set[str] = set()
        for case_path in case_files:
            with self.subTest(case=case_path.relative_to(ROOT)):
                text = case_path.read_text(encoding="utf-8")
                description = re.search(r"^- description:\s*(.+)$", text, re.MULTILINE)
                metadata_id = re.search(r"^\s+id:\s*(.+)$", text, re.MULTILINE)
                skill_fields = re.findall(r"^\s+skill:\s*(.+)$", text, re.MULTILINE)
                metadata_kind = re.search(r"^\s+kind:\s*(.+)$", text, re.MULTILINE)

                self.assertIsNotNone(description)
                self.assertIsNotNone(metadata_id)
                self.assertTrue(skill_fields)
                self.assertIsNotNone(metadata_kind)
                self.assertEqual(description.group(1), metadata_id.group(1))
                self.assertNotIn(metadata_id.group(1), ids)
                ids.add(metadata_id.group(1))
                self.assertIn(
                    metadata_kind.group(1),
                    {"apply", "compose", "review", "route", "self-review"},
                )

                skill_name = skill_fields[-1]
                if skill_name != "skill-routing":
                    self.assertTrue((ROOT / skill_name / "SKILL.md").is_file())
                    self.assertIn(f"skill: file://../{skill_name}/SKILL.md", text)

    def test_promptfoo_configs_reference_existing_local_files(self) -> None:
        eval_root = ROOT / "evals"
        for config_name in ("promptfooconfig.yaml", "promptfooconfig.api.yaml"):
            config_path = eval_root / config_name
            self.assertTrue(config_path.is_file())
            text = config_path.read_text(encoding="utf-8")
            self.assertIn("file://cases/**/*.yaml", text)
            for relative in re.findall(r"file://([A-Za-z0-9_./-]+\.(?:md|mjs|yaml))", text):
                if "*" not in relative:
                    self.assertTrue((eval_root / relative).is_file(), relative)

    def test_primary_routing_and_composition_contracts_are_distinct(self) -> None:
        prompt_root = ROOT / "evals" / "prompts"
        route_prompt = (prompt_root / "route-skill.md").read_text(encoding="utf-8")
        compose_prompt = (prompt_root / "compose-skills.md").read_text(encoding="utf-8")

        self.assertIn("Choose exactly one primary skill", route_prompt)
        self.assertNotIn("Secondary skills:", route_prompt)
        self.assertIn("Choose exactly one primary skill", compose_prompt)
        self.assertIn("every applicable secondary skill", compose_prompt)
        self.assertIn("Secondary skills:", compose_prompt)

    def test_review_prompts_support_principles_and_self_review(self) -> None:
        prompt_root = ROOT / "evals" / "prompts"
        review_prompt = (prompt_root / "review-code.md").read_text(encoding="utf-8")
        self_review_prompt = (prompt_root / "self-review-code.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("{{ principles }}", review_prompt)
        self.assertIn("{{ project_instructions }}", review_prompt)
        self.assertIn("Name an applicable principle canonically", review_prompt)
        self.assertIn("{{ principles }}", self_review_prompt)
        self.assertIn("final self-review", self_review_prompt)

        for config_name in ("promptfooconfig.yaml", "promptfooconfig.api.yaml"):
            config_text = (ROOT / "evals" / config_name).read_text(encoding="utf-8")
            self.assertIn("file://prompts/self-review-code.md", config_text)

    def test_ci_runs_deterministic_suite(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("actions/checkout@v7", workflow)
        self.assertIn("actions/setup-python@v6", workflow)
        self.assertIn("python -B -m unittest discover -s tests -v", workflow)


if __name__ == "__main__":
    unittest.main()
