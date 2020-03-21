import sys
import math
import curses # kontroll a kepernyo felett
import random

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
            kepernyo.addstr(x+metszet_szama, y, self.metszetek[metszet_szama])


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
        self.pozicio_X = 0
        self.pozicio_Y = 0
        self.irany = 1
        self.kepkocka = 0
    
    def rajzol(self):
        if self.irany > 0:
            self.mozdulatok[jobbra_menes_kepek[int(self.kepkocka/1)]]\
                .rajzol(self.megjelenesi_kepernyo, self.pozicio_X, self.pozicio_Y)
        else:
            self.mozdulatok[balra_menes_kepek[int(self.kepkocka/1)]]\
                .rajzol(self.megjelenesi_kepernyo, self.pozicio_X, self.pozicio_Y)

    def ujkep(self):
        if self.kepkocka >= 3:
            self.kepkocka = 0
        else:
            self.kepkocka += 1

    def jobbralep(self):
        self.pozicio_Y += 1
        self.irany = 1
        self.ujkep()

    def balralep(self):
        self.pozicio_Y -= 1
        self.irany = -1
        self.ujkep()

    def fellep(self):
        self.pozicio_X -= 1
        self.ujkep()

    def lelep(self):
        self.pozicio_X += 1
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
        self.szalak = [Vonal()]
        self.utolsoszal = 0

    def uj_szal(self, AX, AY, BX, BY):
        ujszal = Vonal()
        ujszal.pont_beallitas(AX, AY, BX, BY)
        self.szalak.append(ujszal)
        self.utolsoszal += 1

    def rajzol(self, kepernyo):
        szal_eleme = "-"
        for sz in self.szalak:
            irany_y = 1
            irany_x = 1
            if sz.atfogo_Y < 0:
                irany_y = -1
            if sz.atfogo_X < 0:
                irany_x = -1

            elem_x = sz.A.X
            elem_y = sz.A.Y

            if sz.atfogo_X == 0:
                for i in range(sz.atfogo_Y*irany_y):
                    kepernyo.addstr(elem_x, elem_y, szal_eleme)
                    elem_y += irany_y

            elif sz.atfogo_Y == 0:
                for i in range(sz.atfogo_X*irany_x):
                    kepernyo.addstr(elem_x, elem_y, szal_eleme)
                    elem_x += irany_x

            elif abs(sz.atfogo_X) < abs(sz.atfogo_Y):
                szakasz_hossza = int(abs(1.0*sz.atfogo_Y/sz.atfogo_X))
                maradek = abs(sz.atfogo_Y) % abs(sz.atfogo_X)
                for lepes in range(sz.atfogo_X*irany_x):
                    for i in range(szakasz_hossza):
                        kepernyo.addstr(elem_x, elem_y, szal_eleme)
                        elem_y += irany_y
                    if maradek > 0:
                        kepernyo.addstr(elem_x, elem_y, szal_eleme)
                        elem_y += irany_y
                        maradek -= 1
                    elem_x += irany_x
            else:
                szakasz_hossza = int(abs(1.0 * sz.atfogo_X/sz.atfogo_Y))
                maradek = abs(sz.atfogo_X) % abs(sz.atfogo_Y)
                for lepes in range(sz.atfogo_Y*irany_y):
                    for i in range(szakasz_hossza):
                        kepernyo.addstr(elem_x, elem_y, szal_eleme)
                        elem_x += irany_x
                    if maradek > 0:
                        kepernyo.addstr(elem_x, elem_y, szal_eleme)
                        elem_x += irany_x
                        maradek -= 1
                    elem_y += irany_y


idomero = 0
halotszo = False
sajat_halo = Pokhalo()
try:
    fokepernyo = curses.initscr() # letrehoz egy 'curses' ablakot
    fokepernyo.timeout(200)
    curses.noecho()               # a lenyomott karakterek nem jelennek meg
    curses.cbreak()               # a lenyomott billentyut 'enter' nelkul is regisztralja
    curses.curs_set(0)            # a kurzor ne latsszon a kepernyon
    kepernyo_szelesseg, kepernyo_magassag = fokepernyo.getmaxyx()

    botond = Karakter(fokepernyo, 2)
    botond.pozicio_X = 10
    botond.pozicio_Y = 10
    botond.alak_feltoltese("pok.txt")

    legy = Karakter(fokepernyo, 2)
    legy.pozicio_Y = 25
    legy.pozicio_X = 25
    legy.alak_feltoltese("pok.txt")

    szavanna = Vilag(fokepernyo)
    szavanna.feltoltes("doboz.txt")
    
    def kozeprerajzol(string_bemenet):
        fokepernyo.addstr(int(kepernyo_szelesseg/2), int(kepernyo_magassag/2), string_bemenet)
        #fokepernyo.refresh()

    vilag_faljnev = "siksag.txt"
    c = '<gomb>'
    while 1:
        fokepernyo.clear()
        szavanna.rajzol()
        sajat_halo.rajzol(fokepernyo)
        #botond.pozicio_X = szavanna.talaj[botond.pozicio_Y]-botond.magassag
        #legy.pozicio_X = szavanna.talaj[legy.pozicio_Y]-legy.magassag
        botond.rajzol()
        c = fokepernyo.getch()
        if c == ord('x') or c == ord("X"):
            break
        elif c == JOBBRA:
            botond.jobbralep()
        elif c == BALRA:
            botond.balralep()
        elif c == FEL:
            botond.fellep()
        elif c == LE:
            botond.lelep()
        elif c == ord('h') or c == ord('H'):
            halotszo = not halotszo
            if halotszo:
                sajat_halo.uj_szal(botond.pozicio_X+botond.magassag-1, botond.pozicio_Y, botond.pozicio_X+botond.magassag-1, botond.pozicio_Y)
        else:
            pass
        if idomero%2 == 0:
            random_iranyba(legy)
        if halotszo:
            sajat_halo.szalak[sajat_halo.utolsoszal].pont_beallitas(None, None, botond.pozicio_X+botond.magassag-1, botond.pozicio_Y)
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
