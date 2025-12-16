# 🧮 Shapesy

**Shapesy** je edukativna Python aplikacija s grafičkim sučeljem koja omogućuje izračunavanje
geometrijskih svojstava **2D i 3D oblika**.  
Aplikacija je namijenjena učenicima i početnicima koji uče objektno programiranje, rad s
Tkinter GUI-jem te osnovnu geometriju.

---

## ✨ Funkcionalnosti

- Odabir **2D i 3D oblika** pomoću RadioButtona
- Dinamički prikaz parametara ovisno o odabranom obliku
- Izračun:
  - **Površine**
  - **Opsega** (2D oblici)
  - **Volumena** (3D oblici)
- Vizualni **preview oblika** na `Canvas` widgetu (centriran i skaliran)
- **Povijest izračuna** s mogućnošću ponavljanja i brisanja zapisa
- Spremanje i učitavanje povijesti u **XML datoteku**
- Burger izbornik s:
  - **O aplikaciji**
  - **Formule**
- Responzivno sučelje prilagođeno i manjim zaslonima

---

## 📐 Podržani oblici

### 2D oblici
- Krug
- Pravokutnik
- Kvadrat
- Trapez

### 3D oblici
- Kugla
- Kocka
- Kvadar

---

## 🧠 Arhitektura aplikacije

Aplikacija je izrađena prema **objektno-orijentiranom principu**:

- `Shape` – bazna klasa za sve oblike
- Svaki oblik:
  - definira svoje parametre
  - implementira vlastite formule
  - sadrži metodu za crtanje (`draw`)
- GUI je odvojen od logike izračuna
- Dodavanje novog oblika zahtijeva samo:
  1. Poznavanje formule
  2. Definiranje nove klase

---

## 🛠 Tehnologije

- **Python 3**
- **Tkinter** (GUI)
- **ttk** (moderniji widgeti)
- **xml.etree.ElementTree** (spremanje podataka)
- **math** (matematičke konstante i funkcije)

---

## ▶️ Pokretanje aplikacije

1. Kloniraj repozitorij:
   ```bash
   git clone https://github.com/korisnik/shapesy.git
