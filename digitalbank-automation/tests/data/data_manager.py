"""
Gestionnaire centralisé des données de test DigitalBank
Unifie l'accès aux données statiques (JSON) et dynamiques (factories/DB)
"""

import os
import json
from typing import Optional, Any

from tests.data.database import DatabaseManager, get_db
from tests.data.factories import (
    UserFactory, AccountFactory, TransactionFactory,
    BeneficiaryFactory, BillFactory
)


# Cache pour les données JSON
_json_data_cache: Optional[dict] = None


def load_test_data() -> dict:
    """
    Charge les données de test depuis le fichier JSON

    Fonction unique et centralisée pour charger les données statiques.
    Remplace les 3 implémentations dupliquées dans le codebase.

    Returns:
        Dictionnaire contenant toutes les données de test

    Example:
        >>> data = load_test_data()
        >>> data['users']['standard']['email']
        'test@digitalbank.fr'
    """
    global _json_data_cache

    if _json_data_cache is not None:
        return _json_data_cache

    data_path = os.path.join(os.path.dirname(__file__), 'test_users.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        _json_data_cache = json.load(f)

    return _json_data_cache


def clear_cache() -> None:
    """Vide le cache des données JSON"""
    global _json_data_cache
    _json_data_cache = None


class TestDataManager:
    """
    Gestionnaire centralisé des données de test

    Fournit un accès unifié aux données:
    - Statiques : depuis test_users.json
    - Dynamiques : via les factories avec Faker
    - Persistées : via la base de données SQLite

    Attributes:
        env: Environnement de test ('dev', 'int', 'uat', 'preprod')
    """

    def __init__(self, env: str = 'dev'):
        """
        Initialise le gestionnaire de données

        Args:
            env: Environnement de test
        """
        self.env = env
        self._db: Optional[DatabaseManager] = None

    @property
    def db(self) -> DatabaseManager:
        """Retourne l'instance de base de données (lazy loading)"""
        if self._db is None:
            self._db = get_db(self.env)
        return self._db

    # ═══════════════════════════════════════════════════════════════
    # DONNÉES STATIQUES (JSON)
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def get_static_data() -> dict:
        """Retourne toutes les données statiques du JSON"""
        return load_test_data()

    @staticmethod
    def get_user(user_key: str) -> dict:
        """
        Retourne un utilisateur par sa clé

        Args:
            user_key: Clé de l'utilisateur ('standard', 'with_2fa', 'additional')

        Returns:
            Dictionnaire de l'utilisateur
        """
        data = load_test_data()
        return data['users'].get(user_key, {})

    @staticmethod
    def get_account(account_key: str) -> dict:
        """
        Retourne un compte par sa clé

        Args:
            account_key: Clé du compte ('compte_courant', 'livret_a')

        Returns:
            Dictionnaire du compte
        """
        data = load_test_data()
        return data['accounts'].get(account_key, {})

    @staticmethod
    def get_beneficiary(beneficiary_key: str) -> dict:
        """
        Retourne un bénéficiaire par sa clé

        Args:
            beneficiary_key: Clé du bénéficiaire ('marc_bernard', 'julie_petit')

        Returns:
            Dictionnaire du bénéficiaire
        """
        data = load_test_data()
        return data['beneficiaries'].get(beneficiary_key, {})

    @staticmethod
    def get_bill(bill_key: str) -> dict:
        """
        Retourne une facture par sa clé

        Args:
            bill_key: Clé de la facture ('edf', 'orange')

        Returns:
            Dictionnaire de la facture
        """
        data = load_test_data()
        return data['bills'].get(bill_key, {})

    @staticmethod
    def get_invalid_credentials() -> dict:
        """Retourne les identifiants invalides pour les tests d'erreur"""
        data = load_test_data()
        return data['invalid_credentials']

    @staticmethod
    def get_password_requirements() -> dict:
        """Retourne les exigences de mot de passe"""
        data = load_test_data()
        return data['password_requirements']

    # ═══════════════════════════════════════════════════════════════
    # DONNÉES DYNAMIQUES (FACTORIES)
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def generate_user(**kwargs) -> Any:
        """Génère un utilisateur via la factory"""
        return UserFactory.build(**kwargs)

    @staticmethod
    def generate_account(**kwargs) -> Any:
        """Génère un compte via la factory"""
        return AccountFactory.build(**kwargs)

    @staticmethod
    def generate_transaction(**kwargs) -> Any:
        """Génère une transaction via la factory"""
        return TransactionFactory.build(**kwargs)

    @staticmethod
    def generate_beneficiary(**kwargs) -> Any:
        """Génère un bénéficiaire via la factory"""
        return BeneficiaryFactory.build(**kwargs)

    @staticmethod
    def generate_bill(**kwargs) -> Any:
        """Génère une facture via la factory"""
        return BillFactory.build(**kwargs)

    # ═══════════════════════════════════════════════════════════════
    # SEEDING (DONNÉES DE RÉFÉRENCE)
    # ═══════════════════════════════════════════════════════════════

    def seed_standard_data(self) -> None:
        """
        Initialise la base avec les données de référence du JSON

        Crée en base de données les utilisateurs, comptes, bénéficiaires
        et factures définis dans test_users.json
        """
        from tests.data.models import User, Account, Beneficiary, Bill

        self.db.create_tables()
        data = load_test_data()

        with self.db.session() as session:
            # Utilisateurs
            for key, user_data in data['users'].items():
                user = User(
                    email=user_data['email'],
                    password=user_data['password'],
                    name=user_data['name'],
                    has_2fa=user_data.get('has_2fa', False),
                    totp_code=user_data.get('totp_code')
                )
                session.add(user)

            session.flush()

            # Récupérer l'utilisateur standard pour les associations
            standard_user = session.query(User).filter_by(
                email=data['users']['standard']['email']
            ).first()

            if standard_user:
                # Comptes
                for key, account_data in data['accounts'].items():
                    account = Account(
                        user_id=standard_user.id,
                        type=account_data['type'],
                        number=account_data['number'],
                        balance=0.0
                    )
                    session.add(account)

                # Bénéficiaires
                for key, ben_data in data['beneficiaries'].items():
                    beneficiary = Beneficiary(
                        user_id=standard_user.id,
                        name=ben_data['name'],
                        iban=ben_data['iban']
                    )
                    session.add(beneficiary)

            # Factures (sans user_id)
            for key, bill_data in data['bills'].items():
                bill = Bill(
                    provider=bill_data['provider'],
                    reference=bill_data['reference'],
                    amount=bill_data['amount']
                )
                session.add(bill)

    def cleanup(self) -> None:
        """Supprime toutes les données de la base"""
        self.db.drop_tables()

    def reset(self) -> None:
        """Réinitialise la base avec les données de référence"""
        self.db.reset_database()
        self.seed_standard_data()
