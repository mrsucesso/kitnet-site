#!/usr/bin/env python3
"""Adiciona Schema LocalBusiness, BreadcrumbList e otimizações de performance."""

import os
import re
from pathlib import Path

# Schema LocalBusiness base
LOCAL_BUSINESS_SCHEMA = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"RealEstateAgent","name":"Kitnet Mais Top","image":"https://kitnet.mais.top/logo.png","url":"https://kitnet.mais.top","telephone":"+556781227323","address":{"@type":"PostalAddress","streetAddress":"Av. Aracruz com Sr. do Bonfim","addressLocality":"Campo Grande","addressRegion":"MS","addressCountry":"BR"},"geo":{"@type":"GeoCoordinates","latitude":"-20.4697","longitude":"-54.6201"},"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"08:00","closes":"20:00"},"priceRange":"R$","areaServed":{"@type":"City","name":"Campo Grande"}}</script>'''

# Preconnect hints
PRECONNECT = '''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://cdnjs.cloudflare.com">
  <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">'''

# og:locale
OG_LOCALE = '  <meta property="og:locale" content="pt_BR">'

def add_schema_and_optimizations(filepath, breadcrumbs=None):
    """Adiciona schema e otimizações em um arquivo HTML."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # 1. Adiciona preconnect antes do primeiro <link> ou <script>
    if 'preconnect' not in content:
        # Encontra a posição após o </title> para inserir preconnect
        title_end = content.find('</title>')
        if title_end != -1:
            insert_pos = title_end + len('</title>')
            content = content[:insert_pos] + '\n' + PRECONNECT + content[insert_pos:]
            changes.append('preconnect')
    
    # 2. Adiciona og:locale antes do primeiro og:type
    if 'og:locale' not in content and 'og:type' in content:
        og_type_pos = content.find('<meta property="og:type"')
        if og_type_pos != -1:
            content = content[:og_type_pos] + OG_LOCALE + '\n' + content[og_type_pos:]
            changes.append('og_locale')
    
    # 3. Adiciona LocalBusiness schema antes do fechamento do </head>
    if 'RealEstateAgent' not in content:
        head_end = content.rfind('</head>')
        if head_end != -1:
            content = content[:head_end] + LOCAL_BUSINESS_SCHEMA + '\n' + content[head_end:]
            changes.append('localbusiness')
    
    # 4. Adiciona BreadcrumbList se fornecido
    if breadcrumbs and 'BreadcrumbList' not in content:
        head_end = content.rfind('</head>')
        if head_end != -1:
            breadcrumb_schema = f'<script type="application/ld+json">{breadcrumbs}</script>'
            content = content[:head_end] + breadcrumb_schema + '\n' + content[head_end:]
            changes.append('breadcrumb')
    
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✅ {filepath}: {", ".join(changes)}')
        return True
    else:
        print(f'  ⏭️  {filepath}: nada a fazer')
        return False

def main():
    base_dir = Path('.')
    modified = 0
    
    # Home
    if add_schema_and_optimizations(base_dir / 'index.html'):
        modified += 1
    
    # Kitnets index
    if add_schema_and_optimizations(base_dir / 'kitnets' / 'index.html'):
        modified += 1
    
    # Páginas de unidades
    for i in range(1, 7):
        filepath = base_dir / 'kitnets' / f'kitnet-{i:02d}.html'
        if filepath.exists():
            if add_schema_and_optimizations(filepath):
                modified += 1
    
    # Artigos index
    artigos_index = base_dir / 'artigos' / 'index.html'
    if artigos_index.exists():
        if add_schema_and_optimizations(artigos_index):
            modified += 1
    
    # Artigos individuais
    artigos = [
        'kitnet-direto-com-proprietario-campo-grande.html',
        'kitnet-individual-para-alugar-campo-grande.html',
        'kitnet-mobiliada-em-campo-grande-ms.html',
        'kitnet-novos-estados-campo-grande.html',
    ]
    for artigo in artigos:
        filepath = base_dir / 'artigos' / artigo
        if filepath.exists():
            if add_schema_and_optimizations(filepath):
                modified += 1
    
    # Regras
    regras = base_dir / 'regras-e-condicoes' / 'index.html'
    if regras.exists():
        if add_schema_and_optimizations(regras):
            modified += 1
    
    print(f'\n📊 Total de arquivos modificados: {modified}')

if __name__ == '__main__':
    main()
