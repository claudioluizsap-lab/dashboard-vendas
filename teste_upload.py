import requests

r = requests.post(
    "http://127.0.0.1:5000/carregar-planilha",
    files={"planilha": open("planilha_exemplo.xlsx", "rb")}
)
print(r.text)
