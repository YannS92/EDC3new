"""
Page Object pour la page Factures DigitalBank
"""

from selenium.webdriver.common.by import By
from tests.utils.base_page import BasePage
import allure


class BillsPage(BasePage):
    """Page Factures de l'application DigitalBank"""

    # Messages
    BILL_SUCCESS = (By.CSS_SELECTOR, "[data-testid='bill-success']")

    # Listes de factures
    PENDING_BILLS = (By.CSS_SELECTOR, "[data-testid='pending-bills']")
    PAID_BILLS = (By.CSS_SELECTOR, "[data-testid='paid-bills']")
    BILL_ITEMS = (By.CSS_SELECTOR, ".bill-item")

    # Modal de confirmation
    MODAL_CONFIRM = (By.CSS_SELECTOR, "[data-testid='modal-confirm-payment']")
    BTN_CANCEL_PAYMENT = (By.CSS_SELECTOR, "[data-testid='btn-cancel-payment']")
    BTN_CONFIRM_PAYMENT = (By.CSS_SELECTOR, "[data-testid='btn-confirm-payment']")

    def __init__(self, driver):
        """Initialise la page Factures"""
        super().__init__(driver)

    def is_bills_page_displayed(self):
        """Vérifie si la page de factures est affichée"""
        return self.is_element_visible(self.PENDING_BILLS, timeout=5)

    @allure.step("Récupération des factures en attente")
    def get_pending_bills(self):
        """Récupère la liste des factures en attente"""
        bills = []
        container = self.find_element(self.PENDING_BILLS)
        items = container.find_elements(By.CSS_SELECTOR, ".bill-item")
        for item in items:
            bill = {
                'provider': item.find_element(By.CSS_SELECTOR, '.bill-provider').text,
                'reference': item.find_element(By.CSS_SELECTOR, '.bill-reference').text,
                'due_date': item.find_element(By.CSS_SELECTOR, '.bill-due').text,
                'amount': item.find_element(By.CSS_SELECTOR, '.bill-amount').text,
                'id': item.find_element(By.CSS_SELECTOR, '[data-bill-id]').get_attribute('data-bill-id')
            }
            bills.append(bill)
        return bills

    @allure.step("Récupération des factures payées")
    def get_paid_bills(self):
        """Récupère la liste des factures payées"""
        bills = []
        if not self.is_element_visible(self.PAID_BILLS, timeout=2):
            return bills
        container = self.find_element(self.PAID_BILLS)
        items = container.find_elements(By.CSS_SELECTOR, ".bill-item")
        for item in items:
            bill = {
                'provider': item.find_element(By.CSS_SELECTOR, '.bill-provider').text,
                'reference': item.find_element(By.CSS_SELECTOR, '.bill-reference').text,
                'amount': item.text.split('€')[0].split()[-1] + '€'
            }
            bills.append(bill)
        return bills

    def has_pending_bills(self):
        """Vérifie s'il y a des factures en attente"""
        empty = (By.CSS_SELECTOR, "[data-testid='pending-bills'] .empty-state")
        return not self.is_element_visible(empty, timeout=2)

    @allure.step("Clic sur Payer pour la facture {bill_id}")
    def click_pay_bill(self, bill_id):
        """Clique sur le bouton Payer d'une facture"""
        btn = (By.CSS_SELECTOR, f"[data-testid='btn-pay-bill-{bill_id}']")
        self.click(btn)

    @allure.step("Confirmation du paiement")
    def confirm_payment(self):
        """Confirme le paiement dans la modal"""
        self.wait.until(lambda d: 'hidden' not in self.find_element(
            self.MODAL_CONFIRM
        ).get_attribute('class'))
        self.click(self.BTN_CONFIRM_PAYMENT)

    @allure.step("Annulation du paiement")
    def cancel_payment(self):
        """Annule le paiement dans la modal"""
        self.click(self.BTN_CANCEL_PAYMENT)

    @allure.step("Paiement de la facture {bill_id}")
    def pay_bill(self, bill_id):
        """Effectue le paiement complet d'une facture"""
        self.click_pay_bill(bill_id)
        self.confirm_payment()

    def get_success_message(self):
        """Récupère le message de succès"""
        if self.is_element_visible(self.BILL_SUCCESS, timeout=3):
            element = self.find_element(self.BILL_SUCCESS)
            if 'hidden' not in element.get_attribute('class'):
                return self.get_text(self.BILL_SUCCESS)
        return None

    def get_pending_bills_count(self):
        """Récupère le nombre de factures en attente"""
        return len(self.get_pending_bills())

    def is_modal_displayed(self):
        """Vérifie si la modal de confirmation est affichée"""
        if self.is_element_visible(self.MODAL_CONFIRM, timeout=2):
            element = self.find_element(self.MODAL_CONFIRM)
            return 'hidden' not in element.get_attribute('class')
        return False
