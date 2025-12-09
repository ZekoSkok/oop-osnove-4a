from email.mime import base
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
import xml.etree.ElementTree as ET
import math

from geo_kalk import Cuboid

# ----------------------
#  Styling / Theme
# ----------------------
BG = "#F5FAFF"
PANEL = "#FFFFFF"
ACCENT = "#1E88E5"      # material blue
SUBTLE = "#7B8FA1"
ACTION = "#00C853"      # save btn
WARN = "#FF5252"        # delete btn
BTN_TEXT = "#FFFFFF"
FONT = ("Segoe UI", 10)

# --------------------
#  Base model oblika
# --------------------
class Shape:
    """
    Bazna klasa za sve oblike.
    Podklase definiraju: name, params (lista (key,label,default)), tip ("2D"/"3D")
    Svaka podklasa nadjačava area(), perimeter(), volume() i draw().
    """
    name = "Shape"
    params = []   # [('r','Radius',5), ('a','Side',3)...]
    tip = "2D"

    def __init__(self, **kwargs):
        # params iz kwargs ili default
        self.values = {}
        for key, label, default in self.params:
            try:
                self.values[key] = float(kwargs.get(key, default))
            except Exception:
                # fallback u slučaju greške; spriječava error pri krivom unosu-
                self.values[key] = float(default)

    # placeholder za izračune
    def area(self):
        return None

    def perimeter(self):
        return None

    def volume(self):
        return None

    # centriranje crteža na canavas i skaliranje
    def draw(self, canvas, preview_ratio=0.4):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 10), max(canvas.winfo_height(), 10)
        cx, cy = w/2, h/2
        # default simple placeholder
        canvas.create_text(cx, cy, text=self.name, fill=SUBTLE, font=("Segoe UI", 12))

# --------
#  Oblici
# --------
class Krug(Shape):
    name = "Krug"
    tip = "2D"
    params = [('r', 'Radijus', 5.0)]

    def area(self):
        r = self.values['r']
        return math.pi * r * r

    def perimeter(self):
        r = self.values['r']
        return 2 * math.pi * r

    def draw(self, canvas, preview_ratio=0.4):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 10), max(canvas.winfo_height(), 10)
        cx, cy = w/2, h/2
        base = min(w, h) * preview_ratio
        default = Krug.params[0][2]
        scale = max(0.2, min(3.0, self.values['r'] / default))
        r = base * scale
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=ACCENT, width=3)

class Pravokutnik(Shape):
    name = "Pravokutnik"
    tip = "2D"
    params = [('a', 'Širina', 6.0), ('b', 'Visina', 4.0)]

    def area(self):
        return self.values['a'] * self.values['b']

    def perimeter(self):
        return 2 * (self.values['a'] + self.values['b'])

    def draw(self, canvas, preview_ratio=0.4):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 10), max(canvas.winfo_height(), 10)
        cx, cy = w/2, h/2
        maxdim = max(self.values['a'], self.values['b'], 1.0)
        base = min(w, h) * preview_ratio
        base_w = base * (self.values['a'] / maxdim)
        base_h = base * (self.values['b'] / maxdim)
        canvas.create_rectangle(cx-base_w, cy-base_h, cx+base_w, cy+base_h, outline="#26A69A", width=3)

class Kvadrat(Pravokutnik):
    name = "Kvadrat"
    tip = "2D"
    params = [('a', 'Stranica', 5.0)]

    def area(self):
        return self.values['a'] * self.values['a']
    
    def perimeter(self):
        return 4 * self.values['a']

    def __init__(self, **kwargs):
        # proslijedi Pravokutniku s a=a, b=a
        val = {}
        a = float(kwargs.get('a', Kvadrat.params[0][2]))
        val['a'] = a
        val['b'] = a
        super().__init__(**val)

    def draw(self, canvas, preview_ratio=0.4):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 10), max(canvas.winfo_height(), 10)
        cx, cy = w/2, h/2
        base = min(w, h) * preview_ratio
        default = Kvadrat.params[0][2]
        scale = max(0.2, min(3.0, self.values['a'] / default))
        r = base * scale * 0.7
        canvas.create_rectangle(cx-r, cy-r, cx+r, cy+r, outline="#26A69A", width=3)

