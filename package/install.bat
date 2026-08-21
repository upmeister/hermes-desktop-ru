@echo off
REM Hermes Desktop RU installer (double-click friendly)
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-asar.ps1" %*
set ERR=%ERRORLEVEL%
if %ERR% neq 0 (
  echo.
  echo USTANOVKA NE UDALAS - smotrite soobscheniya vyshe
  echo Help: install.bat -Help
  pause
  exit /b %ERR%
)
echo.
echo USTANOVKA OK - perezapustite Hermes Desktop
pause
