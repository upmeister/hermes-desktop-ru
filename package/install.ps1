# Installer wrapper: user-friendly entry point.
# Usage:  powershell -ExecutionPolicy Bypass -File install.ps1 [-Doctor]
& $PSScriptRoot\install-asar.ps1 @args
exit $LASTEXITCODE