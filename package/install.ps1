param(
  [switch]$Doctor,
  [switch]$Help,
  [string]$Root
)
# User-facing entry. Forwards all args to install-asar.ps1
& "$PSScriptRoot\install-asar.ps1" @PSBoundParameters
exit $LASTEXITCODE
