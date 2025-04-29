@echo off
REM ======================
REM  FakeApp  – версия 1.0.1
REM ======================

setlocal
set "LOCAL_VER=1.0.1"

echo -------------------------
echo FakeApp demo (v%LOCAL_VER%)
echo -------------------------

REM вызов проверщика обновлений
python "%~dp0update_checker.py" %LOCAL_VER%

echo [FakeApp] woking...
echo Done.
echo.

pause
endlocal
