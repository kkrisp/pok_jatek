import sys
import math
import curses # kontroll a kepernyo felett
import random
import geometria as geo

FEL = 65
LE = 66
JOBBRA = 67
BALRA = 68

lehetseges_mozdulatok = [
            "alap1_J",
            "alap2_J",
            "megy1_J",
            "megy2_J",
            "megy3_J",
            "megy4_J",
            "alap1_B",
            "alap2_B",
            "megy1_B",
            "megy2_B",
            "megy3_B",
            "megy4_B"]

jobbra_menes_kepek = ["megy1_J", "megy2_J", "megy3_J", "megy4_J"]
balra_menes_kepek = ["megy1_B", "megy2_B", "megy3_B", "megy4_B"]


def kovetkezo_szam(jelen_szam, max_szam):
    if (jelen_szam + 1) < max_szam:
        return jelen_szam + 1
    else:
        return 0


def elozo_szam(jelen_szam, max_szam):
    if (jelen_szam - 1) < 0:
        return max_szam - 1
    else:
        return jelen_szam - 1


class Pont:
    def __init__(self, X=0, Y=0):
        self.X = X
        self.Y = Y


class Vonal:
    def __init__(self):
        self.A = Pont()
        self.B = Pont()
        self.atfogo_X = self.fuggoleges_atgofotszamol()
        self.atfogo_Y = self.vizszintes_atgofotszamol()
        self.hossz = self.hosszatszamol()
        self.szog = self.szogetszamol()

    def pont_beallitas(self, AX=None, AY=None, BX=None, BY=None):
        if AX:
            self.A.X = AX
        if AY:
            self.A.Y = AY
        if BX:
            self.B.X = BX
        if BY:
            self.B.Y = BY

        self.atfogo_X = self.fuggoleges_atgofotszamol()
        self.atfogo_Y = self.vizszintes_atgofotszamol()
        self.hossz = self.hosszatszamol()
        self.szog = self.szogetszamol()

    def vizszintes_atgofotszamol(self):
        return self.B.Y - self.A.Y

    def fuggoleges_atgofotszamol(self):
        return self.B.X - self.A.X

    def hosszatszamol(self):
        # sqrt(a^2 + b^2)
        return math.sqrt(math.pow(self.atfogo_X, 2) + pow(self.atfogo_Y, 2))

    def szogetszamol(self):
        if self.atfogo_Y == 0:
            if self.atfogo_X > 0:
                return 90
            else:
                return -90
        else:
            return math.atan(self.atfogo_X/self.atfogo_Y)

    def rajzol(self, kepernyo):
            szal_eleme = "-"
            irany_y = 1
            irany_x = 1
            if self.atfogo_Y < 0:
                irany_y = -1
            if self.atfogo_X < 0:
                irany_x = -1

            elem_x = self.A.X
            elem_y = self.A.Y

            if self.atfogo_X == 0:
                for i in range(self.atfogo_Y*irany_y):
                    kepernyo.addstr(elem_x, elem_y, szal_eleme)
                    elem_y += irany_y

            elif self.atfogo_Y == 0:
                for i in range(self.atfogo_X*irany_x):
                    kepernyo.addstr(elem_x, elem_y, szal_eleme)
                    elem_x += irany_x

            elif abs(self.atfogo_X) < abs(self.atfogo_Y):
                szakasz_hossza = int(abs(1.0*self.atfogo_Y/self.atfogo_X))
                maradek = abs(self.atfogo_Y) % abs(self.atfogo_X)
                for lepes in range(self.atfogo_X*irany_x):
                    for i in range(szakasz_hossza):
                        kepernyo.addstr(elem_x, elem_y, szal_eleme)
                        elem_y += irany_y
                    if maradek > 0:
                        kepernyo.addstr(elem_x, elem_y, szal_eleme)
                        elem_y += irany_y
                        maradek -= 1
                    elem_x += irany_x
            else:
                szakasz_hossza = int(abs(1.0 * self.atfogo_X/self.atfogo_Y))
                maradek = abs(self.atfogo_X) % abs(self.atfogo_Y)
                for lepes in range(self.atfogo_Y*irany_y):
                    for i in range(szakasz_hossza):
                        kepernyo.addstr(elem_x, elem_y, szal_eleme)
                        elem_x += irany_x
                    if maradek > 0:
                        kepernyo.addstr(elem_x, elem_y, szal_eleme)
                        elem_x += irany_x
                        maradek -= 1
                    elem_y += irany_y



def random_iranyba(karakter_ami_lep):
    random_szam = random.random()
    if random_szam < 0.25:
        karakter_ami_lep.jobbralep()
    elif random_szam < 0.5:
        karakter_ami_lep.balralep()
    elif random_szam < 0.75:
        karakter_ami_lep.fellep()
    else:
        karakter_ami_lep.lelep()


class Mozdulat:
    def __init__(self, magassag):
        self.magassag = magassag
        self.metszetek = [""] * magassag

    def rajzol(self, kepernyo, x, y):
        for metszet_szama in range(self.magassag):
            kepernyo.addstr(x-self.magassag+metszet_szama, y, self.metszetek[metszet_szama])


