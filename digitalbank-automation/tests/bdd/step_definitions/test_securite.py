"""
Tests BDD pour la sécurité
Charge les scénarios depuis les fichiers feature
"""

import os
from pytest_bdd import scenarios

# Import des step definitions
from tests.bdd.step_definitions.common_steps import *
from tests.bdd.step_definitions.authentication_steps import *
from tests.bdd.step_definitions.security_steps import *

# Chemin absolu normalisé vers les features
FEATURE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'features', 'securite'))

# Chargement des scénarios
scenarios(FEATURE_DIR)
