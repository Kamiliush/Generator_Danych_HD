from faker import Faker
import numpy as np
import csv
import random
import string
import datetime

pola_csv_klienci = ['id', 'imie', 'nazwisko', 'email', 'numer_telefonu', 'data_urodzin', 'plec', 'adres_dostawy']
pola_csv_produkty = ['id', 'producent', 'kod_producenta', 'kod_sklepu', 'kategoria', 'wymiary', 'waga',
                     'gwarancja_miesiace']
pola_csv_promocje = ['id', 'data_poczatek', 'data_koniec', 'opis', 'kwota']
pola_csv_sprzedaz = ['id', 'id_produktu', 'id_klienta', 'id_promocja', 'data_sprzedazy', 'liczba_produktow',
                     'cena_katalogowa', 'cena_sprzedazy', 'najnizsza_cena_30dni', 'rabat_kwotowy', 'rabat_procentowy',
                     'metoda_dostawy', 'forma_platnosci', 'czy_oplacone', 'czy_dostarczone', 'data_dostawy',
                     'czy_zwrocony', 'data_zwrotu', 'powod_zwrotu', 'zwracana_liczba_przedmiotow', 'typ_zwrotu',
                     'status_zwrotu']

fake = Faker('pl_PL')


def wygeneruj_klientow(liczba=1, ziarno=None):
    wynik = []
    np.random.seed(ziarno)
    random.seed(ziarno)
    Faker.seed(ziarno)
    for i in range(liczba):
        plec = np.random.choice(['Mezczyzna', 'Kobieta', 'Brak'], p=[0.55, 0.35, 0.1])
        imie = fake.first_name_male() if plec == 'Mezczyzna' else fake.first_name_female()
        nazwisko = fake.last_name_male() if plec == 'Mezczyzna' else fake.last_name_female()
        wynik.append({
            'id': i + 1,
            'imie': imie,
            'nazwisko': nazwisko,
            'email': imie.lower() + nazwisko.lower() + '@' + fake.free_email_domain(),
            'numer_telefonu': fake.phone_number(),
            'data_urodzin': fake.date(),
            'plec': plec,
            'adres_dostawy': fake.address().replace('\n', ' ')
        })
    return wynik


def wygeneruj_produkty(liczba=1, ziarno=None):
    wynik = []
    np.random.seed(ziarno)
    random.seed(ziarno)
    Faker.seed(ziarno)

    for i in range(liczba):
        wynik.append({
            'id': i + 1,
            'producent': np.random.choice(['Dell', 'HP', 'Lenovo', 'ASUS', 'Acer', 'MSI', 'Apple', 'Gigabyte', 'LG',
                                           'Microsoft', 'Razer', 'Huawei', 'Toshiba'],
                                          p=[0.23, 0.17, 0.13, 0.12, 0.11, 0.1, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01]),
            'kod_producenta': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            'kod_sklepu': ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
            'kategoria': np.random.choice(['Laptopy', 'Monitory', 'Myszki', 'Klawiatury', 'Komputery stacjonarne',
                                           'Smartfony', 'Tablety', 'Pendrive\'y'],
                                          p=[0.1, 0.03, 0.12, 0.10, 0.05, 0.2, 0.1, 0.3]),
            'wymiary': f"{random.randint(1, 100)}-{random.randint(1, 100)}-{random.randint(1, 100)} cm",
            'waga': f"{random.uniform(0.01, 5.0):.2f} kg",
            'gwarancja_miesiace': np.random.choice([24, 36], p=[0.9, 0.1]),
        })
    return wynik


def wygeneruj_promocje(liczba=1, ziarno=None):
    np.random.seed(ziarno)
    Faker.seed(ziarno)

    wynik = []
    for i in range(liczba):
        data_poczatek = fake.date_between(start_date='-2y', end_date='today')
        data_koniec = fake.date_between(start_date=data_poczatek, end_date='+9d')
        wynik.append({
            'id': i + 1,
            'data_poczatek': data_poczatek.strftime('%d-%m-%Y'),
            'data_koniec': data_koniec.strftime('%d-%m-%Y'),
            'opis': fake.sentence(),
            'kwota': round(random.uniform(1.0, 1000.0), 2)
        })
    return wynik


