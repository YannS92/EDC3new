# Strategie d'Automatisation des Tests - DigitalBank

## 1. Introduction

Ce document definit la strategie d'automatisation des tests pour l'application bancaire DigitalBank. L'objectif est d'ameliorer la qualite du produit et de reduire le temps de livraison en automatisant les tests critiques dans le cadre d'une methodologie Agile avec des sprints de deux semaines.

---

## 2. Perimetre de l'Automatisation

### 2.1 Phases de Tests Concernees

| Phase | Description | Automatisation | Statut |
|-------|-------------|----------------|--------|
| Tests Fonctionnels | Validation des parcours utilisateur | Oui (Selenium) | Implemente |
| Tests BDD | Scenarios Gherkin en francais | Oui (pytest-bdd) | Implemente |
| Tests de Regression | Verification de non-regression | Oui (Suite complete) | Implemente |
| Tests d'Accessibilite | Conformite WCAG 2.1 | Oui (axe-core) | Implemente |
| Tests Unitaires | Validation des composants individuels | Hors perimetre | - |
| Tests de Performance | Charge et temps de reponse | Prevus (Sprint futur) | Non implemente |
| Tests de Securite | Vulnerabilites OWASP | Prevus (Sprint futur) | Non implemente |

### 2.2 Types de Tests Automatises

1. **Tests Smoke** (`@pytest.mark.smoke`) : Verification rapide des fonctionnalites critiques (~11 tests, ~1 min)
2. **Tests de Regression** (`@pytest.mark.regression`) : Suite complete apres chaque modification (~42 tests, ~3 min)
3. **Tests BDD** : Scenarios Gherkin avec double couverture (fonctionnel + BDD)
4. **Tests d'Accessibilite** (`@pytest.mark.accessibility`) : Conformite WCAG 2.1 via axe-core

---

## 3. Environnements de Test

### 3.1 Architecture des Environnements

| Environnement | Usage | Donnees | Frequence d'execution |
|---------------|-------|---------|----------------------|
| Docker | Execution CI/CD et locale | Donnees synthetiques (SQLite) | A chaque push/PR |
| DEV | Developpement local | Donnees mockees (SQLite) | A chaque commit |
| INT | Tests d'integration | Donnees synthetiques | Quotidien |
| UAT | Tests fonctionnels et acceptance | Donnees anonymisees | Par sprint |
| PREPROD | Validation pre-production | Clone production | Hebdomadaire |

### 3.2 Configuration des Environnements

Fichier : `config/environments.yaml`

```yaml
environments:
  docker:
    base_url: "http://webapp/"             # Conteneur nginx
    timeout: 60

  dev:
    base_url: "http://127.0.0.1:5500/digitalbank/"
    timeout: 30

  int:
    base_url: "https://int.digitalbank.local"
    api_url: "https://api-int.digitalbank.local"
    database: "digitalbank_int"

  uat:
    base_url: "https://uat.digitalbank.local"
    api_url: "https://api-uat.digitalbank.local"
    database: "digitalbank_uat"

  preprod:
    base_url: "https://preprod.digitalbank.com"
    api_url: "https://api-preprod.digitalbank.com"
    database: "digitalbank_preprod"
```

Chaque environnement dispose de sa propre base SQLite (`test_data_{env}.db`) pour l'isolation des donnees.

---

## 4. Outils d'Automatisation

### 4.1 Stack Technique Retenue

| Categorie | Outil | Justification |
|-----------|-------|---------------|
| **Framework Web** | Selenium 4.16 | Standard industrie, large communaute |
| **Framework Mobile** | Appium 3.1 | Multi-plateforme (iOS/Android), configure mais non utilise dans cette phase |
| **Langage** | Python 3.11 | Lisibilite, bibliotheques riches, courbe d'apprentissage faible |
| **Framework Test** | pytest 8.0 | Fixtures, parametrization, plugins, markers |
| **BDD** | pytest-bdd 7.0 | Gherkin natif en francais, integration pytest |
| **Tests Accessibilite** | axe-core (axe-selenium-python) | Reference WCAG 2.1, integration Selenium |
| **Reporting** | pytest-html + Allure | Rapport HTML autonome + donnees Allure |
| **CI/CD** | GitHub Actions + Docker | Integration native GitHub, containerisation |
| **Gestion Donnees** | Faker + SQLAlchemy + SQLite | Generation donnees realistes, ORM, isolation par env |
| **Containerisation** | Docker Compose | Orchestration webapp (nginx) + tests (Python/Chrome) |

