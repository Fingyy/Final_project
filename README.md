# Online shop
Online shop je webová aplikace vyvinutá pomocí Django frameworku v rámci závěrečného projektu kurzu Python. Nepřihlášení uživatelé mohou pouze prohlížet produkty, zatímco registrovaní a přihlášení uživatelé mají možnost nakupovat, spravovat své profily a prohlížet své objednávky. Aplikace zahrnuje víceúrovňovou správu: skupina tv_admin má oprávnění přidávat, mazat a upravovat produkty, skupina stock_admin pro správu skladu se stará o aktualizaci množství produktů na skladě a administrátor má kromě těchto funkcí přístup také ke všem objednávkám.

## Funkce
- [x] Administrátorský panel pro správu
- [x] Definování oprávnění admin/uživatel
- [x] Vytvořené skupiny tv_admin pro správu TV a stock_admin pro správu skladu
- [x] Přidávání, ediatce a mazání produktů umožněno skupině tv_admin
- [x] Přidávání, ediatce a mazání položek na skaldě umožněno skupině stock_admin
- [x] Zobrazení datumu a času na úvodní stránce
- [x] Registrace a přihlášení uživatelů
- [x] Správa uživatelských profilů
- [x] Validace vstupních dat (při registraci, úpravě profilu)
- [x] Prohlížení a vyhledávání produktů
- [x] Filtrování produktů podle kategorií
- [x] Proklik přes obrázky na úvodní stránce na produkty
- [x] Přidávání produktů do košíka
- [x] Zobrazení a editace košíka
- [x] Zobrazení všech objednávek pro admina
- [x] Testování

## Použité technologie
- Django, Python
- HTML, CSS, JavaScript
- SQLite
- Selenium

## Požadavky
- python>= 3.12
- django==4.1.1
- pillow==10.4.0
- reportlab==4.2.5
- chardet==5.2.0
- selenium~=4.25.0

## Setup
### 1. Klonování repozitáře:
```
git clone https://github.com/Fingyy/Final_project.git
```
### 2. Vytvoření a nastavení virtual env:
Windows
```
pip install virtualenv
python -m virtualenv venv
.\venv\Scripts\activate
```
Mac
```
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
```
### 3. Instalace závislostí:
```
pip install -r requirements.txt
```
### 4. Nastavení databáze:
```
python manage.py migrate
```
### 5. Načítání statických souborů:
```
python manage.py collectstatic
```
### 6. Spuštění serveru:
```
python manage.py runserver
```
### 7. Přístup k aplikaci:
- Otevřete webový prohlížeč a přejděte na http://localhost:8000/
- Pro administrativní rozhraní přejděte na http://localhost:8000/admin/


## Databázové modely a ER Diagram

### Přehled modelů

- **Brand:** Uchovává názvy značek s unikátními hodnotami.
- **TVDisplayTechnology, TVDisplayResolution, TVOperationSystem:** Modely pro různé vlastnosti televizorů.
- **Category:** Kategorizuje produkty do různých skupin.
- **Television:** Hlavní model pro televizory, včetně detailů jako velikost obrazovky, technologie displeje atd.
- **ItemsOnStock:** Sleduje množství dostupných televizorů na skladě, s unikátními omezeními.
- **Profile:** Uchovává uživatelské profily, včetně validací a volby komunikačního kanálu.
- **Order:** Model pro objednávky, sleduje status a další detaily objednávky.
- **OrderItem:** Umožňuje definici jednotlivých položek v objednávce.

### Vztahy mezi modely

**1. OneToMany (1:N) vztahy**
- Brand → Television
- TVDisplayTechnology → Television
- TVDisplayResolution → Television
- TVOperationSystem → Television
- User → Profile
- User → Order
- Order → OrderItem
- Television → ItemsOnStock

**2. ManyToMany (M:N) vztahy**
- Television → Category
- Order → Television

### ER Diagram
![my_final_project_models](https://github.com/user-attachments/assets/ee6166a5-8ec0-43d8-9922-7e35bd699987)
