from .forms import CustomAuthenticationForm
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Brand, Television, ItemsOnStock, TVDisplayTechnology, TVDisplayResolution, TVOperationSystem


# Ověřují, že se může úspěšně vytvořit značka
class BrandModelTest(TestCase):
    def test_create_brand(self):
        brand = Brand.objects.create(brand_name='Test Brand')
        self.assertEqual(brand.brand_name, 'Test Brand')

    def test_brand_string_representation(self):
        brand = Brand.objects.create(brand_name='Test Brand')
        self.assertEqual(str(brand), 'Test Brand')


# Správně zobrazující se technologie
class TVDisplayTechnologyModelTest(TestCase):
    def test_create_display_technology(self):
        tech = TVDisplayTechnology.objects.create(name='LED', description='Light Emitting Diode')
        self.assertEqual(tech.name, 'LED')

    def test_display_technology_string_representation(self):
        tech = TVDisplayTechnology.objects.create(name='OLED')
        self.assertEqual(str(tech), 'OLED')


# Kontrola modelu podle rozlišení a jeho následné řetězení
class TVDisplayResolutionModelTest(TestCase):
    def test_create_display_resolution(self):
        resolution = TVDisplayResolution.objects.create(name='4K')
        self.assertEqual(resolution.name, '4K')

    def test_display_resolution_string_representation(self):
        resolution = TVDisplayResolution.objects.create(name='1080p')
        self.assertEqual(str(resolution), '1080p')


# Kontrola vytvoření modelu podle operačního systému a vrácení správného názvu.
class TVOperationSystemModelTest(TestCase):
    def test_create_operation_system(self):
        os = TVOperationSystem.objects.create(name='Android TV')
        self.assertEqual(os.name, 'Android TV')

    def test_operation_system_string_representation(self):
        os = TVOperationSystem.objects.create(name='Tizen')
        self.assertEqual(str(os), 'Tizen')


# Test zajišťuje, že objekt televizoru je správně vytvořen a uchovává data, jak se očekává
class TelevisionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Vytvoření potřebných instancí pro testy
        cls.brand = Brand.objects.create(brand_name='Test Brand')
        cls.display_technology = TVDisplayTechnology.objects.create(name='LED')
        cls.display_resolution = TVDisplayResolution.objects.create(name='4K')
        cls.operation_system = TVOperationSystem.objects.create(name='Android TV')

        cls.television = Television.objects.create(
            brand=cls.brand,
            brand_model='Test Model',
            tv_released_year=2022,
            tv_screen_size=55,
            smart_tv=True,
            refresh_rate=60,
            display_technology=cls.display_technology,
            display_resolution=cls.display_resolution,
            operation_system=cls.operation_system,
            description='Test Description',
            price=1000.00
        )

    def test_tv_creation(self):
        self.assertEqual(self.television.brand.brand_name, 'Test Brand')
        self.assertEqual(self.television.brand_model, 'Test Model')
        self.assertEqual(self.television.tv_screen_size, 55)
        self.assertTrue(self.television.smart_tv)


# Testuje, zda v přihlašovacím formuláři funguje validace
class CustomAuthenticationFormTest(TestCase):
    def setUp(self):
        # Vytvoření testovacího uživatele
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_form_is_valid(self):
        form = CustomAuthenticationForm(data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = CustomAuthenticationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)


# Test validace v košíku nelze přidat víc, než je skladem
class CartViewTests(TestCase):
    def setUp(self):
        # Vytvoření značky
        self.brand = Brand.objects.create(brand_name='Test Brand')

        # Vytvoření uživatele
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Vytvoření televize
        self.television = Television.objects.create(
            brand=self.brand,
            brand_model='Test Model',
            tv_released_year=2021,
            tv_screen_size=55,
            smart_tv=True,
            refresh_rate=60,
            display_technology=self.create_display_technology(),
            display_resolution=self.create_display_resolution(),
            operation_system=self.create_operation_system(),
            price=1000.00
        )

        # Vytvoření položky na skladě
        self.stock_item = ItemsOnStock.objects.create(
            television_id=self.television,
            quantity=5  # Maximální počet na skladě
        )

    @staticmethod
    def create_display_technology():
        return TVDisplayTechnology.objects.create(name='LED', description='LED Technology')

    @staticmethod
    def create_display_resolution():
        return TVDisplayResolution.objects.create(name='4K')

    @staticmethod
    def create_operation_system():
        return TVOperationSystem.objects.create(name='Android TV')

    def test_get_add_to_cart_exceed_stock(self):
        # Přidání televize do košíku 5krát
        for _ in range(5):
            self.client.get(reverse('add_to_cart', args=[self.television.id]))

        # Pokus o přidání ještě jednou
        response = self.client.get(reverse('add_to_cart', args=[self.television.id]))

        # Ověření, že odpověď je 200 (na stejné stránce) - pokud se přesměrování neděje
        if response.status_code == 200:
            self.assertContains(response, 'Nelze přidat více než 5 ks do košíku.')  # Upravte text podle potřeby
        else:
            # Ověření chybové hlášky při případném přesměrování
            final_response = self.client.get(response.url)
            self.assertContains(final_response, 'Nelze přidat více než 5 ks do košíku.')  # Upravte text podle potřeby

        # Ověření, že množství v košíku je maximálně 5
            cart = self.client.session.get('cart', {})
            self.assertEqual(cart.get(str(self.television.id), {}).get('quantity'), 5)


# Test na ověření registrace a uživatelských práv admin
class MySeleniumAdminTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()  # Inicializace webového prohlížeče
        cls.selenium.implicitly_wait(10)

        # Vytvoření admina
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@admin.com'
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_admin_login(self):
        # Přihlášení jako admin
        self.selenium.get(f'{self.live_server_url}/login/')

        # Vyplnění přihlašovacího formuláře
        self.selenium.find_element(By.NAME, 'username').send_keys('admin')
        self.selenium.find_element(By.NAME, 'password').send_keys('admin')
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()

        page_source = self.selenium.page_source

        # Ověření, že admin uvidí "Sklad" a "Objednávky"
        self.assertIn("Sklad", page_source)
        self.assertIn("Objednávky", page_source)


# Test na ověření registrace a uživatelských práv admin
class MySeleniumUserTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()  # Inicializace webového prohlížeče
        cls.selenium.implicitly_wait(10)

        cls.normal_user = User.objects.create_user(
            username='sileniumuser',
            password='heslouser0',
            email='test@seznam.cz'
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_user_login(self):
        # Přihlášení jako běžný uživatel
        self.selenium.get(f'{self.live_server_url}/login/')

        # Vyplnění přihlašovacího formuláře
        self.selenium.find_element(By.NAME, 'username').send_keys('sileniumuser')
        self.selenium.find_element(By.NAME, 'password').send_keys('heslouser0')
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()

        page_source = self.selenium.page_source

        # Ověření, že uživatel uvidí sekci "Košík"
        self.assertIn("Košík", page_source)

        # Ověření, že uživatel uvidí sekci "Profil"
        self.assertIn("Profil", page_source)

        # Ověření, že uživatel uvidí sekci "Odhlásit"
        self.assertIn("Odhlásit", page_source)
