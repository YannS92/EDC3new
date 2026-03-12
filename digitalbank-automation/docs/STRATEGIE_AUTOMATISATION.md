# Stratégie d'Automatisation des Tests - DigitalBank

## 1. Introduction

Ce document définit la stratégie d'automatisation des tests pour l'application bancaire DigitalBank. L'objectif est d'améliorer la qualité du produit et de reduire le temps de livraison en automatisant les tests critiques dans le cadre d'une methodologie **Agile** avec des sprints de deux semaines.

---

## 2. Perimetre de l'Automatisation

### 2.1 Types de Tests et Couverture d'Automatisation

| Phase                 | Description                           | Automatisation            | Statut         |
| --------------------- | ------------------------------------- | ------------------------- | -------------- |
| Tests Fonctionnels    | Validation des parcours utilisateur   | Oui (Playwright + pytest) | Implemente     |
| Tests BDD             | Scénarios Gherkin en francais         | Oui (pytest-bdd)          | Implemente     |
| Tests de Regression   | Verification de non-regression        | Oui (Suite complete)      | Implemente     |
| Tests d'Accessibilite | Conformite WCAG 2.1                   | Oui (axe-core)            | Implemente     |
| Tests Unitaires       | Validation des composants individuels | Hors perimetre            | -              |
| Tests de Performance  | Charge et temps de reponse            | Prevus (Sprint 6)         | Non implemente |
| Tests de Securite     | Vulnerabilités OWASP                  | Prevus (Sprint futur)     | Non implemente |

### 2.2 Couverture par Types de Tests

On va utiliser une approche mêlant tests techniques et fonctionnels à cette étape du projet. Ces deux problématiques devraient idéalement être dissociées à long terme, on va procéder de cette manière car il est difficile d'avoir une bonne emprise sur ces problématiques au démarrage du projet :

1. **Tests Smoke** (`@pytest.mark.smoke`) : Vérification rapide des fonctionnalités critiques (~11 tests, ~1 min)
2. **Tests de Régression** (`@pytest.mark.regression`) : Suite complète après chaque modification (~30 tests, ~3 min)
3. **Tests Critiques** (`@pytest.mark.critical`) : Tests bloquants pour la mise en production (~8 tests)
4. **Tests BDD** : Scénarios Gherkin avec double couverture (fonctionnel + BDD), 14 scénarios
5. **Tests d'Accessibilité** (`@pytest.mark.accessibility`) : Conformite WCAG 2.1 via axe-core

À long terme, les catégories actuelles (smoke, regression, critical) seront progressivement remplacées par une classification reposant sur plusieurs dimensions indépendantes décrivant les propriétés des tests.

Une première dimension décrira le type de scénario testé (positif, négatif, cas limites).
Une seconde dimension permettra d’identifier le type de test (bout en bout, accessibilité, BDD, API, etc.).
Une troisième dimension reflétera la criticité métier des fonctionnalités testées (critique, important, normal).

Enfin, une dimension liée à la complexité ou au coût d’exécution des tests pourra également être introduite (rapide, moyen, lent). Cette distinction permettra d’optimiser l’exécution des suites dans une logique d’éco-conception, en adaptant le périmètre exécuté selon le contexte (Pull Request, CI rapide, exécution complète, etc.).

Cette approche permettra d’éviter les catégories trop larges comme « régression », qui deviennent ambiguës lorsque la suite de tests s’agrandit.

Cela organise un compromis satisfaisant pour démarrer sur les premiers sprints sans perdre de temps.

### 2.3 Couverture par Browser et Viewport

L'exécution couvre **9 configurations** en parallèle (3 browsers x 3 viewports).
Ces 9 configurations ont d'abord été organisées selon leur fréquence d'utilisation sur des applications similaires, dans l'ordre décroissant :

- chromium mobile
- wekbit mobile
- chromium desktop
- webkit desktop
- firefox desktop
- chromium tablet
- webkit tablet
- firefox mobile
- firefox tablet

