"""
Steps spécifiques à la sécurité pour les tests BDD
"""

from pytest_bdd import given, when, then, parsers
import allure


# ═══════════════════════════════════════════════════════════════
# STEPS "GIVEN" - PRÉCONDITIONS SÉCURITÉ
# ═══════════════════════════════════════════════════════════════

@given("je suis sur la page de sécurité")
def sur_page_securite(dashboard_page, security_page):
    """Navigue vers la page de sécurité"""
    with allure.step("Navigation vers la page de sécurité"):
        dashboard_page.navigate_to_tab('security')
        assert security_page.is_security_page_displayed(), \
            "La page de sécurité devrait être affichée"


@given("la double authentification est désactivée")
def deux_fa_desactivee(security_page, context):
    """S'assure que la 2FA est désactivée"""
    with allure.step("Vérification que la 2FA est désactivée"):
        if security_page.is_2fa_enabled():
            security_page.disable_2fa()
        context['initial_2fa_state'] = False


@given("la double authentification est activée")
def deux_fa_activee(security_page, context):
    """S'assure que la 2FA est activée"""
    with allure.step("Vérification que la 2FA est activée"):
        if not security_page.is_2fa_enabled():
            security_page.enable_2fa()
        context['initial_2fa_state'] = True


# ═══════════════════════════════════════════════════════════════
# STEPS "WHEN" - ACTIONS SÉCURITÉ
# ═══════════════════════════════════════════════════════════════

@when("je navigue vers la page de sécurité")
def naviguer_page_securite(dashboard_page, security_page):
    """Navigue vers la page de sécurité"""
    with allure.step("Navigation vers la page de sécurité"):
        dashboard_page.navigate_to_tab('security')


@when("j'ouvre la modal de changement de mot de passe")
def ouvrir_modal_mot_de_passe(security_page):
    """Ouvre la modal de changement de mot de passe"""
    with allure.step("Ouverture de la modal de changement de mot de passe"):
        security_page.open_change_password_modal()


@when(parsers.parse('je change mon mot de passe de "{current}" à "{new}"'))
def changer_mot_de_passe(security_page, current, new, context):
    """Change le mot de passe"""
    with allure.step(f"Changement de mot de passe"):
        security_page.change_password(current, new)
        context['new_password'] = new


@when("j'active la double authentification")
def activer_2fa(security_page, context):
    """Active la 2FA"""
    with allure.step("Activation de la double authentification"):
        security_page.enable_2fa()
        context['2fa_action'] = 'enable'


@when("je désactive la double authentification")
def desactiver_2fa(security_page, context):
    """Désactive la 2FA"""
    with allure.step("Désactivation de la double authentification"):
        security_page.disable_2fa()
        context['2fa_action'] = 'disable'


@when("j'annule le changement de mot de passe")
def annuler_changement_mot_de_passe(security_page):
    """Annule le changement de mot de passe"""
    with allure.step("Annulation du changement de mot de passe"):
        security_page.cancel_password_change()


@when(parsers.parse('je saisis un nouveau mot de passe "{password}"'))
def saisir_nouveau_mot_de_passe(security_page, password, context):
    """Saisit un nouveau mot de passe"""
    with allure.step(f"Saisie du nouveau mot de passe"):
        security_page.enter_new_password(password)
        context['entered_password'] = password


# ═══════════════════════════════════════════════════════════════
# STEPS "THEN" - VÉRIFICATIONS SÉCURITÉ
# ═══════════════════════════════════════════════════════════════

@then("la page de sécurité est affichée")
def page_securite_affichee(security_page):
    """Vérifie que la page de sécurité est affichée"""
    with allure.step("Vérification de l'affichage de la page de sécurité"):
        assert security_page.is_security_page_displayed(), \
            "La page de sécurité devrait être affichée"


@then("la modal de changement de mot de passe est affichée")
def modal_mot_de_passe_affichee(security_page):
    """Vérifie que la modal est affichée"""
    with allure.step("Vérification de l'affichage de la modal"):
        assert security_page.is_modal_displayed(), \
            "La modal devrait être affichée"


@then("la modal de changement de mot de passe est fermée")
def modal_mot_de_passe_fermee(security_page):
    """Vérifie que la modal est fermée"""
    with allure.step("Vérification de la fermeture de la modal"):
        assert not security_page.is_modal_displayed(), \
            "La modal devrait être fermée"


@then("un message de succès de changement de mot de passe est affiché")
def message_succes_mot_de_passe(security_page):
    """Vérifie qu'un message de succès est affiché"""
    with allure.step("Vérification du message de succès"):
        success = security_page.get_success_message()
        assert success is not None, "Un message de succès devrait être affiché"
        assert "modifié" in success.lower() or "succès" in success.lower(), \
            "Le message devrait indiquer le succès"


@then("un message d'erreur de mot de passe incorrect est affiché")
def message_erreur_mot_de_passe_incorrect(security_page):
    """Vérifie qu'un message d'erreur est affiché"""
    with allure.step("Vérification du message d'erreur"):
        error = security_page.get_password_error()
        assert error is not None, "Un message d'erreur devrait être affiché"
        assert "incorrect" in error.lower(), \
            "Le message devrait mentionner 'incorrect'"


@then("la double authentification est activée")
def verifier_2fa_activee(security_page):
    """Vérifie que la 2FA est activée"""
    with allure.step("Vérification de l'activation de la 2FA"):
        assert security_page.is_2fa_enabled(), \
            "La double authentification devrait être activée"


@then("la double authentification est désactivée")
def verifier_2fa_desactivee(security_page):
    """Vérifie que la 2FA est désactivée"""
    with allure.step("Vérification de la désactivation de la 2FA"):
        assert not security_page.is_2fa_enabled(), \
            "La double authentification devrait être désactivée"


@then("un message de succès d'activation 2FA est affiché")
def message_succes_activation_2fa(security_page):
    """Vérifie le message de succès d'activation 2FA"""
    with allure.step("Vérification du message de succès"):
        success = security_page.get_success_message()
        assert success is not None, "Un message de succès devrait être affiché"
        assert "activée" in success.lower(), \
            "Le message devrait mentionner 'activée'"


@then("un message de succès de désactivation 2FA est affiché")
def message_succes_desactivation_2fa(security_page):
    """Vérifie le message de succès de désactivation 2FA"""
    with allure.step("Vérification du message de succès"):
        success = security_page.get_success_message()
        assert success is not None, "Un message de succès devrait être affiché"
        assert "désactivée" in success.lower(), \
            "Le message devrait mentionner 'désactivée'"


@then(parsers.parse('le critère de longueur affiche "{status}"'))
def verifier_critere_longueur(security_page, status):
    """Vérifie le statut du critère de longueur"""
    with allure.step(f"Vérification du critère de longueur: {status}"):
        requirements = security_page.get_password_requirements_status()
        expected = status.lower() == "valide"
        assert requirements.get('length') == expected, \
            f"Le critère de longueur devrait être {'valide' if expected else 'invalide'}"
