"""
Page Object pour la page Sécurité DigitalBank
"""

from tests.utils.base_page import BasePage
import allure


class SecurityPage(BasePage):
    """Page Sécurité de l'application DigitalBank"""

    # Messages
    SECURITY_SUCCESS = "[data-testid='security-success']"

    # Toggles
    TOGGLE_2FA = "[data-testid='toggle-2fa']"
    TOGGLE_EMAIL_NOTIF = "[data-testid='toggle-email-notifications']"
    TOGGLE_SMS_NOTIF = "[data-testid='toggle-sms-notifications']"
    TWO_FA_GROUP = "[data-testid='2fa-toggle-group']"

    # Bouton changement mot de passe
    BTN_CHANGE_PASSWORD = "[data-testid='btn-change-password']"

    # Informations utilisateur
    USER_NAME = "[data-testid='user-name']"
    USER_EMAIL = "[data-testid='user-email']"
    USER_PHONE = "[data-testid='user-phone']"

    # Modal changement mot de passe
    MODAL_CHANGE_PASSWORD = "[data-testid='modal-change-password']"
    INPUT_CURRENT_PASSWORD = "[data-testid='input-current-password']"
    INPUT_NEW_PASSWORD = "[data-testid='input-new-password']"
    INPUT_CONFIRM_PASSWORD = "[data-testid='input-confirm-password']"
    BTN_CANCEL_PASSWORD = "[data-testid='btn-cancel-password']"
    BTN_SAVE_PASSWORD = "[data-testid='btn-save-password']"
    PASSWORD_ERROR = "[data-testid='password-error']"
    PASSWORD_REQUIREMENTS = "[data-testid='password-requirements']"

    # Requirements individuels
    REQ_LENGTH = "#req-length"
    REQ_UPPER = "#req-upper"
    REQ_LOWER = "#req-lower"
    REQ_NUMBER = "#req-number"
    REQ_SPECIAL = "#req-special"

    def __init__(self, page):
        super().__init__(page)

    def is_security_page_displayed(self):
        return self.is_element_visible(self.BTN_CHANGE_PASSWORD, timeout=5)

    # --- Méthodes 2FA ---

    @allure.step("Activation/Désactivation 2FA")
    def toggle_2fa(self):
        self.page.locator(self.TOGGLE_2FA).dispatch_event("click")

    def is_2fa_enabled(self):
        return self.page.locator(self.TOGGLE_2FA).is_checked()

    @allure.step("Activation de la 2FA")
    def enable_2fa(self):
        if not self.is_2fa_enabled():
            self.toggle_2fa()

    @allure.step("Désactivation de la 2FA")
    def disable_2fa(self):
        if self.is_2fa_enabled():
            self.toggle_2fa()

    # --- Méthodes Notifications ---

    @allure.step("Toggle notifications email")
    def toggle_email_notifications(self):
        self.page.locator(self.TOGGLE_EMAIL_NOTIF).dispatch_event("click")

    @allure.step("Toggle notifications SMS")
    def toggle_sms_notifications(self):
        self.page.locator(self.TOGGLE_SMS_NOTIF).dispatch_event("click")

    def is_email_notifications_enabled(self):
        return self.page.locator(self.TOGGLE_EMAIL_NOTIF).is_checked()

    def is_sms_notifications_enabled(self):
        return self.page.locator(self.TOGGLE_SMS_NOTIF).is_checked()

    # --- Méthodes Changement Mot de Passe ---

    @allure.step("Ouverture modal changement mot de passe")
    def open_change_password_modal(self):
        self.click(self.BTN_CHANGE_PASSWORD)
        self.wait_for_not_hidden(self.MODAL_CHANGE_PASSWORD)

    @allure.step("Saisie du mot de passe actuel")
    def enter_current_password(self, password):
        self.enter_text(self.INPUT_CURRENT_PASSWORD, password)

    @allure.step("Saisie du nouveau mot de passe")
    def enter_new_password(self, password):
        self.enter_text(self.INPUT_NEW_PASSWORD, password)

    @allure.step("Confirmation du nouveau mot de passe")
    def enter_confirm_password(self, password):
        self.enter_text(self.INPUT_CONFIRM_PASSWORD, password)

    @allure.step("Enregistrement du nouveau mot de passe")
    def save_password(self):
        self.click(self.BTN_SAVE_PASSWORD)

    @allure.step("Annulation du changement de mot de passe")
    def cancel_password_change(self):
        self.click(self.BTN_CANCEL_PASSWORD)

    @allure.step("Changement de mot de passe")
    def change_password(self, current_password, new_password):
        self.open_change_password_modal()
        self.enter_current_password(current_password)
        self.enter_new_password(new_password)
        self.enter_confirm_password(new_password)
        self.save_password()

    def get_password_error(self):
        if self.is_element_visible(self.PASSWORD_ERROR, timeout=3):
            locator = self.find_element(self.PASSWORD_ERROR)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.PASSWORD_ERROR)
        return None

    def are_password_requirements_displayed(self):
        if self.is_element_visible(self.PASSWORD_REQUIREMENTS, timeout=2):
            locator = self.find_element(self.PASSWORD_REQUIREMENTS)
            return 'hidden' not in (locator.get_attribute('class') or '')
        return False

    def get_password_requirements_status(self):
        requirements = {}
        if self.are_password_requirements_displayed():
            requirements['length'] = 'requirement-met' in (self.page.locator(self.REQ_LENGTH).get_attribute('class') or '')
            requirements['upper'] = 'requirement-met' in (self.page.locator(self.REQ_UPPER).get_attribute('class') or '')
            requirements['lower'] = 'requirement-met' in (self.page.locator(self.REQ_LOWER).get_attribute('class') or '')
            requirements['number'] = 'requirement-met' in (self.page.locator(self.REQ_NUMBER).get_attribute('class') or '')
            requirements['special'] = 'requirement-met' in (self.page.locator(self.REQ_SPECIAL).get_attribute('class') or '')
        return requirements

    # --- Méthodes Infos Utilisateur ---

    def get_user_info(self):
        return {
            'name': self.get_text(self.USER_NAME),
            'email': self.get_text(self.USER_EMAIL),
            'phone': self.get_text(self.USER_PHONE)
        }

    # --- Messages ---

    def get_success_message(self):
        if self.is_element_visible(self.SECURITY_SUCCESS, timeout=3):
            locator = self.find_element(self.SECURITY_SUCCESS)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.SECURITY_SUCCESS)
        return None

    def is_modal_displayed(self):
        if self.is_element_visible(self.MODAL_CHANGE_PASSWORD, timeout=2):
            locator = self.find_element(self.MODAL_CHANGE_PASSWORD)
            return 'hidden' not in (locator.get_attribute('class') or '')
        return False
