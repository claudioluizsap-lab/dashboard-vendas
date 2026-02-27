@echo off
title Curva ABC - Publicar Online
echo.
echo  ========================================
echo    CURVA ABC - Atualizando e Publicando
echo  ========================================
echo.

cd /d "D:\Users\Claudio\Documents\verdent-projects\new-project\curva-abc-app"

echo  [1/2] Lendo planilha e gerando dados...
python gerar_dados.py
if %errorlevel% neq 0 (
    echo  ERRO ao ler a planilha!
    pause
    exit /b 1
)

echo.
echo  [2/2] Publicando no Netlify...
netlify deploy --prod --dir=dist
if %errorlevel% neq 0 (
    echo  ERRO ao publicar!
    pause
    exit /b 1
)

echo.
echo  ========================================
echo   PUBLICADO COM SUCESSO!
echo   https://playful-pony-9fc24f.netlify.app
echo  ========================================
echo.
start "" "https://playful-pony-9fc24f.netlify.app"
pause
