# Hotfix — ordem das fotos da MASSA Tee (trezewear.com)

**Data:** 2026-08-11
**O que mudou:** na página do produto (`/produto?p=massa-tee`), a ordem das duas
primeiras fotos da galeria foi invertida:

- Antes: `['massa-frente.jpg','massa-tras.jpg','massa-grupo.jpg']`
- Depois: `['massa-tras.jpg','massa-frente.jpg','massa-grupo.jpg']`

Ou seja: a foto das **costas** (arte da Massa / logo) agora aparece primeiro, e a
foto da **frente** (escudos no peito) em segundo. A terceira foto (grupo) não mudou.

## Como foi publicado

O código-fonte do site não estava em nenhum repositório GitHub — os deploys
anteriores do projeto Vercel `treze-landing` foram feitos via CLI a partir de
containers de sessões antigas (fonte perdida). O deploy atual tem 10 funções
serverless (`/api/lead` etc.) cujo código não é recuperável por HTTP, então
**não era seguro reconstruir o site inteiro**.

Solução aplicada (deploy cirúrgico):

1. Novo deployment de produção contendo **apenas 2 arquivos**:
   - `produto.html` — cópia exata da versão em produção, com a única mudança na
     linha do catálogo da `massa-tee` (este diretório guarda a cópia).
   - `vercel.json` — replica `cleanUrls` e os headers de segurança originais
     para `/produto`, e faz **proxy de todo o resto** (home, carrinho, custom,
     customizer, imagens, `/api/*`) para o deployment anterior, que permanece
     intacto na Vercel:
     `https://treze-landing-l17z0go2q-pedropacebh-2174s-projects.vercel.app`
2. Para o proxy funcionar, a proteção "Vercel Authentication" do projeto foi
   ajustada de "Standard Protection" para **"Only Preview Deployments"** — as
   URLs geradas de produção (mesmo conteúdo público de trezewear.com) ficaram
   acessíveis; previews continuam protegidos.

## Atenção — fonte da verdade

O deployment publicado depende do deployment antigo (não deletar o deployment
`treze-landing-l17z0go2q` na Vercel). **Quando o código-fonte original do site
for localizado** (a conversa "treze" no claude.ai / máquina local), aplicar a
mesma troca no `produto.html` de lá, senão o próximo deploy completo volta a
ordem antiga das fotos.