class Trapez(Shape):
    name = "Trapez"
    tip = "2D"
    params = [
        ('a', 'Donja baza', 8.0),
        ('b', 'Gornja baza', 5.0),
        ('h', 'Visina', 4.0)
    ]

    def area(self):
        a = self.values['a']
        b = self.values['b']
        h = self.values['h']
        return (a + b) * h / 2

    def perimeter(self):
        a = self.values['a']
        b = self.values['b']
        h = self.values['h']

        # Izračun kosih stranica za jednakokračni trapez
        # s = sqrt((|a-b|/2)^2 + h^2)
        half_diff = abs(a - b) / 2
        s = math.sqrt(half_diff**2 + h**2)

        return a + b + 2 * s

    def draw(self, canvas, preview_ratio=0.5):
        canvas.delete("all")

        w = max(canvas.winfo_width(), 50)
        h_canvas = max(canvas.winfo_height(), 50)
        cx, cy = w / 2, h_canvas / 2

        # OSNOVNO SKALIRANJE
        base = min(w, h_canvas) * preview_ratio

        a = self.values['a']
        b = self.values['b']
        h = self.values['h']

        # Normalizacija
        max_p = max(a, b, h, 1)
        scale = base / max_p

        # Konačne dimenzije
        A = a * scale
        B = b * scale
        H = h * scale

        # Donja baza – centrirano
        x1 = cx - A/2
        x2 = cx + A/2
        y1 = cy + H/2

        # Gornja baza – kraća, pomaknuta prema sredini
        x3 = cx - B/2
        x4 = cx + B/2
        y2 = cy - H/2

        # Crtanje trapeza
        canvas.create_polygon(
            x1, y1,   # donja lijeva
            x2, y1,   # donja desna
            x4, y2,   # gornja desna
            x3, y2,   # gornja lijeva
            outline=ACCENT,
            fill="",
            width=3
        )



class Kugla(Shape):
    name = "Kugla"
    tip = "3D"
    params = [('r', 'Radijus', 4.0)]

    def area(self):
        r = self.values['r']
        return 4 * math.pi * r * r

    def volume(self):
        r = self.values['r']
        return (4/3) * math.pi * r**3

    def draw(self, canvas, preview_ratio=0.35):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 10), max(canvas.winfo_height(), 10)
        cx, cy = w/2, h/2
        base = min(w, h) * preview_ratio
        default = Kugla.params[0][2]
        scale = max(0.2, min(3.0, self.values['r'] / default))
        r = base * scale
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=ACCENT, width=3)
        # luk za 3D efekt
        canvas.create_oval(cx-r, cy-r*0.2, cx+r, cy+r*0.2, outline=SUBTLE)

class Kocka(Shape):
    name = "Kocka"
    tip = "3D"
    params = [('a', 'Stranica', 4.0)]

    def area(self):
        a = self.values['a']
        return 6 * a * a

    def volume(self):
        a = self.values['a']
        return a ** 3

    def draw(self, canvas, preview_ratio=0.45):
        canvas.delete("all")
        w = max(canvas.winfo_width(), 50)
        h = max(canvas.winfo_height(), 50)
        cx, cy = w / 2, h / 2

        # Osnovna veličina previewa
        base = min(w, h) * preview_ratio

        # Skaliranje prema dimenziji (stranica)
        default = Kocka.params[0][2]
        scale = max(0.2, min(3.0, self.values["a"] / default))

        s = base * scale   # duljina stranice
        # Offset za pseudo-3D efekt
        offset = s * 0.4

        # Koordinate prednje stranice (kvadrat)
        x1, y1 = cx - s/2, cy - s/2
        x2, y2 = cx + s/2, cy + s/2

        # Koordinate zadnje stranice (pomaknute)
        x1b, y1b = x1 - offset, y1 - offset
        x2b, y2b = x2 - offset, y2 - offset

        # Crtanje prednjeg kvadrata
        canvas.create_rectangle(x1, y1, x2, y2, outline="#26A69A", width=3)

        # Crtanje zadnjeg kvadrata
        canvas.create_rectangle(x1b, y1b, x2b, y2b, outline="#80CBC4", width=2)

        # Poveznice između stranica
        canvas.create_line(x1, y1, x1b, y1b, fill="#26A69A", width=2)
        canvas.create_line(x2, y1, x2b, y1b, fill="#26A69A", width=2)
        canvas.create_line(x1, y2, x1b, y2b, fill="#26A69A", width=2)
        canvas.create_line(x2, y2, x2b, y2b, fill="#26A69A", width=2)

