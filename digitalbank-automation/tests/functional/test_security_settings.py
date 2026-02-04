"""
Tests fonctionnels pour les paramètres de sécurité DigitalBank
"""

import json
import pytest
import allure
from tests.utils.pages.login_page import LoginPage
from tests.utils.pages.dashboard_page import DashboardPage
from tests.utils.pages.security_page import SecurityPage


@allure.epic("DigitalBank")
@allure.feature("Sécurité")
class TestSecuritySettings:
    """Suite de tests pour les paramètres de sécurité"""

    @pytest.fixture(autouse=True)
    def setup(self, web_driver, test_data):
        """Configuration avant chaque test"""
        self.driver = web_driver
        self.login_page = LoginPage(web_driver)
        self.dashboard = DashboardPage(web_driver)
        self.security_page = SecurityPage(web_driver)
        self.test_data = test_data

        # Connexion préalable
        self._login_and_navigate_to_security()

    def _login_and_navigate_to_security(self):
        """Helper: connexion et navigation vers sécurité"""
        user = self.test_data['users']['standard']
        self.login_page.login(user['email'], user['password'])
        self.dashboard.navigate_to_tab('security')

    # ═══════════════════════════════════════════════════════════════
    # TESTS CHANGEMENT MOT DE PASSE
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Changement mot de passe")
    @allure.title("Ouverture modal changement mot de passe")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_open_change_password_modal(self):
        """
        TC-SEC-001: Ouverture de la modal de changement de mot de passe
        """
        self.security_page.open_change_password_modal()

        assert self.security_page.is_modal_displayed(), \
            "La modal devrait être affichée"

    @allure.story("Changement mot de passe")
    @allure.title("Changement mot de passe réussi")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_change_password_success(self):
        """
        TC-SEC-002: Changement de mot de passe avec succès

        Préconditions:
        - Utilisateur connecté

        Étapes:
        1. Ouvrir la modal
        2. Saisir le mot de passe actuel
        3. Saisir un nouveau mot de passe valide
        4. Confirmer le nouveau mot de passe
        5. Enregistrer

        Résultat attendu:
        - Message de succès affiché
        """
        user = self.test_data['users']['standard']
        new_password = self.test_data['password_requirements']['valid_new_password']

        self.security_page.change_password(user['password'], new_password)

        success = self.security_page.get_success_message()
        assert success is not None, "Un message de succès devrait être affiché"
        assert "modifié" in success.lower() or "succès" in success.lower()

    @allure.story("Changement mot de passe")
    @allure.title("Échec - mot de passe actuel incorrect")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_change_password_wrong_current(self):
        """
        TC-SEC-003: Erreur si mot de passe actuel incorrect
        """
        wrong_current = "WrongCurrent123!"
        new_password = self.test_data['password_requirements']['valid_new_password']

        self.security_page.change_password(wrong_current, new_password)

        error = self.security_page.get_password_error()
        assert error is not None, "Un message d'erreur devrait être affiché"
        assert "incorrect" in error.lower()

    @allure.story("Changement mot de passe")
    @allure.title("Validation des critères de mot de passe")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_password_requirements_validation(self):
        """
        TC-SEC-004: Vérification des critères de mot de passe

        Critères:
        - 8 caractères minimum
        - 1 majuscule
        - 1 minuscule
        - 1 chiffre
        - 1 caractère spécial
        """
        user = self.test_data['users']['standard']

        self.security_page.open_change_password_modal()
        self.security_page.enter_current_password(user['password'])

        # Test mot de passe trop court
        self.security_page.enter_new_password("Abc1!")

        requirements = self.security_page.get_password_requirements_status()

        assert requirements.get('length') == False, \
            "Le critère de longueur devrait échouer"

    @allure.story("Changement mot de passe")
    @allure.title("Annulation du changement")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_cancel_password_change(self):
        """
        TC-SEC-005: Annulation du changement de mot de passe
        """
        self.security_page.open_change_password_modal()
        assert self.security_page.is_modal_displayed()

        self.security_page.cancel_password_change()

        assert not self.security_page.is_modal_displayed(), \
            "La modal devrait être fermée"

    # ═══════════════════════════════════════════════════════════════
    # TESTS DOUBLE AUTHENTIFICATION (2FA)
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Double Authentification")
    @allure.title("Activation de la 2FA")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_enable_2fa(self):
        """
        TC-SEC-006: Activation de la double authentification
        """
        # S'assurer que la 2FA est désactivée
        if self.security_page.is_2fa_enabled():
            self.security_page.disable_2fa()

        self.security_page.enable_2fa()

        success = self.security_page.get_success_message()
        assert success is not None, "Un message de succès devrait être affiché"
        assert "activée" in success.lower()
        assert self.security_page.is_2fa_enabled()

    @allure.story("Double Authentification")
    @allure.title("Désactivation de la 2FA")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_disable_2fa(self):
        """
        TC-SEC-007: Désactivation de la double authentification
        """
        # S'assurer que la 2FA est activée
        if not self.security_page.is_2fa_enabled():
            self.security_page.enable_2fa()

        self.security_page.disable_2fa()

        success = self.security_page.get_success_message()
        assert success is not None, "Un message de succès devrait être affiché"
        assert "désactivée" in success.lower()
        assert not self.security_page.is_2fa_enabled()

    # ═══════════════════════════════════════════════════════════════
    # TESTS NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Notifications")
    @allure.title("Toggle notifications email")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_toggle_email_notifications(self):
        """
        TC-SEC-008: Activation/désactivation notifications email
        """
        initial_state = self.security_page.is_email_notifications_enabled()
        self.security_page.toggle_email_notifications()
        new_state = self.security_page.is_email_notifications_enabled()

        assert new_state != initial_state, \
            "L'état des notifications devrait avoir changé"

    @allure.story("Notifications")
    @allure.title("Toggle notifications SMS")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_toggle_sms_notifications(self):
        """
        TC-SEC-009: Activation/désactivation notifications SMS
        """
        initial_state = self.security_page.is_sms_notifications_enabled()
        self.security_page.toggle_sms_notifications()
        new_state = self.security_page.is_sms_notifications_enabled()

        assert new_state != initial_state, \
            "L'état des notifications devrait avoir changé"

    # ═══════════════════════════════════════════════════════════════
    # TESTS INFORMATIONS UTILISATEUR
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Informations utilisateur")
    @allure.title("Affichage des informations")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_display_user_info(self):
        """
        TC-SEC-010: Vérification de l'affichage des informations
        """
        user = self.test_data['users']['standard']
        info = self.security_page.get_user_info()

        assert info['email'] == user['email'], \
            "L'email affiché devrait correspondre"
        assert user['name'] in info['name'], \
            "Le nom affiché devrait correspondre"

    # ═══════════════════════════════════════════════════════════════
    # TESTS ACCESSIBILITÉ
    # ═══════════════════════════════════════════════════════════════

    @allure.story("Accessibilité")
    @allure.title("Conformité WCAG page sécurité")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.accessibility
    @pytest.mark.wcag
    def test_security_page_accessibility(self):
        """
        TC-A11Y-SEC: Vérification accessibilité page sécurité
        """
        violations = self.security_page.check_accessibility()
        critical_violations = [v for v in violations if v.get('impact') == 'critical']

        if violations:
            allure.attach(
                json.dumps(violations, indent=2),
                name="Violations accessibilité",
                attachment_type=allure.attachment_type.JSON
            )

        assert len(critical_violations) == 0, \
            f"Violations critiques détectées: {critical_violations}"
