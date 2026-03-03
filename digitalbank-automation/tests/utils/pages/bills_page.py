"""
Page Object pour la page Factures DigitalBank
"""

from tests.utils.base_page import BasePage
import allure


class BillsPage(BasePage):
    """Page Factures de l'application DigitalBank"""

    # Messages
    BILL_SUCCESS = "[data-testid='bill-success']"

    # Listes de factures
    PENDING_BILLS = "[data-testid='pending-bills']"
    PAID_BILLS = "[data-testid='paid-bills']"
    BILL_ITEMS = ".bill-item"

    # Modal de confirmation
    MODAL_CONFIRM = "[data-testid='modal-confirm-payment']"
    BTN_CANCEL_PAYMENT = "[data-testid='btn-cancel-payment']"
    BTN_CONFIRM_PAYMENT = "[data-testid='btn-confirm-payment']"

    def __init__(self, page):
        super().__init__(page)

    def is_bills_page_displayed(self):
        return self.is_element_visible(self.PENDING_BILLS, timeout=5)

    @allure.step("Récupération des factures en attente")
    def get_pending_bills(self):
        bills = []
        for item in self.page.locator(f"{self.PENDING_BILLS} .bill-item").all():
            bill = {
                'provider': item.locator('.bill-provider').inner_text(),
                'reference': item.locator('.bill-reference').inner_text(),
                'due_date': item.locator('.bill-due').inner_text(),
                'amount': item.locator('.bill-amount').inner_text(),
                'id': item.locator('[data-bill-id]').get_attribute('data-bill-id')
            }
            bills.append(bill)
        return bills

    @allure.step("Récupération des factures payées")
    def get_paid_bills(self):
        bills = []
        if not self.is_element_visible(self.PAID_BILLS, timeout=2):
            return bills
        for item in self.page.locator(f"{self.PAID_BILLS} .bill-item").all():
            text = item.inner_text()
            bill = {
                'provider': item.locator('.bill-provider').inner_text(),
                'reference': item.locator('.bill-reference').inner_text(),
                'amount': text.split('€')[0].split()[-1] + '€'
            }
            bills.append(bill)
        return bills

    def has_pending_bills(self):
        return not self.is_element_visible(f"{self.PENDING_BILLS} .empty-state", timeout=2)

    @allure.step("Clic sur Payer pour la facture {bill_id}")
    def click_pay_bill(self, bill_id):
        self.click(f"[data-testid='btn-pay-bill-{bill_id}']")

    @allure.step("Confirmation du paiement")
    def confirm_payment(self):
        self.wait_for_not_hidden(self.MODAL_CONFIRM)
        self.click(self.BTN_CONFIRM_PAYMENT)

    @allure.step("Annulation du paiement")
    def cancel_payment(self):
        self.click(self.BTN_CANCEL_PAYMENT)

    @allure.step("Paiement de la facture {bill_id}")
    def pay_bill(self, bill_id):
        self.click_pay_bill(bill_id)
        self.confirm_payment()

    def get_success_message(self):
        if self.is_element_visible(self.BILL_SUCCESS, timeout=3):
            locator = self.find_element(self.BILL_SUCCESS)
            if 'hidden' not in (locator.get_attribute('class') or ''):
                return self.get_text(self.BILL_SUCCESS)
        return None

    def get_pending_bills_count(self):
        return len(self.get_pending_bills())

    def is_modal_displayed(self):
        if self.is_element_visible(self.MODAL_CONFIRM, timeout=2):
            locator = self.find_element(self.MODAL_CONFIRM)
            return 'hidden' not in (locator.get_attribute('class') or '')
        return False
