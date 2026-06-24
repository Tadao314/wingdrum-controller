@echo off
echo [1/2] PyInstaller build...
python -m PyInstaller --clean wingdrum.spec
if errorlevel 1 ( echo BUILD FAILED & pause & exit /b 1 )
echo [2/2] Inno Setup...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" ( "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" wingdrum_installer.iss & goto done )
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" ( "C:\Program Files\Inno Setup 6\ISCC.exe" wingdrum_installer.iss & goto done )
echo Inno Setup not found. Get it at: https://jrsoftware.org/isdl.php
:done
echo Done!
pause
