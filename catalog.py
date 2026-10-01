"""Curated package IDs. Update IDs here as upstream repositories change."""
TOOLS = [
    # key, name, group, winget ID, Debian/Ubuntu package, official page
    ('git', 'Git', 'Essenciais', 'Git.Git', 'git', 'https://git-scm.com'),
    ('node', 'Node.js LTS + npm', 'Linguagens', 'OpenJS.NodeJS.LTS', 'nodejs npm', 'https://nodejs.org'),
    ('python', 'Python 3', 'Linguagens', 'Python.Python.3.13', 'python3 python3-pip python3-venv', 'https://www.python.org'),
    ('ruby', 'Ruby', 'Linguagens', 'RubyInstallerTeam.RubyWithDevKit.3.4', 'ruby-full', 'https://www.ruby-lang.org'),
    ('r', 'R', 'Linguagens', 'RProject.R', 'r-base', 'https://www.r-project.org'),
    ('go', 'Go', 'Linguagens', 'GoLang.Go', 'golang', 'https://go.dev'),
    ('java', 'Java 21 JDK', 'Linguagens', 'EclipseAdoptium.Temurin.21.JDK', 'openjdk-21-jdk', 'https://adoptium.net'),
    ('vscode', 'Visual Studio Code', 'IDEs', 'Microsoft.VisualStudioCode', None, 'https://code.visualstudio.com/docs/setup/linux'),
    ('arduino', 'Arduino IDE', 'IDEs', 'ArduinoSA.IDE.stable', None, 'https://www.arduino.cc/en/software'),
    ('rstudio', 'RStudio', 'IDEs', 'Posit.RStudio', None, 'https://posit.co/download/rstudio-desktop'),
    ('docker', 'Docker', 'Infraestrutura', 'Docker.DockerDesktop', 'docker.io', 'https://docs.docker.com/engine/install'),
    ('kubectl', 'Kubernetes CLI (kubectl)', 'Infraestrutura', 'Kubernetes.kubectl', None, 'https://kubernetes.io/docs/tasks/tools'),
    ('minikube', 'Minikube', 'Infraestrutura', 'Kubernetes.minikube', None, 'https://minikube.sigs.k8s.io/docs/start'),
    ('helm', 'Helm', 'Infraestrutura', 'Helm.Helm', None, 'https://helm.sh/docs/intro/install'),
    ('terraform', 'Terraform', 'Infraestrutura', 'Hashicorp.Terraform', None, 'https://developer.hashicorp.com/terraform/install'),
    ('virtualbox', 'VirtualBox', 'Infraestrutura', 'Oracle.VirtualBox', None, 'https://www.virtualbox.org/wiki/Downloads'),
    ('wsl', 'WSL + Ubuntu', 'Infraestrutura', None, None, 'https://learn.microsoft.com/windows/wsl/install'),
    ('aws', 'AWS CLI v2', 'Nuvem', 'Amazon.AWSCLI', None, 'https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html'),
    ('gcloud', 'Google Cloud CLI', 'Nuvem', 'Google.CloudSDK', None, 'https://cloud.google.com/sdk/docs/install'),
    ('azure', 'Azure CLI', 'Nuvem', 'Microsoft.AzureCLI', None, 'https://learn.microsoft.com/cli/azure/install-azure-cli'),
    ('postman', 'Postman', 'Backend', 'Postman.Postman', None, 'https://www.postman.com/downloads'),
    ('xampp', 'XAMPP', 'Backend', 'ApacheFriends.Xampp.8.2', None, 'https://www.apachefriends.org/download.html'),
    ('postgres', 'PostgreSQL', 'Backend', 'PostgreSQL.PostgreSQL.17', 'postgresql', 'https://www.postgresql.org/download'),
    ('sqlite', 'SQLite', 'Backend', 'SQLite.SQLite', 'sqlite3', 'https://www.sqlite.org/download.html'),
    ('angular', 'Angular CLI', 'Frontend', None, None, 'https://angular.dev/tools/cli/setup-local'),
    ('react', 'React / Vite (Node + receita)', 'Frontend', None, None, 'https://react.dev/learn/build-a-react-app-from-scratch'),
    ('angularjs', 'AngularJS (legado, fim do suporte)', 'Frontend', None, None, 'https://docs.angularjs.org'),
]
CATALOG = {t[0]: dict(zip(('key', 'name', 'group', 'winget', 'apt', 'url'), t)) for t in TOOLS}
PROFILES = {
    'Frontend': ['git', 'node', 'vscode', 'angular', 'react'],
    'Backend': ['git', 'python', 'node', 'postgres', 'postman', 'vscode'],
    'DevOps': ['git', 'docker', 'kubectl', 'minikube', 'helm', 'terraform', 'aws', 'gcloud'],
    'Dados': ['python', 'r', 'rstudio', 'postgres', 'vscode'],
}
