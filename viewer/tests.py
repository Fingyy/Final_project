#pip install selenium
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
import time


class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Vytvoření admin uživatele pro test
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@admin.com'
        )

    def test_signup(self):
        # Přístup na stránku registrace
        self.selenium.get(f'{self.live_server_url}/signup/')

        # Vyplnění vstupních polí
        username_input = self.selenium.find_element(By.NAME, "username")
        first_name_input = self.selenium.find_element(By.NAME, "first_name")
        last_name_input = self.selenium.find_element(By.NAME, "last_name")
        email_input = self.selenium.find_element(By.NAME, "email")
        password1_input = self.selenium.find_element(By.NAME, "password1")
        password2_input = self.selenium.find_element(By.NAME, "password2")

        username_input.send_keys('testuser')
        first_name_input.send_keys('Test')
        last_name_input.send_keys('User')
        email_input.send_keys('testuser@example.com')
        password1_input.send_keys('testpassword123')
        password2_input.send_keys('testpassword123')

        # Odeslání formuláře
        self.selenium.find_element(By.XPATH, '//button[text()="Registrovat"]').click()

        # Ověření přesměrování na domovskou stránku
        time.sleep(2)  # Čekání na načtení stránky
        self.assertEqual(self.selenium.current_url, f'{self.live_server_url}/')

        # Ověření, že se zobrazuje správný text po registraci
        self.assertIn("Welcome to Online shop", self.selenium.page_source)
def test_login(self):
    # Přístup na stránku přihlášení
    self.selenium.get(f'{self.live_server_url}/login/')

    # Vyplnění vstupních polí pro uživatelské jméno a heslo
    username_input = self.selenium.find_element(By.NAME, "username")
    password_input = self.selenium.find_element(By.NAME, "password")
    username_input.send_keys('admin')
    password_input.send_keys('admin')

    # Odeslání formuláře
    self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()

    # Čekání na načtení stránky
    time.sleep(5)

    # Ověření, že jsme na domovské stránce
    self.assertEqual(self.selenium.current_url, f'{self.live_server_url}/')

    # Ověření, že se zobrazuje správný text pro přihlášeného uživatele
    self.assertIn("Welcome to Online shop", self.selenium.page_source)

    # Ověření, že se zobrazuje sekce „Sklad“
    self.assertIn("Sklad", self.selenium.page_source)  # Ověření, že sekce Sklad je přítomna

    # Místo kontroly přesného HTML jsem použila text pro snížení chybovosti.
    self.assertIn("Sklad", self.selenium.page_source)
