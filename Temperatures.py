import math
import statistics
from datetime import datetime

class Raport:

    def __init__(self,plik="",WD=[], PD={}, ND=[], pr=0., Sl=[],W={},help=[]):
        self.Nazwa_Pliku = plik
        self.Wszystkie_Dane = WD
        self.Poprawne_Dane = PD
        self.Niepoprawne_Dane = ND
        self.Slownik = Sl
        self.Wyniki = W
        self.Pomoc_temp=help




    def generuj_raport(self, Plik):
        self.Nazwa_Pliku = Plik
        self.Wyniki = {
            "wadliwe_logi": None,
            "procent_wadliwych_logow": "100.0",
            "czas_trwania_raportu": 0,
            "temperatura": {"max": None, "min": None, "srednia": None},
            "najdluzszy_czas_przegrzania": 0,
            "liczba_okresow_przegrzania": 0,
            "problemy": {
                "wysoki_poziom_zaklocen_EM": False,
                "wysokie_ryzyko_uszkodzenia_silnika_z_powodu_temperatury": False
            }
        }
        return self.Wyniki
    def odczyt_danych(self):
        pomoc = ""
        odczyt = open(self.Nazwa_Pliku, "r")
        line = odczyt.readline()
        line = line.rstrip("\n")
        while line != "":
            # self.Wszystkie_Dane.append(line)
            pomoc += line
            tab_pomoc = pomoc.split(" ")
            # print(tab_pomoc)
            self.Wszystkie_Dane.append(tab_pomoc)
            line = odczyt.readline()
            line = line.rstrip("\n")
            pomoc=""
        odczyt.close()
        # print(self.Wszystkie_Dane)

    def znajdowanie_poprawnych_danych(self):
        dane = ''
        pomoc = 0

        for i in range (0,len(self.Wszystkie_Dane)):
            if len(self.Wszystkie_Dane[i])!=3:
                self.Niepoprawne_Dane.append(self.Wszystkie_Dane[i])

                pomoc=0
            # wyraz = i
            # print(i)
            else:
                try:
                    datetime.strptime(self.Wszystkie_Dane[i][0],"%Y-%m-%d")
                    pomoc +=1
                except:
                    pomoc +=0
                try:
                    datetime.strptime(self.Wszystkie_Dane[i][1],"%H:%M")
                    pomoc+=1
                except:
                    pomoc +=0
                try:
                    a = self.Wszystkie_Dane[i][2]
                    if a[-1]=="." or a[-2]==".":
                        pomoc +=0
                    elif a[-1]=="C":
                        a = a[:-1]
                        a = float(a)
                        if a >= 0:
                            pomoc += 1
                        else:
                            pomoc += 0
                    else:
                        pomoc+=0
                except ValueError:
                        pomoc += 0

                if pomoc == 3:
                    # print(i)
                    # self.Porawne_Dane.append(self.Wszystkie_Dane[i])
                    self.Poprawne_Dane[i]=[self.Wszystkie_Dane[i]]
                    self.Pomoc_temp.append(
                                {"data": ((self.Wszystkie_Dane[i][0]) + " " + (self.Wszystkie_Dane[i][1])), "temperatura": float((self.Wszystkie_Dane[i][2])[:-1])})

                else:

                    self.Niepoprawne_Dane.append(self.Wszystkie_Dane[i])
                    self.Pomoc_temp.append(0)
                pomoc=0


        self.Wyniki["wadliwe_logi"] = self.Niepoprawne_Dane



    def proce_blend(self):
        if ((len(self.Niepoprawne_Dane) * 100) / len(self.Wszystkie_Dane)) - (
                (len(self.Niepoprawne_Dane) * 100) // len(self.Wszystkie_Dane)) >= 0.5:
            Procent_Blendow = (len(self.Niepoprawne_Dane) * 100) / len(self.Wszystkie_Dane)
            Procent_Blendow = round(Procent_Blendow,1)
            # Procent_Blendow = int(self.Procent_Blendow)
            if Procent_Blendow > 10:
                self.Wyniki["problemy"]["wysoki_poziom_zaklocen_EM"]=True
        else:
            Procent_Blendow = (len(self.Niepoprawne_Dane) * 100) / len(self.Wszystkie_Dane)
            Procent_Blendow = round(Procent_Blendow,1)
            # Procent_Blendow = int(self.Procent_Blendow)
            if Procent_Blendow > 10:
                self.Wyniki["problemy"]["wysoki_poziom_zaklocen_EM"]=True
        self.Wyniki["procent_wadliwych_logow"]=Procent_Blendow



    def zapisz_jako_slownik(self):
        for i in self.Poprawne_Dane.values():
            self.Slownik.append(
                {"data": ((i[0][0]) + " " + (i[0][1])), "temperatura": float((i[0][2])[:-1])})
        # for j in range (0, len(self.Slownik)):
        #     print(self.Slownik[j]["temperatura"])

    def uzupelnij_statytyke(self):
        temperatury=[]
        Statystyka = {"Min": 0, "Max": 0, "Srednia": 0}
        for i in range(len(self.Slownik)):
            if self.Slownik[i]!=0:
                temperatury.append(self.Slownik[i]["temperatura"])
        try:
            Statystyka["Max"]=round((max(temperatury)),1)
            self.Wyniki["temperatura"]["max"]=Statystyka["Max"]
            Statystyka["Min"]=round(min(temperatury),1)
            self.Wyniki["temperatura"]["min"] = Statystyka["Min"]
            Statystyka["Srednia"]=round(statistics.mean(temperatury),1)
            self.Wyniki["temperatura"]["srednia"] = Statystyka["Srednia"]
        except:
            self.Wyniki["temperatura"]["max"] = None
            self.Wyniki["temperatura"]["min"] = None
            self.Wyniki["temperatura"]["srednia"] = None

    def czas_trwania_raportu(self):
        try:
            Data_pierszwa = datetime.strptime(self.Slownik[0]["data"],"%Y-%m-%d %H:%M")
            Data_ostania = datetime.strptime(self.Slownik[-1]["data"],"%Y-%m-%d %H:%M")
            Czas_Raportu=((Data_ostania - Data_pierszwa).total_seconds()/60)
            Czas_Raportu= int(Czas_Raportu)
            self.Wyniki["czas_trwania_raportu"]=Czas_Raportu
        except:
            Czas_Raportu = 0
            Czas_Raportu = round(Czas_Raportu,0)
            self.Wyniki["czas_trwania_raportu"] = Czas_Raportu


    def czas_najdluzszego_przegrzania(self):

        Przegrzania = []
        Przegrzanie = []
        Czasy = []
        Czas=0
        self.Pomoc_temp.append(0)

        for i in self.Pomoc_temp:
            if i!=0 and i["temperatura"]>100:

                Przegrzanie.append(i["data"])
            else:
                if Przegrzanie != []:
                    Przegrzania.append(Przegrzanie)
                    Przegrzanie=[]
                else:
                    Przegrzanie = []
        for j in Przegrzania:
            Konic_Przegrzania = datetime.strptime(j[-1],"%Y-%m-%d %H:%M")
            Poczatek_Przegrznia = datetime.strptime(j[0],"%Y-%m-%d %H:%M")
            Czas  = (Konic_Przegrzania-Poczatek_Przegrznia).total_seconds()/60
            Czas = int(Czas)
            Czasy.append(Czas)
            Czas= 0

        try:
            Najdluzsze_Przegrzanie = max(Czasy)
            Okresy_Przegrzania = len(Czasy)
        except:
            Najdluzsze_Przegrzanie=0
            Okresy_Przegrzania=0
        self.Wyniki["najdluzszy_czas_przegrzania"]=Najdluzsze_Przegrzanie
        self.Wyniki["liczba_okresow_przegrzania"]=Okresy_Przegrzania
        if Najdluzsze_Przegrzanie > 10:
            self.Wyniki["problemy"]["wysokie_ryzyko_uszkodzenia_silnika_z_powodu_temperatury"] = True




main1 = Raport()
main1.generuj_raport("dane.txt")
main1.odczyt_danych()
main1.znajdowanie_poprawnych_danych()
main1.proce_blend()
main1.zapisz_jako_slownik()
main1.uzupelnij_statytyke()
main1.czas_trwania_raportu()
main1.czas_najdluzszego_przegrzania()
print(main1.Wyniki)
# for i in main1.Wyniki:
#     print(i,main1.Wyniki[i])

