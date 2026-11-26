"""Gera uma página de proposta 3D para um cliente: p/<codigo>/index.html + modelo.json.

Uso:
  python3 _fonte/proposta.py --stl peca.stl --peca "Ímã abridor Boca" \
      --corte 4.01 --partes "Base e linha da boca:Preto" "Lábios:Vermelho" \
      --dias 10 [--cliente "Nome"] [--material PETG] [--obs "texto"]

--corte divide a peça em alturas (mm, de baixo pra cima). Cada corte cria mais uma parte,
que pode ter uma cor diferente (troca de filamento naquela camada).
Sem --corte, a peça tem uma parte só.
"""
import argparse, datetime, json, os, secrets, string
import numpy as np, trimesh

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORES = [("Preto", "#1C1C1E"), ("Cinza Grafite", "#3C3F44"), ("Cinza Claro", "#A8ACB0"), ("Branco Dental", "#ECE7DC"),
         ("Marrom", "#5E3B25"), ("Vermelho", "#C3161F"), ("Laranja", "#EF6A1C"), ("Amarelo", "#F2C300"), ("Azul", "#1F5BC4"),
         ("Verde", "#1F8A40"), ("Natural Translúcido", "#E6ECEE"), ("Azul Marinho Translúcido", "#1A2D69"),
         ("Verde Neon Translúcido", "#5FD43A"), ("Laranja Neon Translúcido", "#FF6B1E"), ("Branco Blackout", "#F6F6F3"),
         ("Fibra de Carbono", "#2C2C2E")]

ap = argparse.ArgumentParser()
ap.add_argument('--stl', required=True)
ap.add_argument('--peca', required=True)
ap.add_argument('--corte', type=float, nargs='*', default=[])
ap.add_argument('--partes', nargs='+', required=True, help='"Nome:Cor padrão", de baixo pra cima')
ap.add_argument('--dias', type=int, default=10)
ap.add_argument('--cliente', default='')
ap.add_argument('--material', default='PETG')
ap.add_argument('--obs', default='')
ap.add_argument('--codigo', default='')
a = ap.parse_args()
assert len(a.partes) == len(a.corte) + 1, 'precisa de uma parte a mais que o número de cortes'

m = trimesh.load(a.stl, force='mesh')
m.vertices -= [(m.bounds[0][0] + m.bounds[1][0]) / 2, (m.bounds[0][1] + m.bounds[1][1]) / 2, m.bounds[0][2]]
ext = m.extents

pedacos, resto = [], m
for z in a.corte:
    pedacos.append(trimesh.intersections.slice_mesh_plane(resto, [0, 0, -1], [0, 0, z]))
    resto = trimesh.intersections.slice_mesh_plane(resto, [0, 0, 1], [0, 0, z])
pedacos.append(resto)

nomes = dict(CORES)
partes = []
for spec, p in zip(a.partes, pedacos):
    nome, cor = spec.split(':')
    assert cor in nomes, f'cor desconhecida: {cor}'
    partes.append({'nome': nome, 'cor': cor, 'p': [round(float(v), 3) for v in p.triangles.reshape(-1)]})

codigo = a.codigo or ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(7))
validade = (datetime.date.today() + datetime.timedelta(days=a.dias)).isoformat()
pasta = os.path.join(RAIZ, 'p', codigo)
os.makedirs(pasta, exist_ok=True)
with open(os.path.join(pasta, 'modelo.json'), 'w') as f:
    json.dump({'partes': partes}, f, separators=(',', ':'))

cfg = {
    'codigo': codigo, 'peca': a.peca, 'cliente': a.cliente, 'validade': validade, 'material': a.material, 'obs': a.obs,
    'tamanho': ' × '.join(f'{v:.1f}'.replace('.', ',').replace(',0', '') for v in ext) + ' mm',
    'cores': CORES,
}
modelo = open(os.path.join(RAIZ, '_fonte', 'proposta_modelo.html'), encoding='utf-8').read()
html = modelo.replace('/*CONFIG*/', 'const CFG = ' + json.dumps(cfg, ensure_ascii=False) + ';')
with open(os.path.join(pasta, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print(f'p/{codigo}/  validade {validade}  tamanho {cfg["tamanho"]}')
