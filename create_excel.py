import pandas as pd

data = {
    'Código': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010', 
               'P011', 'P012', 'P013', 'P014', 'P015', 'P016', 'P017', 'P018', 'P019', 'P020'],
    'Descrição': ['Notebook Dell', 'Mouse Logitech', 'Teclado Mecânico', 'Monitor LG 24"', 'Webcam HD',
                  'Headset Gamer', 'Pen Drive 32GB', 'HD Externo 1TB', 'Impressora HP', 'Roteador WiFi',
                  'Switch 8 portas', 'Cabo HDMI', 'Mousepad', 'Cadeira Gamer', 'Mesa para Computador',
                  'Luminária LED', 'Suporte Monitor', 'Estabilizador', 'No-break 600VA', 'Gabinete ATX'],
    'Quantidade': [15, 150, 80, 25, 40, 30, 200, 35, 12, 45, 20, 180, 120, 8, 10, 50, 35, 25, 15, 18],
    'Valor Unitário': [3500.00, 45.00, 250.00, 890.00, 180.00, 320.00, 25.00, 380.00, 1200.00, 220.00,
                       150.00, 15.00, 20.00, 1800.00, 650.00, 85.00, 95.00, 180.00, 420.00, 280.00]
}

df = pd.DataFrame(data)
df.to_excel('curva-abc-app/exemplo-estoque.xlsx', index=False, engine='openpyxl')
print('✅ Arquivo exemplo-estoque.xlsx criado com sucesso!')
