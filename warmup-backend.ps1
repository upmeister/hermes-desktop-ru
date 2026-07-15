# Pre-warm Hermes backend by starting it briefly
# This ensures Python compiles all modules at login, not when the app launches
$hermesHome = "$env:LOCALAPPDATA\hermes"
$pythonPath = "$hermesHome\hermes-agent\venv\Scripts\python.exe"

if (Test-Path $pythonPath) {
    # Just import hermes to trigger compilation (doesn't start the server)
    & $pythonPath -c "import hermes_cli.main; print('Hermes backend pre-warmed')" 2>&1 | Out-Null
}
