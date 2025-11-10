import tkinter as tk
from tkinter import messagebox
import math

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
        w, h = canvas.winfo_width(), canvas.winfo_height()
        canvas.create_text(w/2, h/2, text=self.naziv, fill="gray", font=("Arial", 10, "italic"))


# ===== OBLICI =====

class Krug(Oblik):
    naziv = "Krug"; dimenzije = ["radijus"]
    def izracunaj_povrsinu(self): return math.pi * self.parametri["radijus"]**2
    def izracunaj_opseg(self): return 2 * math.pi * self.parametri["radijus"]
    def nacrtaj(self, c):
        c.delete("all")
        w,h=c.winfo_width(),c.winfo_height(); cx,cy=w/2,h/2; r=min(w,h)*0.35
        c.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#0077cc", width=3)

class Pravokutnik(Oblik):
    naziv="Pravokutnik"; dimenzije=["sirina","visina"]
    def izracunaj_povrsinu(self): a,b=self.parametri["sirina"],self.parametri["visina"]; return a*b
    def izracunaj_opseg(self): a,b=self.parametri["sirina"],self.parametri["visina"]; return 2*(a+b)
    def nacrtaj(self,c):
        c.delete("all")
        w,h=c.winfo_width(),c.winfo_height(); cx,cy=w/2,h/2; rw,rh=w*0.35,h*0.25
        c.create_rectangle(cx - rw, cy - rh, cx + rw, cy + rh, outline="#009933", width=3)

class Kvadrat(Pravokutnik):
    naziv="Kvadrat"; dimenzije=["stranica"]
    def izracunaj_povrsinu(self): return self.parametri["stranica"]**2
    def izracunaj_opseg(self): return 4*self.parametri["stranica"]
    def nacrtaj(self,c):
        c.delete("all")
        w,h=c.winfo_width(),c.winfo_height(); cx,cy=w/2,h/2; s=min(w,h)*0.35
        c.create_rectangle(cx - s, cy - s, cx + s, cy + s, outline="#ffaa00", width=3)

class Kugla(Oblik):
    naziv="Kugla"; dimenzije=["radijus"]; tip="3D"
    def izracunaj_povrsinu(self): return 4*math.pi*self.parametri["radijus"]**2
    def izracunaj_volumen(self): return (4/3)*math.pi*self.parametri["radijus"]**3
    def nacrtaj(self,c):
        c.delete("all")
        w,h=c.winfo_width(),c.winfo_height(); cx,cy=w/2,h/2; r=min(w,h)*0.35
        c.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#33aaff", width=3)
        c.create_oval(cx - r*0.8, cy - r*0.25, cx + r*0.8, cy + r*0.25, outline="#aaddff")

class Kocka(Oblik):
    naziv="Kocka"; dimenzije=["stranica"]; tip="3D"
    def izracunaj_povrsinu(self): return 6*self.parametri["stranica"]**2
    def izracunaj_volumen(self): return self.parametri["stranica"]**3
    def nacrtaj(self,c):
        c.delete("all")
        w,h=c.winfo_width(),c.winfo_height(); cx,cy=w/2,h/2; s=min(w,h)*0.25
        c.create_rectangle(cx - s, cy - s, cx + s, cy + s, outline="#cc6600", width=3)
        c.create_rectangle(cx - s + 20, cy - s - 20, cx + s + 20, cy + s - 20, outline="#cc6600", width=3)
        for line in [(-s,-s,s,-s-20),(s,-s,s+20,-s-20),(s,s,s+20,s-20),(-s,s,-s+20,s-20)]:
            c.create_line(cx+line[0],cy+line[1],cx+line[2],cy+line[3])

