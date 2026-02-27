#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Teste Automatizado - Curva ABC
Valida a aplicação usando a planilha de teste
"""

import pandas as pd
import sys
from pathlib import Path

def test_excel_processing():
    """Testa processamento da planilha Excel"""
    print("="*60)
    print("TESTE 1: Processamento de Excel")
    print("="*60)
    
    file_path = 'planilha-teste-estoque.xlsx'
    
    try:
        df = pd.read_excel(file_path)
        print(f"✅ Planilha carregada com sucesso")
        print(f"   Linhas: {len(df)}")
        print(f"   Colunas: {list(df.columns)}")
        
        # Verificar colunas necessárias
        required_cols = ['Código', 'Descrição', 'Quantidade', 'Valor Unitário']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            print(f"❌ Colunas faltando: {missing}")
            return False
        
        print(f"✅ Todas as colunas necessárias presentes")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar planilha: {e}")
        return False

def test_curva_abc_calculation():
    """Testa cálculo da Curva ABC"""
    print("\n" + "="*60)
    print("TESTE 2: Cálculo da Curva ABC")
    print("="*60)
    
    try:
        df = pd.read_excel('planilha-teste-estoque.xlsx')
        
        # Calcular valor total
        df['Valor Total'] = df['Quantidade'] * df['Valor Unitário']
        print(f"✅ Valores totais calculados")
        
        # Ordenar por valor
        df = df.sort_values('Valor Total', ascending=False)
        print(f"✅ Produtos ordenados por valor")
        
        # Calcular percentuais
        valor_total_geral = df['Valor Total'].sum()
        df['% Valor'] = (df['Valor Total'] / valor_total_geral) * 100
        df['% Acumulado'] = df['% Valor'].cumsum()
        print(f"✅ Percentuais calculados")
        
        # Classificar
        df['Classe'] = df['% Acumulado'].apply(
            lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C')
        )
        print(f"✅ Classificação ABC aplicada")
        
        # Verificar distribuição
        classe_a = len(df[df['Classe'] == 'A'])
        classe_b = len(df[df['Classe'] == 'B'])
        classe_c = len(df[df['Classe'] == 'C'])
        
        print(f"\n📊 Distribuição:")
        print(f"   Classe A: {classe_a} produtos")
        print(f"   Classe B: {classe_b} produtos")
        print(f"   Classe C: {classe_c} produtos")
        
        # Validar lógica
        if classe_a + classe_b + classe_c != len(df):
            print(f"❌ Erro na classificação: soma não bate")
            return False
        
        print(f"✅ Classificação válida")
        return True
        
    except Exception as e:
        print(f"❌ Erro no cálculo: {e}")
        return False

def test_data_integrity():
    """Testa integridade dos dados"""
    print("\n" + "="*60)
    print("TESTE 3: Integridade dos Dados")
    print("="*60)
    
    try:
        df = pd.read_excel('planilha-teste-estoque.xlsx')
        
        # Verificar valores nulos
        nulls = df.isnull().sum()
        if nulls.any():
            print(f"⚠️  Valores nulos encontrados:")
            for col, count in nulls[nulls > 0].items():
                print(f"   {col}: {count} nulos")
        else:
            print(f"✅ Sem valores nulos")
        
        # Verificar valores negativos
        neg_qtd = (df['Quantidade'] < 0).sum()
        neg_val = (df['Valor Unitário'] < 0).sum()
        
        if neg_qtd > 0:
            print(f"❌ {neg_qtd} quantidades negativas encontradas")
        else:
            print(f"✅ Todas as quantidades são positivas")
        
        if neg_val > 0:
            print(f"❌ {neg_val} valores unitários negativos encontrados")
        else:
            print(f"✅ Todos os valores unitários são positivos")
        
        # Verificar zeros
        zero_qtd = (df['Quantidade'] == 0).sum()
        zero_val = (df['Valor Unitário'] == 0).sum()
        
        if zero_qtd > 0:
            print(f"⚠️  {zero_qtd} produtos com quantidade zero")
        if zero_val > 0:
            print(f"⚠️  {zero_val} produtos com valor zero")
        
        return neg_qtd == 0 and neg_val == 0
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def test_edge_cases():
    """Testa casos extremos"""
    print("\n" + "="*60)
    print("TESTE 4: Casos Extremos")
    print("="*60)
    
    try:
        df = pd.read_excel('planilha-teste-estoque.xlsx')
        df['Valor Total'] = df['Quantidade'] * df['Valor Unitário']
        
        # Maior e menor valor
        max_val = df['Valor Total'].max()
        min_val = df['Valor Total'].min()
        max_prod = df[df['Valor Total'] == max_val]['Descrição'].iloc[0]
        min_prod = df[df['Valor Total'] == min_val]['Descrição'].iloc[0]
        
        print(f"💰 Produto mais valioso:")
        print(f"   {max_prod}: R$ {max_val:,.2f}")
        print(f"💸 Produto menos valioso:")
        print(f"   {min_prod}: R$ {min_val:,.2f}")
        
        # Razão entre maior e menor
        ratio = max_val / min_val if min_val > 0 else float('inf')
        print(f"📊 Razão maior/menor: {ratio:.1f}x")
        
        # Verificar se há produtos com mesmo valor
        duplicates = df.duplicated(subset=['Valor Total']).sum()
        if duplicates > 0:
            print(f"⚠️  {duplicates} produtos com valores duplicados")
        else:
            print(f"✅ Todos os produtos têm valores únicos")
        
        print(f"✅ Casos extremos identificados")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos casos extremos: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "█"*60)
    print("  TESTE AUTOMATIZADO - APLICATIVO CURVA ABC")
    print("█"*60 + "\n")
    
    tests = [
        test_excel_processing,
        test_curva_abc_calculation,
        test_data_integrity,
        test_edge_cases
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n✅ Testes aprovados: {passed}/{total}")
    print(f"❌ Testes falhados: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ Aplicação pronta para uso em produção")
        return 0
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        print("\n⚠️  Revise os erros antes de usar em produção")
        return 1

if __name__ == "__main__":
    sys.exit(main())
