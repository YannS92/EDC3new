"""
Configuration pytest-bdd pour les tests BDD DigitalBank
Fixtures spécifiques aux tests Gherkin
"""

import os
import json
import pytest
from tests.utils.pages.login_page import LoginPage
from tests.utils.pages.dashboard_page import DashboardPage
from tests.utils.pages.security_page import SecurityPage


def load_test_data():
    """Charge les données de test depuis le fichier JSON"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_users.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════
# FIXTURES DONNÉES DE TEST
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def test_data():
    """Fixture pour les données de test"""
    return load_test_data()


@pytest.fixture
def standard_user(test_data):
    """Fixture pour l'utilisateur standard"""
    return test_data['users']['standard']


@pytest.fixture
def user_with_2fa(test_data):
    """Fixture pour l'utilisateur avec 2FA"""
    return test_data['users']['with_2fa']


@pytest.fixture
def invalid_credentials(test_data):
    """Fixture pour les identifiants invalides"""
    return test_data['invalid_credentials']


@pytest.fixture
def password_requirements(test_data):
    """Fixture pour les exigences de mot de passe"""
    return test_data['password_requirements']


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
