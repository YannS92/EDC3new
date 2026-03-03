"""
Configuration pytest pour DigitalBank Automation
Ce fichier contient les fixtures et hooks globaux pour les tests
"""

import os
import platform
import pytest
import yaml
import allure
from selenium import webdriver as selenium_webdriver
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Import des modules de données de test
from tests.data import (
    load_test_data,
    DatabaseManager,
)


def load_config(config_file):
    """Charge un fichier de configuration YAML"""
    config_path = os.path.join(os.path.dirname(__file__), "config", config_file)
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def pytest_addoption(parser):
    """Ajoute des options de ligne de commande personnalisées"""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environnement de test: dev, int, uat, preprod",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Exécuter en mode headless (web uniquement)",
    )
    parser.addoption(
        "--viewport",
        action="store",
        default="desktop",
        help="Résolution: desktop (défaut), mobile, tablet",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Navigateur: chromium (défaut), firefox, webkit (macOS uniquement)",
    )


@pytest.fixture(scope="session")
def environment(request):
    """Fixture pour obtenir l'environnement de test"""
    env_name = request.config.getoption("--env")
    config = load_config("environments.yaml")

    if env_name not in config["environments"]:
        raise ValueError(f"Environnement inconnu: {env_name}")

    env_config = config["environments"][env_name]
    env_config["name"] = env_name

    # Remplacer les variables d'environnement
    _replace_env_vars(env_config)

    return env_config


def _replace_env_vars(config):
    """Remplace les placeholders ${VAR} par les valeurs d'environnement"""
    if isinstance(config, dict):
        for key, value in config.items():
            if (
                isinstance(value, str)
                and value.startswith("${")
                and value.endswith("}")
            ):
                env_var = value[2:-1]
                config[key] = os.getenv(env_var, "")
            elif isinstance(value, (dict, list)):
                _replace_env_vars(value)
    elif isinstance(config, list):
        for item in config:
            _replace_env_vars(item)


def get_viewport_size(viewport):
    """Retourne la largeur et hauteur selon la résolution"""
    sizes = {
        "desktop": (1920, 1080),
        "mobile": (390, 844),  # exemple iPhone 14
        "tablet": (768, 1024),  # exemple iPad
    }
    return sizes.get(viewport, (1920, 1080))  # desktop par défaut


@pytest.fixture(scope="function")
def web_driver(request, environment):
    """
    Fixture pour le driver Selenium (web)
    Navigateur sélectionnable via --browser: chromium (défaut), firefox, webkit
    Mode headless activable via --headless
    """
    headless = request.config.getoption("--headless")
    viewport = request.config.getoption("--viewport")
    browser = request.config.getoption("--browser")
    width, height = get_viewport_size(viewport)

    if browser == "chromium":
        options = selenium_webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={width},{height}")
        driver = selenium_webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = selenium_webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")
        driver = selenium_webdriver.Firefox(options=options)

    elif browser == "webkit":
        if platform.system() != "Darwin":
            raise pytest.UsageError(
                "webkit (Safari) n'est disponible que sur macOS. "
                "Utilisez --browser=chromium ou --browser=firefox."
            )
        if headless:
            raise pytest.UsageError("Safari ne supporte pas le mode headless.")
        driver = selenium_webdriver.Safari()
        driver.set_window_size(width, height)

    driver.implicitly_wait(environment.get("implicit_wait", 10))

    # URL de base : variable d'environnement > config
    base_url = os.getenv("BASE_URL", environment["base_url"])
    driver.get(base_url)

    yield driver

    driver.quit()


# ═══════════════════════════════════════════════════════════════
# FIXTURES DONNÉES DE TEST
# ═══════════════════════════════════════════════════════════════


@pytest.fixture(scope="function")
def test_data():
    """
    Fixture pour les données de test statiques (JSON)

    Returns:
        Dictionnaire contenant toutes les données de test
    """
    return load_test_data()


