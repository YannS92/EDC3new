"""
Scripts CLI pour le seeding et le cleanup des données de test
Peut être utilisé en ligne de commande ou via les hooks pytest
"""

import argparse
import sys
from typing import Optional

from tests.data.database import get_db, DatabaseManager
from tests.data.data_manager import TestDataManager
from tests.data.factories import (
    UserFactory, AccountFactory, TransactionFactory,
    BeneficiaryFactory, BillFactory
)


def seed_database(env: str = 'dev', verbose: bool = False) -> None:
    """
    Initialise la base de données avec les données de référence

    Args:
        env: Environnement cible ('dev', 'int', 'uat', 'preprod')
        verbose: Afficher les détails
    """
    if verbose:
        print(f"[SEED] Initialisation de la base de données pour l'environnement '{env}'...")

    manager = TestDataManager(env)
    manager.seed_standard_data()

    if verbose:
        print(f"[SEED] Base de données créée: {manager.db.db_path}")
        print("[SEED] Données de référence insérées avec succès")


def cleanup_database(env: str = 'dev', verbose: bool = False) -> None:
    """
    Supprime toutes les données de la base

    Args:
        env: Environnement cible
        verbose: Afficher les détails
    """
    if verbose:
        print(f"[CLEANUP] Suppression des données pour l'environnement '{env}'...")

    manager = TestDataManager(env)
    manager.cleanup()

    if verbose:
        print("[CLEANUP] Données supprimées avec succès")


def reset_database(env: str = 'dev', verbose: bool = False) -> None:
    """
    Réinitialise complètement la base (drop + seed)

    Args:
        env: Environnement cible
        verbose: Afficher les détails
    """
    if verbose:
        print(f"[RESET] Réinitialisation de la base pour l'environnement '{env}'...")

    manager = TestDataManager(env)
    manager.reset()

    if verbose:
        print(f"[RESET] Base de données réinitialisée: {manager.db.db_path}")


def seed_random_data(env: str = 'dev', count: int = 10, verbose: bool = False) -> None:
    """
    Ajoute des données aléatoires à la base

    Args:
        env: Environnement cible
        count: Nombre d'enregistrements par entité
        verbose: Afficher les détails
    """
    from tests.data.models import User, Account, Transaction, Beneficiary, Bill

    if verbose:
        print(f"[SEED-RANDOM] Génération de {count} enregistrements par entité...")

    db = get_db(env)
    db.create_tables()

    with db.session() as session:
        # Utilisateurs
        users = UserFactory.batch(count)
        for user in users:
            session.add(user)
        session.flush()

        if verbose:
            print(f"  - {count} utilisateurs créés")

        # Comptes pour chaque utilisateur
        for user in users:
            accounts = AccountFactory.batch(2, user_id=user.id)
            for account in accounts:
                session.add(account)
        session.flush()

        if verbose:
            print(f"  - {count * 2} comptes créés")

        # Transactions pour les comptes
        accounts = session.query(Account).all()
        for account in accounts[:count]:
            transactions = TransactionFactory.batch(5, account_id=account.id)
            for tx in transactions:
                session.add(tx)

        if verbose:
            print(f"  - {count * 5} transactions créées")

        # Bénéficiaires
        for user in users[:count // 2]:
            beneficiaries = BeneficiaryFactory.batch(3, user_id=user.id)
            for ben in beneficiaries:
                session.add(ben)

        if verbose:
            print(f"  - {(count // 2) * 3} bénéficiaires créés")

        # Factures
        bills = BillFactory.batch(count)
        for bill in bills:
            session.add(bill)

        if verbose:
            print(f"  - {count} factures créées")

    if verbose:
        print("[SEED-RANDOM] Données aléatoires insérées avec succès")


# ═══════════════════════════════════════════════════════════════
# HOOKS PYTEST
# ═══════════════════════════════════════════════════════════════

def pytest_seed_hook(env: str = 'dev') -> None:
    """
    Hook pour initialiser la base avant les tests

    Utilisation dans conftest.py:
        from tests.data.seed_data import pytest_seed_hook

        @pytest.fixture(scope="session", autouse=True)
        def setup_test_database(request):
            env = request.config.getoption("--env", default="dev")
            pytest_seed_hook(env)
    """
    seed_database(env, verbose=False)


def pytest_cleanup_hook(env: str = 'dev') -> None:
    """
    Hook pour nettoyer la base après les tests

    Utilisation dans conftest.py:
        from tests.data.seed_data import pytest_cleanup_hook

        def pytest_sessionfinish(session, exitstatus):
            env = session.config.getoption("--env", default="dev")
            pytest_cleanup_hook(env)
    """
    cleanup_database(env, verbose=False)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    """Point d'entrée CLI"""
    parser = argparse.ArgumentParser(
        description="Gestion des données de test DigitalBank",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python -m tests.data.seed_data seed --env=dev
  python -m tests.data.seed_data seed --env=uat -v
  python -m tests.data.seed_data cleanup --env=dev
  python -m tests.data.seed_data reset --env=int -v
  python -m tests.data.seed_data random --env=dev --count=20 -v
        """
    )

    parser.add_argument(
        'command',
        choices=['seed', 'cleanup', 'reset', 'random'],
        help="Commande à exécuter"
    )
    parser.add_argument(
        '--env',
        default='dev',
        choices=['dev', 'int', 'uat', 'preprod'],
        help="Environnement cible (défaut: dev)"
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Mode verbeux"
    )
    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help="Nombre d'enregistrements pour la commande 'random' (défaut: 10)"
    )

    args = parser.parse_args()

    try:
        if args.command == 'seed':
            seed_database(args.env, args.verbose)
        elif args.command == 'cleanup':
            cleanup_database(args.env, args.verbose)
        elif args.command == 'reset':
            reset_database(args.env, args.verbose)
        elif args.command == 'random':
            seed_random_data(args.env, args.count, args.verbose)

        if args.verbose:
            print("\n[OK] Opération terminée avec succès")

    except Exception as e:
        print(f"[ERREUR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
