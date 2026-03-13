"""
Page Object pour le Dashboard (Mes Comptes) DigitalBank

Couvre :
- Navigation entre les onglets (Dashboard, Virements, Factures, Sécurité)
- Lecture des cartes de solde et du solde total
- Lecture de la liste des transactions récentes
- Déconnexion

Tous les sélecteurs utilisent l'attribut data-testid pour la stabilité.
"""

from tests.utils.base_page import BasePage
import allure
import re


class DashboardPage(BasePage):
    """Page Dashboard de l'application DigitalBank"""

    # Header
    USER_NAME = "[data-testid='header-user-name']"
    LOGOUT_BUTTON = "[data-testid='btn-logout']"

    # Navigation tabs
    TAB_DASHBOARD = "[data-testid='tab-dashboard']"
    TAB_TRANSFER = "[data-testid='tab-transfer']"
    TAB_BILLS = "[data-testid='tab-bills']"
    TAB_SECURITY = "[data-testid='tab-security']"

    # Balance cards
    BALANCE_CARDS = "[data-testid='balance-cards']"
    ACCOUNT_CARDS = ".balance-card"
    TOTAL_BALANCE = ".total-balance strong"

    # Transactions
    TRANSACTION_LIST = "[data-testid='transaction-list']"
    TRANSACTION_ITEMS = ".transaction-item"

    def __init__(self, page):
        super().__init__(page)

    def is_dashboard_displayed(self):
        """Retourne True si les cartes de solde sont visibles (dashboard affiché)."""
        return self.is_element_visible(self.BALANCE_CARDS, timeout=5)

    @allure.step("Récupération du nom d'utilisateur")
    def get_user_name(self):
        return self.get_text(self.USER_NAME)

    @allure.step("Déconnexion")
    def logout(self):
        self.click(self.LOGOUT_BUTTON)

    @allure.step("Navigation vers {tab_name}")
    def navigate_to_tab(self, tab_name):
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
        balance_text = self.get_text(self.TOTAL_BALANCE)
        clean_value = re.sub(r'[^\d,.-]', '', balance_text)
        clean_value = clean_value.replace(' ', '').replace(',', '.')
        return float(clean_value)

    @allure.step("Récupération des comptes")
    def get_accounts(self):
        accounts = []
        for card in self.page.locator(self.ACCOUNT_CARDS).all():
            account = {
                'type': card.locator('.balance-card-type').inner_text(),
                'number': card.locator('.balance-card-number').inner_text(),
                'balance': card.locator('.balance-amount').inner_text(),
                'id': card.get_attribute('data-account-id')
            }
            accounts.append(account)
        return accounts

    @allure.step("Sélection du compte: {account_id}")
    def select_account(self, account_id):
        self.click(f"[data-testid='account-card-{account_id}']")

    @allure.step("Récupération du solde du compte {account_id}")
    def get_account_balance(self, account_id):
        balance_text = self.get_text(f"[data-testid='balance-{account_id}']")
        clean_value = re.sub(r'[^\d,.-]', '', balance_text)
        clean_value = clean_value.replace(' ', '').replace(',', '.')
        return float(clean_value)

    @allure.step("Récupération des transactions")
    def get_transactions(self):
        transactions = []
        for item in self.page.locator(self.TRANSACTION_ITEMS).all():
            amount_locator = item.locator('.transaction-amount')
            transaction = {
                'description': item.locator('.transaction-description').inner_text(),
                'date': item.locator('.transaction-date').inner_text(),
                'amount': amount_locator.inner_text(),
                'type': 'credit' if 'credit' in (amount_locator.get_attribute('class') or '') else 'debit'
            }
            transactions.append(transaction)
        return transactions

    def has_transactions(self):
        """Retourne True si la liste de transactions contient au moins un élément."""
        return not self.is_element_visible(".empty-state", timeout=2)
