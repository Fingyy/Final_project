from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from viewer.models import Profile, Television, MobilePhone, Order, Brand, ItemsOnStock
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    # Overriding field labels
    old_password = forms.CharField(label=_("Staré heslo"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("Nové heslo"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Potvrďte nové heslo"), widget=forms.PasswordInput)

    # Overriding the error messages
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Hesla se neshodují. Zkuste to znovu."))
        return password2


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label=_('Uživatelské jméno'),
        min_length=3,
        max_length=20,
        help_text=_(
            'Toto pole je povinné. Uživatelské jméno musí být jediněčné, obsahovat minimálně 3 a maximálně 20 znaků, '
            'pouze písmena, číslice a @/./+/-/_ znaky.')
    )
    first_name = forms.CharField(label=_('Jméno'), required=False, )
    last_name = forms.CharField(label=_('Příjmení'), required=False, )
    email = forms.EmailField(
        label=_('Email'), required=True,
        help_text=_('Zadejte prosím platný e-mail.'),
    )
    password1 = forms.CharField(
        label=_('Heslo'),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_('Vaše heslo musí obsahovat alespoň 8 znaků.')
    )
    password2 = forms.CharField(
        label=_('Heslo znovu'),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_('Prosím, zadejte stejné heslo pro ověření.')
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Uživatelské jméno je již použito. Zvolte jiné.'))
        if len(username) > 20:
            raise forms.ValidationError(_('Uživatelské jméno nesmí být delší než 30 znaků.'))
        if len(username) < 3:
            raise forms.ValidationError(_('Uživatelské jméno nesmí být kratší než 3 znaky.'))

        # Vlastní regulární výraz pro kontrolu platnosti uživatelského jména
        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError(
                _('Uživatelské jméno může obsahovat pouze písmena, číslice, a znaky @/./+/-/_.'))

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Zkontroluje, zda je e-mail v platném formátu
        if email and not forms.EmailField().clean(email):
            raise forms.ValidationError(_('Zadejte prosím platný e-mail.'))

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class TVForm(forms.ModelForm):
    class Meta:
        model = Television
        fields = '__all__'


class MobileForm(forms.ModelForm):
    class Meta:
        model = MobilePhone
        fields = '__all__'


class ItemOnStockForm(forms.ModelForm):
    class Meta:
        model = ItemsOnStock
        fields = '__all__'

    """Definujeme si co chceme za chybovou hlášku v případě, že přidáváme na sklad existující komponentu"""
    def clean_television_id(self):
        television_id = self.cleaned_data.get('television_id')
        if ItemsOnStock.objects.filter(television_id=television_id).exists():
            raise forms.ValidationError('Tato položka již je na skladě.')
        return television_id


class OrderForm(forms.ModelForm):
    """
    Moznost zaskrtavani (checkbox) policka na preneseni  udaju z profilu do objednavky. Nastaveno, ze zaskrtnuti neni
    povinne a label zobrazi popis pro uzivatele.
    """
    use_profile_data = forms.BooleanField(required=False, label='Použít údaje z profilu.')

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'city', 'zipcode', 'phone_number',
                  'use_profile_data']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(OrderForm, self).__init__(*args, **kwargs)

        if self.user.is_authenticated:
            profile = self.user.profile
            self.fields['first_name'].initial = profile.first_name
            self.fields['last_name'].initial = profile.last_name
            self.fields['address'].initial = profile.address
            self.fields['city'].initial = profile.city
            self.fields['zipcode'].initial = profile.zipcode
            self.fields['phone_number'].initial = profile.phone_number

    # def clean(self):
    #    if not self.television.exists():
    #        raise ValidationError('V objednavce musi byt alespon televize nebo mobil')

    def save(self, commit=True):
        order = super(OrderForm, self).save(commit=False)
        if self.cleaned_data['use_profile_data']:
            profile = self.user.profile
            order.first_name = profile.first_name
            order.last_name = profile.last_name
            order.address = profile.address
            order.city = profile.city
            order.zipcode = profile.zipcode
            order.phone_number = profile.phone_number

        if commit:
            order.save()
        return order


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth', 'address', 'city', 'zipcode', 'avatar',
                  'communication_channel']

        labels = {
            'first_name': _('Jméno'),
            'last_name': _('Příjmení'),
            'phone_number': _('Telefon'),
            'date_of_birth': _('Datum narození'),
            'address': _('Adresa'),
            'city': _('Město'),
            'zipcode': _('PSČ'),
            'avatar': _('Profilový obrázek'),
            'communication_channel': _('Komunikační kanál'),
        }

    date_of_birth = forms.DateField(
        input_formats=['%Y-%m-%d'],  # Zbezpeci, aby byl pouzit spravny format
        widget=forms.DateInput(attrs={'type': 'date'})  # Customize the widget
    )
