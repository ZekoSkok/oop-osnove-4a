import tkinter as tk

lista_imena = []

def klik():
    ime = unos_imena.get()
    lista_imena.append(ime)
    pozdravna = f''
    for ime in lista_imena:
        pozdravna += f'Pozdrav {ime}!\n'
    pozdrav.config(text=pozdravna)




#Kreiranje prozora
prozor = tk.Tk()
prozor.title('Moj prvi GUI program')

#Static widget
poz_poruka = tk.Label(prozor, text='Pozdrav 4.a!')
poz_poruka.pack()

uputa = tk.Label(prozor, text='Upiši svoje ime!')
uputa.pack()

#Unos podataka
unos_imena = tk.Entry(prozor)
unos_imena.pack()

pozdrav = tk.Label(prozor, text='')
pozdrav.pack()

#Interactive widget
gumb = tk.Button(prozor, text='Pozdravi me!', command=klik)
gumb.pack()




prozor.mainloop()