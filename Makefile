# Makefile - DigitalBank
# 2 conteneurs : webapp (nginx) + tests (python/chrome)

.PHONY: help build test test-all test-bdd up down logs clean

help:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║            DigitalBank - Docker Commands                   ║"
	@echo "╠════════════════════════════════════════════════════════════╣"
	@echo "║                                                            ║"
	@echo "║  make build      Construire l'image des tests              ║"
	@echo "║  make test       Lancer les tests smoke                    ║"
	@echo "║  make test-all   Lancer tous les tests                     ║"
	@echo "║  make test-bdd   Lancer les tests BDD                      ║"
	@echo "║                                                            ║"
	@echo "║  make up         Démarrer l'application (sans tests)       ║"
	@echo "║  make down       Arrêter les conteneurs                    ║"
	@echo "║  make logs       Voir les logs                             ║"
	@echo "║  make clean      Nettoyer images et conteneurs             ║"
	@echo "║                                                            ║"
	@echo "║  Application: http://localhost:8080                        ║"
	@echo "║                                                            ║"
	@echo "╚════════════════════════════════════════════════════════════╝"

build:
	@echo "🔨 Construction de l'image..."
	docker-compose build
	@echo "✅ Image construite"

test: build
	@echo "🧪 Lancement des tests smoke..."
	docker-compose up --abort-on-container-exit --exit-code-from tests
	@echo "✅ Tests terminés"

test-all: build
	@echo "🧪 Lancement de tous les tests..."
	docker-compose run --rm tests tests/ -v --headless --alluredir=reports/allure-results
	@echo "✅ Tests terminés"

test-bdd: build
	@echo "🧪 Lancement des tests BDD..."
	docker-compose run --rm tests tests/bdd/ -v --headless --alluredir=reports/allure-results
	@echo "✅ Tests BDD terminés"

test-regression: build
	@echo "🧪 Lancement des tests de régression..."
	docker-compose run --rm tests tests/ -v --headless -m regression --alluredir=reports/allure-results
	@echo "✅ Tests terminés"

up:
	@echo "🚀 Démarrage de l'application..."
	docker-compose up -d webapp
	@echo "✅ Application disponible sur http://localhost:8080"

down:
	@echo "🛑 Arrêt des conteneurs..."
	docker-compose down
	@echo "✅ Conteneurs arrêtés"

logs:
	docker-compose logs -f

clean:
	@echo "🧹 Nettoyage..."
	docker-compose down -v --rmi local --remove-orphans
	@echo "✅ Nettoyage terminé"