class Kvadar(Shape):
    name = "Kvadar"
    tip = "3D"
    params = [('a', 'Duljina', 6.0), ('b', 'Širina', 4.0), ('c', 'Visina', 3.0)]

    def area(self):
        a, b, c = self.values['a'], self.values['b'], self.values['c']
        return 2 * (a*b + a*c + b*c)

    def volume(self):
        a, b, c = self.values['a'], self.values['b'], self.values['c']
        return a * b * c

    def draw(self, canvas, preview_ratio=0.45):
        canvas.delete("all")
        w = max(canvas.winfo_width(), 50)
        h = max(canvas.winfo_height(), 50)

        cx, cy = w / 2, h / 2

        # Osnovni preview scale
        base = min(w, h) * preview_ratio

        # Dimenzije oblika
        a = self.values["a"]  # širina
        b = self.values["b"]  # visina
        c = self.values["c"]  # dubina
    
        # Normalizacija na default vrijednosti
        defA, defB, defC = Kvadar.params[0][2], Kvadar.params[1][2], Kvadar.params[2][2]

        scaleA = a / defA
        scaleB = b / defB
        scaleC = c / defC
        # Konačna duljina stranica
        w_front = base * scaleA
        h_front = base * scaleB
        offset = base * 0.35 * scaleC  # dubina

        # Prednja stranica
        x1, y1 = cx - w_front/2, cy - h_front/2
        x2, y2 = cx + w_front/2, cy + h_front/2

        # Zadnja stranica (pomaknuta)
        x1b, y1b = x1 - offset, y1 - offset
        x2b, y2b = x2 - offset, y2 - offset

        # Crtanje prednjeg pravokutnika
        canvas.create_rectangle(x1, y1, x2, y2, outline="#1565C0", width=3)

        # Crtanje stražnjeg pravokutnika
        canvas.create_rectangle(x1b, y1b, x2b, y2b, outline="#90CAF9", width=2)
        # Spajanje bridova
        canvas.create_line(x1, y1, x1b, y1b, fill="#1565C0", width=2)
        canvas.create_line(x2, y1, x2b, y1b, fill="#1565C0", width=2)
        canvas.create_line(x1, y2, x1b, y2b, fill="#1565C0", width=2)
        canvas.create_line(x2, y2, x2b, y2b, fill="#1565C0", width=2)

# registri oblika
SHAPES_2D = {
    Krug.name: Krug,
    Pravokutnik.name: Pravokutnik,
    Kvadrat.name: Kvadrat,
    Trapez.name: Trapez,
}
SHAPES_3D = {
    Kugla.name: Kugla,
    Kocka.name: Kocka,
    Kvadar.name: Kvadar,
}

