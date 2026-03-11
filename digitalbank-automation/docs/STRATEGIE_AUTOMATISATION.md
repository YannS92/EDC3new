# Strategie d'Automatisation des Tests - DigitalBank

## 1. Introduction

Ce document definit la strategie d'automatisation des tests pour l'application bancaire DigitalBank. L'objectif est d'ameliorer la qualite du produit et de reduire le temps de livraison en automatisant les tests critiques dans le cadre d'une methodologie **Agile** avec des sprints de deux semaines.

---

## 2. Perimetre de l'Automatisation

### 2.1 Phases de Tests Concernees

| Phase                 | Description                           | Automatisation            | Statut         |
| --------------------- | ------------------------------------- | ------------------------- | -------------- |
| Tests Fonctionnels    | Validation des parcours utilisateur   | Oui (Playwright + pytest) | Implemente     |
| Tests BDD             | Scenarios Gherkin en francais         | Oui (pytest-bdd)          | Implemente     |
| Tests de Regression   | Verification de non-regression        | Oui (Suite complete)      | Implemente     |
| Tests d'Accessibilite | Conformite WCAG 2.1                   | Oui (axe-core)            | Implemente     |
| Tests Unitaires       | Validation des composants individuels | Hors perimetre            | -              |
| Tests de Performance  | Charge et temps de reponse            | Prevus (Sprint 6)         | Non implemente |
| Tests de Securite     | Vulnerabilites OWASP                  | Prevus (Sprint futur)     | Non implemente |

### 2.2 Types de Tests Automatises

1. **Tests Smoke** (`@pytest.mark.smoke`) : Verification rapide des fonctionnalites critiques (~11 tests, ~1 min)
2. **Tests de Regression** (`@pytest.mark.regression`) : Suite complete apres chaque modification (~30 tests, ~3 min)
3. **Tests Critiques** (`@pytest.mark.critical`) : Tests bloquants pour la mise en production (~8 tests)
4. **Tests BDD** : Scenarios Gherkin avec double couverture (fonctionnel + BDD), 14 scenarios
5. **Tests d'Accessibilite** (`@pytest.mark.accessibility`) : Conformite WCAG 2.1 via axe-core

### 2.3 Couverture par Browser et Viewport

L'execution couvre **9 configurations** en parallele (3 navigateurs x 3 viewports).
Ces 9 configurations ont d'abord été ogranisées en fréquence d'utilisation sur applications similaire, dans l'ordre décroissant d'utilisation :

- chromium mobile
- wekbit mobile
- chromium desktop
- webkit desktop
- firefox desktop
- chromium tablet
- webkit tablet
- firefox mobile
- firefox tablet

Cet ordre va nous permettre, dans une approche d'éco-conception, de diminuer les besoins en puissance de calcul en diminuant le nombre de cas de tests exécutés par les configurations les moins utilisées.

On va déterminer 4 niveaux de tests qui vont à cette étape du projet utiliser un mélange de tags technico-fonctionnel, deux problématiques idéalement dissociées au long terme mais suffisant à cette étape du projet, dans l'ordre décroissant du nombre de cas de tests associés :

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

On remarque que la distribution des niveaux ne suit pas exactement la fréquence d'utilisation, la décision a été prise de faire au moins une exécution complète dans chaque technologie et chaque breakpoint/taille d'écran, ce qui permet notamment à certain tests spécifiques commes les tests d'acessibilité de bien remplir leur rôle.

---

## 3. Positionnement de l'Equipe d'Automatisation

### 3.1 Methodologie : Agile vs Cycle en V

#### Organisation retenue : Agile (sprints de 2 semaines)

