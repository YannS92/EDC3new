"""
Page Object pour le Dashboard (Mes Comptes) DigitalBank
"""

from selenium.webdriver.common.by import By
from tests.utils.base_page import BasePage
import allure
import re


class DashboardPage(BasePage):
    """Page Dashboard de l'application DigitalBank"""

    # Header
    USER_NAME = (By.CSS_SELECTOR, "[data-testid='header-user-name']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[data-testid='btn-logout']")

    # Navigation tabs
    TAB_DASHBOARD = (By.CSS_SELECTOR, "[data-testid='tab-dashboard']")
    TAB_TRANSFER = (By.CSS_SELECTOR, "[data-testid='tab-transfer']")
    TAB_BILLS = (By.CSS_SELECTOR, "[data-testid='tab-bills']")
    TAB_SECURITY = (By.CSS_SELECTOR, "[data-testid='tab-security']")

    # Balance cards
    BALANCE_CARDS = (By.CSS_SELECTOR, "[data-testid='balance-cards']")
    ACCOUNT_CARDS = (By.CSS_SELECTOR, ".balance-card")
    TOTAL_BALANCE = (By.CSS_SELECTOR, ".total-balance strong")

    # Transactions
    TRANSACTION_LIST = (By.CSS_SELECTOR, "[data-testid='transaction-list']")
    TRANSACTION_ITEMS = (By.CSS_SELECTOR, ".transaction-item")

    def __init__(self, driver):
        """Initialise la page Dashboard"""
        super().__init__(driver)

    def is_dashboard_displayed(self):
        """Vérifie si le dashboard est affiché"""
        return self.is_element_visible(self.BALANCE_CARDS, timeout=5)

    @allure.step("Récupération du nom d'utilisateur")
    def get_user_name(self):
        """Récupère le nom de l'utilisateur connecté"""
        return self.get_text(self.USER_NAME)

    @allure.step("Déconnexion")
    def logout(self):
        """Se déconnecte de l'application"""
        self.click(self.LOGOUT_BUTTON)

    @allure.step("Navigation vers {tab_name}")
    def navigate_to_tab(self, tab_name):
        """Navigue vers un onglet spécifique"""
        tabs = {
            'dashboard': self.TAB_DASHBOARD,
            'transfer': self.TAB_TRANSFER,
            'bills': self.TAB_BILLS,
            'security': self.TAB_SECURITY
        }
        if tab_name.lower() in tabs:
            self.click(tabs[tab_name.lower()])

    @allure.step("Récupération du solde total")
    def get_total_balance(self):
        """Récupère le solde total de tous les comptes"""
        balance_text = self.get_text(self.TOTAL_BALANCE)
        # Extraction du montant (ex: "20 000,00 €" -> 20000.00)
        clean_value = re.sub(r'[^\d,.-]', '', balance_text)
        clean_value = clean_value.replace(' ', '').replace(',', '.')
        return float(clean_value)

    @allure.step("Récupération des comptes")
    def get_accounts(self):
        """Récupère la liste des comptes"""
        accounts = []
        cards = self.find_elements(self.ACCOUNT_CARDS)
        for card in cards:
            account = {
                'type': card.find_element(By.CSS_SELECTOR, '.balance-card-type').text,
                'number': card.find_element(By.CSS_SELECTOR, '.balance-card-number').text,
                'balance': card.find_element(By.CSS_SELECTOR, '.balance-amount').text,
                'id': card.get_attribute('data-account-id')
            }
            accounts.append(account)
        return accounts

    @allure.step("Sélection du compte: {account_id}")
    def select_account(self, account_id):
        """Sélectionne un compte par son ID"""
        card = (By.CSS_SELECTOR, f"[data-testid='account-card-{account_id}']")
        self.click(card)

    @allure.step("Récupération du solde du compte {account_id}")
    def get_account_balance(self, account_id):
        """Récupère le solde d'un compte spécifique"""
        balance_element = (By.CSS_SELECTOR, f"[data-testid='balance-{account_id}']")
        balance_text = self.get_text(balance_element)
        clean_value = re.sub(r'[^\d,.-]', '', balance_text)
        clean_value = clean_value.replace(' ', '').replace(',', '.')
        return float(clean_value)

    @allure.step("Récupération des transactions")
    def get_transactions(self):
        """Récupère la liste des transactions"""
        transactions = []
        items = self.find_elements(self.TRANSACTION_ITEMS)
        for item in items:
            transaction = {
                'description': item.find_element(By.CSS_SELECTOR, '.transaction-description').text,
                'date': item.find_element(By.CSS_SELECTOR, '.transaction-date').text,
                'amount': item.find_element(By.CSS_SELECTOR, '.transaction-amount').text,
                'type': 'credit' if 'credit' in item.find_element(
                    By.CSS_SELECTOR, '.transaction-amount'
                ).get_attribute('class') else 'debit'
            }
            transactions.append(transaction)
        return transactions

    def has_transactions(self):
        """Vérifie s'il y a des transactions"""
        empty_state = (By.CSS_SELECTOR, ".empty-state")
        return not self.is_element_visible(empty_state, timeout=2)
