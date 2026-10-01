# Validação do catálogo

Data: 1 de outubro de 2026. Versão do aplicativo: 0.2.1.

## Resultado

Foram encontrados os 23 IDs WinGet configurados no catálogo oficial microsoft/winget-pkgs. Os 45 endpoints de instaladores declarados nos manifests consultados responderam HTTP 200 a requisições HEAD. Foram consideradas as versões numéricas mais recentes encontradas em cada diretório; a escolha efetiva de versão e arquitetura na instalação cabe ao WinGet.

Uma requisição HEAD verifica acesso ao endereço sem transferir o instalador inteiro. Portanto, esta verificação não atesta o conteúdo binário, a execução do instalador, os atalhos, o suporte a todas as arquiteturas ou o funcionamento posterior do programa. Os resultados podem mudar após esta data.

## Manifests consultados

| Ferramenta | ID WinGet | Versão do manifest | Endpoints |
| --- | --- | --- | --- |
| Git | `Git.Git` | [2.55.0.5](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/g/Git/Git/2.55.0.5/Git.Git.installer.yaml) | 200, 200 |
| Node.js LTS + npm | `OpenJS.NodeJS.LTS` | [24.19.0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/o/OpenJS/NodeJS/LTS/24.19.0/OpenJS.NodeJS.LTS.installer.yaml) | 200, 200, 200, 200 |
| Python 3 | `Python.Python.3.13` | [3.13.15](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/p/Python/Python/3/13/3.13.15/Python.Python.3.13.installer.yaml) | 200, 200, 200 |
| Ruby | `RubyInstallerTeam.RubyWithDevKit.3.4` | [3.4.10-1](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/r/RubyInstallerTeam/RubyWithDevKit/3/4/3.4.10-1/RubyInstallerTeam.RubyWithDevKit.3.4.installer.yaml) | 200, 200, 200 |
| R | `RProject.R` | [4.6.1](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/r/RProject/R/4.6.1/RProject.R.installer.yaml) | 200 |
| Go | `GoLang.Go` | [1.27.0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/g/GoLang/Go/1.27.0/GoLang.Go.installer.yaml) | 200, 200, 200 |
| Java 21 JDK | `EclipseAdoptium.Temurin.21.JDK` | [21.0.12.101](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/e/EclipseAdoptium/Temurin/21/JDK/21.0.12.101/EclipseAdoptium.Temurin.21.JDK.installer.yaml) | 200 |
| Visual Studio Code | `Microsoft.VisualStudioCode` | [1.140.0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/m/Microsoft/VisualStudioCode/1.140.0/Microsoft.VisualStudioCode.installer.yaml) | 200, 200, 200, 200 |
| Arduino IDE | `ArduinoSA.IDE.stable` | [2.3.10](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/a/ArduinoSA/IDE/stable/2.3.10/ArduinoSA.IDE.stable.installer.yaml) | 200, 200, 200 |
| RStudio | `Posit.RStudio` | [2026.09.0+174](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/p/Posit/RStudio/2026.09.0+174/Posit.RStudio.installer.yaml) | 200 |
| Docker | `Docker.DockerDesktop` | [4.93.0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/d/Docker/DockerDesktop/4.93.0/Docker.DockerDesktop.installer.yaml) | 200, 200 |
| Kubernetes CLI (kubectl) | `Kubernetes.kubectl` | [1.37.1](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/k/Kubernetes/kubectl/1.37.1/Kubernetes.kubectl.installer.yaml) | 200, 200, 200 |
| Minikube | `Kubernetes.minikube` | [1.39.0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/k/Kubernetes/minikube/1.39.0/Kubernetes.minikube.installer.yaml) | 200 |
| Helm | `Helm.Helm` | [4.3.0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/h/Helm/Helm/4.3.0/Helm.Helm.installer.yaml) | 200, 200 |
| Terraform | `Hashicorp.Terraform` | [1.16.4](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/h/Hashicorp/Terraform/1.16.4/Hashicorp.Terraform.installer.yaml) | 200, 200 |
| VirtualBox | `Oracle.VirtualBox` | [7.2.20](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/o/Oracle/VirtualBox/7.2.20/Oracle.VirtualBox.installer.yaml) | 200 |
| AWS CLI v2 | `Amazon.AWSCLI` | [2.37.7](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/a/Amazon/AWSCLI/2.37.7/Amazon.AWSCLI.installer.yaml) | 200 |
| Google Cloud CLI | `Google.CloudSDK` | [587.0.0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/g/Google/CloudSDK/587.0.0/Google.CloudSDK.installer.yaml) | 200 |
| Azure CLI | `Microsoft.AzureCLI` | [2.90.0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/m/Microsoft/AzureCLI/2.90.0/Microsoft.AzureCLI.installer.yaml) | 200, 200 |
| Postman | `Postman.Postman` | [12.30.5](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/p/Postman/Postman/12.30.5/Postman.Postman.installer.yaml) | 200 |
| XAMPP | `ApacheFriends.Xampp.8.2` | [8.2.12-0](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/a/ApacheFriends/Xampp/8/2/8.2.12-0/ApacheFriends.Xampp.8.2.installer.yaml) | 200 |
| PostgreSQL | `PostgreSQL.PostgreSQL.17` | [17.11-4](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/p/PostgreSQL/PostgreSQL/17/17.11-4/PostgreSQL.PostgreSQL.17.installer.yaml) | 200 |
| SQLite | `SQLite.SQLite` | [3.53.4](https://raw.githubusercontent.com/microsoft/winget-pkgs/master/manifests/s/SQLite/SQLite/3.53.4/SQLite.SQLite.installer.yaml) | 200, 200 |

## Verificações locais

- Testes de geração, dependências, instruções complementares e atualização.
- Abertura da interface, seletor de plataforma e janela de etapas complementares.
- Análise de sintaxe PowerShell dos scripts gerados para todos os itens.
- Empacotamento da distribuição sem registros ou configurações pessoais.

## Limites da validação

O WinGet não estava disponível no ambiente de execução usado para esta revisão. Nenhum dos 23 instaladores foi executado por esta auditoria. WSL, Angular CLI e receitas React não fazem parte dos 23 IDs verificados. Não foi feito teste de instalação apt em uma máquina Ubuntu/Debian, nem foi validada a instalação manual das ferramentas nessa plataforma.

A aprovação de uma release para distribuição ampla deve incluir instalação em Windows e Linux de teste, verificação de versões, abertura dos aplicativos gráficos e execução das etapas complementares. Esta entrega não deve ser descrita como instalação integral testada em ambos os sistemas.