| Critere                   | Agile                                 | Cycle en V                                 |
| ------------------------- | ------------------------------------- | ------------------------------------------ |
| **Perimetre**             | Evolutif, incrementiel                | Fixe, defini en debut de projet            |
| **Integration des tests** | Continue, integree dans chaque sprint | Tardive, en phase de recette               |
| **Feedback**              | Rapide (a chaque sprint)              | Lent (decouverte des bugs en fin de cycle) |
| **Maintenance scripts**   | Constante (evolutions frequentes)     | Allégée (perimetre stable)                 |
| **Collaboration**         | Dev + QA + PO ensemble                | Cloisonnement par phase                    |

**Avantages de l'Agile pour l'automatisation :**

- Feedback immediat sur chaque feature developpee
- Automatisation progressive et alignee sur les livraisons
- Identification precoce des regressions (shift left natif)
- Adaptabilite rapide aux changements de specifications

**Inconvenients de l'Agile pour l'automatisation :**

- Maintenance continue des scripts au rythme des evolutions
- Risque de dette technique si les scripts ne sont pas refactores
- Necessite une bonne discipline de tests (conventions, review)

**Pourquoi pas le Cycle en V :**

- DigitalBank est une application evoluant par sprints
- Les tests tardifs du Cycle en V augmentent le cout des corrections
- L'approche Agile permet de valider chaque increment avant integration

### 3.2 Shift Left

Le principe de **shift left** consiste a avancer les activites de test le plus tot possible dans le cycle de developpement, plutot que d'attendre la fin du developpement.

**Mise en oeuvre dans ce projet :**

| Pratique                  | Implementation                                                                 |
| ------------------------- | ------------------------------------------------------------------------------ |
| Tests executes au commit  | GitHub Actions declenche les smoke tests sur chaque push                       |
| Tests bloquants sur PR    | Les tests critiques doivent passer avant tout merge sur `main`                 |
| BDD avant developpement   | Les scenarios Gherkin sont ecrits en amont, servant de specification vivante   |
| Tests smoke < 1 min       | Feedback ultra-rapide pour le developpeur                                      |
| `data-testid` sur l'appli | Les developpeurs integrent les selecteurs de test a la creation des composants |

### 3.3 BDD - Behavior Driven Development

Les tests BDD sont rediges en **Gherkin francais** pour maximiser la comprehension par toutes les parties prenantes (PO, dev, QA) :

```gherkin
# Exemple : tests/bdd/features/authentification/connexion.feature
Scenario: Connexion reussie avec identifiants valides
  Given je suis sur la page de connexion
  When je me connecte avec des identifiants valides
  Then le dashboard est affiche
```

**Benefices :**

- Specification executable (les scenarios servent a la fois de specs et de tests)
- Comprehensible par des non-techniciens
- Double couverture : chaque scenario BDD est complement des tests fonctionnels classiques

---

## 4. Environnements de Test

### 4.1 Architecture des Environnements

| Environnement | Usage                            | Donnees                       | Frequence d'execution |
| ------------- | -------------------------------- | ----------------------------- | --------------------- |
| Docker        | Execution CI/CD et locale        | Donnees synthetiques (SQLite) | A chaque push/PR      |
| DEV           | Developpement local              | Donnees mockees (SQLite)      | A chaque commit       |
| INT           | Tests d'integration              | Donnees synthetiques          | Quotidien             |
| UAT           | Tests fonctionnels et acceptance | Donnees anonymisees           | Par sprint            |
| PREPROD       | Validation pre-production        | Clone production              | Hebdomadaire          |

### 4.2 Configuration des Environnements

Fichier : `config/environments.yaml`

