@echo off
setlocal

REM --- Локальная версия, меняйте вручную ---
set "LOCAL_VER=1.0.0"

echo -------------------------
echo FakeApp demo (v%LOCAL_VER%)
echo -------------------------

REM --- Запускаем проверщик: передаём локальную версию ---
python "%~dp0update_checker.py" %LOCAL_VER%
set "RET=%ERRORLEVEL%"

if %RET% EQU 2 (
  echo [FakeApp] Обновление применено, перезапустите программу.
  pause
  endlocal
  exit /b 0
)

if %RET% NEQ 0 (
  echo [FakeApp] Ошибка при обновлении (код %RET%).
  pause
  endlocal
  exit /b 1
)

REM --- Если код 0, значит актуально или отказ, продолжаем работу ---
echo [FakeApp] выполняю основную логику...
REM ... тут ваша основная функциональность ...
echo [FakeApp] Done.
pause

endlocal
exit /b 0
