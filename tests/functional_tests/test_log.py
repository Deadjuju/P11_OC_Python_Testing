# import time
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# from flask_testing import LiveServerTestCase
#
# from tests.conftest import client, captured_templates, mocker_clubs
# from server import app
#
#
# class TestUserTakesTheTest(LiveServerTestCase):
#     def create_app(self):
#         # Fichier de config uniquement pour les tests.
#         app.config.from_object('tests.functional_tests.config')
#         return app
#
#     # Méthode exécutée avant chaque test
#     def setUp(self):
#         """Setup the test driver"""
#         # Le navigateur est Chrome
#         chrome_driver_path = r'C:\Users\deadj\code_programmation\OpenClassrooms\PROJET 11 - Améliorez une application Web Python par des tests et du débogage\Projet\P11_OC_Python_Testing\tests\functional_tests\chromedriver.exe'
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         service = Service(chrome_driver_path)
#         driver = webdriver.Chrome(service=service, options=options)
#
#     # Méthode exécutée après chaque test
#     def tearDown(self):
#         self.driver.quit()
#
#     def test_user_login(self):
#         print("/" * 500)
#         # On ouvre le navigateur avec l'adresse du serveur.
#         self.driver.get(self.get_server_url())
#         # L'adresse dans l'url doit être celle que l'on attend.
#         assert self.driver.current_url == 'http://localhost:8943/'
