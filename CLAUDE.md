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

# Build and run smoke tests
docker-compose up --build

# Run all tests
docker-compose run --rm tests tests/ -v --env=docker

# Run regression tests
docker-compose run --rm tests tests/ -v --env=docker -m regression

# Run BDD tests
docker-compose run --rm tests tests/bdd/ -v --env=docker

# Stop services
docker-compose down
```

### View tests in real-time (VNC)
```bash
# Start services
docker-compose up -d webapp selenium-hub chrome

# Open http://localhost:7900 in browser to watch tests
```

### Generate Allure reports
```bash
cd digitalbank-automation
pytest tests/ --alluredir=reports/allure-results -v
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
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
| selenium-hub | http://localhost:4444 | Selenium Grid Hub |
| chrome (VNC) | http://localhost:7900 | Visualiser les tests |

## CI/CD

GitHub Actions workflow runs:
1. Smoke tests (blocking)
2. Regression tests (parallelized)
3. Accessibility tests
4. Allure report generation

Triggers: push to main/develop, PRs to main, daily at 8h00 Paris time.
