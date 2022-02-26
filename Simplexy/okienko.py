from tkinter import *
import math
from math import e,log
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.colors import LightSource
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from Equation import Expression
# Import packages
#%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import metoda0 as metoda

global krok
global inf
inf=False
global canvas,toolbar
fig = plt.figure(1)
global ax,X,Y,Z,norm
ax = fig.add_subplot(111)
oldSize = fig.get_size_inches()
fig.set_size_inches([0.75 * s for s in oldSize])


def wyjscie_():
    window.destroy()
    exit()

#funkcje do obsługi pól okna aplikacji
def wczytaj_zakresy():
    if pole_zakresu_x1_min.get() != '':
        zakres_x1_min = float(pole_zakresu_x1_min.get())
        metoda.x1_min = zakres_x1_min
    else:
        pole_zakresu_x1_min.insert(END, metoda.x1_min)
    if pole_zakresu_x1_max.get() != '':
        zakres_x1_max = float(pole_zakresu_x1_max.get())
        metoda.x1_max = zakres_x1_max
    else:
        pole_zakresu_x1_max.insert(END, metoda.x1_max)
    if pole_zakresu_x2_min.get() != '':
        zakres_x2_min = float(pole_zakresu_x2_min.get())
        metoda.x2_min = zakres_x2_min
    else:
        pole_zakresu_x2_min.insert(END, metoda.x2_min)
    if pole_zakresu_x2_max.get() != '':
        zakres_x2_max = float(pole_zakresu_x2_max.get())
        metoda.x2_max = zakres_x2_max
    else:
        pole_zakresu_x2_max.insert(END, metoda.x2_max)
    #print(zakres_x1_min, zakres_x1_max, zakres_x2_min, zakres_x2_max)
    #print(metoda.x1_min, metoda.x1_max, metoda.x2_min, metoda.x2_max)

def wczytaj_funkcje():
    if pole_fcji.get() != '':
        metoda.wzor = pole_fcji.get()
    else:
        pole_fcji.insert(END, metoda.wzor)

def wczytaj_wspolczynniki():
    if pole_odbicia.get() != '':
        metoda.a = float(pole_odbicia.get())
    else:
        pole_odbicia.insert(END, metoda.a)
    if pole_kontr.get() != '':
        metoda.b = float(pole_kontr.get())
    else:
        pole_kontr.insert(END, metoda.b)
    if pole_eks.get() != '':
        metoda.y = float(pole_eks.get())
    else:
        pole_eks.insert(END, metoda.y)

def wczytaj_epsilon():
    if pole_epsilon.get() != '':
        metoda.epsilon = float(pole_epsilon.get())
    else:
        pole_epsilon.insert(END, metoda.epsilon)

def wczytaj_iteracje():
    if pole_max_ilosc_krokow.get() != '':
        metoda.iteracje = float(pole_max_ilosc_krokow.get())
    else:
        pole_max_ilosc_krokow.insert(END, metoda.iteracje)

def wczytaj_jakosc():
    if pole_jakos.get() != '':
        jakosc = int(pole_jakos.get())
    else:
        jakosc = 20
        pole_jakos.insert(END, jakosc)
    return jakosc

def przycisk_oblicz():
    global krok,inf
    metoda.tablica_wynikow = []
    metoda.tablica_simpleksu = []
    metoda.pkt1 = []
    metoda.pkt2 = []
    metoda.pkt3 = []
    wczytaj_funkcje()
    wczytaj_zakresy()
    wczytaj_wspolczynniki()
    wczytaj_epsilon()
    wczytaj_iteracje()

    #print(metoda.epsilon)
    #print(metoda.iteracje)
    metoda.start()
    print(metoda.wzor)
    #print(metoda.pkt1)
    krok = metoda.liczba_iter
    pokaz_krok()
    output3.delete(0.0,END)
    output3.insert(END, str(metoda.liczba_iter))
    if int(metoda.ile_zmiennych(metoda.wzor)) == 2:
        dane_do_funkcji()
        rysowanie_krokow(wczytaj_jakosc())
        inf=True

