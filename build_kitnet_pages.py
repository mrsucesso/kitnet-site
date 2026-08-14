from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).parent
ASSETS = ROOT / 'assets' / 'kitnets'

UNITS = [
    {
        'id': '01', 'status': 'disponível', 'area': '23 m²', 'rooms': '3 peças', 'furnished': 'Sem mobília',
        'short': 'Kitnet 3 peças – sem mobília',
        'details': 'Quarto, sala e cozinha integrada e ampla; banheiro azulejado até o teto; cobertura de laje e piso cerâmico.',
        'note': 'Pronta para mudar',
    },
    {
        'id': '02', 'status': 'disponível', 'area': '20 m²', 'rooms': '3 peças', 'furnished': 'Sem mobília',
        'short': 'Kitnet 3 peças – sem mobília',
        'details': 'Quarto, cozinha e banheiro; banheiro azulejado até o teto; cobertura de laje e piso cerâmico.',
        'note': 'Pronta para mudar',
    },
    {
        'id': '03', 'status': 'ocupada', 'area': '20 m²', 'rooms': '3 peças', 'furnished': 'Sem mobília',
        'short': 'Kitnet 3 peças – sem mobília',
        'details': 'Quarto, cozinha e banheiro; banheiro azulejado; cobertura de laje e PVC e piso cerâmico.',
        'note': 'Ocupada no momento',
    },
    {
        'id': '04', 'status': 'disponível', 'area': '20 m²', 'rooms': '3 peças', 'furnished': 'Mobiliada',
        'short': 'Kitnet 3 peças – mobiliada',
        'details': 'Quarto, cozinha e banheiro; banheiro azulejado; cobertura de PVC e piso cerâmico.',
        'note': 'Pronta para mudar',
    },
    {
        'id': '05', 'status': 'disponível', 'area': '18 m²', 'rooms': '2 peças', 'furnished': 'Mobiliada',
        'short': 'Kitnet 2 peças – mobiliada',
        'details': 'Quarto e cozinha integrados; banheiro azulejado; cobertura de PVC e piso cerâmico.',
        'note': 'Pronta para mudar',
    },
]

WHATSAPP = '556781227323'

def slug(u): return f"kitnet-{u['id']}"

def images_for(u):
    files = sorted((ASSETS / slug(u)).glob('*.png'))
    # Stable editorial order, independent of filename sorting.
    order = ['Fachada Externa', 'Fachada Interna', 'Entrada Unidade', 'Porta Unidade', 'Sala', 'Cozinha', 'Quarto', 'Quarto Detalhe', 'Banheiro', 'Banheiro (2)']
    def rank(p):
        name = p.stem
        for i, label in enumerate(order):
            if label in name: return i
        return 99
    return sorted(files, key=rank)

def optimize_images():
    for u in UNITS:
        for p in images_for(u):
            out = p.with_suffix('.webp')
            if not out.exists():
                Image.open(p).convert('RGB').save(out, 'WEBP', quality=82, method=6)

def wa(u):
    text = f"Olá! Tenho interesse na Kitnet {u['id']}. Gostaria de agendar uma visita."
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(text)}"

def common_css():
    return '''
    .unit-hero{padding-top:9rem;padding-bottom:4rem;background:linear-gradient(180deg,#000 0%,#3d2817 100%)}
    .unit-shell{max-width:1180px;margin:0 auto;padding:0 1.5rem}
    .unit-layout{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(320px,.9fr);gap:2.5rem;align-items:start}
    .gallery{background:#111;border:1px solid rgba(255,255,255,.14);border-radius:1.4rem;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.3)}
    .gallery-main{position:relative;aspect-ratio:4/3;background:#17120e}
    .gallery-main img{width:100%;height:100%;object-fit:cover;display:block}
    .gallery-nav{position:absolute;inset:0;display:flex;justify-content:space-between;align-items:center;padding:1rem;pointer-events:none}
    .gallery-nav button{pointer-events:auto;width:2.8rem;height:2.8rem;border:0;border-radius:50%;background:rgba(0,0,0,.65);color:#ffff6f;font-size:1.2rem;cursor:pointer}
    .gallery-count{position:absolute;bottom:1rem;right:1rem;background:rgba(0,0,0,.7);padding:.45rem .75rem;border-radius:999px;font-size:.78rem;color:#fff}
    .thumbs{display:flex;gap:.55rem;padding:.75rem;overflow-x:auto;background:#0a0a0a}
    .thumbs button{flex:0 0 74px;height:55px;border:2px solid transparent;border-radius:.45rem;overflow:hidden;padding:0;background:#222;cursor:pointer;opacity:.65}
    .thumbs button.active{border-color:#ffff6f;opacity:1}
    .thumbs img{width:100%;height:100%;object-fit:cover}
    .unit-panel{background:rgba(0,0,0,.32);border:1px solid rgba(255,255,255,.12);border-radius:1.4rem;padding:2rem}
    .unit-status{display:inline-flex;padding:.4rem .8rem;border-radius:999px;background:#ffff6f;color:#000;font-size:.75rem;font-weight:800;text-transform:uppercase}
    .unit-status.busy{background:#8b6f47;color:#fff}
    .unit-specs{display:grid;grid-template-columns:repeat(3,1fr);gap:.65rem;margin:1.5rem 0}
    .unit-spec{background:rgba(255,255,255,.06);border-radius:.8rem;padding:.8rem;text-align:center;color:#d0d0d0;font-size:.8rem}
    .unit-spec strong{display:block;color:#fff;font-size:1rem;margin-bottom:.2rem}
    .unit-note{border-left:3px solid #ffff6f;padding:.8rem 1rem;background:rgba(255,255,111,.08);color:#fff;margin:1.25rem 0;line-height:1.5}
    .conditions{background:#000;padding:4rem 1.5rem}
    .condition-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin-top:2rem}
    .condition-card{border:1px solid rgba(255,255,255,.12);border-radius:1rem;padding:1.25rem;background:rgba(255,255,255,.04);color:#d0d0d0;line-height:1.6}
    .condition-card h3{color:#ffff6f;font-size:1rem;margin-bottom:.5rem}
    @media(max-width:800px){.unit-layout{grid-template-columns:1fr}.condition-grid{grid-template-columns:1fr}.unit-panel{padding:1.4rem}}
    '''

