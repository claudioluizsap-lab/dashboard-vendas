#!/bin/bash
# Script de Build e Deploy - Curva ABC
# Linux/macOS

echo "===================================="
echo "  Curva ABC - Build para Produção"
echo "===================================="
echo ""

echo "[1/3] Limpando build anterior..."
rm -rf dist

echo ""
echo "[2/3] Compilando aplicação..."
npm run build

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERRO] Falha na compilação!"
    exit 1
fi

echo ""
echo "[3/3] Build concluído com sucesso!"
echo ""
echo "Arquivos gerados em: dist/"
echo ""
echo "Para testar localmente:"
echo "  npm run preview"
echo ""
echo "Para deploy:"
echo "  - Copie o conteúdo de dist/ para seu servidor"
echo "  - Ou use: vercel deploy --prod"
echo "  - Ou use: netlify deploy --prod --dir=dist"
echo ""