def dane_do_funkcji():
    global X,Y,Z,norm
    wczytaj_zakresy()
    #ax.clear()
    #fn = Expression(metoda.wzor, metoda.przypisz_fn(int(metoda.ile_zmiennych(metoda.wzor))))
    #print(buff1)
    x=np.arange(metoda.x1_min, metoda.x1_max, 0.001*25)
    y=np.arange(metoda.x2_min, metoda.x2_max, 0.001*25)
    X, Y = np.meshgrid(x, y)
    Z=metoda.fn(X,Y)
    norm = cm.colors.Normalize(vmax=abs(Z).max(), vmin=-abs(Z).max())
    #ax.scatter(metoda.tablica_wynikow[krok-1][0], metoda.tablica_wynikow[krok-1][1], metoda.tablica_wynikow[krok-1][2],'o')
    #ax.scatter(metoda.pkt1[krok-1],metoda.pkt2[krok-1],metoda.pkt3[krok-1],'o')
    #ax.set_xlim(-1, 3)
    #ax.set_ylim(-1, 3)
    #ax.set_xticks([])
    #ax.set_yticks([])
    #plt.show()

def przycisk_rysuj():
    if int(metoda.ile_zmiennych(metoda.wzor)) == 2:
        dane_do_funkcji()
        rysowanie_krokow(wczytaj_jakosc())

def rysowanie_krokow(jakosc):
    global ax,krok
    global X,Y,Z,norm
    global canvas,toolbar
    global inf
    if inf==True:
        toolbar.destroy()
        canvas.get_tk_widget().destroy()
    ax.clear()
    wczytaj_zakresy()
    contourf_=ax.contourf(X,Y,Z,extent=(metoda.x1_min, metoda.x1_max, metoda.x2_min, metoda.x2_max),levels=jakosc,origin='lower',cmap='RdPu', norm=norm)
    cbar=fig.colorbar(contourf_)
    #cbar.set_clim(vmin, vmax)
    ax.plot(metoda.tablica_wynikow[krok-1][0], metoda.tablica_wynikow[krok-1][1],'o')
    ax.plot(metoda.pkt1[krok-1],metoda.pkt2[krok-1],'-',color='white')
    ax.set_xlim(metoda.x1_min, metoda.x1_max)
    ax.set_ylim(metoda.x2_min, metoda.x2_max)
    #plt.show()
    canvas = FigureCanvasTkAgg(fig, master=output1)
    toolbar = NavigationToolbar2Tk(canvas,output1)
    toolbar.update()
    #canvas.restore_region()
    canvas.get_tk_widget().pack()
    canvas.draw()
    cbar.remove()


def przycisk_nastepny():
    global krok,canvas
    if metoda.tablica_wynikow != []:
        if krok < metoda.liczba_iter:
            krok += 1
            pokaz_krok()
            if int(metoda.ile_zmiennych(metoda.wzor)) == 2:
                #toolbar.destroy()
                #canvas.get_tk_widget().destroy()
                rysowanie_krokow(wczytaj_jakosc())

def przycisk_poprzedni():
    global krok,canvas
    if metoda.tablica_wynikow != []:
        if krok > 1:
            krok -= 1
            pokaz_krok()
            if int(metoda.ile_zmiennych(metoda.wzor)) == 2:
                #toolbar.destroy()
                #canvas.get_tk_widget().destroy()
                rysowanie_krokow(wczytaj_jakosc())

def pokaz_krok():
    global krok
    output.delete(0.0,END)
    output.insert(END, "Współrzędne wyliczonego punktu: ")
    for i in range (int(metoda.ile_zmiennych(metoda.wzor))+1):
        output.insert(END, str(metoda.tablica_wynikow[krok-1][i]))
        output.insert(END, "\n")
    output.insert(END, "Największa odległość między dwoma punktami simpleksu: ")
    output.insert(END, str(metoda.tablica_wynikow[krok-1][int(metoda.ile_zmiennych(metoda.wzor))+1]))
    output.insert(END, "\n")
    output4.delete(0.0,END)
    output4.insert(END, str(krok))


