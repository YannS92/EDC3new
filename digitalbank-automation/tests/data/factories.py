"""
Factories de données de test avec Faker
Génération de données françaises réalistes
"""

import random
import string
from datetime import datetime, timedelta
from typing import Optional, List
from faker import Faker

from tests.data.models import User, Account, Transaction, Beneficiary, Bill


# Instance Faker configurée pour la France
fake = Faker('fr_FR')


def generate_valid_password() -> str:
    """Génère un mot de passe valide selon les critères DigitalBank"""
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = ''.join(random.choices(string.ascii_lowercase, k=5))
    digit = ''.join(random.choices(string.digits, k=2))
    special = random.choice('!@#$%^&*')
    password = uppercase + lowercase + digit + special
    return ''.join(random.sample(password, len(password)))


def generate_french_iban() -> str:
    """Génère un IBAN français formaté"""
    bank_code = ''.join(random.choices(string.digits, k=5))
    branch_code = ''.join(random.choices(string.digits, k=5))
    account_number = ''.join(random.choices(string.digits, k=11))
    check_digits = ''.join(random.choices(string.digits, k=2))
    return f"FR76 {bank_code} {branch_code} {account_number} {check_digits}"


class UserFactory:
    """Factory pour générer des utilisateurs de test"""

    @staticmethod
    def build(
        email: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        has_2fa: bool = False,
        totp_code: Optional[str] = None
    ) -> User:
        """
        Construit un objet User sans le persister

        Args:
            email: Email de l'utilisateur (auto-généré si None)
            password: Mot de passe (auto-généré si None)
            name: Nom complet (auto-généré si None)
            has_2fa: Activation 2FA
            totp_code: Code TOTP si 2FA activée

        Returns:
            Instance User non persistée
        """
        return User(
            email=email or fake.email(),
            password=password or generate_valid_password(),
            name=name or fake.name(),
            has_2fa=has_2fa,
            totp_code=totp_code or ('123456' if has_2fa else None)
        )

    @staticmethod
    def standard_user() -> User:
        """Retourne un utilisateur standard (sans 2FA)"""
        return UserFactory.build(
            email="test@digitalbank.fr",
            password="Test1234!",
            name="Utilisateur Test",
            has_2fa=False
        )

    @staticmethod
    def user_with_2fa() -> User:
        """Retourne un utilisateur avec 2FA activée"""
        return UserFactory.build(
            email="marie.martin@email.com",
            password="SecurePass456!",
            name="Marie Martin",
            has_2fa=True,
            totp_code="123456"
        )

    @staticmethod
    def random_user(has_2fa: bool = False) -> User:
        """Génère un utilisateur aléatoire"""
        return UserFactory.build(has_2fa=has_2fa)

    @staticmethod
    def batch(count: int, has_2fa: bool = False) -> List[User]:
        """Génère plusieurs utilisateurs aléatoires"""
        return [UserFactory.random_user(has_2fa) for _ in range(count)]


class AccountFactory:
    """Factory pour générer des comptes bancaires"""

    ACCOUNT_TYPES = ["Compte Courant", "Livret A", "PEL", "Compte Joint"]

    @staticmethod
    def build(
        user_id: Optional[int] = None,
        account_type: Optional[str] = None,
        number: Optional[str] = None,
        balance: Optional[float] = None
    ) -> Account:
        """
        Construit un objet Account sans le persister

        Args:
            user_id: ID de l'utilisateur propriétaire
            account_type: Type de compte
            number: Numéro IBAN
            balance: Solde du compte

        Returns:
            Instance Account non persistée
        """
        return Account(
            user_id=user_id,
            type=account_type or random.choice(AccountFactory.ACCOUNT_TYPES),
            number=number or generate_french_iban(),
            balance=balance if balance is not None else round(random.uniform(100, 10000), 2)
        )

    @staticmethod
    def compte_courant(user_id: Optional[int] = None) -> Account:
        """Retourne un compte courant"""
        return AccountFactory.build(
            user_id=user_id,
            account_type="Compte Courant",
            number="FR76 0000 1111 2222 3333 4444 555"
        )

    @staticmethod
    def livret_a(user_id: Optional[int] = None) -> Account:
        """Retourne un Livret A"""
        return AccountFactory.build(
            user_id=user_id,
            account_type="Livret A",
            number="FR76 0000 1111 2222 3333 4444 666"
        )

    @staticmethod
    def random_account(user_id: Optional[int] = None) -> Account:
        """Génère un compte aléatoire"""
        return AccountFactory.build(user_id=user_id)

    @staticmethod
    def batch(count: int, user_id: Optional[int] = None) -> List[Account]:
        """Génère plusieurs comptes aléatoires"""
        return [AccountFactory.random_account(user_id) for _ in range(count)]


