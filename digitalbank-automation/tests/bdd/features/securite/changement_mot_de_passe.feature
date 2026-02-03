@securite
Feature: Changement de mot de passe
  En tant qu'utilisateur connecté
  Je veux pouvoir changer mon mot de passe
  Afin de maintenir la sécurité de mon compte

  Background:
    Given l'application est accessible
    And je suis sur la page de connexion
    And je suis connecté en tant qu'utilisateur standard
    And je suis sur la page de sécurité

  @regression
  Scenario: Ouverture de la modal de changement de mot de passe
    When j'ouvre la modal de changement de mot de passe
    Then la modal de changement de mot de passe est affichée

  @smoke @critical
  Scenario: Changement de mot de passe réussi
    When je change mon mot de passe de "Test1234!" à "NewSecure123!"
    Then un message de succès de changement de mot de passe est affiché

  @regression
  Scenario: Échec de changement avec mot de passe actuel incorrect
    When je change mon mot de passe de "WrongCurrent123!" à "NewSecure123!"
    Then un message d'erreur de mot de passe incorrect est affiché

  @regression
  Scenario: Annulation du changement de mot de passe
    When j'ouvre la modal de changement de mot de passe
    Then la modal de changement de mot de passe est affichée
    When j'annule le changement de mot de passe
    Then la modal de changement de mot de passe est fermée
