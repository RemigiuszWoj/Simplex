from tkinter import *
import numpy as np
import random as rd
from Equation import Expression
import math

##############################################################################
################################## ZMIENNE  ##################################
##############################################################################

#zmienne od użytkownika
wzor = "100*(x2-x1**2)**2 + (1-x1)**2"
epsilon = 1*10** (-3)   #dokladnosc obliczen
iteracje = 200          #ograniczenie do 200 powtorzen petli
x1_min = -1             #wymiary kostki
x1_max = 1
x2_min = -1
x2_max = 1

x0 = 0      #p-t startowy
d = 0       #poczatkowa odleglosc miedzy wierzcholkami simpleksu
a = 1       #wspolczynnik odbicia (a>0)
b = 0.5     #wspolczynnik kontrakcji (0<b<1)
y = 1       #wspolczynnik ekspansji (y>0)
n = 2       #liczba zmiennych niezależnych
fn = Expression(wzor, ["x1","x2"])
tablica_wynikow = []
tablica_simpleksu = []
global liczba_iter
pkt1 = []
pkt2 = []
pkt3 = []

##############################################################################
################################## FUNKCJE  ##################################
##############################################################################

################################## do komunikacji z oknem aplikacji


################################## do działania algorytmu
def tworz(n, przedzial_od,przedzial_do):
    P=[]
    l=[]

    for i in range(n+1):
        for j in range(n):
            l.append(rd.uniform(przedzial_od,przedzial_do))
        P.append(l)
        l=[]
    return P

def oblicz(P, fn, n):
    F=[]
    for i in range(n+1):
        x1 = P[i][0]
        x2 = P[i][1]
        F.append(fn(x1,x2))
    return F

def min(F,n):
    min = 0
    for i in range(n+1):
        if F[i] < F[min] :
            min = i
    return min

def max(F,n):
    max = 0
    for i in range(n+1):
        if F[i] > F[max] :
            max = i
    return max

def srodek(P, n, h):
    sum = []
    for i in range(n):
        sum.append(0)

    for j in range(n+1):
        if j != h :
            for k in range(n):
                sum[k] += P[j][k]
    for l in range(n):
        sum[l] /= n
    return sum

def odbicie(P,srodek,h,a,n):
    odb = []
    for i in range(n):
        odb.append((1+a)*srodek[i]-a*P[h][i])
    return odb

def ekspansja(srodek,Pt,y,n):
    eks = []
    for i in range(n):
        eks.append((1+y)*Pt[i]-y*srodek[i])
    return eks

def kontrakcja(b,MAX,Pp,P,n):
    kontr = []
    for i in range(n):
        kontr.append(b * P[MAX][i] + (1- b) * Pp[i])
    return kontr

def czy_Fo_najwieksze(F,MAX,Fo,n):
    for i in range(n+1):
        if i != MAX:
            if Fo >= F[i]:
                buff = True
            else:
                buff = False
    return buff

def odleglosci_miedzy_p(P,n):
    Dlugosci = []
    Dlugosci.append(math.sqrt((P[0][0] - P[1][0]) ** 2 + (P[0][1] - P[1][1]) ** 2))
    Dlugosci.append(math.sqrt((P[1][0] - P[2][0]) ** 2 + (P[1][1] - P[2][1]) ** 2))
    Dlugosci.append(math.sqrt((P[2][0] - P[0][0]) ** 2 + (P[2][1] - P[0][1]) ** 2))
    return Dlugosci

def redukcja_simplexu(P,l,n):
    Zredukowany_Simplex = []
    Bufor = []

    for j in range(n+1):
        for k in range(n):
            Bufor.append((P[j][k] + P[l][k])/2)
        Zredukowany_Simplex.append(Bufor)
        Bufor = []

    return Zredukowany_Simplex


##############################################################################
################################## ALGORYTM ##################################
##############################################################################
def algorytm(epsilon, n, fn, a, b, y, iteracje):
    global liczba_iter
    liczba_iter = 0

    # tworzenie simpleksu
    P = tworz(n,-1,1)
    odleglosci = odleglosci_miedzy_p(P,n)
    if odleglosci[max(odleglosci,n)] > epsilon:
        stop = True
    else:
        stop = False

    #print(P)
    while stop:
        # liczenie wartosci f-cji w punktach wierzcholkowych simpleksu
        F = oblicz(P,fn,n)
        #print(F)

        # wyznaczenie p-tow z najwieksza i najmniejsza wartoscia funkcji
        MIN = min(F,n)
        MAX = max(F,n)

        # obliczenie środka symetrii simpleksu
        Pp = srodek(P,n,MAX)
        #print(Pp)

        # wyliczenie wartości f-cji dla srodka symetrii simpleksu
        #print(fn(Pp[0],Pp[1]))
        tablica_wynikow.append([Pp[0], Pp[1], fn(Pp[0],Pp[1])])
        tablica_simpleksu.append(P)
        pkt1.append([P[0][0],P[1][0],P[2][0]])
        pkt2.append([P[0][1],P[1][1],P[2][1]])
        pkt3.append([fn(P[0][0],P[0][1]),fn(P[1][0],P[1][1]),fn(P[2][0],P[2][1])])
        #print(P)

        # odbicie p-tu max wzgledem srodka symetrii simpleksu
        Pt = odbicie(P,Pp,MAX,a,n)
        Fo = fn(Pt[0],Pt[1])
        #print(Pt)

        # sprawdzenie czy wartosc f-cji w odbitym p-cie jest wieksza od min
        if fn(Pt[0],Pt[1]) < fn(P[MIN][0],P[MIN][1]):
            Ptt = ekspansja(Pp,Pt,y,n)
            Fe = fn(Ptt[0],Ptt[1])
            if Fe < fn(P[MIN][0],P[MIN][1]):
                P[MAX] = Ptt
            else:
                P[MAX] = Pt
            odleglosci = odleglosci_miedzy_p(P,n)
            if odleglosci[max(odleglosci,n)] < epsilon:
                stop = False

        if fn(Pt[0],Pt[1]) > fn(P[MIN][0],P[MIN][1]):
            if czy_Fo_najwieksze(F,MAX,Fo,n):
                if Fo < F[MAX]:
                    P[MAX] = Pt
            Pttt = kontrakcja(b,MAX,Pp,P,n)
            Fk = fn(Pttt[0],Pttt[1])
            if Fk >= fn(P[MAX][0],P[MAX][1]):
                P = redukcja_simplexu(P,MIN,n)
            else:
                P[MAX] = Pttt
            if czy_Fo_najwieksze(F, MAX, Fo,n) == False:
                P[MAX] = Pt
            odleglosci = odleglosci_miedzy_p(P,n)
            if odleglosci[max(odleglosci,n)] < epsilon:
                stop = False

        if fn(Pt[0],Pt[1]) == fn(P[MIN][0],P[MIN][1]):
            print("Cos poszlo mocno nie tak")

        liczba_iter += 1
        if liczba_iter == iteracje:
            stop = False

    print(Pp)
    print(fn(Pp[0],Pp[1]))
    print(liczba_iter)
    #print(dupa)
    print("Koniec dzialania programu")
    print(tablica_simpleksu)
    return 0

def start():
    algorytm(epsilon, n, fn, a, b, y, iteracje)
