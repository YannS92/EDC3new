# Makefile - DigitalBank Test Automation
# Note: Docker commands should be run from the project root (parent directory)

.PHONY: help test test-all test-bdd seed report

help:
	@echo "═══════════════════════════════════════════════════════════"
	@echo "  DigitalBank Test Automation - Commandes locales"
	@echo "═══════════════════════════════════════════════════════════"
	@echo ""
	@echo "  Tests (local):"
	@echo "    make test        - Tests smoke (headless)"
	@echo "    make test-all    - Tous les tests"
	@echo "    make test-bdd    - Tests BDD uniquement"
	@echo ""
	@echo "  Données:"
	@echo "    make seed        - Initialiser la base SQLite"
	@echo "    make seed-reset  - Réinitialiser la base"
	@echo ""
	@echo "  Rapports:"
	@echo "    make report      - Générer rapport Allure"
	@echo ""
	@echo "  Pour Docker, exécuter depuis la racine du projet:"
	@echo "    cd .. && docker-compose up --build"
	@echo ""

# Tests locaux
test:
	pytest tests/ -v --headless -m smoke --alluredir=reports/allure-results

test-all:
	pytest tests/ -v --headless --alluredir=reports/allure-results

test-bdd:
	pytest tests/bdd/ -v --headless --alluredir=reports/allure-results

test-regression:
	pytest tests/ -v --headless -m regression --alluredir=reports/allure-results

# Données
seed:
	python -m tests.data.seed_data seed --env=dev -v

seed-reset:
	python -m tests.data.seed_data reset --env=dev -v

# Rapports
report:
	allure generate reports/allure-results -o reports/allure-report --clean
	allure open reports/allure-report
