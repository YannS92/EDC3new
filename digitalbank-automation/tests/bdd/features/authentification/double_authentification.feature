@authentification @2fa
Feature: Double authentification (2FA)
  En tant qu'utilisateur avec 2FA activée
  Je veux pouvoir me connecter avec un code de vérification
  Afin de sécuriser l'accès à mon compte

  Background:
    Given l'application est accessible
    And je suis sur la page de connexion

  @smoke @critical
  Scenario: Connexion réussie avec code 2FA valide
    When je me connecte avec "marie.martin@email.com" et "SecurePass456!"
    Then la page 2FA est affichée
    When je saisis le code 2FA "123456"
    And je valide le code 2FA
    Then le dashboard est affiché

  @regression
  Scenario: Échec de connexion avec code 2FA invalide
    When je me connecte avec "marie.martin@email.com" et "SecurePass456!"
    Then la page 2FA est affichée
    When je saisis le code 2FA "000000"
    And je valide le code 2FA
    Then un message d'erreur 2FA est affiché
    And je reste sur la page 2FA

  @regression
  Scenario Outline: Tentatives avec codes 2FA incorrects
    When je me connecte avec "marie.martin@email.com" et "SecurePass456!"
    Then la page 2FA est affichée
    When je saisis le code 2FA "<code>"
    And je valide le code 2FA
    Then un message d'erreur 2FA est affiché
    And je reste sur la page 2FA

    Examples:
      | code   |
      | 000000 |
      | 111111 |
      | 999999 |
