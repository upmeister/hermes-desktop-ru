@echo off
REM Hermes Desktop RU installer (double-click friendly)
chcp 65001 >nul
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-asar.ps1" %*
set ERR=%ERRORLEVEL%
if %ERR% neq 0 (
  echo.
  echo Установка НЕ УДАЛАСЬ - смотрите сообщения выше.
  echo Справка: install.bat -Help
  pause
  exit /b %ERR%
)
echo.
echo Установка ОК - перезапустите Hermes Desktop
pause