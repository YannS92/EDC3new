"""
Page Object pour la page Virements DigitalBank
"""

from selenium.webdriver.common.by import By
from tests.utils.base_page import BasePage
import allure


class TransferPage(BasePage):
    """Page Virements de l'application DigitalBank"""

    # Type de virement
    BTN_INTERNAL = (By.CSS_SELECTOR, "[data-testid='btn-transfer-internal']")
    BTN_EXTERNAL = (By.CSS_SELECTOR, "[data-testid='btn-transfer-external']")

    # Formulaire
    SELECT_FROM_ACCOUNT = (By.CSS_SELECTOR, "[data-testid='select-from-account']")
    SELECT_TO_ACCOUNT = (By.CSS_SELECTOR, "[data-testid='select-to-account']")
    INPUT_AMOUNT = (By.CSS_SELECTOR, "[data-testid='input-amount']")
    INPUT_DESCRIPTION = (By.CSS_SELECTOR, "[data-testid='input-description']")
    BTN_SUBMIT = (By.CSS_SELECTOR, "[data-testid='btn-submit-transfer']")

    # Messages
    TRANSFER_ERROR = (By.CSS_SELECTOR, "[data-testid='transfer-error']")
    TRANSFER_SUCCESS = (By.CSS_SELECTOR, "[data-testid='transfer-success']")

    # Bénéficiaires (virement externe)
    BENEFICIARY_LIST = (By.CSS_SELECTOR, "[data-testid='beneficiary-list']")
    BTN_ADD_BENEFICIARY = (By.CSS_SELECTOR, "[data-testid='btn-add-beneficiary']")

    # Modal ajout bénéficiaire
    MODAL_ADD_BENEFICIARY = (By.CSS_SELECTOR, "[data-testid='modal-add-beneficiary']")
    INPUT_BENEFICIARY_NAME = (By.CSS_SELECTOR, "[data-testid='input-beneficiary-name']")
    INPUT_BENEFICIARY_IBAN = (By.CSS_SELECTOR, "[data-testid='input-beneficiary-iban']")
    BTN_CANCEL_BENEFICIARY = (By.CSS_SELECTOR, "[data-testid='btn-cancel-beneficiary']")
    BTN_SAVE_BENEFICIARY = (By.CSS_SELECTOR, "[data-testid='btn-save-beneficiary']")

    def __init__(self, driver):
        """Initialise la page Virements"""
        super().__init__(driver)

    def is_transfer_page_displayed(self):
        """Vérifie si la page de virement est affichée"""
        return self.is_element_visible(self.SELECT_FROM_ACCOUNT, timeout=5)

    @allure.step("Sélection virement interne")
    def select_internal_transfer(self):
        """Sélectionne le type virement interne"""
        self.click(self.BTN_INTERNAL)

    @allure.step("Sélection virement externe")
    def select_external_transfer(self):
        """Sélectionne le type virement externe"""
        self.click(self.BTN_EXTERNAL)

    @allure.step("Sélection du compte débiteur")
    def select_from_account(self, index=0):
        """Sélectionne le compte source"""
        select = self.find_element(self.SELECT_FROM_ACCOUNT)
        options = select.find_elements(By.TAG_NAME, 'option')
        if len(options) > index:
            options[index].click()

    @allure.step("Sélection du compte créditeur")
    def select_to_account(self, index=0):
        """Sélectionne le compte destination"""
        select = self.find_element(self.SELECT_TO_ACCOUNT)
        options = select.find_elements(By.TAG_NAME, 'option')
        # Skip first option if it's a placeholder
        actual_index = index + 1 if options[0].get_attribute('value') == '' else index
        if len(options) > actual_index:
            options[actual_index].click()

    @allure.step("Saisie du montant: {amount}")
    def enter_amount(self, amount):
        """Saisit le montant du virement"""
        self.enter_text(self.INPUT_AMOUNT, str(amount))

    @allure.step("Saisie du motif: {description}")
    def enter_description(self, description):
        """Saisit le motif du virement"""
        self.enter_text(self.INPUT_DESCRIPTION, description)

    @allure.step("Soumission du virement")
    def submit_transfer(self):
        """Soumet le formulaire de virement"""
        self.click(self.BTN_SUBMIT)

    @allure.step("Virement interne de {amount}€")
    def make_internal_transfer(self, amount, description=""):
        """Effectue un virement interne complet"""
        self.select_internal_transfer()
        self.select_from_account(0)
        self.select_to_account(0)
        self.enter_amount(amount)
        if description:
            self.enter_description(description)
        self.submit_transfer()

    @allure.step("Sélection du bénéficiaire: {beneficiary_id}")
    def select_beneficiary(self, beneficiary_id):
        """Sélectionne un bénéficiaire"""
        beneficiary = (By.CSS_SELECTOR, f"[data-testid='beneficiary-{beneficiary_id}']")
        self.click(beneficiary)

    @allure.step("Ouverture modal ajout bénéficiaire")
    def open_add_beneficiary_modal(self):
        """Ouvre la modal d'ajout de bénéficiaire"""
        self.click(self.BTN_ADD_BENEFICIARY)

    @allure.step("Ajout bénéficiaire: {name}")
    def add_beneficiary(self, name, iban):
        """Ajoute un nouveau bénéficiaire"""
        self.open_add_beneficiary_modal()
        self.wait.until(lambda d: 'hidden' not in self.find_element(
            self.MODAL_ADD_BENEFICIARY
        ).get_attribute('class'))
        self.enter_text(self.INPUT_BENEFICIARY_NAME, name)
        self.enter_text(self.INPUT_BENEFICIARY_IBAN, iban)
        self.click(self.BTN_SAVE_BENEFICIARY)

    @allure.step("Annulation ajout bénéficiaire")
    def cancel_add_beneficiary(self):
        """Annule l'ajout de bénéficiaire"""
        self.click(self.BTN_CANCEL_BENEFICIARY)

    def get_success_message(self):
        """Récupère le message de succès"""
        if self.is_element_visible(self.TRANSFER_SUCCESS, timeout=3):
            element = self.find_element(self.TRANSFER_SUCCESS)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.TRANSFER_SUCCESS)
        return None

    def get_error_message(self):
        """Récupère le message d'erreur"""
        if self.is_element_visible(self.TRANSFER_ERROR, timeout=3):
            element = self.find_element(self.TRANSFER_ERROR)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.TRANSFER_ERROR)
        return None

    def get_beneficiaries(self):
        """Récupère la liste des bénéficiaires"""
        beneficiaries = []
        options = self.find_elements((By.CSS_SELECTOR, ".beneficiary-option"))
        for option in options:
            beneficiary = {
                'name': option.find_element(By.CSS_SELECTOR, '.beneficiary-name').text,
                'iban': option.find_element(By.CSS_SELECTOR, '.beneficiary-iban').text,
                'id': option.get_attribute('data-beneficiary-id')
            }
            beneficiaries.append(beneficiary)
        return beneficiaries
