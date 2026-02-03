"""
Page Object pour la page de connexion DigitalBank
Utilise les data-testid de l'application réelle
"""

from selenium.webdriver.common.by import By
from tests.utils.base_page import BasePage
import allure


class LoginPage(BasePage):
    """Page de connexion de l'application DigitalBank"""

    # Locators basés sur data-testid
    EMAIL_FIELD = (By.CSS_SELECTOR, "[data-testid='input-email']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "[data-testid='input-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='btn-login']")
    REMEMBER_ME_CHECKBOX = (By.CSS_SELECTOR, "[data-testid='checkbox-remember']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "[data-testid='link-forgot-password']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='login-error']")

    # Page 2FA
    TWO_FA_CODE_INPUTS = (By.CSS_SELECTOR, ".code-input")
    TWO_FA_CODE_0 = (By.CSS_SELECTOR, "[data-testid='2fa-code-0']")
    TWO_FA_CODE_1 = (By.CSS_SELECTOR, "[data-testid='2fa-code-1']")
    TWO_FA_CODE_2 = (By.CSS_SELECTOR, "[data-testid='2fa-code-2']")
    TWO_FA_CODE_3 = (By.CSS_SELECTOR, "[data-testid='2fa-code-3']")
    TWO_FA_CODE_4 = (By.CSS_SELECTOR, "[data-testid='2fa-code-4']")
    TWO_FA_CODE_5 = (By.CSS_SELECTOR, "[data-testid='2fa-code-5']")
    TWO_FA_VERIFY_BUTTON = (By.CSS_SELECTOR, "[data-testid='btn-verify-2fa']")
    TWO_FA_ERROR = (By.CSS_SELECTOR, "[data-testid='2fa-error']")

    # Page Reset Password
    RESET_EMAIL_FIELD = (By.CSS_SELECTOR, "[data-testid='input-reset-email']")
    RESET_BUTTON = (By.CSS_SELECTOR, "[data-testid='btn-reset-password']")
    RESET_ERROR = (By.CSS_SELECTOR, "[data-testid='reset-error']")
    RESET_SUCCESS = (By.CSS_SELECTOR, "[data-testid='reset-success']")
    BACK_TO_LOGIN_LINK = (By.CSS_SELECTOR, "[data-testid='link-back-to-login']")

    def __init__(self, driver):
        """Initialise la page de connexion"""
        super().__init__(driver)

    @allure.step("Saisie de l'email: {email}")
    def enter_email(self, email):
        """Saisit l'adresse email"""
        self.enter_text(self.EMAIL_FIELD, email)

    @allure.step("Saisie du mot de passe")
    def enter_password(self, password):
        """Saisit le mot de passe"""
        self.enter_text(self.PASSWORD_FIELD, password)

    @allure.step("Clic sur le bouton de connexion")
    def click_login(self):
        """Clique sur le bouton de connexion"""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Connexion avec email: {email}")
    def login(self, email, password):
        """Effectue une connexion complète"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    @allure.step("Coche 'Se souvenir de moi'")
    def check_remember_me(self):
        """Coche la case 'Se souvenir de moi'"""
        self.click(self.REMEMBER_ME_CHECKBOX)

    @allure.step("Clic sur 'Mot de passe oublié'")
    def click_forgot_password(self):
        """Clique sur le lien mot de passe oublié"""
        self.click(self.FORGOT_PASSWORD_LINK)

    def get_error_message(self):
        """Récupère le message d'erreur de connexion"""
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            element = self.find_element(self.ERROR_MESSAGE)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.ERROR_MESSAGE)
        return None

    def is_login_page_displayed(self):
        """Vérifie si la page de connexion est affichée"""
        return self.is_element_visible(self.EMAIL_FIELD)

    # --- Méthodes 2FA ---

    @allure.step("Saisie du code 2FA: {code}")
    def enter_2fa_code(self, code):
        """Saisit le code 2FA digit par digit"""
        code_str = str(code).zfill(6)
        inputs = [
            self.TWO_FA_CODE_0, self.TWO_FA_CODE_1, self.TWO_FA_CODE_2,
            self.TWO_FA_CODE_3, self.TWO_FA_CODE_4, self.TWO_FA_CODE_5
        ]
        for i, digit in enumerate(code_str):
            self.enter_text(inputs[i], digit)

    @allure.step("Validation du code 2FA")
    def submit_2fa_code(self):
        """Clique sur le bouton de vérification 2FA"""
        self.click(self.TWO_FA_VERIFY_BUTTON)

    @allure.step("Connexion avec 2FA")
    def login_with_2fa(self, email, password, code):
        """Effectue une connexion complète avec 2FA"""
        self.login(email, password)
        self.enter_2fa_code(code)
        self.submit_2fa_code()

    def is_2fa_page_displayed(self):
        """Vérifie si la page 2FA est affichée"""
        return self.is_element_visible(self.TWO_FA_CODE_0, timeout=5)

    def get_2fa_error_message(self):
        """Récupère le message d'erreur 2FA"""
        if self.is_element_visible(self.TWO_FA_ERROR, timeout=3):
            element = self.find_element(self.TWO_FA_ERROR)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.TWO_FA_ERROR)
        return None

    # --- Méthodes Reset Password ---

    @allure.step("Saisie email pour réinitialisation: {email}")
    def enter_reset_email(self, email):
        """Saisit l'email pour la réinitialisation"""
        self.enter_text(self.RESET_EMAIL_FIELD, email)

    @allure.step("Envoi du lien de réinitialisation")
    def submit_reset_password(self):
        """Soumet le formulaire de réinitialisation"""
        self.click(self.RESET_BUTTON)

    @allure.step("Demande de réinitialisation pour: {email}")
    def request_password_reset(self, email):
        """Demande une réinitialisation de mot de passe"""
        self.enter_reset_email(email)
        self.submit_reset_password()

    def is_reset_page_displayed(self):
        """Vérifie si la page de réinitialisation est affichée"""
        return self.is_element_visible(self.RESET_EMAIL_FIELD, timeout=5)

    def get_reset_success_message(self):
        """Récupère le message de succès"""
        if self.is_element_visible(self.RESET_SUCCESS, timeout=3):
            element = self.find_element(self.RESET_SUCCESS)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.RESET_SUCCESS)
        return None

    def get_reset_error_message(self):
        """Récupère le message d'erreur"""
        if self.is_element_visible(self.RESET_ERROR, timeout=3):
            element = self.find_element(self.RESET_ERROR)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.RESET_ERROR)
        return None

    @allure.step("Retour à la page de connexion")
    def click_back_to_login(self):
        """Retourne à la page de connexion"""
        self.click(self.BACK_TO_LOGIN_LINK)
