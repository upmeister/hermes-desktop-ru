param(
  [switch]$Doctor,
  [switch]$Help,
  [switch]$Uninstall,
  [switch]$AllowStaleDist,
  [switch]$Version,
  [string]$Root,
  [string]$Scope,
  [switch]$WithIntro
)
# User-facing entry. Forwards all args to install-asar.ps1 (which calls install.mjs).
& "$PSScriptRoot\install-asar.ps1" @PSBoundParameters
exit $LASTEXITCODE