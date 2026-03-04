"""
Classe de base pour le pattern Page Object Model
Fournit les méthodes communes à toutes les pages (Playwright)
"""

import allure
import logging
import os
from datetime import datetime
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


class BasePage:
    """Classe de base pour toutes les pages de l'application"""

    def __init__(self, page, timeout=15):
        """
        Args:
            page: Instance Playwright Page
            timeout: Timeout par défaut en secondes (converti en ms pour Playwright)
        """
        self.page = page
        self.timeout = timeout
        self._timeout_ms = timeout * 1000

    def find_element(self, selector):
        """
        Retourne un Locator Playwright après avoir attendu que l'élément soit attaché au DOM.

        Args:
            selector: Sélecteur CSS (string)

        Returns:
            Playwright Locator
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="attached", timeout=self._timeout_ms)
            return locator
        except PlaywrightTimeoutError:
            logger.error(f"Élément non trouvé: {selector}")
            self._capture_screenshot(f"element_not_found")
            raise

    def find_elements(self, selector):
        """
        Retourne la liste des Locators correspondant au sélecteur.

        Args:
            selector: Sélecteur CSS (string)

        Returns:
            Liste de Playwright Locators
        """
        try:
            return self.page.locator(selector).all()
        except PlaywrightTimeoutError:
            return []

    def click(self, selector):
        """
        Clique sur un élément (auto-wait Playwright).

        Args:
            selector: Sélecteur CSS (string)
        """
        try:
            self.page.locator(selector).click(timeout=self._timeout_ms)
            logger.info(f"Clic sur l'élément: {selector}")
        except PlaywrightTimeoutError:
            logger.error(f"Élément non cliquable: {selector}")
            self._capture_screenshot(f"element_not_clickable")
            raise

    def enter_text(self, selector, text):
        """
        Efface et remplit un champ texte.

        Args:
            selector: Sélecteur CSS (string)
            text: Texte à saisir
        """
        self.page.locator(selector).fill(text, timeout=self._timeout_ms)
        logger.info(f"Texte saisi dans {selector}: {'*' * len(text) if 'password' in selector.lower() else text}")

    def get_text(self, selector):
        """
        Récupère le texte visible d'un élément.

        Args:
            selector: Sélecteur CSS (string)

        Returns:
            Texte de l'élément
        """
        return self.page.locator(selector).inner_text(timeout=self._timeout_ms)

    def is_element_visible(self, selector, timeout=None):
        """
        Vérifie si un élément est visible.

        Args:
            selector: Sélecteur CSS (string)
            timeout: Timeout en secondes (optionnel)

        Returns:
            True si visible, False sinon
        """
        t_ms = (timeout or self.timeout) * 1000
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=t_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_element_present(self, selector, timeout=None):
        """
        Vérifie si un élément est présent dans le DOM.

        Args:
            selector: Sélecteur CSS (string)
            timeout: Timeout en secondes (optionnel)

        Returns:
            True si présent, False sinon
        """
        t_ms = (timeout or self.timeout) * 1000
        try:
            self.page.locator(selector).wait_for(state="attached", timeout=t_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def wait_for_element_to_disappear(self, selector, timeout=None):
        """
        Attend qu'un élément disparaisse.

        Args:
            selector: Sélecteur CSS (string)
            timeout: Timeout en secondes (optionnel)
        """
        t_ms = (timeout or self.timeout) * 1000
        try:
            self.page.locator(selector).wait_for(state="hidden", timeout=t_ms)
        except PlaywrightTimeoutError:
            logger.warning(f"L'élément est toujours visible: {selector}")

    def wait_for_not_hidden(self, selector, timeout=None):
        """
        Attend qu'un élément n'ait plus la classe CSS 'hidden'.
        Utilisé pour les modales qui utilisent une classe CSS pour se cacher.

        Args:
            selector: Sélecteur CSS (string)
            timeout: Timeout en secondes (optionnel)
        """
        t_ms = (timeout or self.timeout) * 1000
        js_selector = selector.replace("'", '"')
        self.page.wait_for_function(
            f"!document.querySelector('{js_selector}')?.classList.contains('hidden')",
            timeout=t_ms,
        )

    def scroll_to_element(self, selector):
        """
        Fait défiler jusqu'à un élément.

        Args:
            selector: Sélecteur CSS (string)
        """
        self.page.locator(selector).scroll_into_view_if_needed(timeout=self._timeout_ms)

    def get_attribute(self, selector, attribute):
        """
        Récupère un attribut d'un élément.

        Args:
            selector: Sélecteur CSS (string)
            attribute: Nom de l'attribut

        Returns:
            Valeur de l'attribut
        """
        return self.page.locator(selector).get_attribute(attribute, timeout=self._timeout_ms)

    def _capture_screenshot(self, name):
        """Capture une screenshot pour le rapport Allure."""
        try:
            screenshot = self.page.screenshot()
            allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f"Erreur lors de la capture d'écran: {e}")

    def capture_screenshot(self, name=None):
        """
        Capture une screenshot et la sauvegarde dans reports/screenshots.

        Args:
            name: Nom du fichier (optionnel)

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
            self.page.screenshot(path=screenshot_path)
            logger.info(f"Screenshot sauvegardée: {screenshot_path}")
            with open(screenshot_path, 'rb') as f:
                allure.attach(f.read(), name=name, attachment_type=allure.attachment_type.PNG)
            return screenshot_path
        except Exception as e:
            logger.error(f"Erreur lors de la capture d'écran: {e}")
            return None

    def wait_for_page_load(self, timeout=None):
        """Attend le chargement complet de la page."""
        t_ms = (timeout or self.timeout) * 1000
        try:
            self.page.wait_for_load_state("load", timeout=t_ms)
        except Exception:
            pass

    @allure.step("Vérification de l'accessibilité de la page")
    def check_accessibility(self):
        """
        Vérifie l'accessibilité de la page courante (WCAG 2.1) via axe-core.

        Returns:
            Liste des violations trouvées
        """
        try:
            from axe_playwright_python.sync_playwright import Axe
            results = Axe().run(self.page)
            return results.violations if hasattr(results, 'violations') else []
        except Exception as e:
            logger.warning(f"Vérification accessibilité impossible: {e}")
            return []
