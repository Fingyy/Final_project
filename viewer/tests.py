from django.test import TestCase

from viewer.models import Brand, Television, TVDisplayTechnology, TVDisplayResolution, TVOperationSystem

# Ověřují, že se může úspěšně vytvořit značka
class BrandModelTest(TestCase):
    def test_create_brand(self):
        brand = Brand.objects.create(brand_name='Test Brand')
        self.assertEqual(brand.brand_name, 'Test Brand')

    def test_brand_string_representation(self):
        brand = Brand.objects.create(brand_name='Test Brand')
        self.assertEqual(str(brand), 'Test Brand')

# Správně zobrazují technologie
class TVDisplayTechnologyModelTest(TestCase):
    def test_create_display_technology(self):
        tech = TVDisplayTechnology.objects.create(name='LED', description='Light Emitting Diode')
        self.assertEqual(tech.name, 'LED')

    def test_display_technology_string_representation(self):
        tech = TVDisplayTechnology.objects.create(name='OLED')
        self.assertEqual(str(tech), 'OLED')

# Nastavení rozlišení a jeho řetězení
class TVDisplayResolutionModelTest(TestCase):
    def test_create_display_resolution(self):
        resolution = TVDisplayResolution.objects.create(name='4K')
        self.assertEqual(resolution.name, '4K')

    def test_display_resolution_string_representation(self):
        resolution = TVDisplayResolution.objects.create(name='1080p')
        self.assertEqual(str(resolution), '1080p')


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

from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import CustomAuthenticationForm

User = get_user_model()

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
