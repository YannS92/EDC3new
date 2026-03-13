"""
Page Object pour la page de connexion DigitalBank

Couvre trois états de la page de connexion :
- Formulaire email/password principal
- Page de saisie du code 2FA (après connexion d'un compte avec 2FA activée)
- Page de réinitialisation de mot de passe (via le lien 'Mot de passe oublié')

Tous les sélecteurs utilisent l'attribut data-testid pour la stabilité.
"""

from tests.utils.base_page import BasePage
import allure


class LoginPage(BasePage):
    """Page de connexion de l'application DigitalBank"""

    # Locators
    EMAIL_FIELD = "[data-testid='input-email']"
    PASSWORD_FIELD = "[data-testid='input-password']"
    LOGIN_BUTTON = "[data-testid='btn-login']"
    REMEMBER_ME_CHECKBOX = "[data-testid='checkbox-remember']"
    FORGOT_PASSWORD_LINK = "[data-testid='link-forgot-password']"
    ERROR_MESSAGE = "[data-testid='login-error']"

    # Page 2FA
    TWO_FA_CODE_INPUTS = ".code-input"
    TWO_FA_CODE_0 = "[data-testid='2fa-code-0']"
    TWO_FA_CODE_1 = "[data-testid='2fa-code-1']"
    TWO_FA_CODE_2 = "[data-testid='2fa-code-2']"
    TWO_FA_CODE_3 = "[data-testid='2fa-code-3']"
    TWO_FA_CODE_4 = "[data-testid='2fa-code-4']"
    TWO_FA_CODE_5 = "[data-testid='2fa-code-5']"
    TWO_FA_VERIFY_BUTTON = "[data-testid='btn-verify-2fa']"
    TWO_FA_ERROR = "[data-testid='2fa-error']"

    # Page Reset Password
    RESET_EMAIL_FIELD = "[data-testid='input-reset-email']"
    RESET_BUTTON = "[data-testid='btn-reset-password']"
    RESET_ERROR = "[data-testid='reset-error']"
    RESET_SUCCESS = "[data-testid='reset-success']"
    BACK_TO_LOGIN_LINK = "[data-testid='link-back-to-login']"

    def __init__(self, page):
        super().__init__(page)

    @allure.step("Saisie de l'email: {email}")
    def enter_email(self, email):
        self.enter_text(self.EMAIL_FIELD, email)

    @allure.step("Saisie du mot de passe")
    def enter_password(self, password):
        self.enter_text(self.PASSWORD_FIELD, password)

    @allure.step("Clic sur le bouton de connexion")
    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    @allure.step("Connexion avec email: {email}")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    @allure.step("Coche 'Se souvenir de moi'")
    def check_remember_me(self):
        self.click(self.REMEMBER_ME_CHECKBOX)

    @allure.step("Clic sur 'Mot de passe oublié'")
    def click_forgot_password(self):
        self.click(self.FORGOT_PASSWORD_LINK)

    def get_error_message(self):
        """
        Retourne le message d'erreur de connexion s'il est visible.

        Ignore l'élément s'il est présent dans le DOM mais masqué via la classe CSS 'hidden'.

        Returns:
            Texte du message d'erreur, ou None si aucun message visible
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            locator = self.find_element(self.ERROR_MESSAGE)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.ERROR_MESSAGE)
        return None

    def is_login_page_displayed(self):
        """Retourne True si le champ email est visible (page de connexion affichée)."""
        return self.is_element_visible(self.EMAIL_FIELD)

    # --- Méthodes 2FA ---

    @allure.step("Saisie du code 2FA: {code}")
    def enter_2fa_code(self, code):
        code_str = str(code).zfill(6)
        inputs = [
            self.TWO_FA_CODE_0, self.TWO_FA_CODE_1, self.TWO_FA_CODE_2,
            self.TWO_FA_CODE_3, self.TWO_FA_CODE_4, self.TWO_FA_CODE_5
        ]
        for i, digit in enumerate(code_str):
            self.enter_text(inputs[i], digit)

    @allure.step("Validation du code 2FA")
    def submit_2fa_code(self):
        self.click(self.TWO_FA_VERIFY_BUTTON)

    @allure.step("Connexion avec 2FA")
    def login_with_2fa(self, email, password, code):
        self.login(email, password)
        self.enter_2fa_code(code)
        self.submit_2fa_code()

    def is_2fa_page_displayed(self):
        """Retourne True si le premier champ du code 2FA est visible."""
        return self.is_element_visible(self.TWO_FA_CODE_0, timeout=5)

    def get_2fa_error_message(self):
        """
        Retourne le message d'erreur 2FA s'il est visible.

        Returns:
            Texte du message d'erreur 2FA, ou None si aucun message visible
        """
        if self.is_element_visible(self.TWO_FA_ERROR, timeout=3):
            locator = self.find_element(self.TWO_FA_ERROR)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.TWO_FA_ERROR)
        return None

    # --- Méthodes Reset Password ---

    @allure.step("Saisie email pour réinitialisation: {email}")
    def enter_reset_email(self, email):
        self.enter_text(self.RESET_EMAIL_FIELD, email)

    @allure.step("Envoi du lien de réinitialisation")
    def submit_reset_password(self):
        self.click(self.RESET_BUTTON)

    @allure.step("Demande de réinitialisation pour: {email}")
    def request_password_reset(self, email):
        self.enter_reset_email(email)
        self.submit_reset_password()

    def is_reset_page_displayed(self):
        """Retourne True si le champ email de réinitialisation est visible."""
        return self.is_element_visible(self.RESET_EMAIL_FIELD, timeout=5)

    def get_reset_success_message(self):
        """
        Retourne le message de succès de réinitialisation s'il est visible.

        Returns:
            Texte du message de succès, ou None si aucun message visible
        """
        if self.is_element_visible(self.RESET_SUCCESS, timeout=3):
            locator = self.find_element(self.RESET_SUCCESS)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.RESET_SUCCESS)
        return None

    def get_reset_error_message(self):
        """
        Retourne le message d'erreur de réinitialisation s'il est visible.

        Returns:
            Texte du message d'erreur, ou None si aucun message visible
        """
        if self.is_element_visible(self.RESET_ERROR, timeout=3):
            locator = self.find_element(self.RESET_ERROR)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.RESET_ERROR)
        return None

    @allure.step("Retour à la page de connexion")
    def click_back_to_login(self):
        self.click(self.BACK_TO_LOGIN_LINK)
