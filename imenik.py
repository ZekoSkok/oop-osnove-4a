import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os

class Kontakt:
    def __init__(self, ime, email, telefon):
        self.ime = ime
        self.email = email
        self.telefon = telefon

    def __str__(self):
        return f"{self.ime} --- {self.email} --- {self.telefon}"

class ImenikApp:
    def __init__(self, root):
        self.root = root
        self.kontakti = []

        root.title("Imenik")
        root.geometry("500x400")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")

        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=10, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Email:").grid(row=1, column=0, sticky="W")
        self.email_entry = tk.Entry(unos_frame)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Telefon:").grid(row=2, column=0, sticky="W")
        self.telefon_entry = tk.Entry(unos_frame)
        self.telefon_entry.grid(row=2, column=1, padx=10, pady=5, sticky="EW")

        unos_frame.columnconfigure(1, weight=1)

        dodaj_btn = tk.Button(unos_frame, text="Dodaj kontakt", command=self.dodaj_kontakt)
        dodaj_btn.grid(row=3, column=0, columnspan=2, pady=10)

        lista_frame = tk.Frame(root, padx=10, pady=10)
        lista_frame.grid(row=1, column=0, sticky="NSEW")

        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(lista_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")

        scrollbar = tk.Scrollbar(lista_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        gumbi_frame = tk.Frame(root, padx=10, pady=10)
        gumbi_frame.grid(row=2, column=0, sticky="EW")

        spremi_btn = tk.Button(gumbi_frame, text="Spremi kontakte", command=self.spremi_kontakte)
        spremi_btn.grid(row=0, column=0, padx=5, pady=5)

        #Tu bi inače došo učitaj btn, al ne treba nam zbog toga što kasnije implementiram pametno učitavanje

        obrisi_btn = tk.Button(gumbi_frame, text="Obriši kontakt", command=self.obrisi_kontakt)
        obrisi_btn.grid(row=0, column=2, padx=5, pady=5)

        self.ucitaj_kontakte()

    def dodaj_kontakt(self):
        ime = self.ime_entry.get().strip()
        email = self.email_entry.get().strip()
        telefon = self.telefon_entry.get().strip()

        if not (ime and email and telefon):
            messagebox.showwarning("TW", "Fali ti nešto twin")
            return

        kontakt = Kontakt(ime, email, telefon)
        self.kontakti.append(kontakt)
        self.osvjezi_prikaz()

        self.ime_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)

    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for k in self.kontakti:
            self.listbox.insert(tk.END, str(k))

    def spremi_kontakte(self):
        #if not self.kontakti:
            #messagebox.showinfo("uhh", "Šta želiš spremit?")
            #return

            #Inače bih koristio ovo gore, ali u slučaju da obrišemo kontakt kada je bio sam, ne možemo spremiti tu promjenu jer program smatra listbox praznim, ali pri sljedećem učitavanju će se kontakt vratiti, pa funkcionalnost nije potpuna, tkd je dopušteno spremanje praznog imenika

        with open("kontakti.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Ime", "Email", "Telefon"])
            for k in self.kontakti:
                writer.writerow([k.ime, k.email, k.telefon])

        messagebox.showinfo("Yippee", f"stored u {os.getcwd()}")
        self.root.destroy() #mrsko mi je napravit ekstra klik

    def ucitaj_kontakte(self):
        try:
            if not os.path.exists("kontakti.csv"):
                return

            with open("kontakti.csv", "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.kontakti = [Kontakt(row["Ime"], row["Email"], row["Telefon"]) for row in reader]

            self.osvjezi_prikaz()
        except FileNotFoundError:
            pass

    def obrisi_kontakt(self):
        selekcija = self.listbox.curselection()
        if not selekcija:
            messagebox.showwarning("???", "Koga brišemo boss?")
            return

        indeks = selekcija[0]
        self.kontakti.pop(indeks)
        self.osvjezi_prikaz()
        messagebox.showinfo("del :)", "Bye bye")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImenikApp(root)
    root.mainloop()
