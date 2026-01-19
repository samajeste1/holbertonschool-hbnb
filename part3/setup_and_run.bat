@echo off
REM ================================================
REM  HBnB Part 3 - Configuration et lancement
REM  Ce script fait TOUT automatiquement
REM ================================================

echo.
echo ================================================
echo    HBnB Part 3 - Configuration Complete
echo ================================================
echo.

REM Etape 1: Creation du venv
echo [1/6] Creation de l'environnement virtuel...
if not exist "venv" (
    python -m venv venv
    echo       venv cree avec succes
) else (
    echo       venv existe deja
)

REM Etape 2: Activation
echo.
echo [2/6] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Etape 3: Installation des dependances
echo.
echo [3/6] Installation des dependances...
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo       Dependances installees

REM Etape 4: Initialisation de la base de donnees
echo.
echo [4/6] Initialisation de la base de donnees...
if exist "development.db" (
    del development.db
    echo       Ancienne base supprimee
)
python init_db.py
echo       Base de donnees creee

REM Etape 5: Creation des donnees de test
echo.
echo [5/6] Creation des donnees de test...
python seed_data.py

REM Etape 6: Lancement du serveur
echo.
echo [6/6] Lancement du serveur...
echo.
echo ================================================
echo  Configuration terminee ! Le serveur demarre...
echo ================================================
echo.

python run.py

pause