#Okinko
window =Tk()
window.title("Metoda pełzającego Remika")

#ramka f-cji
ramka_funkcji = LabelFrame(window, text="Funkcja")
ramka_funkcji.grid(row=0, column=1, columnspan=8, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

Label (ramka_funkcji, text="Podaj funkcje").grid(row=1,column=0,sticky='W')

pole_fcji = Entry(ramka_funkcji, width = 51)
pole_fcji.grid(row=1, column=3, columnspan=8, sticky="WE", pady=5, padx = 5)


#ramka zakresow
ramka_zakresu = LabelFrame(window, text="Zakresy")
ramka_zakresu.grid(row=1, column=1, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

Label (ramka_zakresu, text="< x1 <").grid(row=1,column=3,sticky='W')
Label (ramka_zakresu, text="< x2 <").grid(row=2,column=3,sticky='W')

pole_zakresu_x1_min = Entry(ramka_zakresu)
pole_zakresu_x1_min.grid(row=1, column=1, columnspan=1, sticky="WE", pady=5, padx = 5)
pole_zakresu_x1_max = Entry(ramka_zakresu)
pole_zakresu_x1_max.grid(row=1, column=4, columnspan=1, sticky="WE", pady=5, padx = 5)
pole_zakresu_x2_min = Entry(ramka_zakresu)
pole_zakresu_x2_min.grid(row=2, column=1, columnspan=1, sticky="WE", pady=5, padx = 5)
pole_zakresu_x2_max = Entry(ramka_zakresu)
pole_zakresu_x2_max.grid(row=2, column=4, columnspan=1, sticky="WE", pady=5, padx = 5)

Button(ramka_zakresu,text="Wczytaj", command=wczytaj_zakresy, width = 10, height = 3).grid(row=1,column=6, rowspan=2, sticky='E',pady=2, padx = 5)

#ramka_wspol
ramka_wspol = LabelFrame(window, text="Współczynniki")
ramka_wspol.grid(row=2, column=1, columnspan=7, rowspan=1, sticky='NS', padx=5, pady=5, ipadx=5, ipady=5)

Label (ramka_wspol, text="Odbicia:").grid(row=1,column=1,sticky='W')
Label (ramka_wspol, text="Kontrakcji:").grid(row=1,column=2,sticky='W')
Label (ramka_wspol, text="Ekspancji:").grid(row=1,column=3,sticky='W')
pole_odbicia = Entry(ramka_wspol, width=20)
pole_odbicia.grid(row=2, column=1, columnspan=1, sticky="WE", pady=5, padx = 5)
pole_kontr = Entry(ramka_wspol, width=20)
pole_kontr.grid(row=2, column=2, columnspan=1, sticky="WE", pady=5, padx = 5)
pole_eks = Entry(ramka_wspol, width=20)
pole_eks.grid(row=2, column=3, columnspan=1, sticky="WE", pady=5, padx = 5)

#ramka epsilon
ramka_epsilon = LabelFrame(window, text="Epsilon")
ramka_epsilon.grid(row=3, column=1, columnspan=5, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

pole_epsilon = Entry(ramka_epsilon, width=24)
pole_epsilon.grid(row=1, column=1, columnspan=1, sticky="WE", pady=10, padx = 5)


#ramka_max_ilosci_krokow
ramka_max_ilosci_krokow = LabelFrame(window, text="Max. ilość kroków")
ramka_max_ilosci_krokow.grid(row=3, column=5, columnspan=5, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

pole_max_ilosc_krokow = Entry(ramka_max_ilosci_krokow, width=24)
pole_max_ilosc_krokow.grid(row=1, column=1, columnspan=1, sticky="WE", pady=10, padx = 5)


#ramka_komunikacji
ramka_komunikacji = LabelFrame(window, text="Stan")
ramka_komunikacji.grid(row=4, column=1, columnspan=7, rowspan=2, sticky='NS', padx=5, pady=5, ipadx=5, ipady=5)

output = Text(ramka_komunikacji,width = 48, height = 6,wrap = WORD)
output.grid(row = 1, column = 1, columnspan = 7, pady=10, padx = 5)


#ramka rysowania
ramka_rysunku = LabelFrame(window)
ramka_rysunku.grid(row=0, column=8, columnspan=6, rowspan=5, sticky='NS', padx=5, pady=5, ipadx=5, ipady=5)

output1 = Text(ramka_rysunku,width = 60, height = 25,wrap = WORD)
output1.grid(row = 1, column = 1, columnspan = 6, rowspan = 5, pady=5, padx = 5)


#ramka promienia i jakosci
ramka_prom_jakos = LabelFrame(window)
ramka_prom_jakos.grid(row=5, column=8, columnspan=4, rowspan=1, sticky='NS', padx=5, pady=5, ipadx=5, ipady=5)

#Label (ramka_prom_jakos, text="Promień:").grid(row=1,column=1,sticky='W')
Label (ramka_prom_jakos, text="Jakość:").grid(row=2,column=1,sticky='W')

#pole_prom = Entry(ramka_prom_jakos, width=25)
#pole_prom.grid(row=1, column=2, columnspan=1, sticky="WE", pady=10, padx = 5)

pole_jakos = Entry(ramka_prom_jakos, width=25)
pole_jakos.grid(row=2, column=2, columnspan=1, sticky="WE", pady=10, padx = 5)

'''
#ramka srodka ukladu
ramka_sr = LabelFrame(window, text="Środek")
ramka_sr.grid(row=5, column=12, columnspan=4, rowspan=1, sticky='NS', padx=5, pady=5, ipadx=5, ipady=5)

Label (ramka_sr, text="x1:").grid(row=1,column=1,sticky='W')
Label (ramka_sr, text="x2:").grid(row=1,column=2,sticky='W')

pole_x1 = Entry(ramka_sr, width=18)
pole_x1.grid(row=2, column=1, columnspan=1, sticky="WE", pady=10, padx = 5)

pole_x2 = Entry(ramka_sr, width=18)
pole_x2.grid(row=2, column=2, columnspan=1, sticky="WE", pady=10, padx = 5)
'''

#ramka przegladu krokowego
ramka_krok = LabelFrame(window, text="Podgląd kolejnych kroków algorytmu")
ramka_krok.grid(row=6, column=1, columnspan=7, rowspan=2, sticky='NS', padx=5, pady=5, ipadx=5, ipady=5)

Label (ramka_krok, text="Ilość kroków:").grid(row=1,column=1,sticky='W')
Label (ramka_krok, text="Krok:").grid(row=2,column=1,sticky='W')

output3 = Text(ramka_krok,width = 38, height = 1,wrap = WORD)
output3.grid(row = 1, column = 2, columnspan = 7, pady=10, padx = 5)

output4 = Text(ramka_krok,width = 38, height = 1,wrap = WORD)
output4.grid(row = 2, column = 2, columnspan = 7, pady=10, padx = 5)

Button(ramka_krok,text="Poprzedni",command=przycisk_poprzedni, width = 13).grid(row=3,column=1, columnspan=2, sticky='E',pady=2, padx = 5)
Button(ramka_krok,text="Następny",command=przycisk_nastepny, width = 13).grid(row=3,column=7, columnspan=2, sticky='E',pady=2, padx = 5)

#przysick rysowania
Button(window,text="Rysuj", command=przycisk_rysuj, width = 14).grid(row=5, column=12, columnspan=4, rowspan=1, sticky='NS', padx=5, pady=5, ipadx=5, ipady=5)

#przysick liczenia
Button(window,text="Oblicz", command=przycisk_oblicz, width = 14).grid(row=7,column=12, sticky='E',pady=2, padx = 5)

#przycisk wyjścia
Button(window,text="Wyjście", width = 14, command=wyjscie_).grid(row=7,column=13,sticky='E',pady=2, padx = 5)

window.mainloop()
