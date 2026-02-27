@echo off
title Dashboard de Projecao
echo ============================================
echo   DASHBOARD DE PROJECAO - Iniciando...
echo ============================================

cd /d "D:\Users\Claudio\Documents\verdent-projects\new-project\dashboard"

:: Encerra processos antigos na porta 9090
echo Encerrando processos antigos...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":9090" ^| findstr "LISTEN" 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)
taskkill /IM ngrok.exe /F >nul 2>&1
timeout /t 2 /nobreak >nul

:: Inicia servidor (escuta em toda a rede)
echo Iniciando servidor...
start /min cmd /c "python app.py"
timeout /t 4 /nobreak >nul

:: Descobre IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0.0.1" ^| findstr /v "169.254"') do (
    set IP_LOCAL=%%a
    goto :found
)
:found
set IP_LOCAL=%IP_LOCAL: =%

:: Abre dashboard local
start "" "http://127.0.0.1:9090"

echo.
echo ============================================
echo   ACESSO LOCAL:  http://127.0.0.1:9090
echo   ACESSO REDE:   http://%IP_LOCAL%:9090
echo ============================================
echo   Compartilhe o endereco de REDE com
echo   qualquer pessoa no mesmo Wi-Fi!
echo ============================================
echo.
echo Pressione qualquer tecla para ENCERRAR o servidor.
pause >nul

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":9090" ^| findstr "LISTEN" 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)
echo Servidor encerrado.
