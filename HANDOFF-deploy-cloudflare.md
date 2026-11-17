# HANDOFF: Deploy Kitnet Mais Top → Cloudflare Pages

## 📋 Contexto
Site de kitnets no GitHub (mrsucesso/kitnet-site). O push pro GitHub funciona, mas o deploy automático no Cloudflare Pages NÃO está disparando.

## ✅ O que já está feito
- Branch `main` do GitHub está atualizado com o design correto (dark theme)
- Branch `gh-pages` também está atualizado (GitHub Actions funciona)
- Página da Kitnet 01 (`kitnets/kitnet-01.html`) está formatada e no lugar
- Assets (fotos, logo) todos commitados
- Workflow `.github/workflows/deploy.yml` restaurado

## ❌ Problema identificado
O Cloudflare Pages **não detecta pushes do GitHub automaticamente**.

Evidência via API Cloudflare:
- Projeto: `kitnet-mais-top` (ID: dadce9c2-4ef9-42a2-910a-2bd582d7d5b0)
- Último deploy: `c20607bc` (2026-08-14T18:16:10Z)
- Todos os deploys são do tipo **`ad_hoc`** (manuais)
- `commit_hash` vazio em todos → integração GitHub desconectada ou quebrada

## 🔧 O que precisa ser feito
1. **No dashboard do Cloudflare Pages** (https://dash.cloudflare.com/):
   - Ir em Workers & Pages → kitnet-mais-top
   - Verificar a aba "Settings" → "Build & deployments"
   - Confirmar se o Git integration está conectado ao repo `mrsucesso/kitnet-site`
   - Se desconectado: reconectar
   - Se conectado mas não disparando: verificar se o webhook do GitHub não foi removido

2. **Alternativa mais robusta**: Configurar o GitHub Actions para fazer deploy DIRETO pro Cloudflare Pages (sem depender do gh-pages):
   - Usar a action `cloudflare/pages-action@v1` no workflow
   - Isso elimina a dependência da integração nativa do Cloudflare

## 📁 Arquivos no workspace
- `index.html` — Home correta (design dark theme, 678 linhas)
- `kitnets/kitnet-01.html` — Página da unidade 01 (formatada, 382 linhas)
- `assets/kitnets/kitnet-01/` — 9 fotos da unidade 01
- `assets/hero/kitnet-01-hero-final.jpg` — Hero image
- `logo.png` — Logo do site
- `.github/workflows/deploy.yml` — Workflow atual (deploy pro gh-pages)
- `CNAME` — `kitnet.mais.top`

## 🔗 Links importantes
- Repo: https://github.com/mrsucesso/kitnet-site
- Site atual: https://kitnet-mais-top.pages.dev/
- Domínio oficial: https://kitnet.mais.top/
- Branch main: https://github.com/mrsucesso/kitnet-site/tree/main
- Branch gh-pages: https://github.com/mrsucesso/kitnet-site/tree/gh-pages

## 📞 Contato do proprietário
- WhatsApp: (67) 8122-7323
- Instagram: @kitnetmaistop
- Endereço: Av. Aracruz com Sr. do Bonfim, Novos Estados, Campo Grande-MS

---
Criado em: 2026-08-14
Handoff por: Kimi Work
Próximo responsável: Hermes

---

## RESOLVIDO em 17/11/2026

O diagnóstico original deste handoff ("Cloudflare Pages não detecta pushes")
estava certo no sintoma e incompleto na causa. Havia **dois** projetos:

| Projeto | Domínio | Origem |
|---|---|---|
| `kitnet-mais-top` | **kitnet.mais.top** | upload direto (sem Git) |
| `kitnet-mais-top-git` | só o `.pages.dev` | integração Git, auto-deploy |

A integração Git funcionava — no projeto errado. O domínio real nunca foi
publicado por push.

Correções aplicadas:

1. `.github/workflows/deploy-pages.yml` passou a publicar em `kitnet-mais-top`,
   com a interpolação de secrets corrigida (estava com chaves quádruplas) e um
   passo final que exige HTTP 200 em `kitnet.mais.top`.
2. Criada a label `deploy-approved`, que não existia — sem ela a condição do
   gate nunca podia ser verdadeira.
3. Auto-deploy do projeto sombra desligado: ele publicava a cada push, sem
   gate, numa URL pública e indexável (conteúdo duplicado).

**Como publicar hoje:** PR com a label `deploy-approved` e merge. Push direto em
`main` não publica — comportamento agora real, não só documentado.