class Karakter:
    def __init__(self, megjelenesi_kepernyo, magassag):
        self.megjelenesi_kepernyo = megjelenesi_kepernyo
        self.magassag = magassag
        self.mozdulatok = {
            "alap1_J" : None,
            "alap2_J" : None,
            "megy1_J" : None,
            "megy2_J" : None,
            "megy3_J" : None,
            "megy4_J" : None,
            "alap1_B" : None,
            "alap2_B" : None,
            "megy1_B" : None,
            "megy2_B" : None,
            "megy3_B" : None,
            "megy4_B" : None
        }
        self.pozicio = geo.Pont()
        self.halo_kimenet = geo.Pont(self.pozicio.x-self.magassag+1, self.pozicio.y)
        self.irany = 1
        self.kepkocka = 0
    
    def rajzol(self):
        if self.irany > 0:
            self.mozdulatok[jobbra_menes_kepek[int(self.kepkocka/1)]]\
                .rajzol(self.megjelenesi_kepernyo, self.pozicio.x, self.pozicio.y)
        else:
            self.mozdulatok[balra_menes_kepek[int(self.kepkocka/1)]]\
                .rajzol(self.megjelenesi_kepernyo, self.pozicio.x, self.pozicio.y)

    def ujkep(self):
        if self.kepkocka >= 3:
            self.kepkocka = 0
        else:
            self.kepkocka += 1

    def jobbralep(self):
        self.pozicio.y += 1
        self.irany = 1
        self.ujkep()

    def balralep(self):
        self.pozicio.y -= 1
        self.irany = -1
        self.ujkep()

    def fellep(self):
        self.pozicio.x -= 1
        self.ujkep()

    def lelep(self):
        self.pozicio.x += 1
        self.ujkep()

    def alak_feltoltese(self, alak_filenev):
        alakok = open(alak_filenev, 'r')
        for i in range(len(lehetseges_mozdulatok)):
            uj_mozdulat = Mozdulat(self.magassag)
            for m in range(uj_mozdulat.magassag):
                sor = alakok.readline()
                uj_mozdulat.metszetek[m] = sor[:-1]
            self.mozdulatok[lehetseges_mozdulatok[i]] = uj_mozdulat
        alakok.close()


class Vilag:
    def __init__(self, megjelenitesi_kepernyo):
        self.megjelenitesi_kepernyo = megjelenitesi_kepernyo
        self.sorszeletek = [""]
        self.talaj = [13]*92
        self.magassag = 1
        self.szelesseg = 1
        for r in range(18, 44):
            self.talaj[r] = 14
        for r in range(60, 90):
            self.talaj[r] = 12
        for r in range(25):
            self.talaj.append(40)

    def feltoltes(self, filenev):
        kepfajl = open(filenev, 'r')
        kepsor = kepfajl.readline()
        while len(kepsor):
            self.sorszeletek.append(kepsor)
            if self.szelesseg < len(kepsor):
                self.szelesseg = len(kepsor) + 1
            for j in range(self.szelesseg - len(kepsor)):
                self.sorszeletek[self.magassag] += " "
            self.magassag += 1
            kepsor = kepfajl.readline()[:-1]
        kepfajl.close()

    def rajzol(self):
        for i in range(len(self.sorszeletek)):
            self.megjelenitesi_kepernyo.addstr(i, 0, self.sorszeletek[i])
        #self.megjelenitesi_kepernyo.refresh()


class Pokhalo:
    def __init__(self):
        self.szalak = [geo.Vektor()]
        self.utolsoszal = 0

    def uj_szal(self, kezdopont, vegpont):
        ujszal = geo.Vektor(kezdopont, vegpont)
        self.szalak.append(ujszal)
        self.utolsoszal += 1

    def rajzol(self, kepernyo, foszal):
        cnt = 0
        for sz in self.szalak:
            if cnt != foszal:
                geo.vonalat_rajzol(sz, kepernyo, elem='.')
            else:
                geo.vonalat_rajzol(sz, kepernyo, elem='*')
            cnt += 1


def szalat_valaszt(halo, jelenlegi_szal):
    szamlalo2 = 0
    szalak_szama2 = len(halo.szalak)
    while szamlalo2 < szalak_szama2:
        szamlalo2 += 1
        jelenlegi_szal = kovetkezo_szam(jelenlegi_szal, szalak_szama2)
        if geo.pont_vonal_kornyezeteben(botond.pozicio, sajat_halo.szalak[halon_maszik], 5):
            break
    return jelenlegi_szal

