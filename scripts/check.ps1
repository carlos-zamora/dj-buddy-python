<#
.SYNOPSIS
    Run the same checks as `make check` on Windows: ruff lint, ruff format check, mypy, pytest.

.DESCRIPTION
    Windows rarely has GNU make, so this script mirrors the Makefile's `check` target step for step.
    It stops at the first failing step and exits with that step's exit code, so CI and git hooks
    can rely on it. Run it from anywhere; it switches to the repository root first.

.PARAMETER Fix
    Apply ruff's safe fixes and reformat the code before checking (like `make format`).

.EXAMPLE
    ./scripts/check.ps1
    Run every check.

.EXAMPLE
    ./scripts/check.ps1 -Fix
    Fix lint and formatting first, then run every check.
#>
[CmdletBinding()]
param(
    [switch]$Fix
)

$ErrorActionPreference = 'Stop'

# Run from the repository root (this script lives in <root>/scripts).
Set-Location (Split-Path -Parent $PSScriptRoot)

function Invoke-Step {
    <#
    .SYNOPSIS
        Run one check through `uv run` and stop the script if it fails.
    .PARAMETER Name
        Short label printed before the step runs.
    .PARAMETER Arguments
        The command and its arguments, passed to `uv run`.
    #>
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string[]]$Arguments
    )
    Write-Host "==> $Name" -ForegroundColor Cyan
    & uv run @Arguments
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $Name" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

if ($Fix) {
    Invoke-Step -Name 'ruff fix' -Arguments @('ruff', 'check', '--fix', '.')
    Invoke-Step -Name 'ruff format' -Arguments @('ruff', 'format', '.')
}

Invoke-Step -Name 'ruff lint' -Arguments @('ruff', 'check', '.')
Invoke-Step -Name 'ruff format check' -Arguments @('ruff', 'format', '--check', '.')
Invoke-Step -Name 'mypy' -Arguments @('mypy')
Invoke-Step -Name 'pytest' -Arguments @('pytest')

Write-Host 'All checks passed.' -ForegroundColor Green