```yaml
environments:
  docker:
    base_url: "http://webapp/" # Conteneur nginx interne
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

Chaque environnement dispose de sa propre base SQLite (`test_data_{env}.db`) pour l'isolation des donnees.
Parametrable via `--env` : `pytest tests/ --env=uat`

---

## 5. Outils d'Automatisation

### 5.1 Stack Technique Retenue

| Categorie               | Outil                       | Version    | Justification                                                                                          |
| ----------------------- | --------------------------- | ---------- | ------------------------------------------------------------------------------------------------------ |
| **Framework Web**       | Playwright                  | 1.42.0     | Multi-navigateur natif (Chromium/Firefox/WebKit), plus rapide que Selenium, headless Linux sans config |
| **Langage**             | Python                      | 3.10       | Lisibilite, bibliotheques riches, courbe d'apprentissage faible                                        |
| **Framework Test**      | pytest                      | 8.0        | Fixtures, parametrization, plugins, markers                                                            |
| **BDD**                 | pytest-bdd                  | 7.0        | Gherkin natif en francais, integration pytest                                                          |
| **Tests Accessibilite** | axe-playwright-python       | latest     | Reference WCAG 2.1, integration Playwright                                                             |
| **Reporting**           | pytest-html + Allure        | 4.1 / 2.13 | Rapport HTML autonome + donnees Allure pour dashboards                                                 |
| **CI/CD**               | GitHub Actions + Docker     | -          | Integration native GitHub, containerisation reproductible                                              |
| **Gestion Donnees**     | Faker + SQLAlchemy + SQLite | 22.0 / 2.0 | Generation donnees realistes, ORM, isolation par env                                                   |
| **Containerisation**    | Docker Compose              | -          | Orchestration webapp (nginx) + 9 conteneurs de test                                                    |
| **Parallélisation**     | pytest-xdist                | 3.5        | Execution en parallele des tests au sein d'un conteneur                                                |

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
│   │   │   ├── authentification/     # connexion, deconnexion, 2FA (8 scenarios)
│   │   │   └── securite/            # changement mot de passe, gestion 2FA (6 scenarios)
│   │   └── step_definitions/        # Implementation des steps Python
│   ├── data/                   # Gestion des donnees de test
│   │   ├── test_users.json          # Donnees statiques de reference
│   │   ├── models.py                # Modeles SQLAlchemy (User, Account, Transaction...)
│   │   ├── factories.py             # Factories Faker (generation dynamique)
│   │   ├── database.py              # DatabaseManager (Singleton par env)
│   │   ├── data_manager.py          # Gestionnaire centralise
│   │   ├── seed_data.py             # Scripts seed/cleanup/reset + CLI
│   │   └── db/                      # Bases SQLite par environnement
│   └── utils/                  # Page Object Model
│       ├── base_page.py             # BasePage Playwright (waits, click, accessibilite)
│       └── pages/
│           ├── login_page.py        # Page connexion + 2FA + reset
│           ├── dashboard_page.py    # Page tableau de bord
│           ├── security_page.py     # Page parametres securite
│           ├── transfer_page.py     # Page virements (Page Object pret, tests Sprint 4)
│           └── bills_page.py        # Page factures (Page Object pret, tests Sprint 5)
├── reports/                    # Rapports generes
│   ├── report-{browser}-{viewport}.html  # Rapport pytest-html par config
│   └── allure-results/              # Donnees brutes Allure
├── docs/                       # Documentation
├── Dockerfile                  # Image Playwright Python (mcr.microsoft.com/playwright/python:v1.42.0)
├── requirements.txt            # Dependances Python
└── conftest.py                 # Configuration pytest globale (fixtures, hooks, BDD)
```

### 5.3 Pattern Page Object Model (POM)

Toutes les pages heritent de `BasePage` qui fournit :

- Attentes implicites Playwright (`locator.wait_for()`, `wait_for_function()`)
- Actions communes (`click`, `enter_text`, `get_text`)
- Verification d'accessibilite via axe-core (`check_accessibility`)
- Capture de screenshots pour Allure (`_capture_screenshot`)
- Support `dispatch_event("click")` pour les elements caches par CSS

Les locators utilisent des selecteurs CSS avec attributs `data-testid` pour la stabilite, decouples du DOM.

---

## 6. Planification des Developpements

### 6.1 Roadmap par Sprint