def wygeneruj_sprzedaz(liczba=1, ziarno=None, id_kl_max=1, id_prod_max=1, id_prom_max=1):
    np.random.seed(ziarno)
    random.seed(ziarno)
    Faker.seed(ziarno)
    wynik = []

    for i in range(liczba):
        cena_katalogowa = round(random.uniform(10.0, 1000.0), 2)
        rabat_kwotowy = round(random.uniform(1.0, cena_katalogowa / 2.5), 2)
        cena_sprzedazy = round(cena_katalogowa - rabat_kwotowy, 2)
        data_sprzedazy = fake.date_time_between(start_date='-2y', end_date='now')
        czas_dostawy = np.random.exponential(scale=3, size=1)
        czas_dostawy = np.clip(czas_dostawy, 1, 7)
        czas_dostawy = int(np.round(czas_dostawy[0]))
        data_dostawy_konw = ''
        data_zwrotu_konw = ''
        liczba_produktow = int(np.random.normal(loc=5.5, scale=2.5))
        czy_zwrocone = ''
        powod_zwrotu = ''
        zwracana_liczba_przedmiotow = ''
        typ_zwrotu = ''
        status_zwrotu = ''
        czy_oplacone = np.random.choice(['tak', 'nie'], p=[0.93, 0.07])
        if czy_oplacone == 'tak':
            czy_dostarczone = np.random.choice(['tak', 'nie'], p=[0.9, 0.1])
            if czy_dostarczone == 'tak':
                data_dostawy = data_sprzedazy + datetime.timedelta(days=czas_dostawy)
                data_dostawy_konw = data_dostawy.strftime('%d-%m-%Y, %H:%M:%S')
                czy_zwrocone = np.random.choice(['tak', 'nie'], p=[0.15, 0.85])
                if czy_zwrocone == 'tak':
                    data_zwrotu = fake.date_time_between(start_date=data_dostawy, end_date='+14d')
                    data_zwrotu_konw = data_zwrotu.strftime('%d-%m-%Y, %H:%M:%S')
                    powod_zwrotu = fake.sentence()
                    zwracana_liczba_przedmiotow = np.random.randint(0, 10)
                    typ_zwrotu = np.random.choice(['Bez podania przyczyny', 'reklamacja', 'rękojmia'], p=[0.75, 0.2, 0.05])
                    status_zwrotu = np.random.choice(['W toku', 'Uznany', 'Odrzucony'], p=[0.1, 0.75, 0.15])

        wynik.append({
            'id': i + 1,
            'id_produktu': random.randint(1, id_prod_max),
            'id_klienta': random.randint(1, id_kl_max),
            'id_promocja': random.randint(1, id_prom_max),
            'data_sprzedazy':  data_sprzedazy.strftime('%d-%m-%Y, %H:%M:%S'),
            'liczba_produktow': liczba_produktow,
            'cena_katalogowa': cena_katalogowa,
            'cena_sprzedazy': cena_sprzedazy,
            'najnizsza_cena_30dni': round(random.uniform(cena_sprzedazy, cena_katalogowa), 2),
            'rabat_kwotowy': rabat_kwotowy,
            'rabat_procentowy': round((rabat_kwotowy / cena_katalogowa) * 100, 2),
            'metoda_dostawy': np.random.choice(['paczkomat', 'kurier', 'odbiór w punkcie', 'przesyłka pocztowa']),
            'forma_platnosci': np.random.choice(['karta', 'przelew', 'blik'], p=[0.3, 0.2, 0.5]),
            'czy_oplacone': czy_oplacone,
            'czy_dostarczone': czy_dostarczone,
            'data_dostawy': data_dostawy_konw,
            'czy_zwrocony': czy_zwrocone,
            'data_zwrotu': data_zwrotu_konw,
            'powod_zwrotu': powod_zwrotu,
            'zwracana_liczba_przedmiotow': zwracana_liczba_przedmiotow,
            'typ_zwrotu': typ_zwrotu,
            'status_zwrotu': status_zwrotu

        })
    return wynik


def zapisz_do_csv(nazwa, tryb, koniec_linii, pola, dane, kodowanie='utf8'):
    with open(nazwa, tryb, newline=koniec_linii, encoding=kodowanie) as file:
        writer = csv.DictWriter(file, fieldnames=pola)
        writer.writeheader()
        writer.writerows(dane)


klienci = wygeneruj_klientow(10_000, 22)
print(klienci)
zapisz_do_csv('dimKlienci.csv', 'w', '', pola_csv_klienci, klienci)
produkty = wygeneruj_produkty(5000, 22)
print(produkty)
zapisz_do_csv('dimProdukty.csv', 'w', '', pola_csv_produkty, produkty)
promocje = wygeneruj_promocje(1000, 22)
print(promocje)
zapisz_do_csv('dimPromocje.csv', 'w', '', pola_csv_promocje, promocje)
sprzedaz = wygeneruj_sprzedaz(200_000, 22, 10_000, 5000, 1000)
print(sprzedaz)
zapisz_do_csv('factSprzedaz.csv', 'w', '', pola_csv_sprzedaz, sprzedaz)

