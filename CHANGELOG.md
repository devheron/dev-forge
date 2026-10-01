# Histórico de versões

## 0.4.0 — 2026-10-01

- Executável portátil Windows x64 com ícone, sem exigir instalação de Python.
- Build automatizado de binário portátil Linux x64.
- Botão para criar um atalho na área de trabalho ou no menu de aplicativos.
- Atualizador escolhe pacote de código-fonte ou executável conforme a distribuição em uso.
- Configurações de executáveis preservadas na pasta de dados do usuário.
- Actions compila e verifica os executáveis antes de publicar a release.
- Enviar uma versão nova em version.json para main dispara a criação da tag e da release.
- Publicação reutiliza uma release existente, evitando erro de tag duplicada.
- Guias locais separados para primeira publicação e atualizações futuras.

## 0.3.0 — 2026-10-01

- Layout adaptável com painéis lado a lado ou empilhados conforme a janela.
- Lista de ferramentas com busca, textos ajustáveis e rolagem pelo mouse.
- Abas separadas para comandos e etapas complementares.
- Botões e controles alinhados, com reorganização em janelas menores.
- README público focado na instalação e no uso do aplicativo.
- Guia de publicação separado, excluído do Git e dos pacotes de release.
- Captura da interface incluída na apresentação do projeto.

## 0.2.1 — 2026-10-01

- Documentação distingue aplicativos gráficos, ferramentas de terminal e serviços.
- Etapas após instalação disponíveis em um botão próprio e exibidas ao iniciar o terminal.
- Scripts também apresentam as orientações e as instalações manuais pendentes.
- R incluído como dependência ao selecionar RStudio.
- Validação dos manifests WinGet e dos endpoints de download documentada.

## 0.2.0 — 2026-10-01

- Seletor visual de sistema operacional com botões Windows e Linux.
- Cores para comandos, comentários, validações, títulos e referências oficiais.
- Versão e data de publicação no cabeçalho.
- Histórico de alterações acessível no aplicativo.
- Consulta opcional de releases estáveis no GitHub.
- Download solicitado pelo usuário, verificação SHA-256 e abertura da nova versão em pasta separada.
- Validação de caminhos e limites de tamanho antes de extrair atualizações.
- Documentação de manutenção, publicação e privacidade.

## 0.1.0 — 2026-10-01

- Catálogo inicial com 27 ferramentas e quatro perfis de desenvolvimento.
- Geração de scripts PowerShell e Bash.
- Inclusão de dependências básicas e referências de instalação manual.
- Interface local com cópia, exportação e execução de scripts.
