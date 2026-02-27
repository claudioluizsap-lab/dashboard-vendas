import pandas as pd
import sys

def buscar_planilha():
    print("=" * 70)
    print("        SISTEMA DE BUSCA EM PLANILHA - BANCO DE DADOS")
    print("=" * 70)
    print()
    
    # Escolher arquivo
    print("Arquivos disponíveis:")
    print("1. exemplo_estoque.csv")
    print("2. Relatorio_ABC_Mercadorias.xlsx")
    print()
    
    escolha_arquivo = input("Escolha o arquivo (1 ou 2): ").strip()
    
    if escolha_arquivo == "1":
        arquivo = "exemplo_estoque.csv"
        df = pd.read_csv(arquivo)
    elif escolha_arquivo == "2":
        arquivo = "Relatorio_ABC_Mercadorias.xlsx"
        df = pd.read_excel(arquivo, sheet_name='Análise ABC')
    else:
        print("❌ Opção inválida!")
        return
    
    print(f"\n✓ Arquivo carregado: {arquivo}")
    print(f"✓ Total de registros: {len(df)}")
    print(f"✓ Colunas disponíveis: {', '.join(df.columns)}")
    print()
    
    while True:
        print("\n" + "=" * 70)
        print("OPÇÕES DE BUSCA:")
        print("=" * 70)
        print("1. Buscar por Código")
        print("2. Buscar por Produto (nome)")
        print("3. Buscar por Quantidade (exata)")
        print("4. Filtrar por Quantidade (maior que)")
        print("5. Filtrar por Quantidade (menor que)")
        print("6. Listar todos os registros")
        print("7. Busca avançada (múltiplos critérios)")
        print("0. Sair")
        print("=" * 70)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "0":
            print("\n👋 Encerrando o sistema de busca...")
            break
        
        elif opcao == "1":
            codigo = input("\n🔍 Digite o código a buscar: ").strip().upper()
            resultado = df[df['Código'].str.upper().str.contains(codigo, na=False)]
            exibir_resultado(resultado, f"Código contendo '{codigo}'")
        
        elif opcao == "2":
            produto = input("\n🔍 Digite o nome do produto (ou parte dele): ").strip()
            resultado = df[df['Produto'].str.contains(produto, case=False, na=False)]
            exibir_resultado(resultado, f"Produto contendo '{produto}'")
        
        elif opcao == "3":
            try:
                qtd = int(input("\n🔍 Digite a quantidade exata: ").strip())
                resultado = df[df['Quantidade'] == qtd]
                exibir_resultado(resultado, f"Quantidade = {qtd}")
            except ValueError:
                print("❌ Valor inválido! Digite um número inteiro.")
        
        elif opcao == "4":
            try:
                qtd = int(input("\n🔍 Digite a quantidade mínima: ").strip())
                resultado = df[df['Quantidade'] > qtd]
                exibir_resultado(resultado, f"Quantidade > {qtd}")
            except ValueError:
                print("❌ Valor inválido! Digite um número inteiro.")
        
        elif opcao == "5":
            try:
                qtd = int(input("\n🔍 Digite a quantidade máxima: ").strip())
                resultado = df[df['Quantidade'] < qtd]
                exibir_resultado(resultado, f"Quantidade < {qtd}")
            except ValueError:
                print("❌ Valor inválido! Digite um número inteiro.")
        
        elif opcao == "6":
            exibir_resultado(df, "Todos os registros")
        
        elif opcao == "7":
            busca_avancada(df)
        
        else:
            print("❌ Opção inválida!")
        
        input("\n⏎ Pressione ENTER para continuar...")

def exibir_resultado(df_resultado, criterio):
    print("\n" + "=" * 70)
    print(f"RESULTADO DA BUSCA: {criterio}")
    print("=" * 70)
    
    if len(df_resultado) == 0:
        print("❌ Nenhum registro encontrado.")
    else:
        print(f"✓ Encontrados {len(df_resultado)} registro(s):\n")
        
        # Exibir de forma formatada
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 50)
        
        print(df_resultado.to_string(index=False))
        
        # Estatísticas
        if 'Quantidade' in df_resultado.columns:
            print(f"\n📊 ESTATÍSTICAS:")
            print(f"   Total de Quantidade: {df_resultado['Quantidade'].sum():,}")
            print(f"   Média: {df_resultado['Quantidade'].mean():.2f}")
            print(f"   Mínimo: {df_resultado['Quantidade'].min()}")
            print(f"   Máximo: {df_resultado['Quantidade'].max()}")

def busca_avancada(df):
    print("\n" + "=" * 70)
    print("BUSCA AVANÇADA - Múltiplos Critérios")
    print("=" * 70)
    
    filtros = []
    
    # Filtro por código
    codigo = input("\n🔍 Código (deixe vazio para ignorar): ").strip()
    if codigo:
        filtros.append(df['Código'].str.upper().str.contains(codigo.upper(), na=False))
    
    # Filtro por produto
    produto = input("🔍 Produto (deixe vazio para ignorar): ").strip()
    if produto:
        filtros.append(df['Produto'].str.contains(produto, case=False, na=False))
    
    # Filtro por quantidade mínima
    qtd_min = input("🔍 Quantidade mínima (deixe vazio para ignorar): ").strip()
    if qtd_min:
        try:
            filtros.append(df['Quantidade'] >= int(qtd_min))
        except ValueError:
            print("⚠️ Quantidade mínima inválida, ignorando...")
    
    # Filtro por quantidade máxima
    qtd_max = input("🔍 Quantidade máxima (deixe vazio para ignorar): ").strip()
    if qtd_max:
        try:
            filtros.append(df['Quantidade'] <= int(qtd_max))
        except ValueError:
            print("⚠️ Quantidade máxima inválida, ignorando...")
    
    if not filtros:
        print("❌ Nenhum critério informado!")
        return
    
    # Aplicar todos os filtros
    resultado = df.copy()
    for filtro in filtros:
        resultado = resultado[filtro]
    
    criterios = []
    if codigo:
        criterios.append(f"Código={codigo}")
    if produto:
        criterios.append(f"Produto={produto}")
    if qtd_min:
        criterios.append(f"Qtd>={qtd_min}")
    if qtd_max:
        criterios.append(f"Qtd<={qtd_max}")
    
    exibir_resultado(resultado, " E ".join(criterios))

if __name__ == "__main__":
    try:
        buscar_planilha()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
