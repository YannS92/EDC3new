"""
Steps spécifiques à l'authentification pour les tests BDD
"""

from pytest_bdd import given, when, then, parsers
import allure


# ═══════════════════════════════════════════════════════════════
# STEPS "WHEN" - ACTIONS D'AUTHENTIFICATION
# ═══════════════════════════════════════════════════════════════

@when(parsers.parse('je me connecte avec "{email}" et "{password}"'))
def connexion_avec_identifiants(login_page, email, password, context):
    """Effectue une connexion avec les identifiants fournis"""
    with allure.step(f"Connexion avec email: {email}"):
        login_page.login(email, password)
        context['login_email'] = email
        context['login_password'] = password


@when("je me connecte avec des identifiants valides")
def connexion_identifiants_valides(login_page, standard_user, context):
    """Effectue une connexion avec les identifiants valides de l'utilisateur standard"""
    with allure.step(f"Connexion avec {standard_user['email']}"):
        login_page.login(standard_user['email'], standard_user['password'])
        context['current_user'] = standard_user


@when("je me connecte avec un mot de passe incorrect")
def connexion_mot_de_passe_incorrect(login_page, standard_user, invalid_credentials, context):
    """Effectue une connexion avec un mot de passe incorrect"""
    with allure.step("Connexion avec mot de passe incorrect"):
        login_page.login(standard_user['email'], invalid_credentials['wrong_password'])
        context['login_email'] = standard_user['email']


@when("je me connecte avec un email inexistant")
def connexion_email_inexistant(login_page, invalid_credentials, context):
    """Effectue une connexion avec un email inexistant"""
    with allure.step("Connexion avec email inexistant"):
        login_page.login(invalid_credentials['wrong_email'], "SomePassword123!")
        context['login_email'] = invalid_credentials['wrong_email']


@when(parsers.parse('je saisis le code 2FA "{code}"'))
def saisir_code_2fa(login_page, code, context):
    """Saisit le code 2FA"""
    with allure.step(f"Saisie du code 2FA: {code}"):
        login_page.enter_2fa_code(code)
        context['2fa_code'] = code


@when("je valide le code 2FA")
def valider_code_2fa(login_page):
    """Valide le code 2FA"""
    with allure.step("Validation du code 2FA"):
        login_page.submit_2fa_code()


@when("je clique sur le bouton de déconnexion")
def clic_deconnexion(dashboard_page):
    """Clique sur le bouton de déconnexion"""
    with allure.step("Clic sur le bouton de déconnexion"):
        dashboard_page.logout()


@when("je clique sur 'Mot de passe oublié'")
def clic_mot_de_passe_oublie(login_page):
    """Clique sur le lien mot de passe oublié"""
    with allure.step("Clic sur 'Mot de passe oublié'"):
        login_page.click_forgot_password()


@when(parsers.parse('je demande la réinitialisation pour "{email}"'))
def demander_reinitialisation(login_page, email, context):
    """Demande la réinitialisation du mot de passe"""
    with allure.step(f"Demande de réinitialisation pour: {email}"):
        login_page.request_password_reset(email)
        context['reset_email'] = email


# ═══════════════════════════════════════════════════════════════
# STEPS "THEN" - VÉRIFICATIONS D'AUTHENTIFICATION
# ═══════════════════════════════════════════════════════════════

@then("un message d'erreur de connexion est affiché")
def message_erreur_connexion_affiche(login_page):
    """Vérifie qu'un message d'erreur est affiché"""
    with allure.step("Vérification du message d'erreur"):
        error = login_page.get_error_message()
        assert error is not None, "Un message d'erreur devrait être affiché"


@then(parsers.parse('le message d\'erreur contient "{texte}"'))
def message_erreur_contient(login_page, texte):
    """Vérifie le contenu du message d'erreur"""
    with allure.step(f"Vérification que le message contient: {texte}"):
        error = login_page.get_error_message()
        assert error is not None, "Un message d'erreur devrait être affiché"
        assert texte.lower() in error.lower(), \
            f"Le message devrait contenir '{texte}', trouvé: '{error}'"


@then("je reste sur la page de connexion")
def reste_page_connexion(login_page):
    """Vérifie que l'utilisateur reste sur la page de connexion"""
    with allure.step("Vérification du maintien sur la page de connexion"):
        assert login_page.is_login_page_displayed(), \
            "L'utilisateur devrait rester sur la page de connexion"


@then("la page 2FA est affichée")
def page_2fa_affichee(login_page):
    """Vérifie que la page 2FA est affichée"""
    with allure.step("Vérification de l'affichage de la page 2FA"):
        assert login_page.is_2fa_page_displayed(), \
            "La page 2FA devrait être affichée"


@then("un message d'erreur 2FA est affiché")
def message_erreur_2fa_affiche(login_page):
    """Vérifie qu'un message d'erreur 2FA est affiché"""
    with allure.step("Vérification du message d'erreur 2FA"):
        error = login_page.get_2fa_error_message()
        assert error is not None, "Un message d'erreur 2FA devrait être affiché"


@then("je reste sur la page 2FA")
def reste_page_2fa(login_page):
    """Vérifie que l'utilisateur reste sur la page 2FA"""
    with allure.step("Vérification du maintien sur la page 2FA"):
        assert login_page.is_2fa_page_displayed(), \
            "L'utilisateur devrait rester sur la page 2FA"


@then("la page de réinitialisation est affichée")
def page_reinitialisation_affichee(login_page):
    """Vérifie que la page de réinitialisation est affichée"""
    with allure.step("Vérification de l'affichage de la page de réinitialisation"):
        assert login_page.is_reset_page_displayed(), \
            "La page de réinitialisation devrait être affichée"


@then("un message de succès de réinitialisation est affiché")
def message_succes_reinitialisation(login_page):
    """Vérifie qu'un message de succès est affiché"""
    with allure.step("Vérification du message de succès"):
        success = login_page.get_reset_success_message()
        assert success is not None, "Un message de succès devrait être affiché"


@then("un message d'erreur de réinitialisation est affiché")
def message_erreur_reinitialisation(login_page):
    """Vérifie qu'un message d'erreur de réinitialisation est affiché"""
    with allure.step("Vérification du message d'erreur de réinitialisation"):
        error = login_page.get_reset_error_message()
        assert error is not None, "Un message d'erreur devrait être affiché"
