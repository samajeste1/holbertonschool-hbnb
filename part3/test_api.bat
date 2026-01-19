@echo off
REM Script pour tester rapidement l'API HBnB

echo ================================================
echo    Test de l'API HBnB Part 3
echo ================================================
echo.

echo [1] Test du Health Check...
curl -s http://127.0.0.1:5000/health
echo.
echo.

echo [2] Test de connexion Admin...
echo.
curl -X POST http://127.0.0.1:5000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@hbnb.io\",\"password\":\"admin1234\"}"
echo.
echo.

echo [3] Test de connexion User...
echo.
curl -X POST http://127.0.0.1:5000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"john.doe@example.com\",\"password\":\"password123\"}"
echo.
echo.

echo ================================================
echo  Tests termines !
echo ================================================
echo.
echo Pour obtenir un token JWT:
echo   1. Copiez la valeur "access_token" ci-dessus
echo   2. Utilisez-le dans l'en-tete Authorization: Bearer TOKEN
echo.
echo Exemple:
echo curl http://127.0.0.1:5000/api/v1/users -H "Authorization: Bearer VOTRE_TOKEN"
echo.

pause
