# Definicija klase
class Automobil:
    #Definiranje konstruktora
    def __init__(self, marka, model, godina_proizvodnje, boja):
        #Definiranje svojstava ili atributa
        self.marka = marka
        self.model = model
        self.godina_proizvodnje = godina_proizvodnje
        self.boja = boja
        self.upaljen = False #Početno stanje svakog objekta

    #Definirati metode
    def prikazi_informacije(self):
        print(f"Marka: {self.marka}")
        print(f"Model: {self.model}")
        print(f"Godina proizvodnje: {self.godina_proizvodnje}")
        print(f"Boja: {self.boja}")
        print(f"Upaljen: {'Da' if self.upaljen else 'Ne'}")

     
    def upali_auto(self):
        if not self.upaljen:
            self.upaljen = True
            print(f"{self.marka} {self.model} je upaljen.")
        else:
            print(f"{self.marka} {self.model} je već upaljen.")

#Kreiranje objekata
moj_automobil = Automobil("BMW", "M3", 2023, "Bijela")

susjedov_automobil = Automobil("Volkswagen", "Golf II", 1983, "Crveni")

#Pozivanje metoda
moj_automobil.prikazi_informacije()
moj_automobil.upali_auto()
susjedov_automobil.prikazi_informacije()
susjedov_automobil.upali_auto()
moj_automobil.upali_auto()
moj_automobil.prikazi_informacije()
