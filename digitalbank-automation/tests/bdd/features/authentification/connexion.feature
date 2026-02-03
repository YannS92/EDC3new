@authentification
Feature: Connexion utilisateur
  En tant qu'utilisateur de DigitalBank
  Je veux pouvoir me connecter à mon compte
  Afin d'accéder à mes services bancaires

  Background:
    Given l'application est accessible
    And je suis sur la page de connexion

  @smoke @critical
  Scenario: Connexion réussie avec identifiants valides
    When je me connecte avec "test@digitalbank.fr" et "Test1234!"
    Then le dashboard est affiché
    And le nom d'utilisateur "Utilisateur Test" est affiché

  @smoke @regression
  Scenario: Échec de connexion avec mot de passe incorrect
    When je me connecte avec "test@digitalbank.fr" et "WrongPassword123!"
    Then un message d'erreur de connexion est affiché
    And le message d'erreur contient "incorrect"
    And je reste sur la page de connexion

  @regression
  Scenario: Échec de connexion avec email inexistant
    When je me connecte avec "invalid@test.com" et "SomePassword123!"
    Then un message d'erreur de connexion est affiché
    And je reste sur la page de connexion

  @regression
  Scenario Outline: Échec de connexion avec différentes erreurs
    When je me connecte avec "<email>" et "<password>"
    Then un message d'erreur de connexion est affiché
    And je reste sur la page de connexion

    Examples:
      | email                  | password           |
      | test@digitalbank.fr    | wrongpassword      |
      | invalid@email.com      | Test1234!          |
      | notfound@nowhere.com   | Password123!       |
