# Skill Evaluation

The test suite has two layers:

- Deterministic repository tests validate skill structure, metadata, installation manifests,
  agent-instruction installation, eval inventory, and CI wiring.
- Promptfoo behavioral evals exercise primary routing, multi-skill composition, activation guards,
  software-design principle detection and restraint, self-review, and high-risk semantic rules.

The deterministic suite runs in CI and has no third-party Python dependencies:

```powershell
python -B -m unittest discover -s tests -v
```

## Behavioral Evals with Codex Login

The default configuration uses Promptfoo's built-in `openai:codex-sdk` provider. With
`OPENAI_API_KEY` and `CODEX_API_KEY` unset, it can reuse the local Codex/ChatGPT login. The
provider runs from the repository root with a read-only sandbox, no approvals, and network and web
search disabled.

Use the Node version in `.nvmrc`, then run:

```powershell
Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:CODEX_API_KEY -ErrorAction SilentlyContinue
npm.cmd exec --yes --package promptfoo@latest --package @openai/codex-sdk@latest -- promptfoo eval --config evals/promptfooconfig.yaml
```

Override the model with `PROMPTFOO_CODEX_MODEL` when needed.

## Behavioral Evals with an API Key

Set `OPENAI_API_KEY`, then run:

```powershell
npm.cmd exec --yes --package promptfoo@latest -- promptfoo eval --config evals/promptfooconfig.api.yaml
```

The API configuration defaults both the candidate and rubric grader to
`openai:responses:gpt-5.5`. Override them independently with `PROMPTFOO_EVAL_PROVIDER` and
`PROMPTFOO_GRADER_PROVIDER`.

Behavioral evals are intentionally not part of pull-request CI because they require
authentication, incur model usage, and are nondeterministic.

Validate both configurations without making model calls:

```powershell
npm.cmd exec --yes --package promptfoo@latest -- promptfoo validate --config evals/promptfooconfig.yaml --config evals/promptfooconfig.api.yaml
```

See Promptfoo's official documentation for the
[`openai:codex-sdk` provider](https://www.promptfoo.dev/docs/providers/openai-codex-sdk/) and
[`validate` command](https://www.promptfoo.dev/docs/usage/command-line/#promptfoo-validate).

## Adding a Case

Add one YAML file below `evals/cases`, give `description` and `metadata.id` the same unique value,
identify the skill and case kind in metadata, and combine deterministic assertions with one
semantic `llm-rubric`. Update `EXPECTED_EVAL_CASES` in `tests/test_repository.py`.

Use `route-skill` cases for tasks with one clear owner and `compose-skills` cases when requested
work needs multiple applicable checklists. A composition case must choose exactly one primary
skill that owns the requested outcome or explicitly activated governing boundary, then list each
distinct implementation, safety, or verification skill as secondary. Architecture skills remain
ineligible unless the supplied project instructions explicitly activate them.
