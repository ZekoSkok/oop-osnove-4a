import sqlite3


def inicijalizacija_imenika():
    konekcija = sqlite3.connect('Imenik.db')
    kursor = konekcija.cursor()

    sql_naredba = '''
    CREATE TABLE IF NOT EXISTS Imenik (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ime TEXT NOT NULL,
        prezime TEXT NOT NULL,
        broj_telefona TEXT NOT NULL
    );
    '''
    kursor.execute(sql_naredba)
    konekcija.commit()
    konekcija.close()

inicijalizacija_imenika()

def dodaj_kontakt():
    unos_ime = input("Unesite ime: ")
    unos_prezime = input("Unesite prezime: ")
    unos_broj_telefona = input("Unesite broj telefona: ")

    konekcija = sqlite3.connect('Imenik.db')
    kursor = konekcija.cursor()

    sql_naredba = '''
    INSERT INTO Imenik (ime, prezime, broj_telefona)
    VALUES (?, ?, ?);
    '''
    podaci = (unos_ime, unos_prezime, unos_broj_telefona)

    kursor.execute(sql_naredba, podaci)
    konekcija.commit()
    konekcija.close()

def prikazi_kontakte():
    print("\n--- KONTAKTI ---")
    konekcija = sqlite3.connect('Imenik.db')
    kursor = konekcija.cursor()

    kursor.execute("SELECT * FROM Imenik;")
    rezultati = kursor.fetchall()

    print("ID | Ime | Prezime | Broj Telefona")
    print("---------------------")
    for red in rezultati:
        print(f"ID: {red[0]}, Ime: {red[1]}, Prezime: {red[2]}, Broj Telefona: {red[3]}")
    print("---------------------\n")

    konekcija.close()