# ---------------
#  UI Aplikacije
# ---------------
class Shapesy:
    def __init__(self, root):
        self.root = root
        root.title("Shapesy")
        root.configure(bg=BG)
        root.geometry("420x820")  # za fon?!?!?
        root.minsize(360, 640)

        self.current_shape_class = None
        self.current_shape_obj = None
        self.history = []  # list of dicts

        self.build_header()

        # Glavni scrollable container
        self.container = tk.Frame(root, bg=BG)
        self.container.pack(fill="both", expand=True)

        # Canvas for scrolling main content
        self.scroll_canvas = tk.Canvas(self.container, bg=BG, highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.v_scroll = ttk.Scrollbar(self.container, orient="vertical", command=self.scroll_canvas.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.scroll_canvas.configure(yscrollcommand=self.v_scroll.set)

        # Frame INSIDE canvas
        self.main_frame = tk.Frame(self.scroll_canvas, bg=BG)

        # Create window that holds main_frame
        self.scroll_window = self.scroll_canvas.create_window((0, 0),window=self.main_frame,anchor="nw")

        # Proper event bindings
        self.main_frame.bind("<Configure>", self.on_main_frame_configure)
        self.scroll_canvas.bind("<Configure>", self.on_canvas_configure)

        #UI builder
        # Inside __init__
        self.build_shape_selector()
        self.build_param_section()
        self.build_action_row()
        self.build_canvas_preview()
        self.build_history_section()

        # initialize
        self.shape_type_var.set("2D")
        self.refresh_shape_list()


    def on_main_frame_configure(self, event=None):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.scroll_canvas.itemconfig(self.scroll_window, width=event.width)

    # ----------------------
    # header
    # ----------------------
    def build_header(self):
        header = tk.Frame(self.root, bg=BG, pady=8)
        header.pack(fill="x")

        # minimalist calculator logo drawn on small canvas
        logo = tk.Canvas(header, width=44, height=44, bg=BG, highlightthickness=0)
        logo.pack(side="left", padx=12)
        # stylized calculator: rounded rectangle + small screen + two buttons
        logo.create_rectangle(6, 6, 38, 38, outline=ACCENT, width=3)
        logo.create_rectangle(10, 10, 34, 18, outline=ACCENT, width=2)
        logo.create_oval(13, 22, 18, 27, outline=ACCENT, width=2)
        logo.create_oval(24, 22, 29, 27, outline=ACCENT, width=2)

        title = tk.Label(header, text="Shapesy", bg=BG, fg=ACCENT, font=("Segoe UI", 18, "bold"))
        title.pack(side="left")

        # simple hamburger (flat button)
        menu_btn = tk.Button(header, text="☰", bg=BG, fg=SUBTLE, font=("Segoe UI", 16),
                             activebackground=BG, bd=0, command=self.open_menu)
        menu_btn.pack(side="right", padx=12)

    def open_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="O aplikaciji", command=self.show_about)
        menu.add_command(label="Formule", command=self.show_formulas)
        menu.add_command(label="Spremi povijest", command=self.save_xml)
        menu.add_command(label="Učitaj povijest", command=self.load_xml)
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def show_about(self):
        win = tk.Toplevel(self.root)
        win.title("O aplikaciji")
        win.configure(bg=BG)
        tk.Label(win, text="Shapesy\nEdukativni geometrijski kalkulator", font=("Segoe UI", 12, "bold"), bg=BG, fg=ACCENT).pack(padx=16, pady=(12,4))
        tk.Label(win, text="Izračunava površinu/opseg/volumen za osnovne oblike.\nAutomatski prikazuje preview oblika i čuva povijest.\nMožeš spremiti/učitati povijest u XML.", bg=BG, justify="left").pack(padx=12, pady=8)
        tk.Button(win, text="Zatvori", command=win.destroy, bg=ACCENT, fg=BTN_TEXT).pack(pady=10)

    def show_formulas(self):
        win = tk.Toplevel(self.root)
        win.title("Formule")
        win.configure(bg=BG)
        txt = (
            "2D:\n"
            " Krug: P = πr² ; O = 2πr\n"
            " Pravokutnik: P = a·b ; O = 2(a+b)\n"
            " Kvadrat: P = a² ; O = 4a\n\n"
            "3D:\n"
            " Kugla: Površina = 4πr² ; Volumen = 4/3 πr³\n"
            " Kocka: Površina = 6a² ; Volumen = a³\n"
            " Kvadar: Površina = 2(ab+ac+bc) ; Volumen = a·b·c\n"
        )
        ttk.Label(win, text="Formule", font=("Segoe UI", 12, "bold")).pack(pady=8)
        st = scrolledtext.ScrolledText(win, height=12, width=48)
        st.insert("1.0", txt)
        st.configure(state="disabled")
        st.pack(padx=8, pady=8)

    # ----------------------
    # Helpers for scroll
    # ----------------------
    def on_frame_configure(self):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        # make canvas width follow root width
        self.scroll_canvas.itemconfig(self.scroll_window, width=self.scroll_canvas.winfo_width())

    # ----------------------
    # Shape selection (type + list)
    # ----------------------
    def build_shape_selector(self):
        box = tk.Frame(self.main_frame, bg=BG, pady=6)
        box.pack(fill="x", padx=12)

        tk.Label(box, text="Vrsta oblika", bg=BG, fg=SUBTLE, font=FONT).pack(anchor="w")

        self.shape_type_var = tk.StringVar(value="2D")
        btn_row = tk.Frame(box, bg=BG)
        btn_row.pack(fill="x", pady=6)
        rb2 = tk.Radiobutton(btn_row, text="2D", variable=self.shape_type_var, value="2D",
                             command=self.refresh_shape_list, bg=BG)
        rb3 = tk.Radiobutton(btn_row, text="3D", variable=self.shape_type_var, value="3D",
                             command=self.refresh_shape_list, bg=BG)
        rb2.pack(side="left", padx=6)
        rb3.pack(side="left", padx=6)

        # list of shapes
        self.shape_list_frame = tk.Frame(box, bg=BG)
        self.shape_list_frame.pack(fill="x", pady=(4,0))

    def refresh_shape_list(self):
        for w in self.shape_list_frame.winfo_children():
            w.destroy()
        typ = self.shape_type_var.get()
        shapes = SHAPES_2D if typ == "2D" else SHAPES_3D
        self.shape_name_var = tk.StringVar()
        first = True
        for name, cls in shapes.items():
            rb = tk.Radiobutton(self.shape_list_frame, text=name, variable=self.shape_name_var, value=name,
                                command=self.on_shape_selected, bg=BG, anchor="w")
            rb.pack(fill="x", padx=6, pady=2)
            if first:
                self.shape_name_var.set(name)
                first = False
        # draw initial preview
        self.on_shape_selected()

    # ----------------------
    # Parameter section (dynamic from class params)
    # ----------------------
    def build_param_section(self):
        box = tk.Frame(self.main_frame, bg=BG, pady=6)
        box.pack(fill="x", padx=12)
        tk.Label(box, text="Parametri", bg=BG, fg=SUBTLE, font=FONT).pack(anchor="w")
        self.params_frame = tk.Frame(box, bg=BG)
        self.params_frame.pack(fill="x", pady=6)

    def on_shape_selected(self):
        # called whenever a shape radio is clicked
        typ = self.shape_type_var.get()
        name = getattr(self, "shape_name_var", tk.StringVar(master=self.root, value="")).get()
        if not name:
            return
        cls = (SHAPES_2D if typ == "2D" else SHAPES_3D).get(name)
        self.current_shape_class = cls
        # instantiate with defaults for preview
        defaults = {k: d for k, _, d in cls.params}
        self.current_shape_obj = cls(**defaults)
        # draw preview
        self.draw_preview()
        # refresh param entries
        self.render_param_entries()

    def render_param_entries(self):
        for w in self.params_frame.winfo_children():
            w.destroy()
        self.parameter_vars = {}
        cls = self.current_shape_class
        if not cls:
            return
        for key, label, default in cls.params:
            row = tk.Frame(self.params_frame, bg=BG)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, width=12, anchor="w", bg=BG).pack(side="left")
            var = tk.StringVar(value=str(default))
            ent = tk.Entry(row, textvariable=var, font=FONT)
            ent.pack(side="left", fill="x", expand=True, padx=6)
            self.parameter_vars[key] = var
            # draw live preview when entry changes (after focus out)
            ent.bind("<FocusOut>", lambda e: self.update_preview_from_params())

    def update_preview_from_params(self):
        # read values, ignore errors, use defaults on invalid
        values = {}
        for k, var in self.parameter_vars.items():
            try:
                values[k] = float(var.get())
            except:
                # fallback to class default
                for kk, lbl, d in self.current_shape_class.params:
                    if kk == k:
                        values[k] = float(d)
                        break
        # instantiate and draw
        self.current_shape_obj = self.current_shape_class(**values)
        self.draw_preview()

    # ----------------------
    # Action row (calculate, repeat, delete)
    # ----------------------
    def build_action_row(self):
        box = tk.Frame(self.main_frame, bg=BG, pady=6)
        box.pack(fill="x", padx=12)

        calc_btn = tk.Button(box, text="Izračunaj", bg=ACCENT, fg=BTN_TEXT, font=FONT,
                             command=self.calculate_shape, width=12)
        calc_btn.pack(side="left", padx=4)

        repeat_btn = tk.Button(box, text="Ponovi iz povijesti", bg="#FFA726", fg=BTN_TEXT, font=FONT,
                               command=self.repeat_from_history)
        repeat_btn.pack(side="left", padx=4)

        delete_btn = tk.Button(box, text="Obriši zapis", bg=WARN, fg=BTN_TEXT, font=FONT,
                               command=self.delete_history_item)
        delete_btn.pack(side="left", padx=4)

    # ----------------------
    # Canvas preview
    # ----------------------
    def build_canvas_preview(self):
        box = tk.Frame(self.main_frame, bg=BG, pady=6)
        box.pack(fill="both", expand=False, padx=12)
        tk.Label(box, text="Preview oblika", bg=BG, fg=SUBTLE, font=FONT).pack(anchor="w")
        self.preview_canvas = tk.Canvas(box, bg=PANEL, height=260, highlightthickness=1, highlightbackground="#E3F2FD")
        self.preview_canvas.pack(fill="both", expand=True, pady=6)
        # redraw on resize
        self.preview_canvas.bind("<Configure>", lambda e: self.draw_preview())

    def draw_preview(self):
        if self.current_shape_obj:
            # try to draw using values from parameter_vars if present
            if hasattr(self, "parameter_vars") and self.parameter_vars:
                vals = {}
                for k, var in self.parameter_vars.items():
                    try:
                        vals[k] = float(var.get())
                    except:
                        # fallback to default
                        for kk, lbl, d in self.current_shape_class.params:
                            if kk == k:
                                vals[k] = float(d)
                obj = self.current_shape_class(**vals)
                obj.draw(self.preview_canvas)
            else:
                self.current_shape_obj.draw(self.preview_canvas)

    # ----------------------
    # History UI (list, save/load)
    # ----------------------
    def build_history_section(self):
        box = tk.Frame(self.main_frame, bg=BG, pady=6)
        box.pack(fill="both", expand=True, padx=12, pady=(6,20))
        tk.Label(box, text="Povijest izračuna", bg=BG, fg=SUBTLE, font=FONT).pack(anchor="w")
        self.history_list = tk.Listbox(box, height=8)
        self.history_list.pack(fill="both", expand=True, pady=6)
    
    # ----------------------
    # Calculation / history logic
    # ----------------------
    def calculate_shape(self):
        if not self.current_shape_class:
            messagebox.showerror("Greška", "Odaberite oblik.")
            return
        # gather params
        kwargs = {}
        for key, _, default in self.current_shape_class.params:
            if hasattr(self, "parameter_vars") and key in self.parameter_vars:
                try:
                    kwargs[key] = float(self.parameter_vars[key].get())
                except:
                    kwargs[key] = float(default)
            else:
                kwargs[key] = float(default)
        obj = self.current_shape_class(**kwargs)
        area = obj.area()
        perim = obj.perimeter()
        vol = obj.volume()
        # text result
        parts = []
        if area is not None:
            parts.append(f"Površina: {area:.3f}")
        if perim is not None:
            parts.append(f"Opseg: {perim:.3f}")
        if vol is not None:
            parts.append(f"Volumen: {vol:.3f}")
        result_text = " | ".join(parts) if parts else "Nije definirano"
        # push to history (structured)
        hist_item = {
            "shape": self.current_shape_class.name,
            "type": self.current_shape_class.tip,
            "params": kwargs,
            "area": area,
            "perimeter": perim,
            "volume": vol,
            "text": result_text
        }
        self.history.append(hist_item)
        # display summary
        display = f"{hist_item['shape']} {hist_item['params']} → {result_text}"
        self.history_list.insert(tk.END, display)
        # set current object and redraw preview to use entered params
        self.current_shape_obj = obj
        self.draw_preview()

    def repeat_from_history(self):
        sel = self.history_list.curselection()
        if not sel:
            messagebox.showinfo("Info", "Odaberite zapis u povijesti.")
            return
        idx = sel[0]
        item = self.history[idx]
        # set shape type and selected shape
        typ = item['type']
        if typ == "2D":
            self.shape_type_var.set("2D")
        else:
            self.shape_type_var.set("3D")
        self.refresh_shape_list()
        self.shape_name_var.set(item['shape'])
        # set param entries
        self.on_shape_selected()
        for k, v in item['params'].items():
            if k in self.parameter_vars:
                self.parameter_vars[k].set(str(v))
        # perform calculation (which will also redraw)
        self.calculate_shape()

    def delete_history_item(self):
        sel = self.history_list.curselection()
        if not sel:
            messagebox.showinfo("Info", "Odaberite zapis da obrišete.")
            return
        idx = sel[0]
        self.history_list.delete(idx)
        self.history.pop(idx)

    # ----------------------
    # XML save/load (structured)
    # ----------------------
    def save_xml(self):
        if not self.history:
            messagebox.showinfo("Info", "Povijest je prazna.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if not path:
            return
        root = ET.Element("History")
        for it in self.history:
            e = ET.SubElement(root, "Entry", shape=it['shape'], type=it['type'])
            params = ET.SubElement(e, "Params")
            for k, v in it['params'].items():
                p = ET.SubElement(params, "Param", name=k)
                p.text = str(v)
            if it['area'] is not None:
                ET.SubElement(e, "Area").text = str(it['area'])
            if it['perimeter'] is not None:
                ET.SubElement(e, "Perimeter").text = str(it['perimeter'])
            if it['volume'] is not None:
                ET.SubElement(e, "Volume").text = str(it['volume'])
        tree = ET.ElementTree(root)
        tree.write(path, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("OK", "Povijest spremljena u XML.")

    def load_xml(self):
        path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if not path:
            return
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            self.history.clear()
            self.history_list.delete(0, tk.END)
            for entry in root.findall("Entry"):
                shape_name = entry.get("shape")
                typ = entry.get("type", "2D")
                # params
                params_node = entry.find("Params")
                params = {}
                if params_node is not None:
                    for p in params_node.findall("Param"):
                        name = p.get("name")
                        try:
                            params[name] = float(p.text)
                        except:
                            params[name] = p.text
                area_node = entry.find("Area")
                per_node = entry.find("Perimeter")
                vol_node = entry.find("Volume")
                area = float(area_node.text) if area_node is not None else None
                perim = float(per_node.text) if per_node is not None else None
                vol = float(vol_node.text) if vol_node is not None else None
                text_parts = []
                if area is not None: text_parts.append(f"P={area:.3f}")
                if perim is not None: text_parts.append(f"O={perim:.3f}")
                if vol is not None: text_parts.append(f"V={vol:.3f}")
                display = f"{shape_name} {params} → {' | '.join(text_parts)}"
                self.history.append({
                    "shape": shape_name,
                    "type": typ,
                    "params": params,
                    "area": area,
                    "perimeter": perim,
                    "volume": vol,
                    "text": " | ".join(text_parts)
                })
                self.history_list.insert(tk.END, display)
            messagebox.showinfo("OK", "XML učitan.")
        except Exception as e:
            messagebox.showerror("Greška", f"Neuspjelo učitavanje XML: {e}")

# ----------------------
#  Run
# ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Shapesy(root)
    root.mainloop()
