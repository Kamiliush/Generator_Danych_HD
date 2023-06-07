from faker import Faker
import numpy as np
import csv
import random
import string

pola_csv_klienci = ['id', 'imie', 'nazwisko', 'email', 'numer_telefonu', 'data_urodzin', 'plec', 'adres_dostawy']
pola_csv_produkty = ['id', 'producent', 'kod_producenta', 'kod_sklepu', 'kategoria', 'wymiary', 'waga',
                     'gwarancja_miesiace']
pola_csv_promocje = ['id', 'data_poczatek', 'data_koniec', 'opis', 'kwota']
pola_csv_sprzedaz = ['id', 'id_produktu', 'id_klienta', 'id_promocja', 'data', 'liczba_produktow', 'cena_katalogowa',
                     'cena_sprzedazy', 'najnizsza_cena_30dni', 'czy_oplacone', 'rabat_kwotowy', 'rabat_procentowy',
                     'metoda_dostawy',
                     'czy_dostarczony', 'forma_platnosci', 'czy_zwrocony']

fake = Faker('pl_PL')


def wygeneruj_klientow(liczba=1, ziarno=None):
    wynik = []
    np.random.seed(ziarno)
    Faker.seed(ziarno)
    for i in range(liczba):
        plec = np.random.choice(['Mezczyzna', 'Kobieta', 'Brak'], p=[0.5, 0.4, 0.1])
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
            'wymiary': f"{random.randint(1, 100)}-{random.randint(1, 100)}-{random.randint(1, 100)}",
            'waga': f"{random.uniform(0.01, 5.0):.2f} kg",
            'gwarancja_miesiace': np.random.choice([24, 36], p=[0.9, 0.1]),
        })
    return wynik


def wygeneruj_promocje(liczba=1, ziarno=None):
    np.random.seed(ziarno)
    Faker.seed(ziarno)
    data_poczatek = fake.date_between(start_date='-2y', end_date='today')
    data_koniec = fake.date_between(start_date=data_poczatek, end_date='+9d')
    wyjscie = []
    for i in range(liczba):
        wyjscie.append({
            'id': i + 1,
            'data_poczatek': data_poczatek.strftime('%d-%m-%Y'),
            'data_koniec': data_koniec.strftime('%d-%m-%Y'),
            'opis': fake.sentence(),
            'kwota': round(random.uniform(1.0, 1000.0), 2)
        })
    return wyjscie


def wygeneruj_sprzedaz(liczba=1, ziarno=None, id_max=1, produkt_max=1):
    np.random.seed(ziarno)
    Faker.seed(ziarno)
    wyjscie = []

    for i in range(liczba):
        cena_katalogowa = round(random.uniform(10.0, 1000.0), 2)
        cena_sprzedazy = round(random.uniform(1.0, cena_katalogowa), 2)
        rabat_kwotowy = round(random.uniform(0.0, cena_sprzedazy), 2)
        data_zakupu = fake.date_time_between(start_date='-2y', end_date='now')

        wyjscie.append({
            'id': i + 1,
            'id_produktu': random.randint(1, id_max),
            'id_klienta': random.randint(1, id_max),
            'id_promocja': random.randint(1, id_max),
            'data':  data_zakupu.strftime('%d-%m-%Y, %H:%M:%S'),
            'liczba_produktow': int(np.random.normal(loc=5.5, scale=2.5)),
            'cena_katalogowa': cena_katalogowa,
            'cena_sprzedazy': cena_sprzedazy,
            'najnizsza_cena_30dni': round(random.uniform(cena_sprzedazy, cena_katalogowa), 2),
            'czy_oplacone': np.random.choice(['tak', 'nie'], p=[0.9, 0.1]),
            'rabat_kwotowy': rabat_kwotowy,
            'rabat_procentowy': round((rabat_kwotowy / cena_sprzedazy) * 100, 2),
            'metoda_dostawy': np.random.choice(['paczkomat', 'kurier', 'odbiór osobisty', 'przesyłka pocztowa']),
            'czy_dostarczony': np.random.choice(['tak', 'nie'], p=[0.9, 0.1]),
            'forma_platnosci': np.random.choice(['karta', 'przelew', 'blik'], p=[0.3, 0.2, 0.5]),
            'czy_zwrocony': np.random.choice(['tak', 'nie'], p=[0.15, 0.85])

        })
    return wyjscie


def zapisz_do_csv(nazwa, tryb, koniec_linii, pola, dane, kodowanie='utf8'):
    with open(nazwa, tryb, newline=koniec_linii, encoding=kodowanie) as file:
        writer = csv.DictWriter(file, fieldnames=pola)
        writer.writeheader()
        writer.writerows(dane)


klienci = wygeneruj_klientow(100, 2)
print(klienci)
# zapisz_do_csv('dimKlienci.txt', 'w', '', pola_csv_klienci, klienci)
produkty = wygeneruj_produkty(100, 2)
print(produkty)
# zapisz_do_csv('dimProdukty.txt', 'w', '', pola_csv_produkty, produkty)
promocje = wygeneruj_promocje(100, 2)
print(promocje)
# zapisz_do_csv('dimPromocje.txt', 'w', '', pola_csv_promocje, promocje)
sprzedaz = wygeneruj_sprzedaz(10000, 2, 100)
print(sprzedaz)
# zapisz_do_csv('factSprzedaz.txt', 'w', '', pola_csv_sprzedaz, sprzedaz)

