@echo off
setlocal
set "APP_DIR=%~dp0.."
set "APP_EXE=LIDE.exe"

pushd "%APP_DIR%" || exit /b

if not exist "%APP_EXE%" (
    echo LIDE.exe not found in %APP_DIR%
    pause
    exit /b 1
)

start "" "%APP_EXE%"

popd
endlocal
