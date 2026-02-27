@echo off
title Curva ABC - Liberando Firewall e Iniciando...
echo.
echo  Liberando porta 8080 no Firewall...
netsh advfirewall firewall delete rule name="Curva ABC App" >nul 2>&1
netsh advfirewall firewall add rule name="Curva ABC App" dir=in action=allow protocol=TCP localport=8080
echo  OK!
echo.
echo  Iniciando servidor...
cd /d "D:\Users\Claudio\Documents\verdent-projects\new-project\curva-abc-app"
python servidor.py
pause
