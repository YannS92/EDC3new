"""
Steps communs réutilisables pour les tests BDD
"""

from pytest_bdd import given, when, then, parsers
import allure


# ═══════════════════════════════════════════════════════════════
# STEPS "GIVEN" - PRÉCONDITIONS
# ═══════════════════════════════════════════════════════════════

@given("l'application est accessible")
def application_accessible(login_page):
    """Vérifie que l'application est accessible"""
    with allure.step("Vérification de l'accessibilité de l'application"):
        assert login_page.is_login_page_displayed(), \
            "L'application devrait être accessible"


@given("je suis sur la page de connexion")
def sur_page_connexion(login_page):
    """Vérifie que l'utilisateur est sur la page de connexion"""
    with allure.step("Vérification de la page de connexion"):
        assert login_page.is_login_page_displayed(), \
            "La page de connexion devrait être affichée"


@given("je suis connecté en tant qu'utilisateur standard")
def connecte_utilisateur_standard(login_page, dashboard_page, standard_user, context):
    """Connecte l'utilisateur standard"""
    with allure.step(f"Connexion avec {standard_user['email']}"):
        login_page.login(standard_user['email'], standard_user['password'])
        assert dashboard_page.is_dashboard_displayed(), \
            "Le dashboard devrait être affiché après connexion"
        context['current_user'] = standard_user


@given("je suis connecté en tant qu'utilisateur avec 2FA")
def connecte_utilisateur_2fa(login_page, dashboard_page, user_with_2fa, context):
    """Connecte l'utilisateur avec 2FA"""
    with allure.step(f"Connexion avec {user_with_2fa['email']}"):
        login_page.login(user_with_2fa['email'], user_with_2fa['password'])
        assert login_page.is_2fa_page_displayed(), \
            "La page 2FA devrait être affichée"
        login_page.enter_2fa_code(user_with_2fa['totp_code'])
        login_page.submit_2fa_code()
        assert dashboard_page.is_dashboard_displayed(), \
            "Le dashboard devrait être affiché après validation 2FA"
        context['current_user'] = user_with_2fa


# ═══════════════════════════════════════════════════════════════
# STEPS "THEN" - VÉRIFICATIONS COMMUNES
# ═══════════════════════════════════════════════════════════════

@then("le dashboard est affiché")
def dashboard_affiche(dashboard_page):
    """Vérifie que le dashboard est affiché"""
    with allure.step("Vérification de l'affichage du dashboard"):
        assert dashboard_page.is_dashboard_displayed(), \
            "Le dashboard devrait être affiché"


@then("la page de connexion est affichée")
def page_connexion_affichee(login_page):
    """Vérifie que la page de connexion est affichée"""
    with allure.step("Vérification de l'affichage de la page de connexion"):
        assert login_page.is_login_page_displayed(), \
            "La page de connexion devrait être affichée"


@then(parsers.parse("le nom d'utilisateur \"{user_name}\" est affiché"))
def nom_utilisateur_affiche(dashboard_page, user_name):
    """Vérifie que le nom d'utilisateur est affiché"""
    with allure.step(f"Vérification du nom d'utilisateur: {user_name}"):
        displayed_name = dashboard_page.get_user_name()
        assert user_name in displayed_name, \
            f"Le nom '{user_name}' devrait être affiché, trouvé: '{displayed_name}'"
