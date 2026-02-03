@securite @2fa
Feature: Gestion de la double authentification
  En tant qu'utilisateur connecté
  Je veux pouvoir activer ou désactiver la 2FA
  Afin de gérer le niveau de sécurité de mon compte

  Background:
    Given l'application est accessible
    And je suis sur la page de connexion
    And je suis connecté en tant qu'utilisateur standard
    And je suis sur la page de sécurité

  @smoke @critical
  Scenario: Activation de la double authentification
    Given la double authentification est désactivée
    When j'active la double authentification
    Then un message de succès d'activation 2FA est affiché
    And la double authentification est activée

  @regression @critical
  Scenario: Désactivation de la double authentification
    Given la double authentification est activée
    When je désactive la double authentification
    Then un message de succès de désactivation 2FA est affiché
    And la double authentification est désactivée
