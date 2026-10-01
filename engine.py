"""Generate reviewed scripts from an allowlisted catalog, never user commands."""
from catalog import CATALOG
import shlex

def resolve(keys):
    selected = set(keys)
    if not selected <= CATALOG.keys():
        raise ValueError('Ferramenta desconhecida')
    if selected & {'angular', 'react'}:
        selected.add('node')
    if 'minikube' in selected:
        selected.update(('docker', 'kubectl'))
    if 'rstudio' in selected:
        selected.add('r')
    return [item for key, item in CATALOG.items() if key in selected]

def generate(keys, platform):
    items = resolve(keys)
    manual = []
    if platform == 'windows':
        lines = ["# Dev Forge - revise antes de executar", "$ErrorActionPreference = 'Stop'", "if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Instale App Installer / WinGet pela Microsoft Store.' }", "Start-Transcript -Path (Join-Path $PSScriptRoot ('install-' + (Get-Date -Format yyyyMMdd-HHmmss) + '.log'))", 'try {']
        for item in items:
            if item['winget']:
                package = item['winget']
                lines += [f"Write-Host 'Instalando {item['name']}'", f'winget install --id {package} --exact --source winget --accept-source-agreements --accept-package-agreements --disable-interactivity', "if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne -1978335189) { throw ('WinGet falhou: ' + $LASTEXITCODE) }"]
            elif item['key'] == 'wsl':
                lines += ['wsl --install -d Ubuntu', "if ($LASTEXITCODE -ne 0) { throw 'WSL falhou. Verifique virtualizacao e requisitos.' }"]
            elif item['key'] != 'angular':
                manual.append(item)
        if any(i['key'] == 'angular' for i in items):
            lines += ["$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')", 'npm.cmd install -g @angular/cli', "if ($LASTEXITCODE -ne 0) { throw 'Angular CLI falhou' }"]
        lines += ["Write-Host 'Pacotes automaticos processados. Confira as etapas complementares abaixo.'"]
        lines += ["Write-Host '" + line.replace("'", "''") + "'" for line in notes(keys, platform).splitlines() if line]
        lines += ["Write-Host 'Instalacao manual pendente: " + item['name'].replace("'", "''") + " - " + item['url'] + "'" for item in manual]
        lines += ['} finally { Stop-Transcript }', "Read-Host 'Pressione Enter para fechar'"]
    elif platform == 'linux':
        lines = ['#!/usr/bin/env bash', 'set -euo pipefail', '# Dev Forge: Ubuntu / Debian, pacotes da distribuicao.', 'source /etc/os-release', 'case "$ID" in ubuntu|debian) ;; *) echo "Use Ubuntu ou Debian."; exit 1;; esac', '[ "$(id -u)" -ne 0 ] || { echo "Execute como usuario comum, com sudo."; exit 1; }', 'sudo -v', 'exec > >(tee -a "dev-forge-install-$(date +%Y%m%d-%H%M%S).log") 2>&1', 'sudo apt-get update']
        for item in items:
            if item['apt']:
                lines.append('sudo apt-get install -y ' + item['apt'])
            else:
                manual.append(item)
        lines.append('echo "Pacotes automaticos processados. Confira as etapas complementares abaixo."')
        lines += ["printf '%s\\n' " + shlex.quote(line) for line in notes(keys, platform).splitlines() if line]
        lines += ["printf '%s\\n' " + shlex.quote('Instalacao manual pendente: ' + item['name'] + ' - ' + item['url']) for item in manual]
    else:
        raise ValueError('Plataforma desconhecida')
    return '\n'.join(lines) + '\n', manual

