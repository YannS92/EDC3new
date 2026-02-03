"""
Classe de base pour le pattern Page Object Model
Fournit les méthodes communes à toutes les pages
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class BasePage:
    """Classe de base pour toutes les pages de l'application"""

    def __init__(self, driver, timeout=15):
        """
        Initialise la page de base

        Args:
            driver: Instance du driver (Appium ou Selenium)
            timeout: Timeout par défaut pour les attentes (secondes)
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, locator):
        """
        Trouve un élément avec attente explicite

        Args:
            locator: Tuple (By, value) pour localiser l'élément

        Returns:
            WebElement trouvé
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Élément non trouvé: {locator}")
            self._capture_screenshot(f"element_not_found_{locator[1]}")
            raise

    def find_elements(self, locator):
        """
        Trouve plusieurs éléments

        Args:
            locator: Tuple (By, value) pour localiser les éléments

        Returns:
            Liste de WebElements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            return []

    def click(self, locator):
        """
        Clique sur un élément après attente de cliquabilité

        Args:
            locator: Tuple (By, value) pour localiser l'élément
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.info(f"Clic sur l'élément: {locator}")
        except TimeoutException:
            logger.error(f"Élément non cliquable: {locator}")
            self._capture_screenshot(f"element_not_clickable_{locator[1]}")
            raise

    def enter_text(self, locator, text):
        """
        Saisit du texte dans un champ

        Args:
            locator: Tuple (By, value) pour localiser l'élément
            text: Texte à saisir
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Texte saisi dans {locator}: {'*' * len(text) if 'password' in str(locator).lower() else text}")

    def get_text(self, locator):
        """
        Récupère le texte d'un élément

        Args:
            locator: Tuple (By, value) pour localiser l'élément

        Returns:
            Texte de l'élément
        """
        element = self.find_element(locator)
        return element.text

    def is_element_visible(self, locator, timeout=None):
        """
        Vérifie si un élément est visible

        Args:
            locator: Tuple (By, value) pour localiser l'élément
            timeout: Timeout personnalisé (optionnel)

        Returns:
            True si visible, False sinon
        """
        try:
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=None):
        """
        Vérifie si un élément est présent dans le DOM

        Args:
            locator: Tuple (By, value) pour localiser l'élément
            timeout: Timeout personnalisé (optionnel)

        Returns:
            True si présent, False sinon
        """
        try:
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_disappear(self, locator, timeout=None):
        """
        Attend qu'un élément disparaisse

        Args:
            locator: Tuple (By, value) pour localiser l'élément
            timeout: Timeout personnalisé (optionnel)
        """
        try:
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logger.warning(f"L'élément est toujours visible: {locator}")

    def scroll_to_element(self, locator):
        """
        Fait défiler jusqu'à un élément

        Args:
            locator: Tuple (By, value) pour localiser l'élément
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_attribute(self, locator, attribute):
        """
        Récupère un attribut d'un élément

        Args:
            locator: Tuple (By, value) pour localiser l'élément
            attribute: Nom de l'attribut

        Returns:
            Valeur de l'attribut
        """
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def _capture_screenshot(self, name):
        """
        Capture une screenshot pour le rapport Allure

        Args:
            name: Nom du fichier de screenshot
        """
        try:
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f"Erreur lors de la capture d'écran: {e}")

    def capture_screenshot(self, name=None):
        """
        Capture une screenshot et la sauvegarde dans le dossier reports/screenshots

        Args:
            name: Nom du fichier (optionnel, généré automatiquement si non fourni)

        Returns:
            Chemin du fichier screenshot
        """
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}"

        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        if not name.endswith('.png'):
            name = f"{name}.png"

        screenshot_path = os.path.join(screenshot_dir, name)

        try:
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot sauvegardée: {screenshot_path}")
            with open(screenshot_path, 'rb') as f:
                screenshot_content = f.read()
            allure.attach(screenshot_content, name=name, attachment_type=allure.attachment_type.PNG)
            return screenshot_path
        except Exception as e:
            logger.error(f"Erreur lors de la capture d'écran: {e}")
            return None

    def wait_for_page_load(self, timeout=None):
        """
        Attend le chargement complet de la page (Web uniquement)

        Args:
            timeout: Timeout personnalisé (optionnel)
        """
        try:
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        except Exception:
            pass  # Ignorer pour les drivers mobiles

    @allure.step("Vérification de l'accessibilité de la page")
    def check_accessibility(self):
        """
        Vérifie l'accessibilité de la page courante (WCAG 2.1)

        Returns:
            Dictionnaire avec les violations trouvées
        """
        try:
            from axe_selenium_python import Axe
            axe = Axe(self.driver)
            axe.inject()
            results = axe.run()
            return results.get('violations', [])
        except Exception as e:
            logger.warning(f"Vérification accessibilité impossible: {e}")
            return []
