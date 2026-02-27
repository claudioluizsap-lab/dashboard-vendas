import time, sys, os, urllib.request, json
from pyngrok import ngrok, conf

TOKEN = '39o60nvFMrrLTwewzdHoUtDy50J_UDCSVNRzGeWsuJSkds6r'
PORTA = 9090
URL_FILE = os.path.join(os.path.dirname(__file__), 'ngrok_url.txt')

def deletar_tuneis_remotos():
    try:
        req = urllib.request.Request(
            'https://api.ngrok.com/endpoints',
            headers={'Authorization': f'Bearer {TOKEN}', 'Ngrok-Version': '2'}
        )
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        endpoints = data.get('endpoints', [])
        for ep in endpoints:
            eid = ep.get('id', '')
            if eid:
                del_req = urllib.request.Request(
                    f'https://api.ngrok.com/endpoints/{eid}',
                    method='DELETE',
                    headers={'Authorization': f'Bearer {TOKEN}', 'Ngrok-Version': '2'}
                )
                urllib.request.urlopen(del_req, timeout=10)
                print(f'[LIMPO] Endpoint remoto {eid} removido', flush=True)
        time.sleep(3)
    except Exception as e:
        print(f'[AVISO] Nao foi possivel limpar endpoints: {e}', flush=True)

ngrok.set_auth_token(TOKEN)
print('[INFO] Limpando tuneis antigos...', flush=True)
try:
    ngrok.kill()
except:
    pass
deletar_tuneis_remotos()

while True:
    try:
        tunnels = ngrok.get_tunnels()
        ativos = [t for t in tunnels if str(PORTA) in t.config.get('addr', '')]
        if ativos:
            url = ativos[0].public_url
        else:
            t = ngrok.connect(PORTA, 'http')
            url = t.public_url

        with open(URL_FILE, 'w') as f:
            f.write(url)
        print(f'[OK] Online: {url}', flush=True)
        time.sleep(30)

    except Exception as e:
        print(f'[ERRO] {e} - Reiniciando em 8s...', flush=True)
        try:
            ngrok.kill()
        except:
            pass
        deletar_tuneis_remotos()
        time.sleep(8)
