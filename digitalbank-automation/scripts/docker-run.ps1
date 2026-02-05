# Script PowerShell pour exécuter les tests Docker
# Usage: .\scripts\docker-run.ps1 [command] [options]
#
# Commandes:
#   build       - Construire les images Docker
#   up          - Démarrer tous les services
#   test        - Exécuter les tests (smoke par défaut)
#   test-all    - Exécuter tous les tests
#   test-bdd    - Exécuter les tests BDD
#   stop        - Arrêter tous les services
#   clean       - Nettoyer les conteneurs et images
#   logs        - Afficher les logs
#   vnc         - Ouvrir le viewer VNC (noVNC)
#   allure      - Démarrer le serveur Allure
#
# Options:
#   -v          - Mode verbeux

param(
    [Parameter(Position=0)]
    [string]$Command = "help",

    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args,

    [switch]$v
)

$ErrorActionPreference = "Stop"

# Couleurs pour l'affichage
function Write-Info { Write-Host "[INFO] $args" -ForegroundColor Cyan }
function Write-Success { Write-Host "[OK] $args" -ForegroundColor Green }
function Write-Error { Write-Host "[ERREUR] $args" -ForegroundColor Red }

# Vérifier que Docker est installé
function Test-Docker {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Error "Docker n'est pas installé ou n'est pas dans le PATH"
        exit 1
    }
    if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Error "docker-compose n'est pas installé"
        exit 1
    }
}

# Build des images
function Invoke-Build {
    Write-Info "Construction des images Docker..."
    docker-compose build
    Write-Success "Images construites"
}

# Démarrer les services
function Invoke-Up {
    Write-Info "Démarrage des services..."
    docker-compose up -d webapp selenium-hub chrome
    Write-Info "Attente du démarrage de Selenium Grid..."
    Start-Sleep -Seconds 10
    Write-Success "Services démarrés"
    Write-Info "Application web: http://localhost:8080"
    Write-Info "Selenium Grid: http://localhost:4444"
    Write-Info "VNC Viewer: http://localhost:7900"
}

# Exécuter les tests
function Invoke-Test {
    param([string]$Marker = "smoke")

    Invoke-Up

    Write-Info "Exécution des tests ($Marker)..."
    docker-compose run --rm tests tests/ -v --env=docker -m $Marker --alluredir=reports/allure-results

    Write-Success "Tests terminés"
}

# Exécuter tous les tests
function Invoke-TestAll {
    Invoke-Up

    Write-Info "Exécution de tous les tests..."
    docker-compose run --rm tests tests/ -v --env=docker --alluredir=reports/allure-results

    Write-Success "Tests terminés"
}

# Exécuter les tests BDD
function Invoke-TestBDD {
    Invoke-Up

    Write-Info "Exécution des tests BDD..."
    docker-compose run --rm tests tests/bdd/ -v --env=docker --alluredir=reports/allure-results

    Write-Success "Tests BDD terminés"
}

# Arrêter les services
function Invoke-Stop {
    Write-Info "Arrêt des services..."
    docker-compose down
    Write-Success "Services arrêtés"
}

# Nettoyer
function Invoke-Clean {
    Write-Info "Nettoyage..."
    docker-compose down -v --rmi local
    Write-Success "Nettoyage terminé"
}

# Afficher les logs
function Invoke-Logs {
    docker-compose logs -f
}

# Ouvrir VNC
function Invoke-VNC {
    Write-Info "Ouverture du viewer VNC..."
    Start-Process "http://localhost:7900"
}

# Démarrer Allure
function Invoke-Allure {
    Write-Info "Démarrage du serveur Allure..."
    docker-compose --profile reporting up -d allure
    Start-Sleep -Seconds 5
    Write-Success "Allure disponible sur http://localhost:5050"
    Start-Process "http://localhost:5050"
}

# Aide
function Show-Help {
    Write-Host @"
Usage: .\scripts\docker-run.ps1 [command] [options]

Commandes:
  build       Construire les images Docker
  up          Démarrer tous les services (webapp, selenium)
  test        Exécuter les tests smoke (défaut)
  test-all    Exécuter tous les tests
  test-bdd    Exécuter les tests BDD uniquement
  stop        Arrêter tous les services
  clean       Nettoyer les conteneurs et images
  logs        Afficher les logs des conteneurs
  vnc         Ouvrir le viewer VNC (noVNC) dans le navigateur
  allure      Démarrer le serveur de rapports Allure
  help        Afficher cette aide

Exemples:
  .\scripts\docker-run.ps1 build
  .\scripts\docker-run.ps1 test
  .\scripts\docker-run.ps1 test-all
  .\scripts\docker-run.ps1 vnc
  .\scripts\docker-run.ps1 stop
"@
}

# Main
Test-Docker

switch ($Command.ToLower()) {
    "build"    { Invoke-Build }
    "up"       { Invoke-Up }
    "test"     { Invoke-Test -Marker ($Args[0] ?? "smoke") }
    "test-all" { Invoke-TestAll }
    "test-bdd" { Invoke-TestBDD }
    "stop"     { Invoke-Stop }
    "clean"    { Invoke-Clean }
    "logs"     { Invoke-Logs }
    "vnc"      { Invoke-VNC }
    "allure"   { Invoke-Allure }
    "help"     { Show-Help }
    default    { Show-Help }
}
