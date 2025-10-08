import tkinter as tk

# Faza 1: "Mozak"
class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"{self.prezime} {self.ime} ({self.razred})"


# Faza 2: GUI
class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.ucenici = []
        self.odabrani_ucenik_index = None

        # Konfiguracija prozora
        self.root.title("Evidencija učenika")
        self.root.geometry("500x400")

        # Frames
        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="NSEW")

        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        # Widgeti za unos
        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, pady=2, sticky="EW")

        tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, pady=5, sticky="W")
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, pady=2, sticky="EW")

        tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, pady=5, sticky="W")
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, pady=2, sticky="EW")

        self.spremi_gumb = tk.Button(unos_frame, text="Dodaj učenika", command=self.dodaj_ucenika)
        self.spremi_gumb.grid(row=3, column=0, columnspan=2, pady=10)

        self.izmijeni_gumb = tk.Button(unos_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.izmijeni_gumb.grid(row=4, column=0, columnspan=2, pady=5)

        # Widgeti za prikaz
        self.lista_label = tk.Label(prikaz_frame, text="Popis učenika:")
        self.lista_label.pack(anchor='nw', padx=10, pady=10)

        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.listbox.bind("<<ListboxSelect>>", self.odaberi_ucenika)

        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()

        if ime and prezime and razred:
            ucenik = Ucenik(ime, prezime, razred)
            self.ucenici.append(ucenik)
        
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.ime_entry.delete(0, tk.END)
        self.prezime_entry.delete(0, tk.END)
        self.razred_entry.delete(0, tk.END)
        for ucenik in self.ucenici:
            self.listbox.insert(tk.END, str(ucenik))

    def odaberi_ucenika(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.odabrani_ucenik_index = selected_index[0]
            ucenik = self.ucenici[self.odabrani_ucenik_index]

            self.ime_entry.delete(0, tk.END)
            self.ime_entry.insert(0, ucenik.ime)
            self.prezime_entry.delete(0, tk.END)
            self.prezime_entry.insert(0, ucenik.prezime)
            self.razred_entry.delete(0, tk.END)
            self.razred_entry.insert(0, ucenik.razred)

    def spremi_izmjene(self):
        if self.odabrani_ucenik_index is not None:
            ucenik = self.ucenici[self.odabrani_ucenik_index]

            ucenik.ime = self.ime_entry.get()
            ucenik.prezime = self.prezime_entry.get()
            ucenik.razred = self.razred_entry.get()

            self.refresh()

            self.odabrani_ucenik_index = None


if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()