| Sprint   | Semaines | Livrables                                                       | Statut      |
| -------- | -------- | --------------------------------------------------------------- | ----------- |
| Sprint 1 | S1-S2    | Framework de base, Page Objects, tests authentification         | Termine     |
| Sprint 2 | S3-S4    | Tests securite, BDD (Gherkin), gestion donnees                  | Termine     |
| Sprint 3 | S5-S6    | Migration Playwright, Docker 9 conteneurs, CI/CD GitHub Actions | Termine     |
| Sprint 4 | S7-S8    | Tests virements bancaires (Page Object pret)                    | A planifier |
| Sprint 5 | S9-S10   | Tests paiement factures (Page Object pret)                      | A planifier |
| Sprint 6 | S11-S12  | Tests performance, optimisation CI/CD                           | A planifier |

### 6.2 Couverture Actuelle par Module

| Module                                                 | Tests Fonctionnels | Tests BDD   | Priorite      | Statut           |
| ------------------------------------------------------ | ------------------ | ----------- | ------------- | ---------------- |
| Authentification (login, 2FA, logout, reset)           | 12 tests           | 8 scenarios | P1 - Critique | Implemente       |
| Parametres Securite (mot de passe, 2FA, notifications) | 11 tests           | 6 scenarios | P2 - Haute    | Implemente       |
| Consultation Compte (solde, historique)                | -                  | -           | P1 - Critique | Page Object pret |
| Virements Bancaires (internes, externes)               | -                  | -           | P1 - Critique | Page Object pret |
| Paiement Factures                                      | -                  | -           | P2 - Haute    | Page Object pret |

**Note** : Les Page Objects `transfer_page.py`, `bills_page.py` et `dashboard_page.py` sont deja developpes et prets a recevoir des tests, permettant une montee en charge rapide lors des prochains sprints.

### 6.3 Repartition des Tests par Marker

| Marker                     | Nombre de tests | Usage                                                  |
| -------------------------- | --------------- | ------------------------------------------------------ |
| `@smoke`                   | ~11             | Verification rapide, execution a chaque push           |
| `@regression`              | ~30             | Suite complete, execution quotidienne                  |
| `@critical`                | ~8              | Tests bloquants pour la mise en production             |
| `@accessibility` / `@wcag` | 2               | Conformite WCAG 2.1                                    |
| `@xfail`                   | 1               | Bug connu documente (labels manquants sur les toggles) |

---

## 7. Criteres d'Eligibilite a l'Automatisation

### 7.1 Matrice de Decision

Un scenario est eligible a l'automatisation s'il repond aux critères suivants :

| Critere                     | Poids | Seuil                                 |
| --------------------------- | ----- | ------------------------------------- |
| Frequence d'execution       | 30%   | >= 1 fois/sprint                      |
| Stabilite fonctionnelle     | 25%   | Pas de changement prevu sur 3 sprints |
| Criticite metier            | 20%   | Bloquant ou majeur                    |
| Complexite d'automatisation | 15%   | Effort < 2 jours                      |
| ROI                         | 10%   | Gain temps > 50% apres 5 executions   |

### 7.2 Scenarios Prioritaires

**Automatises (Sprint 1-3) :**

- Parcours de connexion/deconnexion (standard + 2FA)
- Reinitialisation de mot de passe
- Modification du mot de passe
- Activation/desactivation 2FA
- Gestion des notifications (email/SMS)
- Verification accessibilite (WCAG 2.1)

**A automatiser (Sprint 4-5) :**

- Consultation du solde et historique
- Virement simple entre comptes propres
- Virement vers beneficiaire externe
- Paiement de factures

**Ne pas automatiser :**

- Tests exploratoires
- Scenarios a donnees sensibles reelles
- Fonctionnalites en cours de developpement
- Tests visuels subjectifs (rendu graphique)

### 7.3 Checklist Avant Automatisation

- [ ] Le scenario manuel est documente et valide
- [ ] Les donnees de test sont identifiees
- [ ] Les prerequis techniques sont disponibles (attributs `data-testid`)
- [ ] Les criteres d'acceptance sont definis
- [ ] L'environnement de test est stable

