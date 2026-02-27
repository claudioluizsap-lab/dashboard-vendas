#!/usr/bin/env python3
"""
Servidor local para a aplicação Curva ABC.
Lê a planilha e serve os dados via HTTP.
"""
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import subprocess

PLANILHA = r"D:\Users\Claudio\OneDrive\Nova pasta\Bd_curva abc\curva abc.xlsx"
DIST_DIR = os.path.join(os.path.dirname(__file__), "dist")
DADOS_JSON = os.path.join(DIST_DIR, "dados.json")
ABA = "Produtos mais vendidos"

def ler_planilha():
    try:
        import openpyxl
        wb = openpyxl.load_workbook(PLANILHA, read_only=True, data_only=True)
        ws = wb[ABA]
        rows = list(ws.iter_rows(values_only=True))
        wb.close()

        if not rows:
            return None, "Planilha vazia"

        headers = [str(h).strip().lower() if h else "" for h in rows[0]]

        def find_col(keywords):
            for i, h in enumerate(headers):
                for kw in keywords:
                    if kw in h:
                        return i
            return -1

        idx_cod  = find_col(["cod"])
        idx_desc = find_col(["desc", "prod", "nome"])
        idx_qtd  = find_col(["quant", "qtd", "qt"])
        idx_vunt = find_col(["unit", "prec", "valor u"])
        idx_vtot = find_col(["valor", "total", "venda"])

        produtos = []
        for row in rows[1:]:
            if not any(row):
                continue
            def val(i):
                return row[i] if i >= 0 and i < len(row) else None

            try:
                qtd  = float(val(idx_qtd)  or 0)
                vunt = float(val(idx_vunt) or 0)
                vtot = float(val(idx_vtot) or 0) if idx_vtot >= 0 else qtd * vunt

                # Se não tem valor unitario mas tem total e qtd
                if vunt == 0 and qtd > 0 and vtot > 0:
                    vunt = vtot / qtd

                if qtd == 0 and vtot == 0:
                    continue

                produtos.append({
                    "codigo":       str(val(idx_cod)  or ""),
                    "descricao":    str(val(idx_desc) or ""),
                    "quantidade":   qtd,
                    "valorUnitario": round(vunt, 4),
                })
            except (ValueError, TypeError):
                continue

        return produtos, None
    except Exception as e:
        return None, str(e)


def salvar_json(produtos):
    os.makedirs(DIST_DIR, exist_ok=True)
    with open(DADOS_JSON, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # silencia logs HTTP

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/atualizar":
            produtos, erro = ler_planilha()
            if erro:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"erro": erro}).encode())
                return

            salvar_json(produtos)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "total": len(produtos),
                "mensagem": f"{len(produtos)} produtos carregados"
            }).encode())
            return

        # Serve arquivos estáticos
        super().do_GET()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    # Carregar dados iniciais
    print("🔄 Carregando dados da planilha...")
    produtos, erro = ler_planilha()
    if erro:
        print(f"⚠️  Aviso: {erro}")
        print("   O app abrirá, mas sem dados. Use o botão Atualizar após corrigir o caminho.")
        salvar_json([])
    else:
        salvar_json(produtos)
        print(f"✅ {len(produtos)} produtos carregados de:")
        print(f"   {PLANILHA}")

    porta = 8080
    server = HTTPServer(("0.0.0.0", porta), Handler)
    ip_local = "192.168.0.120"
    print(f"\n🚀 Servidor rodando!")
    print(f"   Local:  http://localhost:{porta}")
    print(f"   Rede:   http://{ip_local}:{porta}")
    print(f"\n   Compartilhe este link na empresa:")
    print(f"   👉  http://{ip_local}:{porta}")
    print("\n   Pressione Ctrl+C para parar\n")

    # Abrir no navegador
    import webbrowser
    webbrowser.open(f"http://localhost:8080")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Servidor encerrado.")


if __name__ == "__main__":
    main()
