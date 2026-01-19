@echo off
echo ================================================
echo       HBnB Part 3 - Demarrage du projet
echo ================================================
echo.

REM Verification de l'environnement virtuel
if not exist "venv\Scripts\activate.bat" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    echo Environnement virtuel cree.
)

REM Activation de l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installation des dependances
echo.
echo Installation des dependances...
pip install -q -r requirements.txt

REM Verification de la base de donnees
if not exist "development.db" (
    echo.
    echo Initialisation de la base de donnees...
    python init_db.py
) else (
    echo.
    echo Base de donnees existante detectee.
    set /p reinit="Voulez-vous reinitialiser la base de donnees ? (o/N): "
    if /i "%reinit%"=="o" (
        python init_db.py --drop
    )
)

REM Demarrage du serveur
echo.
echo ================================================
echo Demarrage du serveur Flask...
echo ================================================
python run.py

pause
