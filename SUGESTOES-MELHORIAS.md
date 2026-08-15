# 📋 Sugestões de Melhoria — Site Kitnet Mais Top

> Análise feita em 15/08/2026

---

## 🔴 Prioridade Alta (Impacto Imediato no SEO e Conversão)

### 1. Schema.org / JSON-LD — Adicionar mais estrutura

**O que já tem:** `Apartment` schema nas páginas de unidade

**O que falta:**

- **Página inicial:** `LocalBusiness` ou `RealEstateAgent` schema com NAP (Name, Address, Phone)
- **Organization** schema no site todo (logo, redes sociais, contato)
- **BreadcrumbList** schema em todas as páginas
- **FAQPage** schema na página de regras (perguntas frequentes sobre locação)
- **Review / AggregateRating** (quando tiver avaliações)

**Exemplo de Organization para colocar no `<head>`:**
```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Kitnet Mais Top",
  "image": "https://kitnet.mais.top/logo.png",
  "url": "https://kitnet.mais.top",
  "telephone": "+556781227323",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Av. Aracruz com Sr. do Bonfim",
    "addressLocality": "Campo Grande",
    "addressRegion": "MS",
    "postalCode": "79022-000",
    "addressCountry": "BR"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "-20.4697",
    "longitude": "-54.6201"
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "opens": "08:00",
    "closes": "20:00"
  },
  "priceRange": "R$",
  "areaServed": {
    "@type": "City",
    "name": "Campo Grande"
  }
}
```

### 2. Google Search Console & Indexação

- **Registrar no Google Search Console** (se ainda não feito)
- **Sitemap já está OK** — só precisa submeter no GSC
- **Verificar indexação** das páginas de artigos (são ótimas para tráfego orgânico)
- **Robots.txt está OK**

### 3. Imagens — Otimização adicional

**O que já faz bem:**
- ✅ Formato WebP
- ✅ Lazy loading
- ✅ Alt text descritivo
- ✅ Tamanhos width/height no HTML

**O que pode melhorar:**
- **srcset responsivo:** Fornecer versões menores para mobile (800px, 1200px)
- **Placeholder/low-res:** Mostrar um blur-up ou cor de fundo enquanto carrega
- **Hero image da home:** `bairro-novos-estados.webp` — verificar se está otimizada (a hero costuma ser pesada)

### 4. PageSpeed — Core Web Vitals

**Prováveis problemas:**
- Tailwind via CDN (`cdn.tailwindcss.com`) — bloqueia renderização. **Solução:** Inline o CSS crítico ou use o build do Tailwind
- Font Awesome via CDN — carrega ícones que talvez não use todos. **Solução:** Subset ou SVG inline
- Google Fonts — pode adicionar `display=swap` e pré-conectar

**Quick wins:**
```html
<!-- Pré-conectar origens externas -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com">
```

---

## 🟡 Prioridade Média (SEO Local e Conversão)

### 5. Google Meu Negócio (GMB)

**Isso é CRUCIAL para imóveis locais.**

- Criar/otimizar perfil no Google Business Profile
- Nome: "Kitnet Mais Top"
- Categoria: "Imobiliária" ou "Aluguel de imóveis"
- Endereço: Av. Aracruz com Sr. do Bonfim, Novos Estados
- Telefone: (67) 8122-7323
- Site: https://kitnet.mais.top
- **Postar fotos das kitnets no GMB** (as mesmas do site)
- **Solicitar avaliações** dos inquilinos atuais
- **Responder TODAS as avaliações**

### 6. Página "Sobre" / Quem Somos

**Falta no site.** O Google valoriza E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness). Uma página sobre:

- Quem é o proprietário (foto ajuda)
- Há quanto tempo aluga kitnets
- Depoimentos de inquilinos
- Diferencial do atendimento

**Isso aumenta a confiança e o ranking.**

### 7. Depoimentos / Social Proof

- Adicionar depoimentos reais de inquilinos nas páginas de unidade
- Fotos dos inquilinos (com permissão) aumentam conversão
- Selo de "Kitnet bem avaliada" ou "Recomendada por moradores"

### 8. Páginas de Artigos — Otimizar para Featured Snippets

**Os artigos já existem e são bons.** Para Featured Snippets:

- Adicionar **FAQ schema** nos artigos
- Usar **listas numeradas** e **tabelas** quando possível
- Responder diretamente na primeira frase (formato "resposta direta")
- Exemplo: *"Uma kitnet individual em Campo Grande custa em média R$ 800 a R$ 1.200 por mês..."*

---

## 🟢 Prioridade Baixa (Refinamentos)

### 9. HTML Semântico e Acessibilidade

**O que já faz bem:**
- ✅ `lang="pt-BR"`
- ✅ `aria-label` nos botões
- ✅ Alt text nas imagens

**O que pode melhorar:**
- Usar `<header>`, `<main>`, `<article>`, `<footer>` em vez de só `<div>`
- Adicionar `aria-current="page"` no link ativo do menu
- Contrast ratio do texto cinza sobre preto — verificar se passa no WCAG AA

### 10. Meta Tags Sociais

**Já tem Open Graph e Twitter Cards** — bom!

**Sugestão:** Adicionar `og:locale`:
```html
<meta property="og:locale" content="pt_BR">
```

### 11. Favicon

**Já tem** `logo.png` como favicon. **Sugestão:** Criar um favicon `.ico` multi-resolução (16x16, 32x32, 180x180 para Apple touch icon).

### 12. Trackeamento

**Adicionar:**
- Google Analytics 4 (GA4)
- Google Tag Manager (opcional)
- Pixel de conversão do WhatsApp (se houver)
- **Eventos:** clique no botão "Tenho interesse", clique no WhatsApp float

### 13. Página 404 Personalizada

Criar uma página 404 amigável com:
- Link para todas as kitnets
- Link para artigos
- CTA do WhatsApp

### 14. Segurança — HTTPS (já deve estar OK no Cloudflare)

- Verificar se o certificado SSL está ativo
- Forçar redirect HTTP → HTTPS
- Adicionar header `Strict-Transport-Security` (HSTS)

---

## 📊 Resumo das Top 5 Ações Recomendadas

| # | Ação | Impacto | Esforço |
|---|------|---------|---------|
| 1 | **Google Meu Negócio** | 🔥🔥🔥🔥🔥 | Baixo |
| 2 | **Schema LocalBusiness + Breadcrumb** | 🔥🔥🔥🔥 | Baixo |
| 3 | **Google Search Console + Indexação** | 🔥🔥🔥🔥 | Baixo |
| 4 | **Página "Sobre" com depoimentos** | 🔥🔥🔥 | Médio |
| 5 | **Otimizar CSS/Fonts (PageSpeed)** | 🔥🔥🔥 | Médio |

---

## 🎯 Dica Bônus: Estratégia de Conteúdo

Os artigos são excelentes para SEO. Próximos temas sugeridos:

- "Como alugar kitnet sem fiador em Campo Grande"
- "Kitnet para estudante em Campo Grande: onde morar"
- "Diferença entre kitnet e quitinete"
- "Bairro Novos Estados: é seguro morar?"
- "Quanto custa morar sozinho em Campo Grande-MS"

**Cada artigo = uma nova porta de entrada orgânica no Google.**
