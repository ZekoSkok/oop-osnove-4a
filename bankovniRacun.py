class BankovniRacun:
    def __init__(self, ime, br):
        self.ime = ime
        self.br = br
        self.stanje = 0.0

    def uplati(self, iznos):
        if iznos > 0:
            self.stanje += iznos
            print(f'Uplata od {iznos:.2f} EUR na račun {self.br} je uspješna.')
        else:
            print('Neispravan iznos za uplatu. Iznos mora biti pozitivan.')

    def isplati(self, iznos):
        if iznos > 0: 
            if self.stanje >= iznos:
                self.stanje -= iznos
                print(f'Isplata od {iznos:.2f} EUR s računa {self.br} je uspješna.')
            else:
                print('Neuspješna isplata. Na stanju nema dovoljno novca.')
            
        else:
            print('Neuspješna isplata. Iznos zaisplatu mora biti pozitivan.')
    
    def info(self):
        print(f'Vlasnik: {self.ime}, Broj računa: {self.br}, Trenutno stanje: {self.stanje:.2f}')
    

mojRacun = BankovniRacun('Zvonimir', 465789123473)

mojRacun.uplati(700)
mojRacun.info()
mojRacun.isplati(1200)
mojRacun.isplati(-200)
mojRacun.isplati(200)
mojRacun.info()
