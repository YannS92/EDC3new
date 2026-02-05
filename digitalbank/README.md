# DigitalBank - Application de Test pour Automatisation

## Vue d'ensemble

DigitalBank est une application bancaire mobile simulée, conçue spécifiquement pour l'examen d'automatisation des tests. Elle implémente toutes les fonctionnalités décrites dans le cahier des charges de l'étude de cas.

---

## Fonctionnalités Implémentées

### 1. Authentification Sécurisée
- Connexion avec identifiant et mot de passe
- Double authentification optionnelle (2FA par SMS)
- Réinitialisation de mot de passe via email
- Option "Se souvenir de moi"

### 2. Consultation de Compte
- Affichage du solde des comptes (Compte Courant, Livret A)
- Historique des transactions récentes
- Solde total multi-comptes

### 3. Virements Bancaires
- Transfert entre comptes propres
- Transfert vers des bénéficiaires tiers
- Validation des informations bancaires (IBAN)
- Ajout de nouveaux bénéficiaires

### 4. Paiement de Factures
- Liste des factures en attente
- Paiement avec confirmation
- Historique des factures payées

### 5. Gestion des Paramètres de Sécurité
- Modification du mot de passe (avec validation des critères)
- Activation/désactivation de la double authentification
- Gestion des notifications (email/SMS)

---

## Identifiants de Test

### Compte Standard (sans 2FA)
```
Email: test@digitalbank.fr
Mot de passe: Test1234!
```

### Compte avec Double Authentification
```
Email: marie.martin@email.com
Mot de passe: SecurePass456!
Code 2FA: 123456
```

### Compte Supplémentaire
```
Email: jean.dupont@email.com
Mot de passe: Password123!
```

---

## Notes Importantes

1. **Mode Test**: L'application affiche une bannière jaune indiquant le mode test
2. **Persistance**: Les données sont stockées en mémoire et réinitialisées au rechargement
3. **Code 2FA**: Le code valide pour les tests est toujours `123456`
4. **IBAN**: Le format attendu est `FR76` suivi de 23 chiffres
5. **Mot de passe**: Doit contenir 8+ caractères, majuscule, minuscule, chiffre, caractère spécial

---