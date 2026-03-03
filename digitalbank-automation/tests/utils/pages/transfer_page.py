"""
Page Object pour la page Virements DigitalBank
"""

from tests.utils.base_page import BasePage
import allure


class TransferPage(BasePage):
    """Page Virements de l'application DigitalBank"""

    # Type de virement
    BTN_INTERNAL = "[data-testid='btn-transfer-internal']"
    BTN_EXTERNAL = "[data-testid='btn-transfer-external']"

    # Formulaire
    SELECT_FROM_ACCOUNT = "[data-testid='select-from-account']"
    SELECT_TO_ACCOUNT = "[data-testid='select-to-account']"
    INPUT_AMOUNT = "[data-testid='input-amount']"
    INPUT_DESCRIPTION = "[data-testid='input-description']"
    BTN_SUBMIT = "[data-testid='btn-submit-transfer']"

    # Messages
    TRANSFER_ERROR = "[data-testid='transfer-error']"
    TRANSFER_SUCCESS = "[data-testid='transfer-success']"

    # Bénéficiaires (virement externe)
    BENEFICIARY_LIST = "[data-testid='beneficiary-list']"
    BTN_ADD_BENEFICIARY = "[data-testid='btn-add-beneficiary']"

    # Modal ajout bénéficiaire
    MODAL_ADD_BENEFICIARY = "[data-testid='modal-add-beneficiary']"
    INPUT_BENEFICIARY_NAME = "[data-testid='input-beneficiary-name']"
    INPUT_BENEFICIARY_IBAN = "[data-testid='input-beneficiary-iban']"
    BTN_CANCEL_BENEFICIARY = "[data-testid='btn-cancel-beneficiary']"
    BTN_SAVE_BENEFICIARY = "[data-testid='btn-save-beneficiary']"

    def __init__(self, page):
        super().__init__(page)

    def is_transfer_page_displayed(self):
        return self.is_element_visible(self.SELECT_FROM_ACCOUNT, timeout=5)

    @allure.step("Sélection virement interne")
    def select_internal_transfer(self):
        self.click(self.BTN_INTERNAL)

    @allure.step("Sélection virement externe")
    def select_external_transfer(self):
        self.click(self.BTN_EXTERNAL)

    @allure.step("Sélection du compte débiteur")
    def select_from_account(self, index=0):
        self.page.locator(self.SELECT_FROM_ACCOUNT).select_option(index=index)

    @allure.step("Sélection du compte créditeur")
    def select_to_account(self, index=0):
        first_value = self.page.locator(f"{self.SELECT_TO_ACCOUNT} option").first.get_attribute('value')
        actual_index = index + 1 if first_value == '' else index
        self.page.locator(self.SELECT_TO_ACCOUNT).select_option(index=actual_index)

    @allure.step("Saisie du montant: {amount}")
    def enter_amount(self, amount):
        self.enter_text(self.INPUT_AMOUNT, str(amount))

    @allure.step("Saisie du motif: {description}")
    def enter_description(self, description):
        self.enter_text(self.INPUT_DESCRIPTION, description)

    @allure.step("Soumission du virement")
    def submit_transfer(self):
        self.click(self.BTN_SUBMIT)

    @allure.step("Virement interne de {amount}€")
    def make_internal_transfer(self, amount, description=""):
        self.select_internal_transfer()
        self.select_from_account(0)
        self.select_to_account(0)
        self.enter_amount(amount)
        if description:
            self.enter_description(description)
        self.submit_transfer()

    @allure.step("Sélection du bénéficiaire: {beneficiary_id}")
    def select_beneficiary(self, beneficiary_id):
        self.click(f"[data-testid='beneficiary-{beneficiary_id}']")

    @allure.step("Ouverture modal ajout bénéficiaire")
    def open_add_beneficiary_modal(self):
        self.click(self.BTN_ADD_BENEFICIARY)

    @allure.step("Ajout bénéficiaire: {name}")
    def add_beneficiary(self, name, iban):
        self.open_add_beneficiary_modal()
        self.wait_for_not_hidden(self.MODAL_ADD_BENEFICIARY)
        self.enter_text(self.INPUT_BENEFICIARY_NAME, name)
        self.enter_text(self.INPUT_BENEFICIARY_IBAN, iban)
        self.click(self.BTN_SAVE_BENEFICIARY)

    @allure.step("Annulation ajout bénéficiaire")
    def cancel_add_beneficiary(self):
        self.click(self.BTN_CANCEL_BENEFICIARY)

    def get_success_message(self):
        if self.is_element_visible(self.TRANSFER_SUCCESS, timeout=3):
            locator = self.find_element(self.TRANSFER_SUCCESS)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.TRANSFER_SUCCESS)
        return None

    def get_error_message(self):
        if self.is_element_visible(self.TRANSFER_ERROR, timeout=3):
            locator = self.find_element(self.TRANSFER_ERROR)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.TRANSFER_ERROR)
        return None

    def get_beneficiaries(self):
        beneficiaries = []
        for option in self.page.locator(".beneficiary-option").all():
            beneficiary = {
                'name': option.locator('.beneficiary-name').inner_text(),
                'iban': option.locator('.beneficiary-iban').inner_text(),
                'id': option.get_attribute('data-beneficiary-id')
            }
            beneficiaries.append(beneficiary)
        return beneficiaries
