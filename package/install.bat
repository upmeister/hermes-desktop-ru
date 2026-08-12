@echo off
REM Install all clone mods (ru-mod + timestamps) into packaged Hermes Desktop.
REM Rule v2 (13.08.2026): install base is ALWAYS the freshly built clone dist
REM (npm run build in apps\desktop), NEVER a shipped package dist - it wipes
REM other mods. Package dist is fallback only.
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-asar.ps1"
if errorlevel 1 (
  echo INSTALL FAILED - see messages above
  pause
  exit /b 1
)
echo INSTALL OK - restart Hermes Desktop to see the mods
pause
