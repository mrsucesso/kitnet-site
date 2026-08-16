#!/usr/bin/env python3
"""
sync-price.py — Atualiza o valor "a partir de R$ ___" em TODO o site
Kitnet Mais Top a partir de um único comando, em vez de editar arquivo por arquivo.

A kitnet-05 (unidade mais barata) é a referência: hoje todas as unidades
custam o mesmo valor, então o script troca o número em todos os lugares
de uma vez (schema JSON-LD + textos visíveis + meta description).

Uso:
    python3 scripts/sync-price.py --novo 950
    python3 scripts/sync-price.py --novo 950 --dry-run   (só mostra o que mudaria, não grava nada)

Depois de rodar: revisar o diff (git diff), e publicar com
    git add -A && git commit -m "chore: atualiza preço base para R$ <novo>/mês"
    git push origin main
    npx wrangler pages deploy . --project-name=kitnet-mais-top --branch=main

NÃO mexe em:
  - preços de OUTROS bairros citados em tabelas comparativas (ex: "Nova Bahia R$ 900 – 1.200")
  - qualquer valor que não seja o preço-base da Kitnet Mais Top
"""
import argparse
import glob
import re
import sys

# Padrões que representam o preço-base atual, aprendidos a partir do
# valor detectado automaticamente na kitnet-05 (fonte da verdade).
# Cada tupla é (texto exato com o valor ANTIGO, texto exato com o valor NOVO)
# — construído dinamicamente a partir do --antigo/--novo informados.

# Templates exatos para os casos que NÃO vêm precedidos de "a partir de"
# (schema JSON-LD, meta description sem qualificador, preço previsto da kitnet-06).
TEMPLATES = [
    ('"price": "{old}"', '"price": "{new}"'),
    ("por R$ {old}/mês.", "por R$ {new}/mês."),
    ("preço previsto de R$ {old}/mês", "preço previsto de R$ {new}/mês"),
]

# Regex genérico: qualquer "a partir de R$ <valor>" (maiúsculo ou minúsculo)
# em qualquer contexto — cobre badges, cards, prosa de artigo, heading etc,
# sem precisar listar frase por frase. Não toca em "R$ <valor>" que NÃO
# vem precedido de "a partir de" (ex: tabela comparativa de outro bairro).
PARTIR_DE_RE_TEMPLATE = r'([Aa] partir de (?:<strong>)?R\$ ?){old}\b'


def detect_current_price(root):
    """Lê o preço atual a partir da kitnet-05 (fonte da verdade)."""
    path = f"{root}/kitnets/kitnet-05.html"
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"ERRO: {path} não encontrado — rode este script de dentro da raiz do repo kitnet-site.")
        sys.exit(1)
    m = re.search(r'"price":\s*"(\d+)"', text)
    if not m:
        print("ERRO: não encontrei o campo price no JSON-LD da kitnet-05. Verifique manualmente.")
        sys.exit(1)
    return m.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--novo", required=True, help="Novo valor do preço-base (só número, ex: 950)")
    ap.add_argument("--antigo", default=None, help="Forçar valor antigo (padrão: detectado da kitnet-05)")
    ap.add_argument("--root", default=".", help="Raiz do repo (padrão: diretório atual)")
    ap.add_argument("--dry-run", action="store_true", help="Só mostra o que mudaria, não grava nada")
    args = ap.parse_args()

    old = args.antigo or detect_current_price(args.root)
    new = args.novo

    if old == new:
        print(f"Preço já é R$ {old} — nada a fazer.")
        return

    print(f"Trocando preço-base: R$ {old} -> R$ {new}\n")

    replacements = [(t_old.format(old=old), t_new.format(new=new)) for t_old, t_new in TEMPLATES]
    partir_de_re = re.compile(PARTIR_DE_RE_TEMPLATE.format(old=re.escape(old)))

    changed_files = {}
    for f in glob.glob(f"{args.root}/**/*.html", recursive=True):
        if ".git" in f:
            continue
        text = open(f, encoding="utf-8").read()
        orig = text
        hits_this_file = 0
        for t_old, t_new in replacements:
            c = text.count(t_old)
            if c:
                text = text.replace(t_old, t_new)
                hits_this_file += c
        text, n_partir = partir_de_re.subn(lambda m: m.group(1) + new, text)
        hits_this_file += n_partir
        if text != orig:
            changed_files[f] = hits_this_file
            if not args.dry_run:
                open(f, "w", encoding="utf-8").write(text)

    if not changed_files:
        print("Nenhuma ocorrência encontrada. Verifique se o valor --antigo está certo.")
        return

    total = sum(changed_files.values())
    for f, n in sorted(changed_files.items()):
        print(f"  {f}: {n} ocorrência(s)")
    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}Total: {total} ocorrência(s) em {len(changed_files)} arquivo(s).")

    # aviso sobre pontos que exigem revisão manual (não são preço-base, ficam de fora por design)
    print(
        "\nNÃO tocado por design (revisar manualmente se necessário):\n"
        "  - Tabelas comparativas de OUTROS bairros (ex: artigo Havan/Atacadão/Assaí)\n"
    )

    if args.dry_run:
        print("Nada foi gravado (--dry-run). Rode sem essa flag para aplicar de verdade.")
    else:
        print("Gravado. Revise com `git diff`, depois publique:")
        print("  git add -A && git commit -m \"chore: atualiza preço base para R$ " + new + "/mês\"")
        print("  git push origin main")
        print("  npx wrangler pages deploy . --project-name=kitnet-mais-top --branch=main")


if __name__ == "__main__":
    main()