Cet ordre nous permet, dans une approche d’éco-conception, de réduire les besoins en puissance de calcul en limitant le nombre de cas de tests exécutés sur les configurations les moins utilisées.

On va déterminer 4 niveaux de tests, dans l'ordre décroissant du nombre de cas de tests associés :

- tous les cas de tests
- regression + critical + smoke
- critical + smoke
- smoke

Ces différentes métriques nous ont ainsi permisent d'organiser le tableau suivant:

| Navigateur | Mobile (390x844)              | Desktop (1920x1080)           | Tablet (768x1024) |
| ---------- | ----------------------------- | ----------------------------- | ----------------- |
| Chromium   | tous                          | regression + critical + smoke | critical + smoke  |
| Firefox    | smoke                         | tous                          | smoke             |
| WebKit     | regression + critical + smoke | critical + smoke              | tous              |

On remarque que la distribution des niveaux ne suit pas exactement la fréquence d'utilisation.
En effet, la décision a été prise d’exécuter au moins une suite complète pour chaque technologie et chaque breakpoint/taille d’écran.
Cela permet à certains tests de bien remplir leur rôle (tel que les tests d'accessibilité) et de vérifier que les différents breakpoints et technologies n'apportent pas de problèmes fonctionnels.

---

## 3. Positionnement de l'Equipe d'Automatisation

### 3.1 Methodologie : Agile vs Cycle en V

#### Organisation retenue : Agile (sprints de 2 semaines)

| Critère                   | Agile                                 | Cycle en V                                 |
| ------------------------- | ------------------------------------- | ------------------------------------------ |
| **Périmètre**             | Évolutif, incrémental                 | Fixe, défini en début de projet            |
| **Intégration des tests** | Continue, integrée dans chaque sprint | Tardive, en phase de recette               |
| **Feedback**              | Rapide (à chaque sprint)              | Lent (découverte des bugs en fin de cycle) |
| **Maintenance scripts**   | Continue (évolutions fréquentes)      | Plus stable (périmètre fixé)               |
| **Collaboration**         | Dev + QA + PO ensemble                | Collaboration plus séquentielle            |

**Pourquoi l'Agile face au Cycle en V dans le contexte :**

- DigitalBank est une application en cours d’évolution dont les fonctionnalités sont amenées à changer
- Procéder par itération permet de s'adapter aux changements entre chaque sprint
- Cette approche facilite la construction progressive du système en validant les briques fonctionnelles au fur et à mesure
- Le V-Model repose sur des phases séquentielles peu adaptées aux changements fréquents
- Les tests étant réalisés en fin de cycle, la détection tardive des défauts augmente le coût de correction

**Avantages de l'Agile pour l'automatisation :**

- Feedback rapide et continu
- Détection précoce des régressions (shift-left natif)
- Automatisation progressive et priorisée (maintenabilité, stabilité)
- Couverture de tests alignée sur la valeur métier (risk-based testing)
- Adaptabilité aux changements de spécifications
- Collaboration forte entre QA, dev et produit

**Inconvenients de l'Agile pour l'automatisation :**

- Maintenance continue des scripts au rythme des évolutions
- Risque de dette technique si la suite de tests n’est pas régulièrement refactorisée
- Nécessite une forte discipline de tests (conventions, revues, standards)
- Instabilité des tests si les fonctionnalités ou interfaces évoluent trop rapidement

### 3.2 Shift Left

Le principe de **shift-left** consiste à déplacer les activités de test le plus tôt possible dans le cycle de vie du logiciel, plutôt que d'attendre la fin du développement, on veut le faire pendant le développement également.

**Mise en oeuvre dans ce projet :**

| Pratique                  | Implémentation                                                                 |
| ------------------------- | ------------------------------------------------------------------------------ | --------------------------- |
| BDD avant developpement   | Les scénarios Gherkin sont ecrits en amont, servant de specification vivante   |
| Tests smoke < 1 min       | Feedback ultra-rapide pour le developpeur                                      |
| Tests executés au commit  | GitHub Actions déclenche les smoke tests sur chaque push                       |
| Tests bloquants sur PR    | Les tests critiques doivent passer avant tout merge sur `main`                 | ! pas sur de la faisabilité |
| `data-testid` sur l'appli | Les développeurs intègrent les sélecteurs de test à la création des composants |

### 3.3 BDD - Behavior Driven Development

#### Introduction

Il a été décidé de rédiger les tests en **Gherkin français**, un formalisme BDD (Behavior Driven Development), pour maximiser la compréhension par toutes les parties prenantes (PO, DEV, QA) :

#### Exemple

Fichier : `tests/bdd/features/authentification/connexion.feature`

```gherkin
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
    When je me connecte avec <email> et <mot de passe>
    Then le dashboard est affiché
    And le nom d'utilisateur <nom utilisateur> est affiché

  @smoke @regression
  Scenario: ......
```

Explications :

- Feature : décrit clairement le domaine fonctionnel
- Background : évite la répétition de steps pour plusieurs scénarios
- Markers (@smoke, @critical, @authentification, ...) : permettent d’exécuter uniquement certains tests ou une suite de tests (marker associé à la feature)

**Concepts clés BDD :**

- Scénarios exécutables : les tests valident directement la spécification métier
- Lisible et compréhensible par toutes les parties prenantes
- Réutilisation des étapes commune pour simplifier la maintenance
- Intégrable facilement dans CI/CD grâce aux markers et filtres

**Workflow Haut Niveau :**

```txt
Scénario métier : défini en langage clair, compréhensible par tous
        ↓
Test automatisé : exécuté automatiquement par le framework BDD
        ↓
Exécution sur l’application : vérification réelle des fonctionnalités
        ↓
Rapport : visualisable par toutes parties prenantes pour un retour rapide (mieux que des logs techniques)
```

---

## 4. Environnements de Test

### 4.1 Architecture des Environnements

| Environnement | Usage                            | Données                       | Frequence d'exécution |
| ------------- | -------------------------------- | ----------------------------- | --------------------- |
| Docker        | Exécution CI/CD et locale        | Données synthétiques (SQLite) | A chaque push/PR      |
| DEV           | Développement local              | Données mockées (SQLite)      | A chaque commit       |
| INT           | Tests d'intégration              | Données synthétiques          | Quotidien             |
| UAT           | Tests fonctionnels et acceptance | Données anonymisées           | Par sprint            |
| PREPROD       | Validation pré-production        | Clone production              | Hebdomadaire          |

### 4.2 Configuration des Environnements

Á cette étape du projet, seul les environnements de développement et docker sont disponibles, l'application n'étant pas encore déployée sur aucun des environnements.

Il a donc été décidé de déployer l'application localement pour les tests, d'où l'environnement docker et local. Cette solution est temporaire, les cas de tests automatisés devraient normalement être exécutés sur l'environnement d'intégration et pas en local.

Fichier : `config/environments.yaml`

```yaml
environments:
  docker:
    base_url: "http://webapp/" # Conteneur nginx du docker compose
    timeout: 60

  dev:
    base_url: "http://localhost:8080/"
    timeout: 30

  int:
    base_url: "https://int.digitalbank.local"
    timeout: 45

  uat:
    base_url: "https://uat.digitalbank.local"
    timeout: 60

  preprod:
    base_url: "https://preprod.digitalbank.com"
    timeout: 60
```

Chaque environnement dispose de sa propre base SQLite (`test_data_{env}.db`) pour l'isolation des données.
Paramètre flexible via `--env` : `pytest tests/ --env=uat`

---

## 5. Framework d'Automatisation

### 5.1 Stack Technique

| Catégorie               | Outil                       | Version    | Justification                                                                                      |
| ----------------------- | --------------------------- | ---------- | -------------------------------------------------------------------------------------------------- |
| **Langage**             | python                      | 3.10       | Lisibilité, bibliothèques riches, courbe d'apprentissage faible                                    |
| **Framework Web**       | playwright                  | 1.42.0     | Multi-navigateur natif (Chromium/Firefox/WebKit), plus rapide que Selenium, moins de configuration |
| **Framework Test**      | pytest                      | 8.0        | Fixtures, paramétrisation, plugins, markers                                                        |
| **BDD**                 | pytest-bdd                  | 7.0        | Gherkin natif en français, intégration pytest                                                      |
| **Parallélisation**     | pytest-xdist                | 3.5        | Exécution en parallèle des tests                                                                   |
| **Relances des échecs** | pytest-rerunfailures        | 16.1       | Relances des tests en échec pour éviter les erreurs dues à l'instabilité de l'environnement        |
| **Reporting**           | pytest-html + allure-pytest | 4.1 / 2.13 | Rapport HTML autonome + données Allure pour dashboards                                             |
| **Tests Accessibilité** | axe-playwright-python       | latest     | Référence WCAG 2.1, intégration Playwright                                                         |
| **Gestion Données**     | Faker + SQLAlchemy + SQLite | 22.0 / 2.0 | Génération de données réalistes, ORM, isolation par environnement                                  |
| **CI/CD**               | GitHub Actions + Docker     | -          | Intégration native GitHub, containerisation reproductible                                          |
| **Containerisation**    | Docker Compose              | -          | Orchestration webapp (nginx) avec 9 conteneurs de test pour simple configuration et stabilité      |

### 5.2 Architecture du Framework

```txt
digitalbank-automation/
├── config/
│   ├── environments.yaml       # Configuration multi-environnement
│   └── test_config.yaml        # Configuration suites de tests
├── tests/
│   ├── functional/             # Tests fonctionnels traditionnels
│   │   ├── test_authentication.py    # 12 tests (login, 2FA, logout, reset, accessibilite)
│   │   └── test_security_settings.py # 11 tests (mot de passe, 2FA, notifications, accessibilite)
│   ├── bdd/                    # Tests BDD (Gherkin francais)
│   │   ├── features/
│   │   │   ├── authentification/     # connexion, deconnexion, 2FA (8 scénarios)
│   │   │   └── securite/            # changement mot de passe, gestion 2FA (6 scénarios)
│   │   └── step_définitions/        # Implementation des steps Python
│   ├── data/                   # Gestion des donnees de test
│   │   ├── test_users.json          # Donnees statiques de reference
│   │   ├── models.py                # Modeles SQLAlchemy (User, Account, Transaction...)
│   │   ├── factories.py             # Factories Faker (generation dynamique)
│   │   ├── database.py              # DatabaseManager (Singleton par env)
│   │   ├── data_manager.py          # Gestionnaire centralisé
│   │   ├── seed_data.py             # Scripts seed/cleanup/reset + CLI
│   │   └── db/                      # Bases SQLite par environnement
│   └── utils/                  # Page Object Model
│       ├── base_page.py             # BasePage Playwright (waits, click, accessibilite)
│       └── pages/
│           ├── login_page.py        # Page connexion + 2FA + reset
│           ├── dashboard_page.py    # Page tableau de bord
│           ├── security_page.py     # Page paramètres sécurité
│           ├── transfer_page.py     # Page virements (Page Object prêt, tests Sprint 4)
│           └── bills_page.py        # Page factures (Page Object prêt, tests Sprint 5)
├── reports/                    # Rapports générés
│   ├── report-{browser}-{viewport}.html  # Rapport pytest-html par config
│   └── allure-results/              # Données brutes Allure
├── docs/                       # Documentation
├── Dockerfile                  # Image Playwright Python (mcr.microsoft.com/playwright/python:v1.42.0)
├── requirements.txt            # Dépendances Python
└── conftest.py                 # Configuration pytest globale (fixtures, hooks, BDD)
```

### 5.3 Pattern de Conception

En plus du patron Flow-Model intégré par la méthode du Behavior-Driven Development, on va utiliser un autre modèle très utile :

- Le Page-Object Model (POM)

Cette méthode fournit une structure maintenable sans répétitions.

Techniquement, on a implémenté des pages de l'interface en script Python et toutes ces pages héritent de `BasePage` qui fournit :

- Attentes implicites Playwright (`locator.wait_for()`, `wait_for_function()`)
- Actions communes (`click`, `enter_text`, `get_text`)
- Vérification d'accessibilité via axe-core (`check_accessibility`)
- Capture de screenshots pour Allure (`_capture_screenshot`)
- Support `dispatch_event("click")` pour les éléments cachés par CSS

Les sélecteurs utilisent des attributs dédiés (`data-testid`) afin de garantir la stabilité des tests et de limiter leur dépendance à la structure du DOM.

---

## 6. Planification des Développements

### 6.1 Roadmap par Sprint

| Sprint   | Semaines | Livrables                                                       | Statut      |
| -------- | -------- | --------------------------------------------------------------- | ----------- |
| Sprint 1 | S1-S2    | Framework de base, Page Objects, tests authentification         | Terminé     |
| Sprint 2 | S3-S4    | Tests sécurité, BDD (Gherkin), gestion données                  | Terminé     |
| Sprint 3 | S5-S6    | Migration Playwright, Docker 9 conteneurs, CI/CD GitHub Actions | Terminé     |
| Sprint 4 | S7-S8    | Tests virements bancaires (Page Object pret)                    | Á planifier |
| Sprint 5 | S9-S10   | Tests paiement factures (Page Object pret)                      | Á planifier |
| Sprint 6 | S11-S12  | Tests performance, optimisation CI/CD                           | Á planifier |

### 6.2 Couverture Actuelle par Module

| Module / Feature                                       | Tests Fonctionnels | Tests BDD   | Priorité      | Statut           |
| ------------------------------------------------------ | ------------------ | ----------- | ------------- | ---------------- |
| Authentification (login, 2FA, logout, reset)           | 12 tests           | 8 scénarios | P1 - Critique | Implementé       |
| Paramètres Securité (mot de passe, 2FA, notifications) | 11 tests           | 6 scénarios | P2 - Haute    | Implementé       |
| Consultation Compte (solde, historique)                | -                  | -           | P1 - Critique | Page Object prêt |
| Virements Bancaires (internes, externes)               | -                  | -           | P1 - Critique | Page Object prêt |
| Paiement Factures                                      | -                  | -           | P2 - Haute    | Page Object prêt |

**Note** : Les Page Objects `transfer_page.py`, `bills_page.py` et `dashboard_page.py` sont déjà développés et prêts a recevoir des tests, permettant une montée en charge rapide lors des prochains sprints.

### 6.3 Repartition des Tests par Marker

| Marker                     | Nombre de tests | Usage                                                  |
| -------------------------- | --------------- | ------------------------------------------------------ |
| `@smoke`                   | ~11             | Vérification rapide, exécution à chaque push           |
| `@regression`              | ~30             | Suite complète, exécution quotidienne                  |
| `@critical`                | ~8              | Tests bloquants pour la mise en production             |
| `@accessibility` / `@wcag` | 2               | Conformité WCAG 2.1                                    |
| `@xfail`                   | 1               | Bug connu documenté (labels manquants sur les toggles) |

---

## 7. Critères d'Éligibilité à l'Automatisation

### 7.1 Matrice de Décision

Un scénario est éligible à l'automatisation s'il répond aux critères suivants :

| Critère                     | Poids | Seuil                                  |
| --------------------------- | ----- | -------------------------------------- |
| Fréquence d'exécution       | 30%   | >= 1 fois/sprint                       |
| Stabilité fonctionnelle     | 25%   | Pas de changement prévu sur 3 sprints  |
| Criticité metier            | 20%   | Bloquant ou majeur                     |
| Complexité d'automatisation | 15%   | Effort d’automatisation < 2 jours      |
| ROI                         | 10%   | Gain de temps > 50% après 5 exécutions |

En fonction du score final :

| Score final | Décision           |
| ----------- | ------------------ |
| ≥ 70%       | Automatiser        |
| 50–69%      | À analyser         |
| < 50%       | Ne pas automatiser |

### 7.2 Scénarios Prioritaires

**Automatisés (Sprint 1-3) :**

- Parcours de connexion/déconnexion (standard + 2FA)
- Réinitialisation de mot de passe
- Modification du mot de passe
- Activation/désactivation 2FA
- Gestion des notifications (email/SMS)
- Vérification accessibilité (WCAG 2.1)

**Á automatiser (Sprint 4-5) :**

- Consultation du solde et historique
- Virement simple entre comptes propres
- Virement vers bénéficiaire externe
- Paiement de factures

**Ne pas automatiser :**

- Tests exploratoires
- Scénarios à données sensibles réelles
- Fonctionnalités en cours de développement
- Tests visuels subjectifs (rendu graphique)

### 7.3 Checklist Avant Automatisation

- [ ] Le scénario manuel est documenté et valide
- [ ] Les données de test sont identifiées
- [ ] Les prérequis techniques sont disponibles (attributs `data-testid`)
- [ ] Les critères d'acceptation sont définis
- [ ] L'environnement de test est stable

---

## 8. Integration CI/CD

### 8.1 Pipeline GitHub Actions

Fichier : `.github/workflows/complete-automation-coverage.yml`

Le pipeline est compose de **2 jobs** :

| Job                 | Description                                                                                            | Dependance | Timeout |
| ------------------- | ------------------------------------------------------------------------------------------------------ | ---------- | ------- |
| **tests**           | Build des 9 images Docker en parallèle, puis exécution sequentielle des 9 conteneurs de test           | -          | 10 min  |
| **publish-results** | Post un commentaire automatique sur les PR/commits avec tableau de synthese et lien vers les artifacts | tests      | -       |

### 8.2 Declencheurs

| Evenement                    | Action                                                |
| ---------------------------- | ----------------------------------------------------- |
| Push sur `main` ou `develop` | Exécution automatique                                 |
| Pull Request vers `main`     | Exécution automatique (bloquant) + commentaire resume |
| Cron `0 23 * * 0-4`          | Exécution quotidienne a 00h00 Paris (lundi-vendredi)  |
| Manuel (`workflow_dispatch`) | Exécution a la demande depuis l'interface GitHub      |

### 8.3 Exécution Docker

```bash
# Exécution complete (9 configurations navigateur x viewport)
docker-compose up --build

# Exécution en arriere-plan
docker-compose up --build -d
docker-compose logs -f tests-chromium-desktop

# Exécution d'une configuration specifique
docker-compose run --rm tests-chromium-desktop
docker-compose run --rm tests-firefox-mobile
docker-compose run --rm tests-webkit-tablet

# Arret
docker-compose down
```

Services disponibles : `tests-chromium-mobile`, `tests-chromium-tablet`, `tests-chromium-desktop`, `tests-webkit-mobile`, `tests-webkit-tablet`, `tests-webkit-desktop`, `tests-firefox-mobile`, `tests-firefox-tablet`, `tests-firefox-desktop`

### 8.4 Rapports et Visibilite

| Type             | Emplacement                                | Description                                     |
| ---------------- | ------------------------------------------ | ----------------------------------------------- |
| pytest-html      | `reports/report-{browser}-{viewport}.html` | Rapport HTML autonome par configuration         |
| Allure           | `reports/allure-results/`                  | Donnees brutes JSON pour generation Allure      |
| Screenshots      | `reports/screenshots/`                     | Captures automatiques uniquement en cas d'echec |
| GitHub Artifacts | Actions > Artifacts                        | Rapports compresses - retention 30 jours        |
| Commentaire PR   | Pull Request                               | Resume automatique des resultats sur chaque PR  |

---

## 9. Systeme de Gestion des Donnees

### 9.1 Architecture 3 Niveaux

| Niveau         | Source                                | Usage                                                                                      |
| -------------- | ------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Statique**   | `test_users.json`                     | Donnees de reference (users, accounts, beneficiaires, factures) - reutilisables a l'infini |
| **Dynamique**  | Factories Faker (`factories.py`)      | Generation de donnees realistes a la volee (noms, emails, IBAN francais)                   |
| **Persistant** | SQLite via SQLAlchemy (`database.py`) | Base de donnees dediee par environnement, reconfigurable                                   |

### 9.2 Modeles de Donnees (ORM)

5 modeles SQLAlchemy avec relations :

- `User` (email, password, name, has_2fa, totp_code)
- `Account` (user_id, type, number/IBAN, balance)
- `Transaction` (account_id, type credit/debit, amount, description)
- `Beneficiary` (user_id, name, iban)
- `Bill` (provider, reference, amount, due_date, paid)

### 9.3 Scripts Pre/Post-Exécution

```bash
# CLI disponible via seed_data.py
python -m tests.data.seed_data seed --env=dev -v       # Initialiser les donnees
python -m tests.data.seed_data cleanup --env=dev -v     # Nettoyer les donnees
python -m tests.data.seed_data reset --env=dev -v       # Reinitialiser (cleanup + seed)
python -m tests.data.seed_data random --env=dev -c 20 -v  # Generer 20 jeux aleatoires
```

Hooks pytest integres dans `conftest.py` :

- Fixtures de setup : preparation des donnees avant exécution
- `pytest_sessionfinish` : fermeture des connexions en fin de session

### 9.4 Isolation Multi-Environnement

- Singleton `DatabaseManager` par environnement
- Base SQLite separee : `tests/data/db/test_data_{env}.db`
- Parametrable via `--env` : `pytest tests/ --env=uat`
- Variables d'environnement supportees (`${DB_USER}`, `${DB_PASSWORD}`)

---

## 10. Gestion de Version

### 10.1 Outil de Versioning

Le code source est versionne avec **Git** et heberge sur **GitHub** :

- Branche `main` : code stable, protegee (merge via PR uniquement)
- Branche `develop` : integration continue
- Branches sprint : `sprint-1`, `sprint-2`, `sprint-3` (une branche par sprint)

### 10.2 Versions et Releases

Les tags Git sont crees a la fin de chaque sprint et associes aux releases projet :

| Tag    | Sprint              | Contenu                                            |
| ------ | ------------------- | -------------------------------------------------- |
| `v1.0` | Sprint 1            | Framework de base + tests authentification         |
| `v2.0` | Sprint 2            | Tests securite + BDD + gestion donnees             |
| `v3.0` | Sprint 3            | Migration Playwright + Docker 9 conteneurs + CI/CD |
| `v4.0` | Sprint 4 (planifie) | Tests virements                                    |
| `v5.0` | Sprint 5 (planifie) | Tests factures                                     |

```bash
# Creer un tag de release
git tag -a v3.0 -m "Sprint 3 : Migration Playwright, Docker 9 conteneurs, CI/CD"
git push origin v3.0
```

### 10.3 Processus de Retour Arriere

En cas de version defaillante, le processus de rollback est le suivant :

1. **Identification** : les tests CI/CD echouent sur `main` → alerte automatique GitHub
2. **Isolation** : identifier le commit/tag de derniere version stable
3. **Retour arriere** :

   ```bash
   # Option 1 : revert du commit defaillant (preserve l'historique)
   git revert <commit-hash>
   git push origin main

   # Option 2 : retour au tag stable (pour une regression multi-commits)
   git checkout v2.0
   git checkout -b hotfix/rollback-v2
   git push origin hotfix/rollback-v2
   # Puis creer une PR vers main
   ```

4. **Validation** : les tests smoke doivent repasser avant remise en production
5. **Docker** : chaque image est taggee (`v3.0`) → relancer l'image stable si necessaire

---

## 11. Conformite et Normes

### 11.1 RGPD

- Aucune donnee personnelle reelle dans les tests
- Donnees synthetiques generees par Faker (locale `fr_FR`)
- Base SQLite locale, pas de transmission de donnees
- Logs de test sans informations sensibles

### 11.2 WCAG 2.1 (Accessibilite)

- Tests automatises via axe-core sur chaque page testee
- Verification des niveaux A et AA
- Bug connu documente : labels manquants sur les toggles (`@xfail`)
- Violations reportees en JSON dans les rapports Allure

### 11.3 Eco-Conception

**Dans les scripts de test :**

- Mode headless par defaut (pas de rendu graphique = moins de CPU/RAM)
- Screenshots uniquement en cas d'echec (pas systematique)
- `wait_until="domcontentloaded"` : navigation plus rapide, moins de requetes inutiles attendues
- Selecteurs `data-testid` stables : moins de reruns dus a des locators fragiles

**Dans l'infrastructure :**

- Exécution parallelisee (`-n auto`) : reduit le temps machine total
- 9 conteneurs en parallèle : meme couverture en moins de temps qu'une exécution sequentielle
- Rapports `--self-contained-html` : un seul fichier, pas d'assets supplementaires
- Nettoyage des donnees en post-exécution via `pytest_sessionfinish`
- Arret automatique des conteneurs après exécution (`docker-compose up` + exit code)

---

## 12. Indicateurs de Suivi

### 12.1 KPIs Automatisation

| Indicateur                                     | Cible         | Actuel                                             |
| ---------------------------------------------- | ------------- | -------------------------------------------------- |
| Couverture automatisee (modules critiques)     | > 70%         | ~40% (2/5 modules implementes)                     |
| Taux de reussite                               | > 95%         | ~97% (40 passed, 1 xpassed, 1 error intermittente) |
| Temps d'exécution suite complete (1 conteneur) | < 10 minutes  | ~6 minutes                                         |
| Faux positifs (reruns reussis)                 | < 5%          | < 5%                                               |
| Couverture navigateurs                         | 3 navigateurs | Chromium + Firefox + WebKit                        |
| Couverture viewports                           | 3 viewports   | Mobile + Tablet + Desktop                          |

### 12.2 Dashboard de Suivi

Les resultats sont visibles via :

- **GitHub Actions** : Statut pass/fail a chaque push/PR (badge de statut)
- **Commentaire automatique sur PR** : tableau de synthese des 9 configurations
- **pytest-html** : Rapport HTML detaille par configuration (`reports/report-{browser}-{viewport}.html`)
- **GitHub Artifacts** : Rapports telechargeable pendant 30 jours
- **Allure** : Donnees brutes pour generation de dashboards enrichis

---

## 13. Gouvernance

### 13.1 Roles et Responsabilites

| Role                | Responsabilite                                   |
| ------------------- | ------------------------------------------------ |
| Test Lead           | Stratégie, priorisation, reporting               |
| Automation Engineer | Developpement et maintenance scripts             |
| Developpeur         | Revue code, testabilite, attributs `data-testid` |
| Product Owner       | Validation critères acceptance                   |

### 13.2 Processus de Revue

1. Tout nouveau script passe par une **Pull Request**
2. Revue obligatoire par un pair (convention POM, docstrings, markers)
3. Tests de validation sur environnement Docker local
4. Merge sur `main` après approbation + tests CI passes

---

## 14. Annexes

### 14.1 Glossaire

- **CI/CD** : Continuous Integration / Continuous Deployment
- **WCAG** : Web Content Accessibility Guidelines
- **RGPD** : Reglement General sur la Protection des Donnees
- **2FA** : Two-Factor Authentication
- **POM** : Page Object Model
- **BDD** : Behavior-Driven Development
- **ROI** : Return On Investment
- **SPA** : Single Page Application
- **Shift Left** : Pratique consistant a tester plus tot dans le cycle de developpement
- **Headless** : Exécution du navigateur sans interface graphique

### 14.2 References

- [Documentation Playwright Python](https://playwright.dev/python/docs/intro)
- [Guide pytest](https://docs.pytest.org/)
- [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core](https://www.deque.com/axe/)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitHub Actions](https://docs.github.com/en/actions)