### 4.2 Architecture du Framework

```
digitalbank-automation/
├── config/
│   ├── environments.yaml       # Configuration multi-environnement
│   └── test_config.yaml        # Configuration suites de tests
├── tests/
│   ├── functional/             # Tests fonctionnels traditionnels
│   │   ├── test_authentication.py    # 12 tests (login, 2FA, logout, reset, accessibilite)
│   │   └── test_security_settings.py # 11 tests (mot de passe, 2FA, notifications, accessibilite)
│   ├── bdd/                    # Tests BDD (Gherkin)
│   │   ├── features/
│   │   │   ├── authentification/     # connexion, deconnexion, 2FA
│   │   │   └── securite/            # changement mot de passe, gestion 2FA
│   │   └── step_definitions/        # Implementation des steps
│   ├── data/                   # Gestion des donnees
│   │   ├── test_users.json          # Donnees statiques
│   │   ├── models.py                # Modeles SQLAlchemy (User, Account, Transaction, etc.)
│   │   ├── factories.py             # Factories Faker (generation dynamique)
│   │   ├── database.py              # DatabaseManager (Singleton par env)
│   │   ├── data_manager.py          # Gestionnaire centralise
│   │   ├── seed_data.py             # Scripts seed/cleanup/reset + CLI
│   │   └── db/                      # Bases SQLite par environnement
│   └── utils/                  # Page Object Model
│       ├── base_page.py             # BasePage (waits, click, accessibilite)
│       └── pages/
│           ├── login_page.py        # Page connexion + 2FA + reset
│           ├── dashboard_page.py    # Page tableau de bord
│           ├── security_page.py     # Page parametres securite
│           ├── transfer_page.py     # Page virements (Page Object pret)
│           └── bills_page.py        # Page factures (Page Object pret)
├── reports/                    # Rapports generes
│   ├── report.html                  # Rapport pytest-html (autonome)
│   └── allure-results/              # Donnees brutes Allure
├── docs/                       # Documentation
├── Dockerfile                  # Image Python + Chrome headless
├── requirements.txt            # Dependances Python
└── conftest.py                # Configuration pytest globale
```

### 4.3 Pattern Page Object Model (POM)

Toutes les pages heritent de `BasePage` qui fournit :
- Attentes explicites (`WebDriverWait`)
- Actions communes (`click`, `enter_text`, `get_text`)
- Verification d'accessibilite via axe-core (`check_accessibility`)
- Capture de screenshots pour Allure
- Support JavaScript click pour les elements caches par CSS

Les locators utilisent des selecteurs CSS avec attributs `data-testid` pour la stabilite.

---

## 5. Planification des Developpements

### 5.1 Roadmap par Sprint

| Sprint | Semaines | Livrables | Statut |
|--------|----------|-----------|--------|
| Sprint 1 | S1-S2 | Framework de base, Page Objects, tests authentification | Termine |
| Sprint 2 | S3-S4 | Tests securite, BDD (Gherkin), gestion donnees | Termine |
| Sprint 3 | S5-S6 | Integration Docker, CI/CD GitHub Actions, rapports | Termine |
| Sprint 4 | S7-S8 | Tests virements bancaires (Page Object pret) | A planifier |
| Sprint 5 | S9-S10 | Tests paiement factures (Page Object pret) | A planifier |
| Sprint 6 | S11-S12 | Tests performance, optimisation CI/CD | A planifier |

### 5.2 Couverture Actuelle par Module

| Module | Tests Fonctionnels | Tests BDD | Priorite | Statut |
|--------|--------------------|-----------|----------|--------|
| Authentification (login, 2FA, logout, reset) | 12 tests | 8 scenarios | P1 - Critique | Implemente |
| Parametres Securite (mot de passe, 2FA, notifications) | 11 tests | 6 scenarios | P2 - Haute | Implemente |
| Consultation Compte (solde, historique) | - | - | P1 - Critique | Page Object pret |
| Virements Bancaires (internes, externes) | - | - | P1 - Critique | Page Object pret |
| Paiement Factures | - | - | P2 - Haute | Page Object pret |

