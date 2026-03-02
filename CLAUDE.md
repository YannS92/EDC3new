# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a test automation framework for the DigitalBank mobile banking application. The project uses Python with pytest, Selenium/Appium, and follows the Page Object Model pattern.

## Project Structure

```
EDC3/
├── digitalbank/              # Application web sous test (HTML)
├── digitalbank-automation/   # Framework de tests automatisés
│   ├── tests/
│   │   ├── functional/       # Tests fonctionnels traditionnels
│   │   ├── bdd/              # Tests BDD (Gherkin)
│   │   ├── data/             # Données de test + factories + SQLite
│   │   └── utils/            # Page Objects et utilitaires
│   ├── config/               # Configuration des environnements
│   └── reports/              # Rapports Allure
└── docker-compose.yml        # Orchestration Docker
```

## Commands

### Install dependencies
```bash
pip install -r digitalbank-automation/requirements.txt
```

### Run tests (local)
```bash
cd digitalbank-automation

# Smoke tests
pytest tests/ -m smoke --headless -v

# All tests
pytest tests/ --headless -v

# BDD tests only
pytest tests/bdd/ --headless -v

# Specific environment
pytest tests/ --env=dev --headless -v
```

### Run tests (Docker) - RECOMMENDED
```bash
# From project root (EDC3/)

# Build and run all tests (rapport HTML + Allure)
docker-compose up --build

# Run in background
docker-compose up --build -d
docker-compose logs -f tests

# Run specific suites
docker-compose run --rm tests tests/ -v --env=docker -m smoke
docker-compose run --rm tests tests/ -v --env=docker -m regression
docker-compose run --rm tests tests/bdd/ -v --env=docker

# Stop services
docker-compose down
```

### View reports
```bash
# Rapport HTML (autonome, pas besoin d'outil)
# Ouvrir digitalbank-automation/reports/report.html dans le navigateur
```

## Architecture

### Page Object Model
All tests use the POM pattern. Pages inherit from `BasePage` (tests/utils/base_page.py) which provides:
- Element finding with explicit waits (`find_element`, `find_elements`)
- Common actions (`click`, `enter_text`, `get_text`)
- Visibility checks (`is_element_visible`, `is_element_present`)
- Accessibility checking via axe-core (`check_accessibility`)
- Screenshot capture for Allure reports

Page objects are in `tests/utils/pages/` and use CSS selectors with `data-testid` attributes.

### Test Data Management
- **Static data**: `tests/data/test_users.json`
- **Factories**: `tests/data/factories.py` (Faker-based generation)
- **Database**: SQLite per environment (`tests/data/db/`)
- **Centralized access**: `from tests.data import load_test_data, UserFactory`

### Fixtures (conftest.py)
- `web_driver` - Selenium Chrome driver (local or remote via Selenium Grid)
- `mobile_driver` - Appium driver for Android/iOS
- `test_data` - Static test data from JSON
- `data_factory` - Dynamic data generation factories
- `standard_user`, `user_with_2fa` - Pre-configured test users

### pytest Markers
- `@pytest.mark.smoke` - Quick critical tests
- `@pytest.mark.regression` - Full test suite
- `@pytest.mark.critical` - Blocking tests
- `@pytest.mark.accessibility` / `@pytest.mark.wcag` - WCAG 2.1 compliance tests

### BDD Structure (tests/bdd/)
- **features/**: Gherkin feature files with French descriptions
- **step_definitions/**: Python step implementations
- Scenarios run alongside traditional tests

## Test Credentials

| Account Type | Email | Password | 2FA Code |
|--------------|-------|----------|----------|
| Standard | test@digitalbank.fr | Test1234! | - |
| With 2FA | marie.martin@email.com | SecurePass456! | 123456 |
| Secondary | jean.dupont@email.com | Password123! | - |

## Docker Services

| Service | URL | Description |
|---------|-----|-------------|
| webapp | http://localhost:8080 | Application DigitalBank |

## CI/CD

GitHub Actions pipeline (4 jobs) :
1. **Smoke tests** (bloquants)
2. **Regression tests** (parallelisés avec `-n auto`)
3. **Accessibility tests** (en parallèle de regression)
4. **Publish results** (commentaire automatique sur les PR)

Triggers: push to main/develop, PRs to main, cron quotidien 8h00 Paris (lun-ven), manual.
