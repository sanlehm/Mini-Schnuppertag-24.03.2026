@echo off
setlocal enabledelayedexpansion
title Mini-Schnuppertag Installer

echo ============================================
echo   Mini-Schnuppertag 24.03.2026 - Installer
echo ============================================
echo.

:: Zielordner definieren
set "DEV_DIR=C:\Dev"
set "PROJECT_NAME=Mini-Schnuppertag-24.03.2026"
set "DEST=%DEV_DIR%\%PROJECT_NAME%"

:: USB-Stick suchen - alle Laufwerke D: bis Z: durchprobieren
echo Suche Projekt auf USB-Stick...
echo.

set "USB_SOURCE="

for %%D in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%D:\%PROJECT_NAME%\solutions.py" (
        set "USB_SOURCE=%%D:\%PROJECT_NAME%"
        echo [GEFUNDEN] USB-Stick auf Laufwerk %%D:
        echo            Quelle: !USB_SOURCE!
        goto :found
    )
)

:: Auch in Unterordnern suchen (z.B. D:\schnuppertag\Mini-...)
for %%D in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%D:\schnuppertag\%PROJECT_NAME%\solutions.py" (
        set "USB_SOURCE=%%D:\schnuppertag\%PROJECT_NAME%"
        echo [GEFUNDEN] USB-Stick auf Laufwerk %%D:
        echo            Quelle: !USB_SOURCE!
        goto :found
    )
)

echo [FEHLER] Projekt nicht gefunden!
echo.
echo Bitte stelle sicher, dass der USB-Stick eingesteckt ist
echo und den Ordner "%PROJECT_NAME%" enthaelt.
echo.
pause
exit /b 1

:found
echo.

:: Dev-Ordner erstellen falls nicht vorhanden
if not exist "%DEV_DIR%\" (
    echo Erstelle Dev-Ordner: %DEV_DIR%
    mkdir "%DEV_DIR%"
    if errorlevel 1 (
        echo [FEHLER] Dev-Ordner konnte nicht erstellt werden!
        pause
        exit /b 1
    )
)

:: Alten Projektordner loeschen falls vorhanden (Ueberschreiben)
if exist "%DEST%\" (
    echo [INFO] Bestehender Ordner wird ueberschrieben: %DEST%
    rmdir /S /Q "%DEST%"
)

:: Projekt kopieren
echo Kopiere Projekt nach: %DEST%
echo Bitte warten...
echo.

xcopy /E /I /H /Y "%USB_SOURCE%" "%DEST%" >nul 2>&1

if errorlevel 1 (
    echo [FEHLER] Kopieren fehlgeschlagen!
    pause
    exit /b 1
)

echo [OK] Projekt erfolgreich kopiert!
echo.

:: ============================================
:: VS Code installieren falls nicht vorhanden
:: ============================================
echo Pruefe VS Code...

set "VSCODE_FOUND=0"
where code >nul 2>&1
if %errorlevel% == 0 set "VSCODE_FOUND=1"
if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" set "VSCODE_FOUND=1"
if exist "%ProgramFiles%\Microsoft VS Code\Code.exe" set "VSCODE_FOUND=1"

if "%VSCODE_FOUND%"=="1" (
    echo [OK] VS Code ist bereits installiert.
    goto :adblocker
)

echo [INFO] VS Code nicht gefunden. Wird jetzt installiert...
echo.

:: Zuerst winget probieren (schnell und sauber)
where winget >nul 2>&1
if %errorlevel% == 0 (
    echo Installiere VS Code via winget...
    winget install Microsoft.VisualStudioCode --silent --accept-package-agreements --accept-source-agreements
    if %errorlevel% == 0 (
        echo [OK] VS Code erfolgreich installiert!
        goto :adblocker
    )
)

:: Fallback: Installer herunterladen und ausfuehren
echo Lade VS Code Installer herunter...
set "VSCODE_INSTALLER=%TEMP%\vscode_setup.exe"

powershell -Command "& { $ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user' -OutFile '%VSCODE_INSTALLER%' }"

if not exist "%VSCODE_INSTALLER%" (
    echo [FEHLER] VS Code Download fehlgeschlagen.
    echo Bitte manuell installieren: https://code.visualstudio.com
    echo.
    goto :adblocker
)

echo Installiere VS Code (bitte warten)...
"%VSCODE_INSTALLER%" /VERYSILENT /MERGETASKS=!runcode,addcontextmenufiles,addcontextmenufolders,associatewithfiles,addtopath /NORESTART
echo [OK] VS Code installiert!

:: PATH aktualisieren damit "code" Befehl funktioniert
set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Microsoft VS Code\bin"

:adblocker
:: ============================================
:: uBlock Origin Adblocker oeffnen
:: ============================================
echo.
echo ============================================
echo   Adblocker installieren (uBlock Origin)
echo ============================================
echo.
echo Empfehlung: uBlock Origin - der beste Adblocker
echo Wird jetzt im Browser geoeffnet zum Installieren...
echo.

timeout /t 2 /nobreak >nul

:: Edge pruefen und uBlock Origin Seite oeffnen
set "EDGE_EXE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE_EXE%" set "EDGE_EXE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"

if exist "%EDGE_EXE%" (
    echo [Edge] Oeffne uBlock Origin fuer Microsoft Edge...
    start "" "%EDGE_EXE%" "https://microsoftedge.microsoft.com/addons/detail/ublock-origin/odfafepnkmbhccpbejgmiehpchacaeak"
    timeout /t 2 /nobreak >nul
)

:: Chrome pruefen und uBlock Origin Seite oeffnen
set "CHROME_EXE=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_EXE%" set "CHROME_EXE=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_EXE%" set "CHROME_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

if exist "%CHROME_EXE%" (
    echo [Chrome] Oeffne uBlock Origin fuer Google Chrome...
    start "" "%CHROME_EXE%" "https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm"
    timeout /t 2 /nobreak >nul
)

echo [INFO] Bitte im Browser auf "Hinzufuegen" / "Add to browser" klicken!
echo.

:: ============================================
:: solutions.py oeffnen
:: ============================================
echo ============================================
echo   Installation abgeschlossen!
echo   Ordner: %DEST%
echo ============================================
echo.

if not exist "%DEST%\solutions.py" (
    echo [FEHLER] solutions.py nicht gefunden in: %DEST%
    pause
    exit /b 1
)

echo Oeffne solutions.py in VS Code...
timeout /t 3 /nobreak >nul

:: VS Code Pfade pruefen
set "CODE_CMD=code"
where code >nul 2>&1
if %errorlevel% neq 0 (
    if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" (
        set "CODE_CMD=%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
    ) else if exist "%ProgramFiles%\Microsoft VS Code\Code.exe" (
        set "CODE_CMD=%ProgramFiles%\Microsoft VS Code\Code.exe"
    )
)

"%CODE_CMD%" "%DEST%\solutions.py"
echo [OK] solutions.py in VS Code geoeffnet.

echo.
echo Fertig! Viel Spass beim Schnuppertag! :)
echo.
pause