idomero = 0
halotszo = False
halon_maszik = 1
halon_maszik_elozo = 0
sajat_halo = Pokhalo()
sajat_halo.uj_szal(geo.Pont(40, 5), geo.Pont(40, 110))
sajat_halo.uj_szal(geo.Pont(5, 5),  geo.Pont(40, 10))
sajat_halo.uj_szal(geo.Pont(5, 120), geo.Pont(40, 110))
kozelben = "kozeleben --- van      "
kov_hely = -1
most_hely = -1
try:
    fokepernyo = curses.initscr() # letrehoz egy 'curses' ablakot
    fokepernyo.timeout(200)
    curses.noecho()               # a lenyomott karakterek nem jelennek meg
    curses.cbreak()               # a lenyomott billentyut 'enter' nelkul is regisztralja
    curses.curs_set(0)            # a kurzor ne latsszon a kepernyon
    kepernyo_szelesseg, kepernyo_magassag = fokepernyo.getmaxyx()

    botond = Karakter(fokepernyo, 2)
    botond.pozicio = geo.Pont(40, 18)
    botond.alak_feltoltese("pok.txt")

    szavanna = Vilag(fokepernyo)
    szavanna.feltoltes("doboz.txt")

    vilag_faljnev = "siksag.txt"
    c = '<gomb>'
    while 1:
        fokepernyo.clear()
        #szavanna.rajzol()
        hely_debug = "most: " + str(most_hely) + " kov.: " + str(kov_hely)
        fokepernyo.addstr(5, 40, hely_debug)

        sajat_halo.rajzol(fokepernyo, halon_maszik)
        botond.rajzol()
        fokepernyo.addstr(2, 2, "Kilepes: 'X', mozgas: nyilak, haloszoves: 'H'")
        fokepernyo.addstr(3, 2, kozelben)
        c = fokepernyo.getch()
        if c == ord('x') or c == ord("X"):
            break
        elif c == JOBBRA:
            kovetkezo_hely = sajat_halo.szalak[halon_maszik].y_helyen(botond.pozicio.y+1)
            kov_hely = kovetkezo_hely
            most_hely = botond.pozicio.x
            if kovetkezo_hely is None:
                pass
            elif kovetkezo_hely < int(botond.pozicio.x-1):
                botond.fellep()
            elif kovetkezo_hely > int(botond.pozicio.x):
                botond.lelep()
            else:
                botond.jobbralep()
        elif c == BALRA:
            kovetkezo_hely = sajat_halo.szalak[halon_maszik].y_helyen(botond.pozicio.y-1)
            kov_hely = kovetkezo_hely
            most_hely = botond.pozicio.x
            if kovetkezo_hely is None:
                pass
            elif kovetkezo_hely > int(botond.pozicio.x+1):
                botond.lelep()
            elif kovetkezo_hely < int(botond.pozicio.x):
                botond.fellep()
            else:
                botond.balralep()
        elif c == FEL:
            #botond.fellep()
            szamlalo = 0
            szalak_szama = len(sajat_halo.szalak)
            if halotszo: szalak_szama -= 1
            while szamlalo < szalak_szama:
                szamlalo += 1
                halon_maszik = kovetkezo_szam(halon_maszik, szalak_szama)
                if geo.pont_vonal_kornyezeteben(botond.pozicio, sajat_halo.szalak[halon_maszik], 3):
                    break
        elif c == LE:
            #botond.lelep()
            szamlalo = 0
            szalak_szama = len(sajat_halo.szalak)
            if halotszo: szalak_szama -= 1
            while szamlalo < szalak_szama:
                szamlalo += 1
                halon_maszik = elozo_szam(halon_maszik, szalak_szama)
                if geo.pont_vonal_kornyezeteben(botond.pozicio, sajat_halo.szalak[halon_maszik], 3):
                    break
        elif c == ord('h') or c == ord('H'):
            halotszo = not halotszo
            if halotszo:
                sajat_halo.uj_szal(botond.pozicio, botond.pozicio)
        elif c == ord('g') or c == ord('G'):
            if halon_maszik < len(sajat_halo.szalak)-1:
                halon_maszik += 1
            else:
                halon_maszik = 0
        elif c == ord('c') or c == ord('C'):
            szamlalo = 0
            szalak_szama = len(sajat_halo.szalak)
            while szamlalo < szalak_szama:
                szamlalo += 1
                halon_maszik = kovetkezo_szam(halon_maszik, szalak_szama)
                if geo.pont_vonal_kornyezeteben(botond.pozicio, sajat_halo.szalak[halon_maszik], 3):
                    break
        else:
            pass

        if halotszo:
            sajat_halo.szalak[sajat_halo.utolsoszal].uj_vegpont(botond.pozicio)
        if halon_maszik >= 0:
            foldre = sajat_halo.szalak[halon_maszik].y_helyen(botond.pozicio.y)
            #if foldre:
            #    botond.pozicio.x = int(foldre)

        fokepernyo.refresh()
        idomero += 1
        if idomero >= 1000000:
            idomero = 0


except: # program bezarasa rendesen, ha valami baj van
    curses.nocbreak()
    fokepernyo.keypad(0)
    curses.echo()        # latsszon a kurzor
    curses.endwin()      # vissza a rendes parancssorhoz
    raise

# program bezarasa, ha minden jol megy
curses.nocbreak()
fokepernyo.keypad(0)
curses.echo()        # latsszon a kurzor
curses.endwin()      # vissza a rendes parancssorhoz