class TransactionFactory:
    """Factory pour générer des transactions bancaires"""

    DESCRIPTIONS_CREDIT = [
        "Virement reçu", "Remboursement", "Salaire", "Prime", "Remboursement Sécu"
    ]
    DESCRIPTIONS_DEBIT = [
        "Paiement CB", "Prélèvement", "Virement émis", "Retrait DAB", "Frais bancaires"
    ]

    @staticmethod
    def build(
        account_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
        amount: Optional[float] = None,
        description: Optional[str] = None,
        date: Optional[datetime] = None,
        reference: Optional[str] = None
    ) -> Transaction:
        """
        Construit un objet Transaction sans le persister

        Args:
            account_id: ID du compte associé
            transaction_type: Type ('credit' ou 'debit')
            amount: Montant
            description: Description
            date: Date de la transaction
            reference: Référence unique

        Returns:
            Instance Transaction non persistée
        """
        t_type = transaction_type or random.choice(['credit', 'debit'])
        descriptions = (
            TransactionFactory.DESCRIPTIONS_CREDIT if t_type == 'credit'
            else TransactionFactory.DESCRIPTIONS_DEBIT
        )

        return Transaction(
            account_id=account_id,
            type=t_type,
            amount=amount if amount is not None else round(random.uniform(10, 500), 2),
            description=description or random.choice(descriptions),
            date=date or fake.date_time_between(start_date='-30d', end_date='now'),
            reference=reference or f"TRX-{fake.uuid4()[:8].upper()}"
        )

    @staticmethod
    def credit(account_id: Optional[int] = None, amount: Optional[float] = None) -> Transaction:
        """Génère une transaction crédit"""
        return TransactionFactory.build(
            account_id=account_id,
            transaction_type='credit',
            amount=amount
        )

    @staticmethod
    def debit(account_id: Optional[int] = None, amount: Optional[float] = None) -> Transaction:
        """Génère une transaction débit"""
        return TransactionFactory.build(
            account_id=account_id,
            transaction_type='debit',
            amount=amount
        )

    @staticmethod
    def batch(count: int, account_id: Optional[int] = None) -> List[Transaction]:
        """Génère plusieurs transactions aléatoires"""
        return [TransactionFactory.build(account_id=account_id) for _ in range(count)]


class BeneficiaryFactory:
    """Factory pour générer des bénéficiaires de virement"""

    @staticmethod
    def build(
        user_id: Optional[int] = None,
        name: Optional[str] = None,
        iban: Optional[str] = None
    ) -> Beneficiary:
        """
        Construit un objet Beneficiary sans le persister

        Args:
            user_id: ID de l'utilisateur propriétaire
            name: Nom du bénéficiaire
            iban: IBAN du bénéficiaire

        Returns:
            Instance Beneficiary non persistée
        """
        return Beneficiary(
            user_id=user_id,
            name=name or fake.name(),
            iban=iban or generate_french_iban()
        )

    @staticmethod
    def marc_bernard(user_id: Optional[int] = None) -> Beneficiary:
        """Retourne le bénéficiaire Marc Bernard (données de test)"""
        return BeneficiaryFactory.build(
            user_id=user_id,
            name="Marc Bernard",
            iban="FR76 7777 8888 9999 0000 1111 222"
        )

    @staticmethod
    def julie_petit(user_id: Optional[int] = None) -> Beneficiary:
        """Retourne la bénéficiaire Julie Petit (données de test)"""
        return BeneficiaryFactory.build(
            user_id=user_id,
            name="Julie Petit",
            iban="FR76 3333 4444 5555 6666 7777 888"
        )

    @staticmethod
    def random_beneficiary(user_id: Optional[int] = None) -> Beneficiary:
        """Génère un bénéficiaire aléatoire"""
        return BeneficiaryFactory.build(user_id=user_id)

    @staticmethod
    def batch(count: int, user_id: Optional[int] = None) -> List[Beneficiary]:
        """Génère plusieurs bénéficiaires aléatoires"""
        return [BeneficiaryFactory.random_beneficiary(user_id) for _ in range(count)]


class BillFactory:
    """Factory pour générer des factures"""

    PROVIDERS = [
        ("EDF", "EDF-"),
        ("Orange", "ORG-"),
        ("Free", "FREE-"),
        ("Engie", "ENG-"),
        ("SFR", "SFR-"),
        ("Veolia", "VEO-"),
    ]

    @staticmethod
    def build(
        provider: Optional[str] = None,
        reference: Optional[str] = None,
        amount: Optional[float] = None,
        due_date: Optional[datetime] = None,
        paid: bool = False
    ) -> Bill:
        """
        Construit un objet Bill sans le persister

        Args:
            provider: Nom du fournisseur
            reference: Référence de facture
            amount: Montant
            due_date: Date d'échéance
            paid: Facture payée ou non

        Returns:
            Instance Bill non persistée
        """
        prov_name, prov_prefix = random.choice(BillFactory.PROVIDERS)
        year = datetime.now().year

        return Bill(
            provider=provider or prov_name,
            reference=reference or f"{prov_prefix}{year}-{random.randint(100000, 999999)}",
            amount=amount if amount is not None else round(random.uniform(20, 200), 2),
            due_date=due_date or (datetime.now() + timedelta(days=random.randint(7, 30))),
            paid=paid
        )

    @staticmethod
    def edf() -> Bill:
        """Retourne une facture EDF (données de test)"""
        return BillFactory.build(
            provider="EDF",
            reference="EDF-2025-001234",
            amount=156.78
        )

    @staticmethod
    def orange() -> Bill:
        """Retourne une facture Orange (données de test)"""
        return BillFactory.build(
            provider="Orange",
            reference="ORG-2025-567890",
            amount=49.99
        )

    @staticmethod
    def random_bill() -> Bill:
        """Génère une facture aléatoire"""
        return BillFactory.build()

    @staticmethod
    def batch(count: int) -> List[Bill]:
        """Génère plusieurs factures aléatoires"""
        return [BillFactory.random_bill() for _ in range(count)]
