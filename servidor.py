"""
Servidor local para atualizar o dashboard via botao.
Rode: python servidor.py
Fica escutando em http://localhost:5050
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess, sys, json
from pathlib import Path
from datetime import datetime
import pandas as pd

EXCEL    = r"D:\Users\Claudio\OneDrive\CAIXA\SALARIO.XLSX"
BASE     = Path(__file__).parent
JSON_OUT = BASE / "data.json"

MESES_PT = {
    "Jan": "Jan", "Feb": "Fev", "Mar": "Mar", "Apr": "Abr",
    "May": "Mai", "Jun": "Jun", "Jul": "Jul", "Aug": "Ago",
    "Sep": "Set", "Oct": "Out", "Nov": "Nov", "Dec": "Dez",
}

def mes_pt(dt):
    abbr = dt.strftime("%b")
    return MESES_PT.get(abbr, abbr) + dt.strftime("/%Y")

def gerar_json():
    df = pd.read_excel(EXCEL, sheet_name="Planilha1")
    df.columns = ["data", "entradas", "salarios", "saldo"]
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df[df["data"].notna()].copy()

    records = []
    for _, r in df.iterrows():
        records.append({
            "mes":      mes_pt(r["data"]),
            "entradas": round(float(r["entradas"]), 2),
            "salarios": round(float(r["salarios"]), 2),
            "saldo":    round(float(r["saldo"]), 2),
        })

    total_entradas = sum(r["entradas"] for r in records)
    total_salarios = sum(r["salarios"] for r in records)
    saldo_atual    = records[-1]["saldo"] if records else 0

    payload = {
        "atualizado":     datetime.now().strftime("%d/%m/%Y %H:%M"),
        "fonte":          "SALARIO.XLSX",
        "total_entradas": round(total_entradas, 2),
        "total_salarios": round(total_salarios, 2),
        "saldo_atual":    round(saldo_atual, 2),
        "dados":          records,
    }
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload

def deploy():
    result = subprocess.run(
        f'netlify deploy --prod --dir "{BASE}" --message "Update {datetime.now().strftime("%d/%m/%Y %H:%M")}"',
        capture_output=True, text=True, shell=True
    )
    return result.returncode == 0

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST")
        self.end_headers()

    def do_GET(self):
        if self.path == "/atualizar":
            try:
                payload = gerar_json()
                ok = deploy()
                resp = json.dumps({
                    "ok": ok,
                    "atualizado": payload["atualizado"],
                    "msg": "Dados atualizados e publicados!" if ok else "JSON gerado mas deploy falhou."
                }, ensure_ascii=False).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp)
            except Exception as e:
                err = json.dumps({"ok": False, "msg": str(e)}).encode()
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(err)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}]", fmt % args)

if __name__ == "__main__":
    server = HTTPServer(("localhost", 5050), Handler)
    print("Servidor rodando em http://localhost:5050")
    print("Pressione Ctrl+C para parar.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
