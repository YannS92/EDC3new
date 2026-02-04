"""
Gestionnaire de base de données SQLite pour les tests DigitalBank
Pattern Singleton avec support multi-environnement
"""

import os
from typing import Optional, Generator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from tests.data.models import Base


class DatabaseManager:
    """
    Gestionnaire de base de données SQLite par environnement
    Implémente le pattern Singleton par environnement
    """
    _instances: dict = {}
    _engines: dict = {}

    def __new__(cls, env: str = 'dev'):
        """Singleton par environnement"""
        if env not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[env] = instance
        return cls._instances[env]

    def __init__(self, env: str = 'dev'):
        if self._initialized:
            return

        self.env = env
        self._db_dir = os.path.join(os.path.dirname(__file__), 'db')
        os.makedirs(self._db_dir, exist_ok=True)

        self.db_path = os.path.join(self._db_dir, f'test_data_{env}.db')
        self._engine = None
        self._session_factory = None
        self._initialized = True

    @property
    def engine(self):
        """Retourne l'engine SQLAlchemy (lazy loading)"""
        if self._engine is None:
            db_url = f'sqlite:///{self.db_path}'
            self._engine = create_engine(db_url, echo=False)
            DatabaseManager._engines[self.env] = self._engine
        return self._engine

    @property
    def session_factory(self):
        """Retourne la factory de sessions (lazy loading)"""
        if self._session_factory is None:
            self._session_factory = sessionmaker(bind=self.engine)
        return self._session_factory

    def create_tables(self) -> None:
        """Crée toutes les tables dans la base de données"""
        Base.metadata.create_all(self.engine)

    def drop_tables(self) -> None:
        """Supprime toutes les tables de la base de données"""
        Base.metadata.drop_all(self.engine)

    def reset_database(self) -> None:
        """Réinitialise la base de données (drop + create)"""
        self.drop_tables()
        self.create_tables()

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Context manager pour les sessions de base de données

        Usage:
            with db.session() as session:
                user = session.query(User).first()
        """
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_session(self) -> Session:
        """
        Retourne une nouvelle session (l'appelant doit la fermer)
        Préférer l'utilisation du context manager session()
        """
        return self.session_factory()

    @classmethod
    def close_all(cls) -> None:
        """Ferme tous les engines et connexions"""
        for env, engine in cls._engines.items():
            engine.dispose()
        cls._engines.clear()
        cls._instances.clear()


def get_db(env: str = 'dev') -> DatabaseManager:
    """
    Factory function pour obtenir une instance DatabaseManager

    Args:
        env: Environnement de test ('dev', 'int', 'uat', 'preprod')

    Returns:
        Instance DatabaseManager pour l'environnement spécifié
    """
    return DatabaseManager(env)
