import pandas as pd
import sys

def busca_rapida():
    """Busca rápida via linha de comando"""
    
    if len(sys.argv) < 2:
        print("=" * 70)
        print("  BUSCA RÁPIDA EM PLANILHA")
        print("=" * 70)
        print("\nUso:")
        print("  python busca_rapida.py <tipo> <valor>")
        print("\nTipos de busca:")
        print("  codigo <valor>       - Buscar por código")
        print("  produto <valor>      - Buscar por nome de produto")
        print("  qtd <numero>         - Buscar quantidade exata")
        print("  qtd_maior <numero>   - Quantidade maior que")
        print("  qtd_menor <numero>   - Quantidade menor que")
        print("  tudo                 - Listar tudo")
        print("\nExemplos:")
        print("  python busca_rapida.py codigo P001")
        print("  python busca_rapida.py produto mouse")
        print("  python busca_rapida.py qtd 150")
        print("  python busca_rapida.py qtd_maior 100")
        print("  python busca_rapida.py tudo")
        print("=" * 70)
        sys.exit(1)
    
    # Carregar dados
    try:
        df = pd.read_csv('exemplo_estoque.csv')
    except:
        try:
            df = pd.read_excel('Relatorio_ABC_Mercadorias.xlsx', sheet_name='Análise ABC')
        except:
            print("❌ Erro ao carregar planilha!")
            sys.exit(1)
    
    tipo = sys.argv[1].lower()
    
    if tipo == "tudo":
        resultado = df
        criterio = "Todos os registros"
    else:
        if len(sys.argv) < 3:
            print("❌ Valor não informado!")
            sys.exit(1)
        
        valor = ' '.join(sys.argv[2:])  # Pegar todos os argumentos restantes
        
        if tipo == "codigo":
            resultado = df[df['Código'].str.upper().str.contains(valor.upper(), na=False)]
            criterio = f"Código contendo '{valor}'"
        
        elif tipo == "produto":
            resultado = df[df['Produto'].str.contains(valor, case=False, na=False)]
            criterio = f"Produto contendo '{valor}'"
        
        elif tipo == "qtd":
            try:
                qtd = int(valor)
                resultado = df[df['Quantidade'] == qtd]
                criterio = f"Quantidade = {qtd}"
            except ValueError:
                print("❌ Quantidade deve ser um número inteiro!")
                sys.exit(1)
        
        elif tipo == "qtd_maior":
            try:
                qtd = int(valor)
                resultado = df[df['Quantidade'] > qtd]
                criterio = f"Quantidade > {qtd}"
            except ValueError:
                print("❌ Quantidade deve ser um número inteiro!")
                sys.exit(1)
        
        elif tipo == "qtd_menor":
            try:
                qtd = int(valor)
                resultado = df[df['Quantidade'] < qtd]
                criterio = f"Quantidade < {qtd}"
            except ValueError:
                print("❌ Quantidade deve ser um número inteiro!")
                sys.exit(1)
        
        else:
            print(f"❌ Tipo de busca inválido: {tipo}")
            sys.exit(1)
    
    # Exibir resultado
    print("\n" + "=" * 70)
    print(f"RESULTADO: {criterio}")
    print("=" * 70)
    
    if len(resultado) == 0:
        print("❌ Nenhum registro encontrado.")
    else:
        print(f"✓ {len(resultado)} registro(s) encontrado(s):\n")
        print(resultado.to_string(index=False))
        
        if 'Quantidade' in resultado.columns:
            print(f"\n📊 Total: {resultado['Quantidade'].sum():,} unidades")

if __name__ == "__main__":
    busca_rapida()
