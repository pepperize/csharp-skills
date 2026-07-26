$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$skillsDir = if ($env:AGENTS_SKILLS_DIR) {
    $env:AGENTS_SKILLS_DIR
} else {
    Join-Path $HOME ".agents\skills"
}
$skillsDir = [System.IO.Path]::GetFullPath($skillsDir).TrimEnd("\")

$skills = @(
    "csharp-readable-code",
    "dotnet-solid-review",
    "dotnet-testing",
    "dotnet-logging-exceptions",
    "dotnet-domain-clarification",
    "dotnet-clean-architecture",
    "dotnet-ddd-architecture",
    "maui-application",
    "maui-ui-testing",
    "dotnet-agent-instructions"
)

New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null

foreach ($skill in $skills) {
    $source = Join-Path $repoRoot $skill
    $target = Join-Path $skillsDir $skill
    $skillFile = Join-Path $source "SKILL.md"

    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        throw "Missing skill: $skillFile"
    }

    if (Test-Path -LiteralPath $target) {
        $existing = Get-Item -LiteralPath $target -Force
        $isLink = ($existing.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0

        if ($isLink) {
            $linkTargets = @($existing.Target)
            if ($linkTargets.Count -ne 1) {
                throw "Cannot determine junction target: $target"
            }

            $currentTarget = $linkTargets[0]
            if (-not [System.IO.Path]::IsPathRooted($currentTarget)) {
                $currentTarget = Join-Path ([System.IO.Path]::GetDirectoryName($target)) $currentTarget
            }

            $currentTarget = [System.IO.Path]::GetFullPath($currentTarget).TrimEnd("\")
            $resolvedSource = [System.IO.Path]::GetFullPath($source).TrimEnd("\")
            if ($currentTarget.Equals($resolvedSource, [System.StringComparison]::OrdinalIgnoreCase)) {
                Write-Host "Already installed: $skill"
                continue
            }

            Write-Host "Updating junction: $skill"
            $resolvedTarget = [System.IO.Path]::GetFullPath($target)
            if ([System.IO.Path]::GetDirectoryName($resolvedTarget) -ne $skillsDir) {
                throw "Refusing to remove junction outside skills directory: $resolvedTarget"
            }
            [System.IO.Directory]::Delete($resolvedTarget)
        } else {
            throw "Refusing to overwrite existing non-link: $target"
        }
    }

    New-Item -ItemType Junction -Path $target -Target $source | Out-Null
    Write-Host "Installed: $skill -> $source"
}

Write-Host ""
Write-Host "Restart Codex to pick up new or changed skills."
