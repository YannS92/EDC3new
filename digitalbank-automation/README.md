# DigitalBank - Automatisation des Tests

Framework d'automatisation des tests pour l'application bancaire mobile DigitalBank.

## Structure du Projet

```
digitalbank-automation/
├── .github/
│   └── workflows/
│       └── test-automation.yml    # Pipeline CI/CD GitHub Actions
├── config/
│   ├── environments.yaml          # Configuration des environnements
│   └── test_config.yaml           # Configuration des tests
├── docs/
│   └── STRATEGIE_AUTOMATISATION.md
├── tests/
│   ├── functional/                # Tests fonctionnels
│   │   ├── test_authentication.py
│   │   ├── test_account.py
│   │   ├── test_transfers.py
│   │   ├── test_payments.py
│   │   └── test_security_settings.py
│   ├── data/
│   │   └── test_users.json        # Données de test
│   └── utils/
│       ├── base_page.py           # Classe de base Page Object
│       └── pages/                 # Page Objects
│           ├── login_page.py
│           ├── dashboard_page.py
│           ├── transfer_page.py
│           ├── bills_page.py
│           └── security_page.py
├── reports/                       # Rapports générés
├── conftest.py                    # Configuration pytest
├── requirements.txt               # Dépendances Python
└── README.md
```

## Installation

### Prérequis

- Python 3.11+
- Chrome/Chromium
- ChromeDriver (installé automatiquement avec selenium-manager)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Exécution des Tests

### Tests Smoke (vérification rapide)

```bash
pytest tests/ -m smoke --headless -v
```

### Tests de Régression (suite complète)

```bash
pytest tests/ -m regression --headless -v
```

### Tests par module

```bash
# Authentification
pytest tests/functional/test_authentication.py -v

# Comptes
pytest tests/functional/test_account.py -v

# Virements
pytest tests/functional/test_transfers.py -v

# Factures
pytest tests/functional/test_payments.py -v

# Sécurité
pytest tests/functional/test_security_settings.py -v
```

### Tests d'accessibilité (WCAG 2.1)

```bash
pytest tests/ -m accessibility --headless -v
```

### Exécution sur différents environnements

```bash
pytest tests/ --env=dev -v      # Développement
pytest tests/ --env=int -v      # Intégration
pytest tests/ --env=uat -v      # Recette
pytest tests/ --env=preprod -v  # Pré-production
```

### Génération des rapports Allure

```bash
# Exécution avec génération des résultats
pytest tests/ --alluredir=reports/allure-results -v

# Génération du rapport HTML
allure generate reports/allure-results -o reports/allure-report --clean

# Ouverture du rapport
allure open reports/allure-report
```

## Identifiants de Test

### Compte Standard (sans 2FA)
- **Email:** test@digitalbank.fr
- **Mot de passe:** Test1234!

### Compte avec 2FA
- **Email:** marie.martin@email.com
- **Mot de passe:** SecurePass456!
- **Code 2FA:** 123456

### Compte Supplémentaire
- **Email:** jean.dupont@email.com
- **Mot de passe:** Password123!

## Pipeline CI/CD

Le pipeline GitHub Actions s'exécute automatiquement:
- À chaque push sur `main` ou `develop`
- À chaque Pull Request vers `main`
- Quotidiennement à 8h00 (Paris)
- Manuellement via `workflow_dispatch`

### Jobs du Pipeline

1. **smoke-tests**: Tests de vérification rapide (bloquants)
2. **regression-tests**: Tests complets parallélisés par module
3. **accessibility-tests**: Tests WCAG 2.1
4. **generate-report**: Génération du rapport Allure consolidé
5. **notify**: Notification des résultats

## Conventions de Code

### Marqueurs pytest

- `@pytest.mark.smoke` - Tests critiques, exécution rapide
- `@pytest.mark.regression` - Tests de régression complets
- `@pytest.mark.critical` - Tests bloquants
- `@pytest.mark.accessibility` - Tests WCAG
- `@pytest.mark.wcag` - Conformité accessibilité

### Page Object Model

Tous les tests utilisent le pattern Page Object Model:

```python
from tests.utils.pages import LoginPage, DashboardPage

def test_example(web_driver):
    login_page = LoginPage(web_driver)
    login_page.login("test@digitalbank.fr", "Test1234!")

    dashboard = DashboardPage(web_driver)
    assert dashboard.is_dashboard_displayed()
```

## Conformité

- **RGPD**: Données de test synthétiques, pas de données personnelles réelles
- **WCAG 2.1**: Tests automatisés avec axe-core
- **Éco-conception**: Scripts optimisés, nettoyage après exécution

## Auteur

Projet réalisé dans le cadre de l'Étude de Cas 3 - Automatisation des Tests.