def page(u):
    imgs = images_for(u)
    first = imgs[0].with_suffix('.webp').name
    busy = u['status'] != 'disponível'
    title = f"Kitnet {u['id']} — {u['short']} | Kitnet Mais Top"
    gallery = []
    for i,p in enumerate(imgs):
        webp = p.with_suffix('.webp').name
        gallery.append(f'<button class="{"active" if i == 0 else ""}" data-index="{i}" aria-label="Ver foto {i+1}"><img src="../assets/kitnets/{slug(u)}/{webp}" alt="Kitnet {u["id"]} — foto {i+1}" loading="lazy"></button>')
    data = ','.join('"../assets/kitnets/%s/%s"' % (slug(u), p.with_suffix('.webp').name) for p in imgs)
    cta = '' if busy else f'<a class="cta" href="{wa(u)}" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> Tenho interesse</a>'
    status = 'Ocupada no momento' if busy else 'Disponível para locação'
    return f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title><meta name="description" content="{u['short']}, {u['area']}, na Av. Aracruz, Novos Estados, Campo Grande-MS."><link rel="icon" type="image/png" href="../logo.png"><script src="https://cdn.tailwindcss.com"></script><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');*{{box-sizing:border-box}}body{{margin:0;background:#000;color:#fff;font-family:Inter,sans-serif}}.serif{{font-family:'Playfair Display',serif}}a{{text-decoration:none}}.cta{{display:flex;justify-content:center;align-items:center;gap:.6rem;background:#ffff6f;color:#000;padding:1rem 1.2rem;border-radius:999px;font-weight:700;margin-top:1.5rem}}.cta:hover{{opacity:.9}}{common_css()}</style></head><body><nav class="fixed top-0 w-full z-50 bg-black/80 backdrop-blur-sm border-b border-white/10"><div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between"><a href="../index.html" class="flex items-center gap-3"><img src="../logo.png" alt="Kitnet Mais Top" class="h-12"><span class="font-semibold text-white">Kitnet Mais Top</span></a><a href="../index.html#kitnets" class="text-sm text-gray-300 hover:text-white">← Ver todas</a></div></nav><main><section class="unit-hero"><div class="unit-shell"><div class="unit-layout"><div class="gallery"><div class="gallery-main"><img id="main-image" src="../assets/kitnets/{slug(u)}/{first}" alt="Kitnet {u['id']} — foto principal"><div class="gallery-nav"><button id="prev" aria-label="Foto anterior">‹</button><button id="next" aria-label="Próxima foto">›</button></div><span class="gallery-count"><span id="current">1</span> / {len(imgs)}</span></div><div class="thumbs">{''.join(gallery)}</div></div><div class="unit-panel"><span class="unit-status{' busy' if busy else ''}">{status}</span><p class="text-[#FFFF6F] text-sm font-semibold mt-6 mb-2">Kitnet Mais Top · Unidade {u['id']}</p><h1 class="serif text-4xl md:text-5xl font-normal leading-tight">{u['short']}</h1><p class="text-gray-300 mt-5 leading-relaxed">{u['details']}</p><div class="unit-specs"><div class="unit-spec"><strong>{u['area']}</strong>Área</div><div class="unit-spec"><strong>{u['rooms']}</strong>Ambientes</div><div class="unit-spec"><strong>{u['furnished']}</strong>Mobília</div></div><p class="text-gray-300"><i class="fas fa-location-dot text-[#FFFF6F] mr-2"></i>Av. Aracruz, próxima à Av. Sr. Bonfim<br><span class="ml-6">Novos Estados, Campo Grande-MS</span></p><p class="text-[#FFFF6F] text-2xl font-bold mt-6">R$ 850<span class="text-sm font-normal text-gray-300"> / mês</span></p><div class="unit-note"><strong>{u['note']}</strong><br><span class="text-gray-300 text-sm">Consulte as condições de locação e agende sua visita.</span></div>{cta}</div></div></div></section><section class="conditions"><div class="unit-shell"><div class="text-center"><p class="text-[#FFFF6F] font-semibold mb-3">Condições de locação</p><h2 class="serif text-3xl md:text-4xl">Tudo claro desde o início</h2></div><div class="condition-grid"><div class="condition-card"><h3><i class="fas fa-receipt mr-2"></i>O aluguel inclui</h3><p>Água, esgoto, IPTU, taxa de lixo e acesso à máquina de lavar compartilhada. A energia elétrica é rateada entre os moradores.</p></div><div class="condition-card"><h3><i class="fas fa-file-shield mr-2"></i>Documentação</h3><p>É realizada consulta ao Serasa. Em caso de restrição de crédito, será necessário apresentar fiador.</p></div><div class="condition-card"><h3><i class="fas fa-key mr-2"></i>Entrada</h3><p>O aluguel é pago antecipadamente. Para receber as chaves, é exigido depósito de segurança de um mês.</p></div><div class="condition-card"><h3><i class="fas fa-user-check mr-2"></i>Perfil</h3><p>Unidades destinadas a pessoas solteiras. Não são aceitos casais, crianças ou animais. Não há garagem.</p></div></div></div></section></main><footer class="bg-black border-t border-white/10 py-8 px-6 text-center"><a href="../index.html" class="text-gray-300 hover:text-white">Kitnet Mais Top</a><p class="text-gray-500 text-sm mt-2">© 2026 - Todos os direitos reservados</p></footer><script>const images=[{data}];let index=0;const main=document.getElementById('main-image'),current=document.getElementById('current'),thumbs=[...document.querySelectorAll('.thumbs button')];function show(i){{index=(i+images.length)%images.length;main.src=images[index];current.textContent=index+1;thumbs.forEach((b,n)=>b.classList.toggle('active',n===index));}}document.getElementById('prev').onclick=()=>show(index-1);document.getElementById('next').onclick=()=>show(index+1);thumbs.forEach((b,n)=>b.onclick=()=>show(n));</script></body></html>'''

