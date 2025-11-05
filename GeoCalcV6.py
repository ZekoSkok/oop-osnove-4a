import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel
import math
import xml.etree.ElementTree as ET

# ===== MODEL =====

class Oblik:
    naziv = "Oblik"
    dimenzije = []
    tip = "2D"

    def __init__(self, **kwargs):
        self.parametri = kwargs

    def izracunaj_povrsinu(self): raise NotImplementedError
    def izracunaj_opseg(self): return None
    def izracunaj_volumen(self): return None

    def nacrtaj(self, canvas):
        canvas.delete("all")
        canvas.create_text(100, 100, text=f"{self.naziv}", fill="gray", font=("Arial", 10, "italic"))

# ===== OBLICI =====

class Krug(Oblik):
    naziv = "Krug"
    dimenzije = ["radijus"]
    def izracunaj_povrsinu(self): return math.pi * self.parametri["radijus"]**2
    def izracunaj_opseg(self): return 2 * math.pi * self.parametri["radijus"]
    def nacrtaj(self, canvas):
        canvas.delete("all")
        canvas.create_oval(30, 30, 170, 170, outline="#0077cc", width=3)

class Pravokutnik(Oblik):
    naziv = "Pravokutnik"
    dimenzije = ["sirina", "visina"]
    def izracunaj_povrsinu(self):
        a, b = self.parametri["sirina"], self.parametri["visina"]
        return a * b
    def izracunaj_opseg(self):
        a, b = self.parametri["sirina"], self.parametri["visina"]
        return 2 * (a + b)
    def nacrtaj(self, canvas):
        canvas.delete("all")
        canvas.create_rectangle(40, 70, 160, 130, outline="#009933", width=3)

class Kvadrat(Pravokutnik):
    naziv = "Kvadrat"
    dimenzije = ["stranica"]
    def izracunaj_povrsinu(self): return self.parametri["stranica"]**2
    def izracunaj_opseg(self): return 4 * self.parametri["stranica"]
    def nacrtaj(self, canvas):
        canvas.delete("all")
        canvas.create_rectangle(60, 60, 140, 140, outline="#ffaa00", width=3)

class Kugla(Oblik):
    naziv = "Kugla"
    dimenzije = ["radijus"]
    tip = "3D"
    def izracunaj_povrsinu(self): return 4 * math.pi * self.parametri["radijus"]**2
    def izracunaj_volumen(self): return (4/3) * math.pi * self.parametri["radijus"]**3
    def nacrtaj(self, canvas):
        canvas.delete("all")
        canvas.create_oval(30, 30, 170, 170, outline="#33aaff", width=3)
        canvas.create_oval(50, 80, 150, 120, outline="#aaddff")

class Kocka(Oblik):
    naziv = "Kocka"
    dimenzije = ["stranica"]
    tip = "3D"
    def izracunaj_povrsinu(self): return 6 * self.parametri["stranica"]**2
    def izracunaj_volumen(self): return self.parametri["stranica"]**3
    def nacrtaj(self, canvas):
        canvas.delete("all")
        canvas.create_rectangle(50, 80, 130, 160, outline="#cc6600", width=3)
        canvas.create_rectangle(70, 60, 150, 140, outline="#cc6600", width=3)
        canvas.create_line(50,80,70,60); canvas.create_line(130,80,150,60)
        canvas.create_line(130,160,150,140); canvas.create_line(50,160,70,140)

class Kvadar(Oblik):
    naziv = "Kvadar"
    dimenzije = ["sirina", "visina", "dubina"]
    tip = "3D"
    def izracunaj_povrsinu(self):
        a,b,c = self.parametri["sirina"], self.parametri["visina"], self.parametri["dubina"]
        return 2*(a*b+a*c+b*c)
    def izracunaj_volumen(self):
        a,b,c = self.parametri["sirina"], self.parametri["visina"], self.parametri["dubina"]
        return a*b*c
    def nacrtaj(self, canvas):
        canvas.delete("all")
        canvas.create_rectangle(50,90,150,150, outline="#9933ff", width=3)
        canvas.create_rectangle(70,70,170,130, outline="#9933ff", width=3)
        canvas.create_line(50,90,70,70); canvas.create_line(150,90,170,70)
        canvas.create_line(150,150,170,130); canvas.create_line(50,150,70,130)

