import tkinter as tk

#Faza 1: "Mozak"
class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"{self.prezime} {self.ime} ({self.razred})"
    

#Faza 2: "GUI"

class EvidencijaApp:
    def dodaj_ucenika(self):
        self.ime = self.ime_entry.get()
        self.prezime = self.prezime_entry.get()
        self.razred = self.razred_entry.get()
        ucenik = Ucenik(self.ime, self.prezime, self.razred)
        if self.ime and self.prezime and self.razred:
            if ucenik not in self.ucenici:
                self.ucenici.append(ucenik)

    def __init__(self, root):
        self.root = root
        self.ucenici = []

        #  Struktura prozora 
        self.root.title("Evidencija učenika")
        self.root.geometry("500x400")

        #  Konfig resp
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        #  Frames
        #    forma
        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="NSEW")

        #    prikaz
        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        # resp okvira
        unos_frame.columnconfigure(1, weight=1)

        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

        #  Widgeti - unos
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

        #  Widgeti - prikaz
        self.lista_label = tk.Label(prikaz_frame, text="Popis učenika:")
        self.lista_label.pack(anchor='nw', padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(prikaz_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.ucenici_text = tk.Text(prikaz_frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set)
        self.ucenici_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.ucenici_text.yview)

    def refresh(self):
        self.ucenici_text.delete(1.0, tk.END)
        for ucenik in self.ucenici:
            self.ucenici_text.insert(tk.END, f"{ucenik}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
root.mainloop()








        






        
