import sys
import time
import curses # kontroll a kepernyo felett

FEL = 65
LE = 66
JOBBRA = 67
BALRA = 68

class Karakter:
    def __init__(self, megjelenesi_kepernyo):
        self.megjelenesi_kepernyo = megjelenesi_kepernyo
        self.alak_jobbra = ["", "", "", ""]
        self.alak_balra = ["", "", "", ""]
        self.alak_jobbra_2 = ["", "", "", ""]
        self.alak_balra_2 = ["", "", "", ""]
        self.pozicio_X = 0
        self.pozicio_Y = 0
        self.irany = 1
        self.mozdulat = 0
    
    def rajzol(self):
        if self.irany > 0:
            for i in range(4):
                self.megjelenesi_kepernyo.addstr(self.pozicio_X+i, self.pozicio_Y, self.alak_jobbra[i])
            #self.megjelenesi_kepernyo.refresh()
        else:
            for i in range(4):
                self.megjelenesi_kepernyo.addstr(self.pozicio_X+i, self.pozicio_Y, self.alak_balra[i])
            #self.megjelenesi_kepernyo.refresh()

    def jobbralep(self):
        self.pozicio_Y += 1
        self.irany = 1

    def balralep(self):
        self.pozicio_Y -= 1
        self.irany = -1

    def fellep(self):
        self.pozicio_X -= 1

    def lelep(self):
        self.pozicio_X += 1
    
    def alak_feltoltese(self, alak_filenev):
        alak = open(alak_filenev, 'r')
        i = 0
        while i < 4:
            sor = alak.readline()
            self.alak_jobbra[i] = sor[:-1]
            i += 1
        while i < 8:
            sor = alak.readline()
            self.alak_balra[i-4] = sor[:-1]
            i += 1
        while i < 12:
            sor = alak.readline()
            self.alak_jobbra_2[i-8] = sor[:-1]
            i += 1
        while i < 16:
            sor = alak.readline()
            self.alak_balra_2[i-12] = sor[:-1]
            i += 1

        alak.close()


class Vilag:
    def __init__(self, megjelenitesi_kepernyo):
        self.megjelenitesi_kepernyo = megjelenitesi_kepernyo
        self.sorszeletek = [""]
        self.talaj = [9]*92
        self.magassag = 1
        self.szelesseg = 1
        for r in range(18, 44):
            self.talaj[r] = 10
        for r in range(60, 90):
            self.talaj[r] = 8

    def feltoltes(self, filenev):
        kepfajl = open(filenev, 'r')
        kepsor = kepfajl.readline()
        while len(kepsor):
            self.sorszeletek.append(kepsor[:-1])
            if self.szelesseg < len(kepsor):
                self.szelesseg = len(kepsor) + 1
            for j in range(self.szelesseg - len(kepsor[:-1])):
                self.sorszeletek[self.magassag] += " "
            self.magassag += 1
            kepsor = kepfajl.readline()[:-1]
        kepfajl.close()

    def rajzol(self):
        for i in range(len(self.sorszeletek)):
            self.megjelenitesi_kepernyo.addstr(i, 0, self.sorszeletek[i])
        #self.megjelenitesi_kepernyo.refresh()


def vilag_betoltese(fajlnev):
    vilag_kep = open(fajlnev, 'r')
    fokepernyo.addstr(0, 0, vilag_kep.read())
    vilag_kep.close()

try:
    fokepernyo = curses.initscr() # letrehoz egy 'curses' ablakot
    curses.noecho()               # a lenyomott karakterek nem jelennek meg
    curses.cbreak()               # a lenyomott billentyut 'enter' nelkul is regisztralja
    curses.curs_set(0)            # a kurzor ne latsszon a kepernyon
    kepernyo_szelesseg, kepernyo_magassag = fokepernyo.getmaxyx()
    botond = Karakter(fokepernyo)
    botond.pozicio_X = 5
    botond.pozicio_Y = 10
    botond.alak_feltoltese("harcos.txt")

    szavanna = Vilag(fokepernyo)
    szavanna.feltoltes("siksag.txt")
    
    def kozeprerajzol(string_bemenet):
        fokepernyo.addstr(int(kepernyo_szelesseg/2), int(kepernyo_magassag/2), string_bemenet)
        #fokepernyo.refresh()

    vilag_faljnev = "siksag.txt"
    c = '<gomb>'
    while 1:
        fokepernyo.clear()
        szavanna.rajzol()
        botond.pozicio_X = szavanna.talaj[botond.pozicio_Y]
        #fokepernyo.addstr(1, 1, "A kilepeshez nyomd meg az X gombot.")
        botond.rajzol()
        c = fokepernyo.getch()
        kozeprerajzol("A lenyomott billentyu: " + str(c))
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
        fokepernyo.refresh()


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