**Note** : Les Page Objects pour les modules non encore testes (`transfer_page.py`, `bills_page.py`, `dashboard_page.py`) sont deja developpes et prets a recevoir des tests. Cela permet une montee en charge rapide lors des prochains sprints.

### 5.3 Repartition des Tests par Marker

| Marker | Nombre de tests | Usage |
|--------|-----------------|-------|
| `@smoke` | ~11 | Verification rapide, execution a chaque push |
| `@regression` | ~30 | Suite complete, execution quotidienne |
| `@critical` | ~8 | Tests bloquants pour la mise en production |
| `@accessibility` / `@wcag` | 2 | Conformite WCAG 2.1 |
| `@xfail` | 1 | Bug connu (labels manquants sur les toggles) |

---

## 6. Criteres d'Eligibilite a l'Automatisation

### 6.1 Matrice de Decision

Un scenario est eligible a l'automatisation s'il repond aux criteres suivants :

| Critere | Poids | Seuil |
|---------|-------|-------|
| Frequence d'execution | 30% | >= 1 fois/sprint |
| Stabilite fonctionnelle | 25% | Pas de changement prevu sur 3 sprints |
| Criticite metier | 20% | Bloquant ou majeur |
| Complexite d'automatisation | 15% | Effort < 2 jours |
| ROI | 10% | Gain temps > 50% apres 5 executions |

### 6.2 Scenarios Prioritaires

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

### 6.3 Checklist Avant Automatisation

- [ ] Le scenario manuel est documente et valide
- [ ] Les donnees de test sont identifiees
- [ ] Les prerequis techniques sont disponibles
- [ ] Les criteres d'acceptance sont definis
- [ ] L'environnement de test est stable

---

## 7. Integration CI/CD

### 7.1 Pipeline GitHub Actions

Fichier : `.github/workflows/test-automation.yml`

Le pipeline est compose de 4 jobs :

| Job | Description | Dependance |
|-----|-------------|------------|
| **smoke-tests** | Tests smoke bloquants (~1 min) | - |
| **regression-tests** | Suite complete parallelisee (`-n auto`) | smoke-tests |
| **accessibility-tests** | Tests WCAG 2.1 | smoke-tests |
| **publish-results** | Resume automatique sur les PR | regression + accessibility |

Les jobs regression et accessibilite s'executent **en parallele** apres les smoke tests.

### 7.2 Declencheurs

| Evenement | Action |
|-----------|--------|
| Push sur `main` ou `develop` | Execution automatique |
| Pull Request vers `main` | Execution automatique (bloquant) + commentaire resume |
| Cron `0 7 * * 1-5` | Execution quotidienne a 8h00 Paris (lundi-vendredi) |
| Manuel (`workflow_dispatch`) | Execution a la demande |

### 7.3 Execution Docker

```bash
# Execution par defaut (tous les tests + rapport HTML)
docker-compose up --build

# Execution en arriere-plan
docker-compose up --build -d
docker-compose logs -f tests

# Execution par suite
docker-compose run --rm tests tests/ -v --env=docker -m smoke
docker-compose run --rm tests tests/ -v --env=docker -m regression
docker-compose run --rm tests tests/bdd/ -v --env=docker
```

### 7.4 Rapports et Visibilite

| Type | Emplacement | Description |
|------|-------------|-------------|
| pytest-html | `reports/report.html` | Rapport HTML autonome, consultable sans outil supplementaire |
| Allure | `reports/allure-results/` | Donnees brutes JSON pour generation Allure (necessite Java) |
| Screenshots | `reports/screenshots/` | Captures automatiques en cas d'echec |
| GitHub Artifacts | Actions > Artifacts | 3 rapports (smoke, regression, accessibilite) - retention 30 jours |
| Commentaire PR | Pull Request | Resume automatique des resultats poste sur chaque PR |

---

## 8. Systeme de Gestion des Donnees

### 8.1 Architecture 3 Niveaux

| Niveau | Source | Usage |
|--------|--------|-------|
| **Statique** | `test_users.json` | Donnees de reference (users, accounts, beneficiaires, factures) |
| **Dynamique** | Factories Faker (`factories.py`) | Generation de donnees realistes a la volee |
| **Persistant** | SQLite via SQLAlchemy (`database.py`) | Base de donnees dediee par environnement |

