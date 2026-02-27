@echo off
REM Script de Build e Deploy - Curva ABC
REM Windows PowerShell

echo ====================================
echo   Curva ABC - Build para Producao
echo ====================================
echo.

echo [1/3] Limpando build anterior...
if exist dist rmdir /s /q dist

echo.
echo [2/3] Compilando aplicacao...
call npm run build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha na compilacao!
    pause
    exit /b 1
)

echo.
echo [3/3] Build concluido com sucesso!
echo.
echo Arquivos gerados em: dist/
echo.
echo Para testar localmente:
echo   npm run preview
echo.
echo Para deploy:
echo   - Copie o conteudo de dist/ para seu servidor
echo   - Ou use: vercel deploy --prod
echo   - Ou use: netlify deploy --prod --dir=dist
echo.

pause
