@echo off
REM Hermes Desktop RU installer (double-click friendly)
chcp 65001 >nul
setlocal
where node >nul 2>nul
if errorlevel 1 (
  echo ERROR: Node.js 18+ is required and must be in PATH.
  pause
  exit /b 1
)
node "%~dp0install.mjs" %*
set ERR=%ERRORLEVEL%
if %ERR% neq 0 (
  echo.
  echo Команда НЕ УДАЛАСЬ - смотрите сообщения выше.
  echo Справка: install.bat help
  pause
  exit /b %ERR%
)
echo.
echo Готово.
pause