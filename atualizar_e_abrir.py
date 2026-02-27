"""
Atualiza data.json com os dados do SALARIO.XLSX e faz deploy no Netlify.
Uso: python atualizar_e_abrir.py
"""
import pandas as pd
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

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
    print(f"[OK] data.json gerado: {len(records)} meses")
    print(f"     Entradas: R$ {total_entradas:,.2f}")
    print(f"     Salarios: R$ {total_salarios:,.2f}")
    print(f"     Saldo:    R$ {saldo_atual:,.2f}")

def deploy():
    print("[...] Fazendo deploy no Vercel...")
    result = subprocess.run(
        f'vercel --prod --yes --cwd "{BASE}"',
        capture_output=True, text=True, shell=True
    )
    print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)
    if result.returncode != 0:
        print("[ERRO]", result.stderr[-500:])
        sys.exit(1)

if __name__ == "__main__":
    gerar_json()
    deploy()
