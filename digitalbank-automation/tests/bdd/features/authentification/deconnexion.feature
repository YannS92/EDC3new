@authentification
Feature: Déconnexion utilisateur
  En tant qu'utilisateur connecté
  Je veux pouvoir me déconnecter
  Afin de sécuriser mon compte quand je quitte l'application

  @smoke @critical
  Scenario: Déconnexion réussie
    Given l'application est accessible
    And je suis sur la page de connexion
    When je me connecte avec "test@digitalbank.fr" et "Test1234!"
    Then le dashboard est affiché
    When je clique sur le bouton de déconnexion
    Then la page de connexion est affichée

  @regression
  Scenario: Déconnexion après connexion avec 2FA
    Given l'application est accessible
    And je suis sur la page de connexion
    When je me connecte avec "marie.martin@email.com" et "SecurePass456!"
    Then la page 2FA est affichée
    When je saisis le code 2FA "123456"
    And je valide le code 2FA
    Then le dashboard est affiché
    When je clique sur le bouton de déconnexion
    Then la page de connexion est affichée
