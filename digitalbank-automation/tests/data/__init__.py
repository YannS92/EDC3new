"""
Package data - Données de test DigitalBank

Ce package fournit un accès centralisé aux données de test:
- Données statiques (JSON) via load_test_data()
- Données dynamiques (Faker) via les factories
- Base de données SQLite via get_db()

Exemples d'utilisation:

    # Charger les données JSON
    from tests.data import load_test_data
    data = load_test_data()
    user = data['users']['standard']

    # Utiliser les factories
    from tests.data import UserFactory, AccountFactory
    user = UserFactory.build()
    account = AccountFactory.compte_courant()

    # Accès à la base de données
    from tests.data import get_db
    db = get_db('dev')
    db.create_tables()
    with db.session() as session:
        session.add(user)

    # Gestionnaire centralisé
    from tests.data import TestDataManager
    manager = TestDataManager('dev')
    manager.seed_standard_data()
"""

# Fonction principale de chargement des données
from tests.data.data_manager import load_test_data, clear_cache, TestDataManager

# Gestionnaire de base de données
from tests.data.database import get_db, DatabaseManager

# Factories pour la génération de données
from tests.data.factories import (
    UserFactory,
    AccountFactory,
    TransactionFactory,
    BeneficiaryFactory,
    BillFactory,
    generate_valid_password,
    generate_french_iban,
)

# Modèles ORM
from tests.data.models import (
    Base,
    User,
    Account,
    Transaction,
    Beneficiary,
    Bill,
)

# Scripts de seeding
from tests.data.seed_data import (
    seed_database,
    cleanup_database,
    reset_database,
    pytest_seed_hook,
    pytest_cleanup_hook,
)

__all__ = [
    # Data loading
    'load_test_data',
    'clear_cache',
    'TestDataManager',
    # Database
    'get_db',
    'DatabaseManager',
    # Factories
    'UserFactory',
    'AccountFactory',
    'TransactionFactory',
    'BeneficiaryFactory',
    'BillFactory',
    'generate_valid_password',
    'generate_french_iban',
    # Models
    'Base',
    'User',
    'Account',
    'Transaction',
    'Beneficiary',
    'Bill',
    # Seeding
    'seed_database',
    'cleanup_database',
    'reset_database',
    'pytest_seed_hook',
    'pytest_cleanup_hook',
]
