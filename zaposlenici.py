


class Zaposlenik:
    def __init__(self, ime, prezime, placa):
        self.ime = ime
        self.prezime = prezime
        self.placa = placa

    def prikazi_info(self):
        print(f'Ime: {self.ime}, Prezime: {self.prezime}, Plaća: {self.placa}€')

class Programer(Zaposlenik):
    def __init__(self, ime, prezime, placa, programski_jezici):
        super().__init__(ime, prezime, placa)
        self.programski_jezici = programski_jezici

    def prikazi_info(self):
        super().prikazi_info()
        print(f'Programski jezici: {", ".join(self.programski_jezici)}')
    
class Menadzer(Zaposlenik):
    def __init__(self, ime, prezime, placa, tim):
        super().__init__(ime, prezime, placa)
        self.tim = tim

    def prikazi_info(self):
        super().prikazi_info()
        print(f'Tim: {", ".join(self.tim)}')

    def dodaj_clana_tima(self, novi_clan):
        self.tim.append(novi_clan)


z1 = Zaposlenik("Ivan", "Grgić", 3000)
p1 = Programer("Dani", "Rondo", 4000, ['Python', 'JavaScript'])
m1 = Menadzer("Marko", "Brščić", 5000, ['Ivan Grgić', 'Dani Rondo'])
    
print("Podaci o zaposleniku:")
z1.prikazi_info()


print("\nPodaci o programeru:")
p1.prikazi_info()


print("\nPodaci o menadžeru:")
m1.prikazi_info()   


m1.dodaj_clana_tima("Ana Butković")

print("\nPodaci o menadžeru:")
m1.prikazi_info()
