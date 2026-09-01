param(
  [switch]$Doctor,
  [switch]$Help,
  [switch]$Uninstall,
  [switch]$AllowStaleDist,
  [switch]$Version,
  [string]$Root
)
# Thin wrapper. Source of truth is install.mjs (Node). Kept so existing
# docs / double-click / old muscle memory keep working on Windows.
$ErrorActionPreference = 'Stop'
$installJs = Join-Path $PSScriptRoot 'install.mjs'
if (-not (Test-Path $installJs)) {
  Write-Host "ERROR: install.mjs not found next to this wrapper"
  exit 1
}
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
  Write-Host "ERROR: Node.js 18+ is required (node not in PATH)"
  exit 1
}
$argv = @($installJs)
if ($Doctor) { $argv += 'doctor' }
elseif ($Uninstall) { $argv += 'uninstall' }
elseif ($Help) { $argv += 'help' }
elseif ($Version) { $argv += 'version' }
else { $argv += 'install' }
if ($AllowStaleDist) { $argv += '--allow-stale-dist' }
if ($Root) { $argv += '--root'; $argv += $Root }
& node @argv
exit $LASTEXITCODE