OBLICI = {
    "Krug": Krug, "Pravokutnik": Pravokutnik, "Kvadrat": Kvadrat,
    "Kugla": Kugla, "Kocka": Kocka, "Kvadar": Kvadar
}


# ===== GUI =====

class KalkulatorOblika:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoKalk – Pametni kalkulator 2D i 3D oblika")
        self.root.geometry("880x650")
        self.root.configure(bg="#f0f7ff")
        self.root.minsize(700, 550)
        self.oblik_var = tk.StringVar(value="Krug")
        self.povijest = []

        # ====== Gornji panel ======
        top_frame = tk.Frame(root, bg="#cce5ff", relief="ridge", bd=2)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        tk.Label(top_frame, text="🧮 GeoKalk – Kalkulator geometrijskih oblika",
                 font=("Arial", 16, "bold"), bg="#cce5ff", fg="#003366").pack(side="left", padx=10, pady=10)

        # Burger meni
        menubutton = tk.Menubutton(top_frame, text="☰", font=("Arial", 14, "bold"), bg="#cce5ff", relief="flat")
        menu = tk.Menu(menubutton, tearoff=0)
        menu.add_command(label="O aplikaciji", command=self.o_aplikaciji)
        menu.add_command(label="Formule", command=self.formule)
        menubutton["menu"] = menu
        menubutton.pack(side="right", padx=15, pady=5)

        # ====== Lijevi panel (odabir i unos) ======
        left_frame = tk.Frame(root, bg="#f7fbff", bd=1, relief="solid")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(left_frame, text="Odaberi oblik:", font=("Arial", 12, "bold"), bg="#f7fbff", fg="#003366").pack(anchor="w", padx=10, pady=5)
        for naziv in OBLICI:
            tk.Radiobutton(left_frame, text=naziv, variable=self.oblik_var, value=naziv,
                           command=self.prikazi_polja, bg="#f7fbff").pack(anchor="w", padx=20)

        self.frame_unos = tk.Frame(left_frame, bg="#f7fbff")
        self.frame_unos.pack(pady=10)

        self.canvas = tk.Canvas(left_frame, width=200, height=200, bg="white", highlightbackground="#99ccff")
        self.canvas.pack(pady=10)

        tk.Button(left_frame, text="Izračunaj", command=self.izracunaj,
                  bg="#0077cc", fg="white", font=("Arial", 11, "bold"), relief="raised").pack(pady=5)

        self.label_povrsina = tk.Label(left_frame, text="", font=("Arial", 10), bg="#f7fbff")
        self.label_opseg = tk.Label(left_frame, text="", font=("Arial", 10), bg="#f7fbff")
        self.label_volumen = tk.Label(left_frame, text="", font=("Arial", 10), bg="#f7fbff")
        self.label_povrsina.pack()
        self.label_opseg.pack()
        self.label_volumen.pack()

        # ====== Desni panel (povijest i akcije) ======
        right_frame = tk.Frame(root, bg="#f7fbff", bd=1, relief="solid")
        right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(right_frame, text="Povijest izračuna:", font=("Arial", 12, "bold"), bg="#f7fbff", fg="#003366").pack(pady=5)
        self.listbox = tk.Listbox(right_frame, width=70, height=15, bg="#ffffff", selectbackground="#cce5ff")
        self.listbox.pack(padx=10, pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(right_frame, bg="#f7fbff")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Spremi u XML", command=self.spremi_povijest, bg="#339933", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Učitaj XML", command=self.ucitaj_povijest, bg="#33aaff", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Ponovi izračun", command=self.ponovi_izracun, bg="#ffaa00", fg="black").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Obriši", command=self.obrisi_zapis, bg="#ff4444", fg="white").grid(row=0, column=3, padx=5)

        # ====== GRID POSTAVKE (RESPONZIVNOST) ======
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)
        root.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)

        self.polja = {}
        self.prikazi_polja()

    # --- Dinamički prikaz polja ---
    def prikazi_polja(self):
        for widget in self.frame_unos.winfo_children():
            widget.destroy()
        self.polja = {}
        oblik = OBLICI[self.oblik_var.get()]
        for i, dim in enumerate(oblik.dimenzije):
            tk.Label(self.frame_unos, text=f"{dim.capitalize()}:", bg="#f7fbff").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            e = tk.Entry(self.frame_unos)
            e.grid(row=i, column=1, padx=5, pady=5)
            self.polja[dim] = e
        oblik(**{d: 1 for d in oblik.dimenzije}).nacrtaj(self.canvas)
        self.label_povrsina.config(text=""); self.label_opseg.config(text=""); self.label_volumen.config(text="")

    # --- Izračun ---
    def izracunaj(self):
        try:
            oblik_klasa = OBLICI[self.oblik_var.get()]
            args = {d: float(e.get()) for d, e in self.polja.items()}
            obj = oblik_klasa(**args)
            obj.nacrtaj(self.canvas)
            p, o, v = obj.izracunaj_povrsinu(), obj.izracunaj_opseg(), obj.izracunaj_volumen()
            self.label_povrsina.config(text=f"Površina: {p:.2f}" if p else "")
            self.label_opseg.config(text=f"Opseg: {o:.2f}" if o else "")
            self.label_volumen.config(text=f"Volumen: {v:.2f}" if v else "")
            zapis = f"{obj.naziv}({', '.join(f'{k}={v}' for k,v in args.items())}):"
            if p: zapis += f" P={p:.2f}"
            if o: zapis += f" O={o:.2f}"
            if v: zapis += f" V={v:.2f}"
            self.listbox.insert(tk.END, zapis)
        except ValueError:
            messagebox.showerror("Greška", "Unesite ispravne brojčane vrijednosti.")
            
    # ----- Ponovi izračun -----
    def ponovi_izracun(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Molimo odaberite zapis iz povijesti.")
            return

        zapis = self.povijest[sel[0]]
        self.oblik_var.set(zapis["oblik"])
        self.prikazi_polja()

        for dim, val in zapis["parametri"].items():
            if dim in self.polja:
                self.polja[dim].delete(0, tk.END)
                self.polja[dim].insert(0, str(val))

        self.izracunaj()

    # --- Brisanje ---
    def obrisi_zapis(self):
        sel = self.listbox.curselection()
        if sel: self.listbox.delete(sel)
        self.canvas.delete("all")
        for e in self.polja.values(): e.delete(0, tk.END)
        self.label_povrsina.config(text=""); self.label_opseg.config(text=""); self.label_volumen.config(text="")

    # --- XML spremanje / učitavanje ---
    def spremi_povijest(self):
        fname = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML datoteke","*.xml")])
        if not fname: return
        root = ET.Element("Povijest")
        for item in self.listbox.get(0, tk.END):
            ET.SubElement(root, "Zapis").text = item
        ET.ElementTree(root).write(fname, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Uspjeh", "Povijest spremljena.")

    def ucitaj_povijest(self):
        fname = filedialog.askopenfilename(filetypes=[("XML datoteke","*.xml")])
        if not fname: return
        try:
            tree = ET.parse(fname)
            self.listbox.delete(0, tk.END)
            for elem in tree.getroot().findall("Zapis"):
                self.listbox.insert(tk.END, elem.text)
            messagebox.showinfo("Uspjeh", "Povijest učitana.")
        except Exception as e:
            messagebox.showerror("Greška", f"Neuspjelo učitavanje: {e}")

    # --- O aplikaciji ---
    def o_aplikaciji(self):
        t = Toplevel(self.root); t.title("O aplikaciji"); t.geometry("420x250")
        tk.Label(t, text="📘 O aplikaciji", font=("Arial", 14, "bold")).pack(pady=10)
        msg = (
            "GeoKalk omogućuje izračun površine, opsega i volumena\n"
            "za 2D i 3D oblike uz jednostavno, responzivno sučelje.\n"
            "Rezultate možete spremiti i ponovno učitati iz XML datoteke."
        )
        tk.Label(t, text=msg, justify="center").pack(padx=20, pady=10)

    # --- Formule ---
    def formule(self):
        t = Toplevel(self.root); t.title("Formule"); t.geometry("430x400")
        tk.Label(t, text="🧮 Formule", font=("Arial", 14, "bold")).pack(pady=10)
        text = (
            "2D:\n Krug: P=πr², O=2πr\n Pravokutnik: P=a×b, O=2(a+b)\n Kvadrat: P=a², O=4a\n\n"
            "3D:\n Kugla: P=4πr², V=(4/3)πr³\n Kocka: P=6a², V=a³\n Kvadar: P=2(ab+ac+bc), V=a×b×c"
        )
        tk.Label(t, text=text, justify="left").pack(padx=20, pady=10)


# ===== POKRETANJE =====
if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorOblika(root)
    root.mainloop()
