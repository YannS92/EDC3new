"""
Configuration pytest-bdd pour les tests BDD DigitalBank
Fixtures spécifiques aux tests Gherkin

Note: Les fixtures de données (test_data, standard_user, user_with_2fa,
invalid_credentials, password_requirements) sont héritées du conftest.py racine.
"""

import pytest
from tests.utils.pages.login_page import LoginPage
from tests.utils.pages.dashboard_page import DashboardPage
from tests.utils.pages.security_page import SecurityPage


# ═══════════════════════════════════════════════════════════════
# FIXTURES PAGE OBJECTS
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def login_page(web_driver):
    """Fixture pour la page de connexion"""
    return LoginPage(web_driver)


@pytest.fixture
def dashboard_page(web_driver):
    """Fixture pour le dashboard"""
    return DashboardPage(web_driver)


@pytest.fixture
def security_page(web_driver):
    """Fixture pour la page de sécurité"""
    return SecurityPage(web_driver)


# ═══════════════════════════════════════════════════════════════
# FIXTURES CONTEXTE DE SCÉNARIO
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def context():
    """
    Fixture pour stocker le contexte partagé entre les steps d'un scénario
    Permet de passer des données entre Given/When/Then
    """
    return {}
