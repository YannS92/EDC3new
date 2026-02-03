# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a test automation framework for the DigitalBank mobile banking application. The project uses Python with pytest, Selenium/Appium, and follows the Page Object Model pattern.

## Commands

### Install dependencies
```bash
pip install -r digitalbank-automation/requirements.txt
```

### Run tests
```bash
# All tests must be run from the digitalbank-automation directory
cd digitalbank-automation

# All tests (traditional + BDD)
pytest tests/ --headless -v

# Smoke tests (quick verification)
pytest tests/ -m smoke --headless -v

# Regression tests (full suite)
pytest tests/ -m regression --headless -v

# Traditional tests only
pytest tests/functional/ --headless -v

# BDD tests only
pytest tests/bdd/ --headless -v

# Single test file
pytest tests/functional/test_authentication.py -v

# Single test method
pytest tests/functional/test_authentication.py::TestAuthentication::test_login_success -v

# Accessibility tests (WCAG 2.1)
pytest tests/ -m accessibility --headless -v

# Run on specific environment
pytest tests/ --env=dev -v   # dev, int, uat, preprod
```

### Generate Allure reports
```bash
pytest tests/ --alluredir=reports/allure-results -v
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## Architecture

### Directory Structure
- `digitalbank-automation/` - Main test automation framework
- `Projet_Etude_de_Cas_3/digitalbank/` - The target application under test (HTML-based banking app)

### Page Object Model
All tests use the POM pattern. Pages inherit from `BasePage` (tests/utils/base_page.py) which provides:
- Element finding with explicit waits (`find_element`, `find_elements`)
- Common actions (`click`, `enter_text`, `get_text`)
- Visibility checks (`is_element_visible`, `is_element_present`)
- Accessibility checking via axe-core (`check_accessibility`)
- Screenshot capture for Allure reports

Page objects are in `tests/utils/pages/` and use CSS selectors with `data-testid` attributes.

### Fixtures (conftest.py)
- `web_driver` - Selenium Chrome driver (use `--headless` flag)
- `mobile_driver` - Appium driver for Android/iOS
- `api_client` - requests Session for API testing
- `environment` - Configuration based on `--env` flag
- `test_data_generator` - Faker instance for generating French test data

### pytest Markers
- `@pytest.mark.smoke` - Quick critical tests
- `@pytest.mark.regression` - Full test suite
- `@pytest.mark.critical` - Blocking tests
- `@pytest.mark.accessibility` / `@pytest.mark.wcag` - WCAG 2.1 compliance tests
- `@pytest.mark.authentification` - Authentication tests
- `@pytest.mark.securite` - Security tests
- `@pytest.mark.2fa` - Two-factor authentication tests

### BDD Structure (tests/bdd/)
The project includes a BDD layer using pytest-bdd for business-readable scenarios:
- **features/**: Gherkin feature files (.feature) with scenarios in French descriptions
- **step_definitions/**: Python step implementations
- Feature files use English keywords (Given/When/Then) with French step text
- Scenarios are automatically collected and run alongside traditional tests

## Test Credentials

| Account Type | Email | Password | 2FA Code |
|--------------|-------|----------|----------|
| Standard | test@digitalbank.fr | Test1234! | - |
| With 2FA | marie.martin@email.com | SecurePass456! | 123456 |
| Secondary | jean.dupont@email.com | Password123! | - |

## CI/CD

GitHub Actions workflow (`.github/workflows/test-automation.yml`) runs:
1. Smoke tests (blocking)
2. Regression tests (parallelized by module)
3. Accessibility tests
4. Allure report generation

Triggers: push to main/develop, PRs to main, daily at 8h00 Paris time, manual dispatch.
