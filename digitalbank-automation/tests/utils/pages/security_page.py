"""
Page Object pour la page Sécurité DigitalBank
"""

from selenium.webdriver.common.by import By
from tests.utils.base_page import BasePage
import allure


class SecurityPage(BasePage):
    """Page Sécurité de l'application DigitalBank"""

    # Messages
    SECURITY_SUCCESS = (By.CSS_SELECTOR, "[data-testid='security-success']")

    # Toggles
    TOGGLE_2FA = (By.CSS_SELECTOR, "[data-testid='toggle-2fa']")
    TOGGLE_EMAIL_NOTIF = (By.CSS_SELECTOR, "[data-testid='toggle-email-notifications']")
    TOGGLE_SMS_NOTIF = (By.CSS_SELECTOR, "[data-testid='toggle-sms-notifications']")
    TWO_FA_GROUP = (By.CSS_SELECTOR, "[data-testid='2fa-toggle-group']")

    # Bouton changement mot de passe
    BTN_CHANGE_PASSWORD = (By.CSS_SELECTOR, "[data-testid='btn-change-password']")

    # Informations utilisateur
    USER_NAME = (By.CSS_SELECTOR, "[data-testid='user-name']")
    USER_EMAIL = (By.CSS_SELECTOR, "[data-testid='user-email']")
    USER_PHONE = (By.CSS_SELECTOR, "[data-testid='user-phone']")

    # Modal changement mot de passe
    MODAL_CHANGE_PASSWORD = (By.CSS_SELECTOR, "[data-testid='modal-change-password']")
    INPUT_CURRENT_PASSWORD = (By.CSS_SELECTOR, "[data-testid='input-current-password']")
    INPUT_NEW_PASSWORD = (By.CSS_SELECTOR, "[data-testid='input-new-password']")
    INPUT_CONFIRM_PASSWORD = (By.CSS_SELECTOR, "[data-testid='input-confirm-password']")
    BTN_CANCEL_PASSWORD = (By.CSS_SELECTOR, "[data-testid='btn-cancel-password']")
    BTN_SAVE_PASSWORD = (By.CSS_SELECTOR, "[data-testid='btn-save-password']")
    PASSWORD_ERROR = (By.CSS_SELECTOR, "[data-testid='password-error']")
    PASSWORD_REQUIREMENTS = (By.CSS_SELECTOR, "[data-testid='password-requirements']")

    # Requirements individuels
    REQ_LENGTH = (By.ID, "req-length")
    REQ_UPPER = (By.ID, "req-upper")
    REQ_LOWER = (By.ID, "req-lower")
    REQ_NUMBER = (By.ID, "req-number")
    REQ_SPECIAL = (By.ID, "req-special")

    def __init__(self, driver):
        """Initialise la page Sécurité"""
        super().__init__(driver)

    def is_security_page_displayed(self):
        """Vérifie si la page de sécurité est affichée"""
        return self.is_element_visible(self.BTN_CHANGE_PASSWORD, timeout=5)

    # --- Méthodes 2FA ---

    @allure.step("Activation/Désactivation 2FA")
    def toggle_2fa(self):
        """Toggle la double authentification"""
        self.click(self.TOGGLE_2FA)

    def is_2fa_enabled(self):
        """Vérifie si la 2FA est activée"""
        toggle = self.find_element(self.TOGGLE_2FA)
        return toggle.is_selected()

    @allure.step("Activation de la 2FA")
    def enable_2fa(self):
        """Active la 2FA si elle ne l'est pas"""
        if not self.is_2fa_enabled():
            self.toggle_2fa()

    @allure.step("Désactivation de la 2FA")
    def disable_2fa(self):
        """Désactive la 2FA si elle est activée"""
        if self.is_2fa_enabled():
            self.toggle_2fa()

    # --- Méthodes Notifications ---

    @allure.step("Toggle notifications email")
    def toggle_email_notifications(self):
        """Toggle les notifications par email"""
        self.click(self.TOGGLE_EMAIL_NOTIF)

    @allure.step("Toggle notifications SMS")
    def toggle_sms_notifications(self):
        """Toggle les notifications SMS"""
        self.click(self.TOGGLE_SMS_NOTIF)

    def is_email_notifications_enabled(self):
        """Vérifie si les notifications email sont activées"""
        toggle = self.find_element(self.TOGGLE_EMAIL_NOTIF)
        return toggle.is_selected()

    def is_sms_notifications_enabled(self):
        """Vérifie si les notifications SMS sont activées"""
        toggle = self.find_element(self.TOGGLE_SMS_NOTIF)
        return toggle.is_selected()

    # --- Méthodes Changement Mot de Passe ---

    @allure.step("Ouverture modal changement mot de passe")
    def open_change_password_modal(self):
        """Ouvre la modal de changement de mot de passe"""
        self.click(self.BTN_CHANGE_PASSWORD)
        self.wait.until(lambda d: 'hidden' not in self.find_element(
            self.MODAL_CHANGE_PASSWORD
        ).get_attribute('class'))

    @allure.step("Saisie du mot de passe actuel")
    def enter_current_password(self, password):
        """Saisit le mot de passe actuel"""
        self.enter_text(self.INPUT_CURRENT_PASSWORD, password)

    @allure.step("Saisie du nouveau mot de passe")
    def enter_new_password(self, password):
        """Saisit le nouveau mot de passe"""
        self.enter_text(self.INPUT_NEW_PASSWORD, password)

    @allure.step("Confirmation du nouveau mot de passe")
    def enter_confirm_password(self, password):
        """Confirme le nouveau mot de passe"""
        self.enter_text(self.INPUT_CONFIRM_PASSWORD, password)

    @allure.step("Enregistrement du nouveau mot de passe")
    def save_password(self):
        """Clique sur Enregistrer"""
        self.click(self.BTN_SAVE_PASSWORD)

    @allure.step("Annulation du changement de mot de passe")
    def cancel_password_change(self):
        """Annule le changement de mot de passe"""
        self.click(self.BTN_CANCEL_PASSWORD)

    @allure.step("Changement de mot de passe")
    def change_password(self, current_password, new_password):
        """Effectue un changement de mot de passe complet"""
        self.open_change_password_modal()
        self.enter_current_password(current_password)
        self.enter_new_password(new_password)
        self.enter_confirm_password(new_password)
        self.save_password()

    def get_password_error(self):
        """Récupère le message d'erreur du mot de passe"""
        if self.is_element_visible(self.PASSWORD_ERROR, timeout=3):
            element = self.find_element(self.PASSWORD_ERROR)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.PASSWORD_ERROR)
        return None

    def are_password_requirements_displayed(self):
        """Vérifie si les exigences de mot de passe sont affichées"""
        if self.is_element_visible(self.PASSWORD_REQUIREMENTS, timeout=2):
            element = self.find_element(self.PASSWORD_REQUIREMENTS)
            return 'hidden' not in element.get_attribute('class')
        return False

    def get_password_requirements_status(self):
        """Récupère le statut de chaque exigence de mot de passe"""
        requirements = {}
        if self.are_password_requirements_displayed():
            requirements['length'] = 'requirement-met' in self.find_element(self.REQ_LENGTH).get_attribute('class')
            requirements['upper'] = 'requirement-met' in self.find_element(self.REQ_UPPER).get_attribute('class')
            requirements['lower'] = 'requirement-met' in self.find_element(self.REQ_LOWER).get_attribute('class')
            requirements['number'] = 'requirement-met' in self.find_element(self.REQ_NUMBER).get_attribute('class')
            requirements['special'] = 'requirement-met' in self.find_element(self.REQ_SPECIAL).get_attribute('class')
        return requirements

    # --- Méthodes Infos Utilisateur ---

    def get_user_info(self):
        """Récupère les informations de l'utilisateur"""
        return {
            'name': self.get_text(self.USER_NAME),
            'email': self.get_text(self.USER_EMAIL),
            'phone': self.get_text(self.USER_PHONE)
        }

    # --- Messages ---

    def get_success_message(self):
        """Récupère le message de succès"""
        if self.is_element_visible(self.SECURITY_SUCCESS, timeout=3):
            element = self.find_element(self.SECURITY_SUCCESS)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.SECURITY_SUCCESS)
        return None

    def is_modal_displayed(self):
        """Vérifie si la modal est affichée"""
        if self.is_element_visible(self.MODAL_CHANGE_PASSWORD, timeout=2):
            element = self.find_element(self.MODAL_CHANGE_PASSWORD)
            return 'hidden' not in element.get_attribute('class')
        return False
