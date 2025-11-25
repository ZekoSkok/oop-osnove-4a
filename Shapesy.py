import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
import xml.etree.ElementTree as ET
import math

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

# ----------------------
#  Shape model base
# ----------------------
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
        # fill params from kwargs; if missing, use default from class
        self.values = {}
        for key, label, default in self.params:
            try:
                self.values[key] = float(kwargs.get(key, default))
            except Exception:
                # fallback in case of bad conversion
                self.values[key] = float(default)

    # geometry methods: override as appropriate
    def area(self):
        return None

    def perimeter(self):
        return None

    def volume(self):
        return None

    # draw on given canvas; must center drawing and use canvas size
    # preview_ratio: how big relative to canvas (0..0.5)
    def draw(self, canvas, preview_ratio=0.4):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 10), max(canvas.winfo_height(), 10)
        cx, cy = w/2, h/2
        # default simple placeholder
        canvas.create_text(cx, cy, text=self.name, fill=SUBTLE, font=("Segoe UI", 12))

# ----------------------
#  Concrete shapes
# ----------------------
class Circle(Shape):
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
        # scale by ratio of param/default
        default = Circle.params[0][2]
        scale = max(0.2, min(3.0, self.values['r'] / default))
        r = base * scale
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=ACCENT, width=3)

class Rectangle(Shape):
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

class Square(Rectangle):
    name = "Kvadrat"
    tip = "2D"
    params = [('a', 'Stranica', 5.0)]

    def __init__(self, **kwargs):
        # forward to Rectangle with a=a, b=a
        val = {}
        a = float(kwargs.get('a', Square.params[0][2]))
        val['a'] = a
        val['b'] = a
        super().__init__(**val)

class Sphere(Shape):
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
        default = Sphere.params[0][2]
        scale = max(0.2, min(3.0, self.values['r'] / default))
        r = base * scale
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=ACCENT, width=3)
        # simple shading arc
        canvas.create_oval(cx-r*0.6, cy-r*0.2, cx+r*0.6, cy+r*0.2, outline=SUBTLE)

class Cube(Shape):
    name = "Kocka"
    tip = "3D"
    params = [('a', 'Stranica', 4.0)]

    def area(self):
        a = self.values['a']
        return 6 * a * a

    def volume(self):
        a = self.values['a']
        return a ** 3

    def draw(self, canvas, preview_ratio=0.32):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 10), max(canvas.winfo_height(), 10)
        cx, cy = w/2, h/2
        base = min(w, h) * preview_ratio
        default = Cube.params[0][2]
        scale = max(0.3, min(2.5, self.values['a'] / default))
        s = base * scale
        offset = s * 0.35
        # front square
        canvas.create_rectangle(cx - s, cy - s, cx + s, cy + s, outline="#8E24AA", width=3)
        # back square offset up-left
        canvas.create_rectangle(cx - s - offset, cy - s - offset, cx + s - offset, cy + s - offset, outline="#8E24AA", width=2)
        # connect
        canvas.create_line(cx - s, cy - s, cx - s - offset, cy - s - offset)
        canvas.create_line(cx + s, cy - s, cx + s - offset, cy - s - offset)
        canvas.create_line(cx + s, cy + s, cx + s - offset, cy + s - offset)
        canvas.create_line(cx - s, cy + s, cx - s - offset, cy + s - offset)

class Cuboid(Shape):
    name = "Kvadar"
    tip = "3D"
    params = [('a', 'Duljina', 6.0), ('b', 'Širina', 4.0), ('c', 'Visina', 3.0)]

    def area(self):
        a, b, c = self.values['a'], self.values['b'], self.values['c']
        return 2 * (a*b + a*c + b*c)

    def volume(self):
        a, b, c = self.values['a'], self.values['b'], self.values['c']
        return a * b * c

    def draw(self, canvas, preview_ratio=0.32):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 10), max(canvas.winfo_height(), 10)
        cx, cy = w/2, h/2
        base = min(w, h) * preview_ratio
        # normalize by largest param
        maxp = max(self.values['a'], self.values['b'], self.values['c'], 1.0)
        rw = base * (self.values['a'] / maxp)
        rh = base * (self.values['b'] / maxp)
        offset = base * 0.28 * (self.values['c'] / maxp)
        # front
        canvas.create_rectangle(cx - rw, cy - rh, cx + rw, cy + rh, outline="#FF7043", width=3)
        # back
        canvas.create_rectangle(cx - rw - offset, cy - rh - offset, cx + rw - offset, cy + rh - offset, outline="#FF7043", width=2)
        # connect
        canvas.create_line(cx - rw, cy - rh, cx - rw - offset, cy - rh - offset)
        canvas.create_line(cx + rw, cy - rh, cx + rw - offset, cy - rh - offset)
        canvas.create_line(cx + rw, cy + rh, cx + rw - offset, cy + rh - offset)
        canvas.create_line(cx - rw, cy + rh, cx - rw - offset, cy + rh - offset)

# registries
SHAPES_2D = {
    Circle.name: Circle,
    Rectangle.name: Rectangle,
    Square.name: Square,
}
SHAPES_3D = {
    Sphere.name: Sphere,
    Cube.name: Cube,
    Cuboid.name: Cuboid,
}

# ----------------------
#  Main App UI
# ----------------------
class Shapesy:
    def __init__(self, root):
        self.root = root
        root.title("Shapesy")
        root.configure(bg=BG)
        root.geometry("420x820")  # mobile-friendly portrait
        root.minsize(360, 640)

        self.current_shape_class = None
        self.current_shape_obj = None
        self.history = []  # list of dicts

        # top frame (logo + title + menu)
        self.build_header()

        # -------- Main container with scrolling (fixed version) --------
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

    def on_main_frame_configure(self, event=None):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.scroll_canvas.itemconfig(self.scroll_window, width=event.width)

        # Build UI sections stacked vertically
        self.build_shape_selector()
        self.build_param_section()
        self.build_action_row()
        self.build_canvas_preview()
        self.build_history_section()

        # initialize
        self.shape_type_var.set("2D")
        self.refresh_shape_list()

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
        delete_btn.pack(side="right", padx=4)

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
        # save/load buttons
        row = tk.Frame(box, bg=BG)
        row.pack(fill="x")
        save_btn = tk.Button(row, text="Spremi XML", bg=ACTION, fg=BTN_TEXT, command=self.save_xml)
        load_btn = tk.Button(row, text="Učitaj XML", bg="#29B6F6", fg=BTN_TEXT, command=self.load_xml)
        save_btn.pack(side="left", padx=6)
        load_btn.pack(side="left", padx=6)

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