def cards():
    out=[]
    for u in UNITS:
        imgs=images_for(u); first=imgs[0].with_suffix('.webp').name; busy=u['status']!='disponível'
        badge='OCUPADA' if busy else 'DISPONÍVEL'
        action='' if busy else f'<a href="kitnets/kitnet-{u["id"]}.html" class="w-full bg-[#FFFF6F] text-black px-4 py-3 rounded-full font-semibold text-sm inline-flex items-center justify-center gap-2 hover:opacity-90 transition">Ver unidade <i class="fas fa-arrow-right"></i></a>'
        out.append(f'''<a href="kitnets/kitnet-{u['id']}.html" class="property-card block"><div class="relative h-64 bg-black"><img src="assets/kitnets/kitnet-{u['id']}/{first}" alt="Kitnet {u['id']} — {u['short']}" class="w-full h-full object-cover" loading="lazy"><span class="badge {'badge-disponivel' if not busy else ''}">{badge}</span></div><p class="specs">{u['area']} • {u['rooms']} • {u['furnished']}</p><p class="address">Av. Aracruz, Novos Estados</p><p class="price">R$ 850/mês</p><div class="px-3 pb-3">{action}</div></a>''')
    return '\n'.join(out)

def update_home():
    p=ROOT/'index.html'; text=p.read_text()
    text=text.replace('''            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">\n                <!-- Kitnet 02 - DISPONÍVEL -->''','''            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">''',1)
    start=text.index('            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">', text.index('<!-- Kitnets -->'))
    end=text.index('            </div>\n        </div>\n    </section>\n\n    <!-- Vantagens -->', start)+len('            </div>')
    text=text[:start]+'''            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">\n'''+cards()+'''\n            </div>'''+text[end:]
    text=text.replace('Internet e água inclusos.', 'Água, esgoto, IPTU e taxa de lixo inclusos; internet como bônus por adimplência.', 1)
    text=text.replace('Pagamento posterior (mora, depois paga)', 'Pagamento antecipado', 1)
    text=text.replace('Sem fiador (se Serasa limpa)', 'Fiador se houver restrição no Serasa', 1)
    text=text.replace('Seguro da unidade: R$35/ano', 'Seguro contra incêndio obrigatório', 1)
    text=text.replace('Internet básica como <strong class="text-[#FFFF6F]">bônus por adimplência</strong>', 'Internet como <strong class="text-[#FFFF6F]">bônus por adimplência</strong>', 1)
    p.write_text(text)

if __name__ == '__main__':
    optimize_images()
    for u in UNITS:
        (ROOT/'kitnets').mkdir(exist_ok=True)
        (ROOT/'kitnets'/f"kitnet-{u['id']}.html").write_text(page(u))
    update_home()
    print('generated', ', '.join(f"kitnet-{u['id']}.html" for u in UNITS))
    for u in UNITS:
        print(u['id'], len(images_for(u)), 'images')
