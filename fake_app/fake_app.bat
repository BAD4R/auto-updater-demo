@echo off
REM ======================
REM  FakeApp  – версия 1.0.0
REM ======================

setlocal
set "LOCAL_VER=1.0.0"

echo -------------------------
echo FakeApp demo (v%LOCAL_VER%)
echo -------------------------

REM вызов проверщика обновлений
python "%~dp0update_checker.py" %LOCAL_VER%

echo [FakeApp] выполняю работу...
echo Готово.
echo.

pause
endlocal
