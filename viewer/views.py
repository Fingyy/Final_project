import logging
from django.http import Http404
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView, FormView, View
from viewer.models import Television, ItemsOnStock, Order, Profile, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from viewer.forms import (TVForm, CustomAuthenticationForm, CustomPasswordChangeForm, ProfileForm, SignUpForm,
                          OrderForm, BrandForm, ItemOnStockForm, TVDisplayTechnologyForm, TVDisplayResolutionForm,
                          TVOperationSystemForm, BrandDeleteForm, TVDisplayTechnologyDeleteForm,
                          TVDisplayResolutionDeleteForm, TVOperationSystemDeleteForm)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automaticky přihlásí uživatele po registraci

            return redirect('home')  # Vrácení na homepage
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile_detail.html'

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(), 'object': self.request.user}


class SubmittableLoginView(LoginView):
    template_name = 'user/login_form.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'user/password_change_form.html'
    success_url = reverse_lazy('profile_detail')
    form_class = CustomPasswordChangeForm


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/edit_profile.html', {'form': form})


class BaseView(TemplateView):
    template_name = 'home.html'
    extra_context = {}


class SearchResultsView(ListView):
    template_name = 'search_results.html'
    model = Television
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Television.objects.filter(
                Q(brand__brand_name__icontains=query) |  # Vyhledávání podle Brand name
                Q(display_technology__name__icontains=query) |  # Vyhledávání podle Display technology
                Q(brand_model__icontains=query)  # Vyhledávání podle Brand model
            )
        return Television.objects.none()  # Vrací prázdný queryset pokud není žádný k dispozici


class BrandCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'television/brand_create.html'
    form_class = BrandForm
    success_url = reverse_lazy('tv_create')

    def test_func(self):
        # Umožní přístup pouze členům skupiny 'tv_admin' nebo superuživatelům
        return self.request.user.is_superuser or self.request.user.groups.filter(name='tv_admin').exists()

    def form_invalid(self, form):
        logger.warning('User provided invalid data.')
        return super().form_invalid(form)


class TVDisplayTechnologyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'television/technology_create.html'
    form_class = TVDisplayTechnologyForm
    success_url = reverse_lazy('tv_create')

    def test_func(self):
        # Umožní přístup pouze členům skupiny 'tv_admin' nebo superuživatelům
        return self.request.user.is_superuser or self.request.user.groups.filter(name='tv_admin').exists()

    def form_invalid(self, form):
        logger.warning('User provided invalid data.')
        return super().form_invalid(form)


class DisplayResolutionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'television/resolution_create.html'
    form_class = TVDisplayResolutionForm
    success_url = reverse_lazy('tv_create')

    def test_func(self):
        # Umožní přístup pouze členům skupiny 'tv_admin' nebo superuživatelům
        return self.request.user.is_superuser or self.request.user.groups.filter(name='tv_admin').exists()

    def form_invalid(self, form):
        logger.warning('User provided invalid data.')
        return super().form_invalid(form)


class OperationSystemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'television/system_create.html'
    form_class = TVOperationSystemForm
    success_url = reverse_lazy('tv_create')

    def test_func(self):
        # Umožní přístup pouze členům skupiny 'tv_admin' nebo superuživatelům
        return self.request.user.is_superuser or self.request.user.groups.filter(name='tv_admin').exists()

    def form_invalid(self, form):
        logger.warning('User provided invalid data.')
        return super().form_invalid(form)


class BrandDeleteView(View):
    template_name = 'television/brand_delete.html'

    def get(self, request, *args, **kwargs):
        form = BrandDeleteForm()  # Instantiate the form
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = BrandDeleteForm(request.POST)
        if form.is_valid():
            brand = form.cleaned_data['brand']
            brand.delete()  # Delete the selected brand
            return redirect('tv_create')
        return render(request, self.template_name, {'form': form})


class TVDisplayTechnologyDeleteView(View):
    template_name = 'television/technology_delete.html'

    def get(self, request, *args, **kwargs):
        form = TVDisplayTechnologyDeleteForm()  # Instantiate the form
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TVDisplayTechnologyDeleteForm(request.POST)
        if form.is_valid():
            display_technology = form.cleaned_data['display_technology']
            display_technology.delete()  # Delete the selected brand
            return redirect('tv_create')
        return render(request, self.template_name, {'form': form})


class TVDisplayResolutionDeleteView(View):
    template_name = 'television/resolution_delete.html'

    def get(self, request, *args, **kwargs):
        form = TVDisplayResolutionDeleteForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TVDisplayResolutionDeleteForm(request.POST)
        if form.is_valid():
            display_resolution = form.cleaned_data['display_resolution']
            display_resolution.delete()  # Delete the selected brand
            return redirect('tv_create')
        return render(request, self.template_name, {'form': form})


