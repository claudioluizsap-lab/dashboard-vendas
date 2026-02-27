@echo off
title Curva ABC - Atualizando dados...
cd /d "%~dp0"
echo ============================================
echo  CURVA ABC - Carregando dados da planilha
echo ============================================
echo.
python atualizar_e_abrir.py abrir
pause
