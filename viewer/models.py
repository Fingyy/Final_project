import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    MinLengthValidator, RegexValidator)
from django.core.exceptions import ValidationError
from django.utils import timezone


class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.brand_name


class TVDisplayTechnology(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TVDisplayResolution(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class TVOperationSystem(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Television(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    brand_model = models.CharField(max_length=50)
    tv_released_year = models.IntegerField(validators=[
        MinValueValidator(2010),
        MaxValueValidator(datetime.date.today().year)
    ])
    tv_screen_size = models.IntegerField()
    smart_tv = models.BooleanField(default=True)
    refresh_rate = models.IntegerField()
    display_technology = models.ForeignKey(TVDisplayTechnology, on_delete=models.CASCADE)
    display_resolution = models.ForeignKey(TVDisplayResolution, on_delete=models.CASCADE)
    operation_system = models.ForeignKey(TVOperationSystem, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name="televisions", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)
    image = models.ImageField(upload_to='television_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.brand} -  {self.brand_model} - {self.tv_screen_size}"'


class ItemsOnStock(models.Model):
    television_id = models.ForeignKey(Television, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    """UniqueConstraint zajistí, že do Modelu nepřidám stejnou položku 2x (je to bezpečnost na úrovni databáze)"""

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['television_id'], name='unique_television')
        ]

    def __str__(self):
        return f'{self.quantity}x {self.television_id}'


def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('Datum nemůže být v budoucnosti.')


class Profile(models.Model):
    """
       Model profilu uživatele, který obsahuje osobní a kontaktní informace.

       Tento model rozšiřuje standardní model uživatele a uchovává dodatečné informace,
       jako jsou jméno, příjmení, telefonní číslo, datum narození, adresa a preferovaný
       komunikační kanál. Umožňuje také nahrát profilový obrázek.

       Atributy:
           communication_channel_choices (list): Možnosti komunikačních kanálů, které si uživatel může vybrat.
           alpha_validator (RegexValidator): Validátor pro kontrolu, zda obsahuje pouze písmena.
           zipcode_validator (RegexValidator): Validátor pro kontrolu PSČ, které musí mít 5 číslic.
           user (OneToOneField): Vztah k modelu User, který představuje uživatele.
           first_name (CharField): Křestní jméno uživatele (max. 50 znaků), musí mít alespoň 2 znaky.
           last_name (CharField): Příjmení uživatele (max. 50 znaků), musí mít alespoň 2 znaky.
           phone_number (CharField): Telefonní číslo (max. 14 znaků), volitelné, s kontrolou formátu.
           date_of_birth (DateField): Datum narození uživatele, volitelné, nesmí být v budoucnosti.
           address (CharField): Adresa uživatele (max. 100 znaků), volitelná.
           city (CharField): Město uživatele (max. 25 znaků), volitelné, s kontrolou písmen.
           zipcode (CharField): PSČ uživatele (max. 5 znaků), volitelné, s kontrolou 5 číslic.
           avatar (ImageField): Profilový obrázek, který se ukládá do složky 'avatars/'.
           communication_channel (CharField): Preferovaný komunikační kanál uživatele (výchozí: 'Email').

       Metody:
           email (property): Vrací e-mailovou adresu uživatele.
           __str__(): Vrací řetězec reprezentující profil uživatele.
       """

    communication_channel_choices = [
        ('Pošta', 'Pošta'),
        ('Email', 'Email'),
        ('Telefon', 'Telefon'),
    ]

    alpha_validator = RegexValidator(
        regex=r'^[^\W\d_]+$',  # Povoluje pouze písmena
        message='Povolena jsou pouze písmena.'
    )

    zipcode_validator = RegexValidator(
        regex=r'^\d{5}$',  # Vyžaduje právě 5 číslic
        message='PSČ musí mít 5 číslic',
        code='invalid_zipcode'
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=False, max_length=50,
                                  validators=[
                                      alpha_validator,
                                      MinLengthValidator(2, message='Jméno musí mít alespoň 2 znaky.')])
    last_name = models.CharField(null=True, blank=False, max_length=50,
                                 validators=[
                                     alpha_validator,
                                     MinLengthValidator(2, message='Příjmení musí mít alespoň 2 znaky.')])
    phone_number = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(regex=r'^\+?\d{9,}$',  # Volitelné "+" na začátku a vyžaduje alespoň 9 znaku,
                           message='Nesprávný formát čísla.'),
        ],
        blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True, validators=[validate_not_future_date])
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=25, blank=True, validators=[alpha_validator])
    zipcode = models.CharField(max_length=5, blank=True, validators=[zipcode_validator])
    avatar = models.ImageField(upload_to='avatars/', default='avatars/profile_pic.png', blank=True, null=True)
    communication_channel = models.CharField(max_length=10, choices=communication_channel_choices, default='Email')

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f'{self.user.username} Profile'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('pending_payment', 'Pending Payment'),
        ('processing', 'Processing'),
        ('on_hold', 'On Hold'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('returned', 'Returned'),
        ('completed', 'Completed'),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    television = models.ManyToManyField(Television)
    order_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"Order #{self.order_id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    television = models.ForeignKey(Television, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