class Kvadar(Oblik):
    naziv="Kvadar"; dimenzije=["sirina","visina","dubina"]; tip="3D"
    def izracunaj_povrsinu(self):
        a,b,c=self.parametri["sirina"],self.parametri["visina"],self.parametri["dubina"]
        return 2*(a*b+a*c+b*c)
    def izracunaj_volumen(self):
        a,b,c=self.parametri["sirina"],self.parametri["visina"],self.parametri["dubina"]
        return a*b*c
    def nacrtaj(self,c):
        c.delete("all")
        w,h=c.winfo_width(),c.winfo_height(); cx,cy=w/2,h/2; rw,rh=min(w,h)*0.3,min(w,h)*0.2; offset=30
        c.create_rectangle(cx - rw, cy - rh, cx + rw, cy + rh, outline="#9933ff", width=3)
        c.create_rectangle(cx - rw + offset, cy - rh - offset, cx + rw + offset, cy + rh - offset, outline="#9933ff", width=3)
        for (x1,y1,x2,y2) in [(-rw,-rh,-rw+offset,-rh-offset),(rw,-rh,rw+offset,-rh-offset),
                              (rw,rh,rw+offset,rh-offset),(-rw,rh,-rw+offset,rh-offset)]:
            c.create_line(cx+x1,cy+y1,cx+x2,cy+y2)

OBLICI_2D={"Krug":Krug,"Pravokutnik":Pravokutnik,"Kvadrat":Kvadrat}
OBLICI_3D={"Kugla":Kugla,"Kocka":Kocka,"Kvadar":Kvadar}


# ===== GLAVNI GUI =====

class ShapesyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shapesy")
        self.root.geometry("580x780")
        self.root.configure(bg="#f3f8ff")
        self.root.minsize(480, 720)

        self.vrsta_var = tk.StringVar(value="2D")
        self.oblik_var = tk.StringVar(value="Krug")
        self.polja = {}
        self.zadnji_objekt = None

        # HEADER
        header = tk.Frame(root, bg="#dceeff", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = tk.Canvas(header, width=45, height=45, bg="#ffffff", highlightthickness=0)
        logo.pack(side="left", padx=12, pady=10)
        logo.create_oval(8, 8, 37, 37, outline="#0077cc", width=3)
        logo.create_rectangle(16, 16, 29, 29, outline="#ffaa00", width=2)

        tk.Label(header, text="Shapesy", bg="#dceeff", fg="#003366",
                 font=("Arial Rounded MT Bold", 20, "bold")).pack(side="left", padx=8)

        # --- FRAME UNOS ---
        self.frame_unos = tk.Frame(root, bg="#f7fbff", bd=2, relief="groove")
        self.frame_unos.pack(fill="x", padx=10, pady=8)

        vrsta_frame = tk.Frame(self.frame_unos, bg="#f7fbff")
        vrsta_frame.pack(anchor="w", pady=5)
        tk.Label(vrsta_frame, text="Vrsta oblika:", bg="#f7fbff",
                 fg="#003366", font=("Arial", 11, "bold")).pack(side="left", padx=(10,5))
        for tip in ("2D","3D"):
            tk.Radiobutton(vrsta_frame, text=tip, variable=self.vrsta_var, value=tip,
                           command=self.osvjezi_oblike, bg="#f7fbff").pack(side="left", padx=5)

        # --- Podokvir za izbor oblika i parametre ---
        self.frame_oblici = tk.Frame(self.frame_unos, bg="#f7fbff")
        self.frame_oblici.pack(fill="x", pady=5)

        self.frame_parametri = tk.Frame(self.frame_unos, bg="#f7fbff")
        self.frame_parametri.pack(fill="x", pady=5)

        tk.Button(self.frame_unos, text="Izračunaj", command=self.izracunaj,
                  bg="#0077cc", fg="white", font=("Arial", 11, "bold")).pack(pady=5)

        self.label_povrsina = tk.Label(self.frame_unos, bg="#f7fbff")
        self.label_opseg = tk.Label(self.frame_unos, bg="#f7fbff")
        self.label_volumen = tk.Label(self.frame_unos, bg="#f7fbff")
        self.label_povrsina.pack()
        self.label_opseg.pack()
        self.label_volumen.pack()

        # --- CANVAS ---
        self.canvas = tk.Canvas(root, bg="white", highlightbackground="#99ccff", height=330)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.bind("<Configure>", self.redraw)

        # --- POVIJEST ---
        frame_history = tk.Frame(root, bg="#f7fbff", bd=1, relief="solid")
        frame_history.pack(fill="both", expand=True, padx=10, pady=8)
        tk.Label(frame_history, text="Povijest izračuna:",
                 font=("Arial", 11, "bold"), bg="#f7fbff", fg="#003366").pack(pady=3)
        self.listbox = tk.Listbox(frame_history, bg="white", height=8, selectbackground="#cce5ff")
        self.listbox.pack(fill="both", expand=True, padx=8, pady=5)

        self.osvjezi_oblike()

    # --- osvježi listu oblika ---
    def osvjezi_oblike(self):
        for w in self.frame_oblici.winfo_children(): w.destroy()
        oblici = OBLICI_2D if self.vrsta_var.get() == "2D" else OBLICI_3D
        prvi = list(oblici.keys())[0]
        self.oblik_var.set(prvi)
        tk.Label(self.frame_oblici, text="Odaberi oblik:", bg="#f7fbff",
                 fg="#003366", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=2)
        for naziv in oblici:
            tk.Radiobutton(self.frame_oblici, text=naziv, variable=self.oblik_var, value=naziv,
                           command=self.prikazi_polja, bg="#f7fbff").pack(anchor="w", padx=20)
        self.prikazi_polja()

    # --- prikaz polja ---
    def prikazi_polja(self):
        for w in self.frame_parametri.winfo_children(): w.destroy()
        self.polja = {}
        oblici = OBLICI_2D if self.vrsta_var.get() == "2D" else OBLICI_3D
        klasa = oblici[self.oblik_var.get()]
        for i,d in enumerate(klasa.dimenzije):
            tk.Label(self.frame_parametri, text=f"{d.capitalize()}:", bg="#f7fbff").grid(row=i, column=0, sticky="e", padx=5, pady=3)
            e=tk.Entry(self.frame_parametri, width=10)
            e.grid(row=i, column=1, sticky="w", padx=5, pady=3)
            self.polja[d]=e
        self.frame_parametri.columnconfigure(1, weight=1)
        obj = klasa(**{d:1 for d in klasa.dimenzije})
        obj.nacrtaj(self.canvas)
        self.zadnji_objekt = obj

    # --- izračun ---
    def izracunaj(self):
        try:
            oblici = OBLICI_2D if self.vrsta_var.get() == "2D" else OBLICI_3D
            klasa = obliki[self.oblik_var.get()]
            args = {d: float(e.get()) for d, e in self.polja.items()}
            obj = klasa(**args)
            obj.nacrtaj(self.canvas)
            self.zadnji_objekt = obj
            p,o,v = obj.izracunaj_povrsinu(), obj.izracunaj_opseg(), obj.izracunaj_volumen()
            self.label_povrsina.config(text=f"Površina: {p:.2f}" if p else "")
            self.label_opseg.config(text=f"Opseg: {o:.2f}" if o else "")
            self.label_volumen.config(text=f"Volumen: {v:.2f}" if v else "")
            zapis=f"{obj.naziv}({', '.join(f'{k}={v}' for k,v in args.items())})"
            if p:zapis+=f" P={p:.2f}"
            if o:zapis+=f" O={o:.2f}"
            if v:zapis+=f" V={v:.2f}"
            self.listbox.insert(tk.END, zapis)
        except ValueError:
            messagebox.showerror("Greška", "Unesite ispravne brojeve.")

    # --- ponovno crtanje pri promjeni veličine ---
    def redraw(self, event=None):
        if self.zadnji_objekt:
            self.zadnji_objekt.nacrtaj(self.canvas)


# ===== RUN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = ShapesyApp(root)
    root.mainloop()
