from django.test import TestCase
from viewer.models import Brand, Television, TVDisplayTechnology, TVDisplayResolution, TVOperationSystem
from django.contrib.auth import get_user_model
from .forms import CustomAuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Brand, Television, ItemsOnStock, TVDisplayTechnology, TVDisplayResolution, TVOperationSystem

User = get_user_model()


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


#Testuje přidání television a kdo je oprávněný
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


# Testuje, zda je formulář platný, když jsou zadány správné údaje a neplatný, když je prázdný.
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