class TVOperationSystemDeleteView(View):
    template_name = 'television/system_delete.html'

    def get(self, request, *args, **kwargs):
        form = TVOperationSystemDeleteForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TVOperationSystemDeleteForm(request.POST)
        if form.is_valid():
            tv_system = form.cleaned_data['tv_system']
            tv_system.delete()  # Delete the selected brand
            return redirect('tv_create')
        return render(request, self.template_name, {'form': form})


class TVListView(ListView):
    template_name = 'television/tv_list.html'
    model = Television
    context_object_name = 'object_list'

    def get_queryset(self):
        # Získání všech televizí
        queryset = Television.objects.all()

        # Filtrování podle značek
        selected_brand = self.request.GET.getlist('brand')
        if selected_brand:
            queryset = queryset.filter(brand__brand_name__in=selected_brand)

        # Filtrování podle technologie
        selected_technology = self.request.GET.getlist('technology')
        if selected_technology:
            queryset = queryset.filter(display_technology__name__in=selected_technology)

        # Filtrování podle rozliseni displeje
        selected_resolution = self.request.GET.getlist('resolution')
        if selected_resolution:
            queryset = queryset.filter(display_resolution__name__in=selected_resolution)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Kontrola, zda uživatel patří do skupiny 'tv_admin'
        context['is_tv_admin'] = user.groups.filter(name='tv_admin').exists()

        # Předání vybraných filtrů do kontextu
        context['selected_brand'] = self.request.GET.getlist('brand')
        context['selected_technology'] = self.request.GET.getlist('technology')
        context['selected_resolution'] = self.request.GET.getlist('resolution')

        # Pro každou televizi přidáme odpovídající položku zásob
        televisions = context['object_list']
        for television in televisions:
            item_on_stock = ItemsOnStock.objects.filter(television_id=television.id).first()
            television.item_on_stock = item_on_stock
        return context


class TVDetailView(DetailView):
    template_name = 'television/tv_detail.html'
    model = Television

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Kontrola, zda uživatel patří do skupiny 'tv_admin', pokud je přihlášen (pro podminkovani v html)
        context['is_tv_admin'] = user.groups.filter(name='tv_admin').exists()

        # Načtení zásob spojených s konkrétní televizí
        television = self.get_object()  # Získáme aktuální instanci Television
        # "First zde mám, abych nemusel pracovat s QuerySetem
        item_on_stock = ItemsOnStock.objects.filter(television_id=television).first()
        context['item_on_stock'] = item_on_stock
        return context


class TVCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'television/tv_creation.html'
    form_class = TVForm
    success_url = reverse_lazy('tv_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='tv_admin').exists()

    def form_invalid(self, form):
        logger.warning('User provided invalid data.')
        return super().form_invalid(form)


class TVUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'television/tv_creation.html'
    model = Television
    form_class = TVForm
    success_url = reverse_lazy('tv_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='tv_admin').exists()

    def form_invalid(self, form):
        logger.warning('User provided invalid data while updating a movie.')
        return super().form_invalid(form)


class TVDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'television/tv_delete.html'
    model = Television
    success_url = reverse_lazy('tv_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='tv_admin').exists()


class FilteredTelevisionListView(ListView):
    model = Television
    template_name = 'television/tv_list_filter.html'
    context_object_name = 'televisions'

    def get_queryset(self):
        queryset = Television.objects.all()  # Zakladni queryset se vsemi televizemi

        smart_tv = self.kwargs.get('smart_tv')
        if smart_tv == 'smart':
            queryset = queryset.filter(smart_tv=True)
        elif smart_tv == 'non-smart':
            queryset = queryset.filter(smart_tv=False)
        elif smart_tv not in ('smart', 'non-smart', None):
            raise Http404

        # Filtrovaní podle rozliseni(display_resolution)
        resolution = self.kwargs.get('resolution')
        if resolution:
            queryset = queryset.filter(
                display_resolution__name=resolution)  # display_resolution je ForeignKey na model TV display resolution

        # Filtrovaní podle technologie (display_technology)
        technology = self.kwargs.get('technology')
        if technology:
            queryset = queryset.filter(
                display_technology__name=technology)  # display_technology je ForeignKey na model TVDisplayTechnology

        # Filtrovaní podle operacniho systemu
        op_system = self.kwargs.get('op_system')
        if op_system:
            queryset = queryset.filter(operation_system__name=op_system)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pridej aktualni filtry do kontextu (napr. pro zobrazeni v sablone)
        context['selected_smart'] = self.kwargs.get('smart_tv', 'All')
        context['selected_resolution'] = self.kwargs.get('resolution', 'All')
        context['selected_technology'] = self.kwargs.get('technology', 'All')
        context['selected_op_system'] = self.kwargs.get('op_system', 'All')

        # Pro každou televizi přidáme odpovídající položku zásob
        televisions = context['object_list']
        for television in televisions:
            item_on_stock = ItemsOnStock.objects.filter(television_id=television.id).first()
            television.item_on_stock = item_on_stock
        return context


class ItemOnStockListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ItemsOnStock
    template_name = 'stock/stock_list.html'
    context_object_name = 'items'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='stock_admin').exists()


class ItemOnStockCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ItemsOnStock
    template_name = 'stock/item_on_stock_create_update.html'
    form_class = ItemOnStockForm
    success_url = reverse_lazy('stock_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='stock_admin').exists()

    """Zamezeni duplicit je poreseno na urovni databaze, zde"""

    def form_invalid(self, form):
        # Přidání logu při neplatném formuláři
        logger.warning('User provided invalid data.')
        # Vrátíme neplatný formulář (s chybami)
        return super().form_invalid(form)


class ItemOnStockUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'stock/item_on_stock_create_update.html'
    model = ItemsOnStock
    form_class = ItemOnStockForm
    success_url = reverse_lazy('stock_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='stock_admin').exists()


class ItemOnStockDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'stock/item_on_stock_delete.html'
    model = ItemsOnStock
    success_url = reverse_lazy('stock_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='stock_admin').exists()


class AddToCartView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, television_id):
        # Ziskame televizi podle ID
        television = get_object_or_404(Television, id=television_id)

        # Ziskame  množství televize na sklade
        item_on_stock = get_object_or_404(ItemsOnStock, television_id=television_id)

        # Inicializujeme kosik, pokud jeste neexistuje
        cart = request.session.get('cart', {})

        # Kontrola, zda uz mame televizor v kosiku
        if str(television_id) in cart:
            current_quantity_in_cart = cart[str(television_id)]['quantity']

            # Kontrola, zda by pridanim dalsiho kusu nepresahl pocet na sklade
            if current_quantity_in_cart + 1 > item_on_stock.quantity:
                # Pokud by pridani dalsiho kusu překrocilo mnozstvi na sklade, zobrazíme chybovou zpravu
                messages.error(request, f'Nelze přidat více než {item_on_stock.quantity} ks do košíku.')
                return redirect('tv_detail', pk=television_id)

            # Pokud skladova zasoba umoznuje pridani, zvysime mnozstvi
            cart[str(television_id)]['quantity'] += 1

        else:
            # Pokud televizor jeste neni v kosiku, zkontrolujeme, zda je alespon 1 kus na sklade
            if item_on_stock.quantity < 1:
                # Neni nic na sklade, zobrazíme chybovou zprávu
                messages.error(request, 'Tento televizor není momentálně na skladě.')
                return redirect('tv_detail', pk=television_id)

            """Přidáme nový televizor do košíku s počátečním množstvím 1"""
            cart[str(television_id)] = {
                'name': television.brand.brand_name,
                'model': television.brand_model,
                'price': str(television.price),
                'quantity': 1
            }

        # Ulozime kosik do session
        request.session['cart'] = cart
        return redirect('view_cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, television_id):
        # Ziskani kosiku ze session
        cart = request.session.get('cart', {})

        # Pokud existuje polozka v kosiku, snizte jeji mnozstvi
        if str(television_id) in cart:
            if cart[str(television_id)]['quantity'] > 1:
                cart[str(television_id)]['quantity'] -= 1
            else:
                del cart[str(television_id)]

        # Ulozime kosik do session
        request.session['cart'] = cart
        return redirect('view_cart')


class CartView(LoginRequiredMixin, View):
    template_name = 'order/cart.html'

    def get(self, request):
        cart = request.session.get('cart', {})

        # Vypocet celkove ceny a poctu polozek
        total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
        total_items = sum(int(item['quantity']) for item in cart.values())

        return render(request, self.template_name, {
            'cart': cart,
            'total_price': total_price,
            'total_items': total_items,
        })


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'order/checkout.html'
    form_class = OrderForm

    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)
    #     self.order = None
    """Přesměrování, pokud je košík prázdný"""

    def dispatch(self, request, *args, **kwargs):
        cart = self.request.session.get('cart', {})
        if not cart:
            return redirect('view_cart')
        return super().dispatch(request, *args, **kwargs)

    """Úspěšné přesměrování po odeslání formuláře"""

    def get_success_url(self):
        return reverse('order_success', kwargs={'order_id': self.order.order_id})

    """
    Inicializace formuláře s údaji uživatele
    """

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.profile.address if hasattr(user, 'profile') else '',
            'city': user.profile.city if hasattr(user, 'profile') else '',
            'zipcode': user.profile.zipcode if hasattr(user, 'profile') else '',
            'phone_number': user.profile.phone_number if hasattr(user, 'profile') else '',
        })
        return initial

    """Předání uživatele do formuláře při jeho inicializaci"""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Předáme uživatele do formuláře
        return kwargs

    """Logika po úspěšném odeslání formuláře (zpracování objednávky)"""

    def form_valid(self, form):
        self.order = form.save(commit=False)  # Vytvoření objednávky, ale zatím neuložíme
        self.order.user = self.request.user  # Priradime uzivatele k objednávce
        self.order.price = 0  # Inicializace celkové ceny na 0
        self.order.save()  # Nejprve ulozime objednavku

        """ Zpracování položek z košíku """
        cart = self.request.session.get('cart', {})
        total_price = 0  # Proměnná pro výpočet celkové ceny

        for television_id, item in cart.items():
            count = item['quantity']  # Získání počtu z košíku
            television = Television.objects.get(id=television_id)

            # Najdeme odpovídající záznam v ItemsOnStock
            stock_item = ItemsOnStock.objects.get(television_id=television)

            # Zkontrolujeme, zda je na skladě dostatečné množství
            if stock_item.quantity < count:
                form.add_error(None, f'Not enough stock for {television.brand_model}.')
                return self.form_invalid(form)

            # Odečteme počet kusů ze skladu
            stock_item.quantity -= count
            stock_item.save()

            # Vytvoření položky objednávky
            order_item = OrderItem.objects.create(order=self.order, television=television, quantity=count)

            total_price += television.price * count  # Přičtení ceny

        self.order.price = total_price
        self.order.status = 'submitted'
        self.order.save()

        self.request.session['cart'] = {}  # Vyčištění košíku
        return super().form_valid(form)


class OrderSuccessView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_success.html'
    context_object_name = 'order'

    def get_object(self, **kwargs):
        # Ziskame objednavku podle order_id predaneho v URL
        order = get_object_or_404(Order, order_id=self.kwargs['order_id'])

        # Overeni, zda je uzivatel vlastnikem objednávky nebo superuser
        if order.user != self.request.user and not self.request.user.is_superuser:
            # Pokud není, vyvoláme 404 chybu
            raise Http404("Nemáte oprávnění k zobrazení této objednávky.")
        return order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Zobrazi pouze objednavky aktualne prihlaseneho uzivatele
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def get_object(self, **kwargs):
        # Ziskame objednavku podle order_id predaneho v URL
        order = get_object_or_404(Order, order_id=self.kwargs['order_id'])

        # Overeni, zda je uzivatel vlastnikem objednavky nebo superuser
        if order.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("Nemáte oprávnění k zobrazení této objednávky.")
        return order


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = "order/order_delete.html"
    success_url = reverse_lazy('order_list')
    context_object_name = 'order'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='tv_admin').exists()

    def get_object(self, **kwargs):
        # Ziskame objednavku podle order_id predaneho v URL
        return get_object_or_404(Order, order_id=self.kwargs['order_id'])


def generate_order_pdf(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    # Vytvoření bufferu
    buffer = io.BytesIO()

    # Vytvoření PDF objektu
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Základní informace o objednávce
    row = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, row, "Objednávka")

    p.setFont("Helvetica", 12)
    row -= 20
    p.drawString(100, row, f"ID objednávky: {order.order_id}")

    row -= 20
    p.drawString(100, row, f"Datum: {order.order_date.strftime('%d.%m.%Y')}")

    row -= 20
    p.drawString(100, row, f"Celková cena objednávky: {int(order.price)} CZK")

    # Seznam zboží v objednávce
    row -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, row, "Zboží v objednávce:")

    # Vykreslení položek
    p.setFont("Helvetica", 12)
    for item in order.items.all():
        row -= 20
        p.drawString(100, row, f"{item.quantity}x {item.television}\" (Cena za 1ks: {int(item.television.price)} CZK)")

    # Ukončení a uložení PDF
    p.showPage()
    p.save()

    # Vrácení souboru jako odpovědi
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"objednavka_{order.order_id}.pdf")


def home(request):
    return render(request, 'home.html')


def terms_view(request):
    return render(request, 'terms.html')


class TermsView(TemplateView):
    template_name = 'terms.html'
