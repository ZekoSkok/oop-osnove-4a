import tkinter as tk
import csv
import xml.etree.ElementTree as et
from xml.dom import minidom

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
        self.izmijeni_gumb.grid(row=3, column=2, columnspan=2, pady=5)

        # Widgeti za prikaz
        self.lista_label = tk.Label(prikaz_frame, text="Popis učenika:")
        self.lista_label.pack(anchor='nw', padx=10, pady=10)

        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.listbox.bind("<<ListboxSelect>>", self.odaberi_ucenika)

        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.csv_gumb =  tk.Button(unos_frame, text='Spremi csv', command=self.spremi_csv)
        self.csv_gumb.grid(row=4, column=0, columnspan=2, pady=5)
        self.csv_ucitaj = tk.Button(unos_frame, text='Učitaj csv', command=self.ucitaj_csv)
        self.csv_ucitaj.grid(row=4, column=2, columnspan=2, pady=5)

        self.xml_spremi = tk.Button(unos_frame, text='Spremi xml', command=self.spremi_xml)
        self.xml_spremi.grid(row=5, column=0, columnspan=2, pady=5)
        self.xml_ucitaj = tk.Button(unos_frame, text='Učitaj xml', command=self.ucitaj_xml)
        self.xml_ucitaj.grid(row=5, column=2, columnspan=2, pady=5)
        

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
        
        
    def spremi_csv(self):

        with open('ucenici.csv', 'w', newline='') as csvfile:
            polja= ['Ime', 'Prezime', 'Razred']
            writer = csv.DictWriter(csvfile, fieldnames=polja)
            writer.writeheader()
            for u in self.ucenici:
                writer.writerow({'Ime': u.ime, 'Prezime': u.prezime, 'Razred': u.razred})
        print(f'Spremljeno u ucenici.csv')

    def ucitaj_csv(self):
        ucitani_ucenici = []
        with open('ucenici.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ucitani_ucenici.append(Ucenik(row['Ime'], row['Prezime'], row['Razred']))
        self.ucenici = ucitani_ucenici
        self.refresh()
        print("Učenici učitani iz 'ucenici.csv'")
        return ucitani_ucenici
    
    def spremi_xml(self):
        root = et.Element('ucenici')
        for u in self.ucenici:
            ucenik_el = et.SubElement(root, 'ucenik')
            et.SubElement(ucenik_el, 'ime').text = u.ime
            et.SubElement(ucenik_el, 'prezime').text = u.prezime
            et.SubElement(ucenik_el, 'razred').text = u.razred

        xml_str = et.tostring(root, encoding='utf-8', method='xml')
        dom = minidom.parseString(xml_str)
        xml_str = dom.toprettyxml(indent=' ')

        with open('ucenici.xml', 'w', encoding='utf-8') as dat:
            dat.write(xml_str)
        
        print(f'Spremljeno u ucenici.xml')

    def ucitaj_xml(self):
        ucitano = []
        tree = et.parse('ucenici.xml')
        root = tree.getroot()

        for ucenik_el in root.findall('ucenik'):
            ime = ucenik_el.find('ime').text
            prezime = ucenik_el.find('prezime').text
            razred = ucenik_el.find('razred').text
            ucitano.append(Ucenik(ime, prezime, razred))
        
        self.ucenici = ucitano
        self.refresh() 
        print(f'Učitano iz ucenici.xml')
        return ucitano 



            




if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()
