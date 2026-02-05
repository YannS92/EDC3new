#!/bin/bash
# Script pour exécuter les tests Docker
# Usage: ./scripts/docker-run.sh [command] [options]
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
#   vnc         - Ouvrir le viewer VNC
#   allure      - Démarrer le serveur Allure

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info() { echo -e "${CYAN}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
error() { echo -e "${RED}[ERREUR]${NC} $1"; exit 1; }

# Vérifier Docker
check_docker() {
    command -v docker >/dev/null 2>&1 || error "Docker n'est pas installé"
    command -v docker-compose >/dev/null 2>&1 || error "docker-compose n'est pas installé"
}

# Build
do_build() {
    info "Construction des images Docker..."
    docker-compose build
    success "Images construites"
}

# Up
do_up() {
    info "Démarrage des services..."
    docker-compose up -d webapp selenium-hub chrome
    info "Attente du démarrage de Selenium Grid..."
    sleep 10
    success "Services démarrés"
    info "Application web: http://localhost:8080"
    info "Selenium Grid: http://localhost:4444"
    info "VNC Viewer: http://localhost:7900"
}

# Test
do_test() {
    local marker="${1:-smoke}"
    do_up
    info "Exécution des tests ($marker)..."
    docker-compose run --rm tests tests/ -v --env=docker -m "$marker" --alluredir=reports/allure-results
    success "Tests terminés"
}

# Test all
do_test_all() {
    do_up
    info "Exécution de tous les tests..."
    docker-compose run --rm tests tests/ -v --env=docker --alluredir=reports/allure-results
    success "Tests terminés"
}

# Test BDD
do_test_bdd() {
    do_up
    info "Exécution des tests BDD..."
    docker-compose run --rm tests tests/bdd/ -v --env=docker --alluredir=reports/allure-results
    success "Tests BDD terminés"
}

# Stop
do_stop() {
    info "Arrêt des services..."
    docker-compose down
    success "Services arrêtés"
}

# Clean
do_clean() {
    info "Nettoyage..."
    docker-compose down -v --rmi local
    success "Nettoyage terminé"
}

# Logs
do_logs() {
    docker-compose logs -f
}

# VNC
do_vnc() {
    info "Ouverture du viewer VNC..."
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:7900"
    elif command -v open &> /dev/null; then
        open "http://localhost:7900"
    else
        info "Ouvrez http://localhost:7900 dans votre navigateur"
    fi
}

# Allure
do_allure() {
    info "Démarrage du serveur Allure..."
    docker-compose --profile reporting up -d allure
    sleep 5
    success "Allure disponible sur http://localhost:5050"
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:5050"
    elif command -v open &> /dev/null; then
        open "http://localhost:5050"
    fi
}

# Help
show_help() {
    cat << EOF
Usage: ./scripts/docker-run.sh [command] [options]

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
  ./scripts/docker-run.sh build
  ./scripts/docker-run.sh test
  ./scripts/docker-run.sh test regression
  ./scripts/docker-run.sh test-all
  ./scripts/docker-run.sh vnc
  ./scripts/docker-run.sh stop
EOF
}

# Main
check_docker

case "${1:-help}" in
    build)    do_build ;;
    up)       do_up ;;
    test)     do_test "$2" ;;
    test-all) do_test_all ;;
    test-bdd) do_test_bdd ;;
    stop)     do_stop ;;
    clean)    do_clean ;;
    logs)     do_logs ;;
    vnc)      do_vnc ;;
    allure)   do_allure ;;
    help|*)   show_help ;;
esac
