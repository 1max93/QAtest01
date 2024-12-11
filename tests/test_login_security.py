"""
Scénario : Test de sécurité du formulaire de login (Injection SQL)
But : Vérifier la robustesse du champ username face à une tentative d'injection SQL
     et s'assurer que l'accès n'est pas accordé dans ce cas.
Étapes :
1. Accéder à la page de login
2. Tenter une injection SQL dans le champ username
3. Soumettre le formulaire
4. Vérifier qu'un message d'erreur s'affiche (aucun accès)
5. Réitérer avec des identifiants valides pour valider le bon fonctionnementt
"""

import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
import HtmlTestRunner

class TestLoginSecurity(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.login_page.open("https://the-internet.herokuapp.com/login")

    def tearDown(self):
        self.driver.quit()

    def test_injection_sql_non_autorisee(self):
        """
        Test: Vérifie qu'une tentative d'injection SQL dans le champ username
        entraîne un message d'erreur et n'autorise pas la connexion.
        """
        print("Tentative d'injection SQL avec username: ' OR '1'='1")
        print("Attendu: Échec de la connexion et message d'erreur approprié.")
        self.login_page.login("' OR '1'='1", "fakepassword")
        error_msg = self.login_page.get_error_message()
        self.assertIn(
            "Your username is invalid!",
            error_msg,
            "Échec du test: l'injection SQL n'a pas été détectée comme invalide."
        )
        print("Résultat: L'injection SQL a été refusée, message d'erreur affiché.")

    def test_connexion_valide_reussie(self):
        """
        Test: Vérifie que l'utilisation d'identifiants valides permet de se connecter
        et d'accéder à la zone sécurisée.
        """
        print("Tentative de connexion avec identifiants valides (tomsmith / SuperSecretPassword!).")
        print("Attendu: Réussite de la connexion et affichage de la zone sécurisée.")
        self.login_page.login("tomsmith", "SuperSecretPassword!")
        header = self.login_page.get_secure_area_header()
        self.assertIn("Secure Area", header, "Échec du test: la connexion valide n'a pas abouti.")
        print("Résultat: Connexion réussie, zone sécurisée accessible.")

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))
