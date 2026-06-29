param(
    [string]$Destination = "$env:USERPROFILE\.codex\skills\agent-launch-gate",
    [switch]$SkipValidate
)

$ErrorActionPreference = "Stop"

$Source = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path -LiteralPath $Destination)) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
}

$Exclude = @(".git", ".github")
Get-ChildItem -LiteralPath $Source -Force |
    Where-Object { $Exclude -notcontains $_.Name } |
    ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $Destination -Recurse -Force
    }

Write-Host "Installed Agent Launch Gate to $Destination"

if (-not $SkipValidate) {
    $Validator = Join-Path $env:USERPROFILE ".codex\skills\.system\skill-creator\scripts\quick_validate.py"
    if (Test-Path -LiteralPath $Validator) {
        python -X utf8 $Validator $Destination
    } else {
        Write-Host "Validator not found at $Validator"
        Write-Host "Install completed, but validation was skipped."
    }
}