@pytest.fixture
def standard_user(test_data):
    """Fixture pour l'utilisateur standard"""
    return test_data["users"]["standard"]


@pytest.fixture
def user_with_2fa(test_data):
    """Fixture pour l'utilisateur avec 2FA"""
    return test_data["users"]["with_2fa"]


@pytest.fixture
def invalid_credentials(test_data):
    """Fixture pour les identifiants invalides"""
    return test_data["invalid_credentials"]


@pytest.fixture
def password_requirements(test_data):
    """Fixture pour les exigences de mot de passe"""
    return test_data["password_requirements"]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook pour capturer les résultats des tests"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_configure(config):
    """Configuration initiale de pytest"""
    # Créer les répertoires nécessaires
    os.makedirs("reports/allure-results", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Ajouter des marqueurs personnalisés
    config.addinivalue_line("markers", "smoke: Tests de vérification rapide")
    config.addinivalue_line("markers", "regression: Tests de régression")
    config.addinivalue_line("markers", "functional: Tests fonctionnels")
    config.addinivalue_line("markers", "api: Tests API")
    config.addinivalue_line("markers", "performance: Tests de performance")
    config.addinivalue_line("markers", "accessibility: Tests d'accessibilité")
    config.addinivalue_line("markers", "critical: Tests critiques")
    config.addinivalue_line("markers", "wcag: Tests conformité WCAG")


def pytest_collection_modifyitems(config, items):
    """Modifier la collection des tests"""
    env = config.getoption("--env")

    # Ajouter des informations sur l'environnement aux tests
    for item in items:
        item.user_properties.append(("environment", env))


# ═══════════════════════════════════════════════════════════════
# HOOKS BDD POUR ALLURE
# ═══════════════════════════════════════════════════════════════


def pytest_bdd_before_scenario(request, feature, scenario):
    """
    Hook exécuté avant chaque scénario BDD
    Configure les métadonnées Allure à partir des tags
    """
    # Mapping des tags vers Allure epic/feature
    allure.dynamic.epic("DigitalBank")
    allure.dynamic.feature(feature.name)
    allure.dynamic.story(scenario.name)

    # Mapping des tags vers Allure severity
    severity_mapping = {
        "critical": allure.severity_level.CRITICAL,
        "blocker": allure.severity_level.BLOCKER,
        "normal": allure.severity_level.NORMAL,
        "minor": allure.severity_level.MINOR,
        "trivial": allure.severity_level.TRIVIAL,
    }

    for tag in scenario.tags:
        tag_lower = tag.lower()
        if tag_lower in severity_mapping:
            allure.dynamic.severity(severity_mapping[tag_lower])


def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    """
    Hook exécuté lors d'une erreur dans un step BDD
    Capture une screenshot et l'attache au rapport Allure
    """
    # Récupérer le driver depuis les fixtures si disponible
    driver = None
    for fixture_name in ["web_driver", "driver"]:
        if fixture_name in request.fixturenames:
            try:
                driver = request.getfixturevalue(fixture_name)
                break
            except Exception:
                continue

    if driver:
        try:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"Erreur - {step.name}",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass

    # Attacher les détails de l'erreur
    allure.attach(
        f"Feature: {feature.name}\n"
        f"Scenario: {scenario.name}\n"
        f"Step: {step.keyword} {step.name}\n"
        f"Error: {str(exception)}",
        name="Détails de l'erreur",
        attachment_type=allure.attachment_type.TEXT,
    )


def pytest_bdd_after_scenario(request, feature, scenario):
    """
    Hook exécuté après chaque scénario BDD
    Peut être utilisé pour le nettoyage ou la capture de screenshots
    """
    pass


def pytest_sessionfinish(session, exitstatus):
    """
    Hook exécuté à la fin de la session de tests
    Ferme toutes les connexions à la base de données
    """
    DatabaseManager.close_all()
