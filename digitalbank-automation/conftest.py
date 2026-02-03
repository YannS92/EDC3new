"""
Configuration pytest pour DigitalBank Automation
Ce fichier contient les fixtures et hooks globaux pour les tests
"""

import os
import pytest
import yaml
from datetime import datetime
from appium import webdriver as appium_webdriver
from selenium import webdriver as selenium_webdriver
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


def load_config(config_file):
    """Charge un fichier de configuration YAML"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', config_file)
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def pytest_addoption(parser):
    """Ajoute des options de ligne de commande personnalisées"""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environnement de test: dev, int, uat, preprod"
    )
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Plateforme: android, ios, web"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Exécuter en mode headless (web uniquement)"
    )


@pytest.fixture(scope="session")
def environment(request):
    """Fixture pour obtenir l'environnement de test"""
    env_name = request.config.getoption("--env")
    config = load_config('environments.yaml')

    if env_name not in config['environments']:
        raise ValueError(f"Environnement inconnu: {env_name}")

    env_config = config['environments'][env_name]
    env_config['name'] = env_name

    # Remplacer les variables d'environnement
    _replace_env_vars(env_config)

    return env_config


def _replace_env_vars(config):
    """Remplace les placeholders ${VAR} par les valeurs d'environnement"""
    if isinstance(config, dict):
        for key, value in config.items():
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1]
                config[key] = os.getenv(env_var, '')
            elif isinstance(value, (dict, list)):
                _replace_env_vars(value)
    elif isinstance(config, list):
        for item in config:
            _replace_env_vars(item)


@pytest.fixture(scope="session")
def test_config():
    """Fixture pour la configuration des tests"""
    return load_config('test_config.yaml')


@pytest.fixture(scope="function")
def mobile_driver(request, environment):
    """Fixture pour le driver Appium (mobile)"""
    platform = request.config.getoption("--platform")
    config = load_config('environments.yaml')

    capabilities = config['capabilities'].get(platform, {}).copy()
    env_appium = environment.get('appium', {})

    capabilities.update({
        'deviceName': env_appium.get('device_name', 'emulator-5554'),
        'app': env_appium.get('app_path', ''),
    })

    appium_server = config.get('appium_server', {})
    server_url = f"http://{appium_server.get('host', 'localhost')}:{appium_server.get('port', 4723)}"

    driver = appium_webdriver.Remote(server_url, capabilities)
    driver.implicitly_wait(environment.get('implicit_wait', 10))

    yield driver

    # Teardown
    driver.quit()


@pytest.fixture(scope="function")
def web_driver(request, environment):
    """Fixture pour le driver Selenium (web)"""
    headless = request.config.getoption("--headless")

    options = selenium_webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = selenium_webdriver.Chrome(options=options)
    driver.implicitly_wait(environment.get('implicit_wait', 10))
    driver.get(environment['base_url'])

    yield driver

    # Teardown
    driver.quit()


@pytest.fixture(scope="function")
def api_client(environment):
    """Fixture pour le client API"""
    import requests

    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })

    # Stocker l'URL de base dans la session
    session.base_url = environment['api_url']

    yield session

    session.close()


@pytest.fixture(scope="session")
def test_data_generator():
    """Fixture pour générer des données de test avec Faker"""
    from faker import Faker
    fake = Faker('fr_FR')
    return fake


@pytest.fixture(scope="function")
def screenshot_on_failure(request, mobile_driver):
    """Capture une screenshot en cas d'échec du test"""
    yield

    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
        mobile_driver.save_screenshot(screenshot_path)


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