### 8.2 Modeles de Donnees (ORM)

5 modeles SQLAlchemy avec relations :
- `User` (email, password, name, has_2fa, totp_code)
- `Account` (user_id, type, number/IBAN, balance)
- `Transaction` (account_id, type credit/debit, amount, description)
- `Beneficiary` (user_id, name, iban)
- `Bill` (provider, reference, amount, due_date, paid)

### 8.3 Scripts Pre/Post-Execution

```bash
# CLI disponible
python -m tests.data.seed_data seed --env=dev -v       # Initialiser
python -m tests.data.seed_data cleanup --env=dev -v     # Nettoyer
python -m tests.data.seed_data reset --env=dev -v       # Reinitialiser
python -m tests.data.seed_data random --env=dev -c 20 -v  # Donnees aleatoires
```

Hooks pytest integres dans `conftest.py` :
- `test_database` (fixture session) : seed automatique au debut des tests
- `pytest_sessionfinish` : fermeture des connexions en fin de session

### 8.4 Isolation Multi-Environnement

- Singleton `DatabaseManager` par environnement
- Base SQLite separee : `tests/data/db/test_data_{env}.db`
- Parametrable via `--env` : `pytest tests/ --env=uat`
- Variables d'environnement supportees (`${DB_USER}`, `${DB_PASSWORD}`)

---

## 9. Conformite et Normes

### 9.1 RGPD

- Aucune donnee personnelle reelle dans les tests
- Donnees synthetiques generees par Faker (locale `fr_FR`)
- Base SQLite locale, pas de transmission de donnees
- Logs de test sans informations sensibles (mots de passe masques)

### 9.2 WCAG 2.1 (Accessibilite)

- Tests automatises via axe-core sur chaque page
- Verification des niveaux A et AA
- Bug connu documente : labels manquants sur les toggles (`@xfail`)
- Violations reportees en JSON dans les rapports Allure

### 9.3 Eco-conception

- Mode headless Chrome (pas de rendu graphique)
- Nettoyage des donnees apres execution
- Rapports legers (`--self-contained-html`)
- Screenshots uniquement en cas d'echec (pas systematique)
- Image Docker optimisee (Python slim + Chrome minimal)

---

## 10. Indicateurs de Suivi

### 10.1 KPIs Automatisation

| Indicateur | Cible | Actuel |
|------------|-------|--------|
| Couverture automatisee (modules critiques) | > 70% | ~40% (2/5 modules) |
| Taux de reussite | > 95% | 100% (41 passed, 1 xfail) |
| Temps d'execution suite complete | < 5 minutes | ~70 secondes |
| Faux positifs | < 5% | 0% |

### 10.2 Dashboard de Suivi

Les resultats sont visibles via :
- **GitHub Actions** : Statut pass/fail a chaque push/PR
- **pytest-html** : Rapport HTML detaille (`reports/report.html`)
- **GitHub Artifacts** : Rapport telechargeables 30 jours
- **GitHub Issues** : Suivi des anomalies detectees

---

## 11. Gouvernance

### 11.1 Roles et Responsabilites

| Role | Responsabilite |
|------|----------------|
| Test Lead | Strategie, priorisation, reporting |
| Automation Engineer | Developpement et maintenance scripts |
| Developpeur | Revue code, testabilite, attributs `data-testid` |
| Product Owner | Validation criteres acceptance |

### 11.2 Processus de Revue

1. Tout nouveau script passe par une Pull Request
2. Revue obligatoire par un pair
3. Tests de validation sur environnement Docker
4. Merge sur branche principale apres approbation

---

## 12. Annexes

### 12.1 Glossaire

- **CI/CD** : Continuous Integration / Continuous Deployment
- **WCAG** : Web Content Accessibility Guidelines
- **RGPD** : Reglement General sur la Protection des Donnees
- **2FA** : Two-Factor Authentication
- **POM** : Page Object Model
- **BDD** : Behavior-Driven Development
- **ROI** : Return On Investment
- **SPA** : Single Page Application

### 12.2 References

- [Documentation Selenium](https://www.selenium.dev/documentation/)
- [Guide pytest](https://docs.pytest.org/)
- [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core](https://www.deque.com/axe/)
- [Docker Compose](https://docs.docker.com/compose/)