def notes(keys, platform):
    selected = {i['key'] for i in resolve(keys)}
    result = []
    if selected:
        result.append('CONFIRMACAO: confira o resultado de cada instalador no terminal. Esta lista e orientacao, nao confirmacao de sucesso. Se houve erro, resolva antes de continuar. Abra um novo terminal para atualizar o PATH.')
    gui = {'vscode': 'Visual Studio Code', 'arduino': 'Arduino IDE', 'rstudio': 'RStudio', 'virtualbox': 'VirtualBox', 'postman': 'Postman', 'xampp': 'XAMPP Control Panel'}
    for key, name in gui.items():
        if key in selected:
            where = 'menu Iniciar do Windows' if platform == 'windows' else 'menu de aplicativos do ambiente grafico, apos concluir a instalacao oficial manual'
            result.append(f'{name}: procure no {where}. O atalho na area de trabalho depende do instalador; nao e garantido.')
    for key, instruction in {
        'git': 'Git: verifique git --version. Configure nome e email localmente quando for criar commits.',
        'node': 'Node/npm: verifique node --version e npm --version em um novo terminal.',
        'python': 'Python: verifique python --version no Windows ou python3 --version no Linux. Crie um ambiente virtual por projeto.',
        'ruby': 'Ruby: verifique ruby --version e gem --version. No Windows, conclua o preparo de MSYS2/DevKit conforme RubyInstaller.',
        'r': 'R: verifique R --version no terminal ou abra o R pelo menu quando disponivel. RStudio e um aplicativo separado.',
        'go': 'Go: verifique go version.',
        'java': 'Java JDK: verifique java -version e javac -version.',
        'vscode': 'VS Code: abra uma pasta de projeto e instale as extensoes das linguagens usadas. Teste code --version em um novo terminal.',
        'arduino': 'Arduino IDE: selecione a placa, instale seu pacote no gerenciador de placas e escolha a porta. Drivers USB podem ser necessarios.',
        'rstudio': 'RStudio: abra o aplicativo e confirme que encontrou o R instalado.',
        'postman': 'Postman: abra o aplicativo e crie uma requisicao para sua API. Escolha autenticar somente se precisar das funcoes de conta.',
        'xampp': 'XAMPP: abra o painel e inicie apenas os servicos necessarios. Verifique portas ocupadas e acesse http://localhost. Nao exponha o ambiente local diretamente na internet.',
        'virtualbox': 'VirtualBox: crie uma VM, escolha uma ISO e ajuste memoria/disco. A instalacao do hipervisor nao baixa nem configura um sistema convidado.',
        'wsl': 'WSL: reinicie se solicitado, abra Ubuntu e crie o usuario Linux. Confira wsl --status.',
        'kubectl': 'kubectl: verifique kubectl version --client. O cliente sozinho nao cria um cluster.',
        'helm': 'Helm: verifique helm version. Configure o contexto do cluster antes de instalar charts.',
        'terraform': 'Terraform: verifique terraform version. Revise terraform plan antes de criar infraestrutura; provedores podem gerar custos.',
        'postgres': 'PostgreSQL: confira psql --version e o servico instalado. Configure usuario, senha e banco localmente. Instalacao do servidor nao garante uma interface grafica; pgAdmin depende dos componentes escolhidos.',
        'sqlite': 'SQLite: verifique sqlite3 --version. Este pacote fornece terminal e utilitarios, nao uma interface grafica de banco.'
    }.items():
        if key in selected:
            result.append(instruction)
    if 'docker' in selected:
        result.append('Docker Windows: habilite virtualizacao/WSL 2, reinicie se solicitado e abra Docker Desktop. Linux: docker.io vem da distribuicao; use sudo docker ou configure acesso conforme a documentacao.')
    if 'minikube' in selected:
        result.append('Depois de Docker estar funcionando: minikube start --driver=docker; kubectl get nodes. Kubernetes local e criado pelo Minikube.')
    if 'react' in selected:
        result.append('Em uma pasta de projetos: npm create vite@latest meu-react -- --template react; cd meu-react; npm install; npm run dev. A receita exige confirmacao e cria um projeto.')
    if 'angular' in selected:
        result.append('Angular: confirme a versao de Node exigida em angular.dev. Linux: apos instalar Node compativel, configure um prefixo npm no usuario e execute npm install -g @angular/cli. Novo projeto: ng new meu-angular.')
    if 'angularjs' in selected:
        result.append('AngularJS encerrou suporte. Disponivel apenas como referencia para manutencao de projetos antigos.')
    if selected & {'aws', 'gcloud', 'azure'}:
        result.append('As CLIs nao criam contas nem recursos pagos. Autentique depois: aws configure / gcloud init / az login.')
    if platform == 'linux':
        result.append('Versoes apt variam por distribuicao. Alguns pacotes podem nao existir em releases antigas; o script para no primeiro erro. Ferramentas sem pacote apt aparecem como instalacao oficial manual.')
    return '\n\n'.join(result)
