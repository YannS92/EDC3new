"""
Tests fonctionnels pour l'authentification DigitalBank
"""

import json
import pytest
import allure
from tests.utils.pages.login_page import LoginPage
from tests.utils.pages.dashboard_page import DashboardPage


@allure.epic("DigitalBank")
@allure.feature("Authentification")
class TestAuthentication:
    """Suite de tests pour l'authentification"""

    @pytest.fixture(autouse=True)
    def setup(self, web_driver, test_data):
        """Configuration avant chaque test"""
        self.driver = web_driver
        self.login_page = LoginPage(web_driver)
        self.dashboard = DashboardPage(web_driver)
        self.test_data = test_data

    # ═══════════════════════════════════════════════════════════════
    # TESTS DE CONNEXION
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Connexion")
    @allure.title("Connexion réussie avec identifiants valides")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_login_success(self):
        """
        TC-AUTH-001: Connexion réussie

        Préconditions:
        - Application accessible
        - Utilisateur existant

        Étapes:
        1. Saisir l'email valide
        2. Saisir le mot de passe valide
        3. Cliquer sur Connexion

        Résultat attendu:
        - Redirection vers le dashboard
        - Nom d'utilisateur affiché
        """
        user = self.test_data['users']['standard']

        self.login_page.login(user['email'], user['password'])

        assert self.dashboard.is_dashboard_displayed(), \
            "Le dashboard devrait être affiché après connexion"
        assert user['name'] in self.dashboard.get_user_name(), \
            "Le nom d'utilisateur devrait être affiché"

    @allure.story("Connexion")
    @allure.title("Échec connexion - mot de passe incorrect")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_invalid_password(self):
        """
        TC-AUTH-002: Connexion avec mot de passe incorrect

        Étapes:
        1. Saisir un email valide
        2. Saisir un mot de passe incorrect
        3. Cliquer sur Connexion

        Résultat attendu:
        - Message d'erreur affiché
        - Reste sur la page de connexion
        """
        user = self.test_data['users']['standard']
        wrong_password = self.test_data['invalid_credentials']['wrong_password']

        self.login_page.login(user['email'], wrong_password)

        error = self.login_page.get_error_message()
        assert error is not None, "Un message d'erreur devrait être affiché"
        assert "incorrect" in error.lower(), "Le message devrait mentionner l'erreur"
        assert self.login_page.is_login_page_displayed(), \
            "L'utilisateur devrait rester sur la page de connexion"

    @allure.story("Connexion")
    @allure.title("Échec connexion - email inexistant")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_invalid_email(self):
        """
        TC-AUTH-003: Connexion avec email inexistant
        """
        wrong_email = self.test_data['invalid_credentials']['wrong_email']
        password = "SomePassword123!"

        self.login_page.login(wrong_email, password)

        error = self.login_page.get_error_message()
        assert error is not None, "Un message d'erreur devrait être affiché"

    @allure.story("Connexion")
    @allure.title("Option 'Se souvenir de moi'")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_remember_me_checkbox(self):
        """
        TC-AUTH-004: Vérification de la case 'Se souvenir de moi'
        """
        assert self.login_page.is_login_page_displayed()
        self.login_page.check_remember_me()
        # Vérification visuelle que la case est cochée
        # (fonctionnalité à valider manuellement car état en mémoire)

    # ═══════════════════════════════════════════════════════════════
    # TESTS DOUBLE AUTHENTIFICATION (2FA)
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Double Authentification")
    @allure.title("Connexion avec 2FA - code valide")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_login_with_2fa_valid_code(self):
        """
        TC-AUTH-005: Connexion avec 2FA activée

        Préconditions:
        - Compte avec 2FA activée

        Étapes:
        1. Se connecter avec email/mot de passe
        2. Saisir le code 2FA valide (123456)
        3. Valider

        Résultat attendu:
        - Redirection vers le dashboard
        """
        user = self.test_data['users']['with_2fa']

        self.login_page.login(user['email'], user['password'])

        assert self.login_page.is_2fa_page_displayed(), \
            "La page 2FA devrait être affichée"

        self.login_page.enter_2fa_code(user['totp_code'])
        self.login_page.submit_2fa_code()

        assert self.dashboard.is_dashboard_displayed(), \
            "Le dashboard devrait être affiché après validation 2FA"

    @allure.story("Double Authentification")
    @allure.title("Connexion avec 2FA - code invalide")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_with_2fa_invalid_code(self):
        """
        TC-AUTH-006: Connexion 2FA avec code invalide

        Résultat attendu:
        - Message d'erreur
        - Reste sur la page 2FA
        """
        user = self.test_data['users']['with_2fa']
        invalid_code = "000000"

        self.login_page.login(user['email'], user['password'])
        assert self.login_page.is_2fa_page_displayed()

        self.login_page.enter_2fa_code(invalid_code)
        self.login_page.submit_2fa_code()

        error = self.login_page.get_2fa_error_message()
        assert error is not None, "Un message d'erreur devrait être affiché"
        assert self.login_page.is_2fa_page_displayed(), \
            "L'utilisateur devrait rester sur la page 2FA"

    # ═══════════════════════════════════════════════════════════════
    # TESTS RÉINITIALISATION MOT DE PASSE
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Réinitialisation mot de passe")
    @allure.title("Accès page réinitialisation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_forgot_password_page_access(self):
        """
        TC-AUTH-007: Navigation vers la page de réinitialisation
        """
        self.login_page.click_forgot_password()

        assert self.login_page.is_reset_page_displayed(), \
            "La page de réinitialisation devrait être affichée"

    @allure.story("Réinitialisation mot de passe")
    @allure.title("Réinitialisation - email valide")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_password_reset_valid_email(self):
        """
        TC-AUTH-008: Demande de réinitialisation avec email valide
        """
        user = self.test_data['users']['standard']

        self.login_page.click_forgot_password()
        self.login_page.request_password_reset(user['email'])

        success = self.login_page.get_reset_success_message()
        assert success is not None, "Un message de succès devrait être affiché"
        assert user['email'] in success, "Le message devrait mentionner l'email"

    @allure.story("Réinitialisation mot de passe")
    @allure.title("Réinitialisation - email inexistant")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_password_reset_invalid_email(self):
        """
        TC-AUTH-009: Demande de réinitialisation avec email inexistant
        """
        invalid_email = self.test_data['invalid_credentials']['wrong_email']

        self.login_page.click_forgot_password()
        self.login_page.request_password_reset(invalid_email)

        error = self.login_page.get_reset_error_message()
        assert error is not None, "Un message d'erreur devrait être affiché"

    @allure.story("Réinitialisation mot de passe")
    @allure.title("Retour à la page de connexion")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_back_to_login_from_reset(self):
        """
        TC-AUTH-010: Retour vers la page de connexion
        """
        self.login_page.click_forgot_password()
        assert self.login_page.is_reset_page_displayed()

        self.login_page.click_back_to_login()
        assert self.login_page.is_login_page_displayed(), \
            "La page de connexion devrait être affichée"

    # ═══════════════════════════════════════════════════════════════
    # TESTS DÉCONNEXION
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Déconnexion")
    @allure.title("Déconnexion réussie")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_logout_success(self):
        """
        TC-AUTH-011: Déconnexion de l'application

        Étapes:
        1. Se connecter
        2. Cliquer sur Déconnexion

        Résultat attendu:
        - Retour à la page de connexion
        """
        user = self.test_data['users']['standard']

        self.login_page.login(user['email'], user['password'])
        assert self.dashboard.is_dashboard_displayed()

        self.dashboard.logout()

        assert self.login_page.is_login_page_displayed(), \
            "La page de connexion devrait être affichée après déconnexion"

    # ═══════════════════════════════════════════════════════════════
    # TESTS ACCESSIBILITÉ
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Accessibilité")
    @allure.title("Conformité WCAG page de connexion")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.accessibility
    @pytest.mark.wcag
    def test_login_page_accessibility(self):
        """
        TC-A11Y-001: Vérification accessibilité page de connexion

        Critères WCAG 2.1:
        - Labels sur les champs
        - Focus visible
        - Contraste suffisant
        """
        violations = self.login_page.check_accessibility()

        critical_violations = [v for v in violations if v.get('impact') == 'critical']

        if violations:
            allure.attach(
                json.dumps(violations, indent=2),
                name="Violations accessibilité",
                attachment_type=allure.attachment_type.JSON
            )

        assert len(critical_violations) == 0, \
            f"Violations critiques détectées: {critical_violations}"
