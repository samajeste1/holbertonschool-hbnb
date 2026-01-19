@echo off
echo ==========================================
echo Demarrage du serveur HBnB Part 2
echo ==========================================
echo.
echo IMPORTANT: Ce script demarre UNIQUEMENT le serveur PART2
echo (SANS authentification JWT)
echo.
echo Arret des serveurs existants...
taskkill /F /IM python3.11.exe >nul 2>&1
timeout /t 2 >nul

echo.
echo Demarrage du serveur Part 2...
cd /d "%~dp0"
python run.py

pause
