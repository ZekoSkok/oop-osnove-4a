class Recept:
    def __init__(self, naziv):
        self.naziv = naziv
        self.sastojci = []

    def dodajSastojak(self, sastojak, količina):
        self.sastojci.append({'naziv': sastojak, 'količina': količina})

    def prikazi(self):
        print(f'Ime recepta: {self.naziv}')
        print(f'Sastojci: {self.sastojci}')

class Kuharica:
    def __init__(self, naziv):
        self.naziv = naziv
        self.recepti = []
        
    def dodajRecept(self, recept):
        self.recepti.append(recept)

    def pronadiRecept(self, nazivRec):
        if nazivRec in self.recepti:
            nazivRec.prikazi()

mojaKuharica = Kuharica('Domaća jela')
recept1 = Recept('Palačinke')
recept2 = Recept('Juha')
recept1.dodajSastojak('Šećer', '200g')
recept1.dodajSastojak('Mlijeko', '1L')
recept2.dodajSastojak('Voda', '2L')
recept2.dodajSastojak('Luk', '150g')
mojaKuharica.dodajRecept(recept1)
mojaKuharica.dodajRecept(recept2)
mojaKuharica.pronadiRecept('Palačinke')
