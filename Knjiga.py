class Knjiga:
    def __init__(self, naslov, autor, god_izdanja):
        self.naslov = naslov
        self.autor = autor
        self.god_izdanja = god_izdanja 

book1 = Knjiga('Stranac', 'Albert Camus', 1942)
book2 = Knjiga('Gospodar prstenova', 'J.R.R. Tolkien', 1954)

print(f'Naslov: {book1.naslov}, Autor: {book1.autor}, Godina izdanja: {book1.god_izdanja}')
print(f'Naslov: {book2.naslov}, Autor: {book2.autor}, Godina izdanja: {book2.god_izdanja}')