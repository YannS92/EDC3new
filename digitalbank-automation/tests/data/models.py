"""
Modèles SQLAlchemy pour les données de test DigitalBank
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Classe de base pour tous les modèles"""
    pass


class User(Base):
    """Modèle utilisateur"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    has_2fa = Column(Boolean, default=False)
    totp_code = Column(String(6), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    beneficiaries = relationship("Beneficiary", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire pour compatibilité JSON"""
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'has_2fa': self.has_2fa,
            'totp_code': self.totp_code,
        }


class Account(Base):
    """Modèle compte bancaire"""
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String(100), nullable=False)  # "Compte Courant", "Livret A", etc.
    number = Column(String(50), unique=True, nullable=False)  # IBAN
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire pour compatibilité JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'number': self.number,
            'balance': self.balance,
        }


class Transaction(Base):
    """Modèle transaction bancaire"""
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    type = Column(String(50), nullable=False)  # "credit", "debit"
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    reference = Column(String(100), nullable=True)

    # Relations
    account = relationship("Account", back_populates="transactions")

    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire pour compatibilité JSON"""
        return {
            'id': self.id,
            'account_id': self.account_id,
            'type': self.type,
            'amount': self.amount,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'reference': self.reference,
        }


class Beneficiary(Base):
    """Modèle bénéficiaire de virement"""
    __tablename__ = 'beneficiaries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    iban = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    user = relationship("User", back_populates="beneficiaries")

    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire pour compatibilité JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'iban': self.iban,
        }


class Bill(Base):
    """Modèle facture à payer"""
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String(100), nullable=False)  # "EDF", "Orange", etc.
    reference = Column(String(100), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=True)
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire pour compatibilité JSON"""
        return {
            'id': self.id,
            'provider': self.provider,
            'reference': self.reference,
            'amount': self.amount,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'paid': self.paid,
        }
