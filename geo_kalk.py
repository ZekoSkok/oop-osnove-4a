from __future__ import annotations
import math
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod


class Oblik:
    def izracunaj_povrsinu(self):
        pass

    def izracunaj_opseg(self):
        pass


class Krug(Oblik):
    def __init__(self, r: float):
        self.r = r

    def izracunaj_povrsinu(self) -> float:
        return math.pi * (self.r ** 2)

    def izracunaj_opseg(self) -> float:
        return 2 * math.pi * self.r


class Pravokutnik(Oblik):
    def __init__(self, sirina: float, visina: float):
        self.sirina = sirina
        self.visina = visina

    def izracunaj_povrsinu(self):
        return self.sirina * self.visina

    def izracunaj_opseg(self):
        return 2 * (self.sirina + self.visina)


class Kvadrat(Pravokutnik):
    def __init__(self, stranica: float):
        super().__init__(stranica, stranica)


def kalkulator():
    root = tk.Tk()
    root.title("Geo Kalkulator — Površina i Opseg")
    root.resizable(False, False)

    pad = 8
    frm = ttk.Frame(root, padding=pad)
    frm.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    oblik_var = tk.StringVar(value="Krug")

    oblici_frame = ttk.LabelFrame(frm, text="Odaberi oblik")
    oblici_frame.grid(column=0, row=0, sticky=tk.W, padx=pad, pady=pad)

    ttk.Radiobutton(oblici_frame, text="Krug", variable=oblik_var, value="Krug", command=lambda: update_inputs()).grid(column=0, row=0, sticky=tk.W, padx=4, pady=2)
    ttk.Radiobutton(oblici_frame, text="Pravokutnik", variable=oblik_var, value="Pravokutnik", command=lambda: update_inputs()).grid(column=1, row=0, sticky=tk.W, padx=4, pady=2)
    ttk.Radiobutton(oblici_frame, text="Kvadrat", variable=oblik_var, value="Kvadrat", command=lambda: update_inputs()).grid(column=2, row=0, sticky=tk.W, padx=4, pady=2)

    # Input polja
    inputs_frame = ttk.LabelFrame(frm, text="Dimenzije")
    inputs_frame.grid(column=0, row=1, sticky=tk.W + tk.E, padx=pad, pady=pad)

    # Radius
    lbl_radius = ttk.Label(inputs_frame, text="Radijus:")
    ent_radius = ttk.Entry(inputs_frame, width=15)

    # Width / Height
    lbl_sirina = ttk.Label(inputs_frame, text="Širina:")
    ent_sirina = ttk.Entry(inputs_frame, width=12)
    lbl_visina = ttk.Label(inputs_frame, text="Visina:")
    ent_visina = ttk.Entry(inputs_frame, width=12)

    # Stranica (kvadrat)
    lbl_stranica = ttk.Label(inputs_frame, text="Stranica:")
    ent_stranica = ttk.Entry(inputs_frame, width=15)

    # Placeholders (grid) — we will grid only relevant widgets in update_inputs

    # Results
    results_frame = ttk.LabelFrame(frm, text="Rezultati")
    results_frame.grid(column=0, row=2, sticky=tk.W + tk.E, padx=pad, pady=pad)

    povrsina_var = tk.StringVar(value="—")
    opseg_var = tk.StringVar(value="—")

    ttk.Label(results_frame, text="Površina:").grid(column=0, row=0, sticky=tk.W, padx=4, pady=2)
    lbl_povrsina = ttk.Label(results_frame, textvariable=povrsina_var)
    lbl_povrsina.grid(column=1, row=0, sticky=tk.W, padx=4, pady=2)

    ttk.Label(results_frame, text="Opseg:").grid(column=0, row=1, sticky=tk.W, padx=4, pady=2)
    lbl_opseg = ttk.Label(results_frame, textvariable=opseg_var)
    lbl_opseg.grid(column=1, row=1, sticky=tk.W, padx=4, pady=2)

    # Calculate button
    btn = ttk.Button(frm, text="Izračunaj", command=lambda: calculate())
    btn.grid(column=0, row=3, sticky=tk.E, padx=pad, pady=(0, pad))


    def clear_inputs():
        ent_radius.delete(0, tk.END)
        ent_sirina.delete(0, tk.END)
        ent_visina.delete(0, tk.END)
        ent_stranica.delete(0, tk.END)


    def osvježi_input():
        for child in inputs_frame.winfo_children():
            child.grid_forget()

        shape = oblik_var.get()
        if shape == "Krug":
            lbl_radius.grid(column=0, row=0, sticky=tk.W, padx=4, pady=2)
            ent_radius.grid(column=1, row=0, sticky=tk.W, padx=4, pady=2)
        elif shape == "Pravokutnik":
            lbl_sirina.grid(column=0, row=0, sticky=tk.W, padx=4, pady=2)
            ent_sirina.grid(column=1, row=0, sticky=tk.W, padx=4, pady=2)
            lbl_visina.grid(column=0, row=1, sticky=tk.W, padx=4, pady=2)
            ent_visina.grid(column=1, row=1, sticky=tk.W, padx=4, pady=2)
        elif shape == "Kvadrat":
            lbl_stranica.grid(column=0, row=0, sticky=tk.W, padx=4, pady=2)
            ent_stranica.grid(column=1, row=0, sticky=tk.W, padx=4, pady=2)

        # Clear previous results and inputs (optional preference)
        povrsina_var.set("—")
        opseg_var.set("—")


    def izracunaj():
        shape = oblik_var.get()
        try:
            if shape == "Krug":
                raw = ent_radius.get().strip()
                if not raw:
                    raise ValueError("Unesite radijus")
                r = float(raw)
                if r < 0:
                    raise ValueError("Radijus ne može biti negativan")
                obj = Krug(r)
            elif shape == "Pravokutnik":
                raw_s = ent_sirina.get().strip()
                raw_v = ent_visina.get().strip()
                if not raw_s or not raw_v:
                    raise ValueError("Unesite širinu i visinu")
                s = float(raw_s)
                v = float(raw_v)
                if s < 0 or v < 0:
                    raise ValueError("Dimenzije ne mogu biti negativne")
                obj = Pravokutnik(s, v)
            elif shape == "Kvadrat":
                raw = ent_stranica.get().strip()
                if not raw:
                    raise ValueError("Unesite duljinu stranice")
                a = float(raw)
                if a < 0:
                    raise ValueError("Duljina stranice ne može biti negativna")
                obj = Kvadrat(a)
            else:
                raise ValueError("Nepoznat oblik")

            p = obj.izracunaj_povrsinu()
            o = obj.izracunaj_opseg()

            povrsina_var.set(f"{p:.4f}")
            opseg_var.set(f"{o:.4f}")

        except ValueError as e:
            messagebox.showerror(title="Pogrešan unos", message=str(e))
        except Exception as e:
            messagebox.showerror(title="Greška", message=f"Došlo je do greške: {e}")

    osvježi_input()

    root.mainloop()


if __name__ == "__main__":
    kalkulator()