---

## 8. Integration CI/CD

### 8.1 Pipeline GitHub Actions

Fichier : `.github/workflows/complete-automation-coverage.yml`

Le pipeline est compose de **2 jobs** :

| Job                 | Description                                                                                            | Dependance | Timeout |
| ------------------- | ------------------------------------------------------------------------------------------------------ | ---------- | ------- |
| **tests**           | Build des 9 images Docker en parallele, puis execution sequentielle des 9 conteneurs de test           | -          | 10 min  |
| **publish-results** | Post un commentaire automatique sur les PR/commits avec tableau de synthese et lien vers les artifacts | tests      | -       |

### 8.2 Declencheurs

| Evenement                    | Action                                                |
| ---------------------------- | ----------------------------------------------------- |
| Push sur `main` ou `develop` | Execution automatique                                 |
| Pull Request vers `main`     | Execution automatique (bloquant) + commentaire resume |
| Cron `0 23 * * 0-4`          | Execution quotidienne a 00h00 Paris (lundi-vendredi)  |
| Manuel (`workflow_dispatch`) | Execution a la demande depuis l'interface GitHub      |

### 8.3 Execution Docker

```bash
# Execution complete (9 configurations navigateur x viewport)
docker-compose up --build

# Execution en arriere-plan
docker-compose up --build -d
docker-compose logs -f tests-chromium-desktop

# Execution d'une configuration specifique
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

### 9.3 Scripts Pre/Post-Execution

```bash
# CLI disponible via seed_data.py
python -m tests.data.seed_data seed --env=dev -v       # Initialiser les donnees
python -m tests.data.seed_data cleanup --env=dev -v     # Nettoyer les donnees
python -m tests.data.seed_data reset --env=dev -v       # Reinitialiser (cleanup + seed)
python -m tests.data.seed_data random --env=dev -c 20 -v  # Generer 20 jeux aleatoires
```

Hooks pytest integres dans `conftest.py` :

- Fixtures de setup : preparation des donnees avant execution
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

- Execution parallelisee (`-n auto`) : reduit le temps machine total
- 9 conteneurs en parallele : meme couverture en moins de temps qu'une execution sequentielle
- Rapports `--self-contained-html` : un seul fichier, pas d'assets supplementaires
- Nettoyage des donnees en post-execution via `pytest_sessionfinish`
- Arret automatique des conteneurs apres execution (`docker-compose up` + exit code)

---

## 12. Indicateurs de Suivi

### 12.1 KPIs Automatisation

| Indicateur                                     | Cible         | Actuel                                             |
| ---------------------------------------------- | ------------- | -------------------------------------------------- |
| Couverture automatisee (modules critiques)     | > 70%         | ~40% (2/5 modules implementes)                     |
| Taux de reussite                               | > 95%         | ~97% (40 passed, 1 xpassed, 1 error intermittente) |
| Temps d'execution suite complete (1 conteneur) | < 10 minutes  | ~6 minutes                                         |
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
| Test Lead           | Strategie, priorisation, reporting               |
| Automation Engineer | Developpement et maintenance scripts             |
| Developpeur         | Revue code, testabilite, attributs `data-testid` |
| Product Owner       | Validation criteres acceptance                   |

### 13.2 Processus de Revue

1. Tout nouveau script passe par une **Pull Request**
2. Revue obligatoire par un pair (convention POM, docstrings, markers)
3. Tests de validation sur environnement Docker local
4. Merge sur `main` apres approbation + tests CI passes

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
- **Headless** : Execution du navigateur sans interface graphique

### 14.2 References

- [Documentation Playwright Python](https://playwright.dev/python/docs/intro)
- [Guide pytest](https://docs.pytest.org/)
- [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core](https://www.deque.com/axe/)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitHub Actions](https://docs.github.com/en/actions)
