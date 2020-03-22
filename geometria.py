import math

KEPARANY = 2
MIN_LIM = 0.00001
LATSZO_LIMIT = 0.7
LATSZO_TAN = 0.1
FELBONTAS = 1

class Szog:
    def __init__(self, fok=0.0, sin=0.0, cos=1.0):
        self.fok = fok
        self.sin = sin
        self.cos = cos
        self.ujraszamol_fok(fok)

    def ujraszamol_fok(self, uj_fok):
        self.fok = uj_fok
        self.sin = math.sin(uj_fok)
        self.cos = math.cos(uj_fok)

    def ujraszamol_sin(self, uj_sin):
        self.fok = math.asin(uj_sin)
        self.sin = uj_sin
        self.cos = math.cos(self.fok)

    def ujraszamol_cos(self, uj_cos):
        self.fok = math.acos(uj_cos)
        self.sin = math.sin(self.fok)
        self.cos = uj_cos


class Pont:
    def __init__(self, x_init=0, y_init=0):
        self.x = x_init
        self.y = y_init


class Vektor:
    def __init__(self, kezdopont=None, vegpont=None):
        self.kezdopont = Pont()
        self.vegpont = Pont()
        if kezdopont is not None:
            self.kezdopont.x = kezdopont.x
            self.kezdopont.y = kezdopont.y
        if vegpont is not None:
            self.vegpont.x = vegpont.x
            self.vegpont.y = vegpont.y
        self.vetulet_x, self.vetulet_y = self.vetuleteket_szamol()
        self.hossz = self.hosszatszamol()
        self.sin = 0.0
        self.cos = 1.0
        self.tan = 0.0
        self.ctan = 1000.0
        self.ujraszamol()

    def vetuleteket_szamol(self):
        vetulet_x = float(self.vegpont.x - self.kezdopont.x)
        vetulet_y = float(self.vegpont.y - self.kezdopont.y)
        return vetulet_x, vetulet_y

    def hosszatszamol(self):
        return math.sqrt(math.pow(self.vetulet_x, 2) + pow(self.vetulet_y, 2))

    def uj_kezdopont(self, uj_pont):
        self.kezdopont.x = uj_pont.x
        self.kezdopont.y = uj_pont.y
        self.ujraszamol()

    def uj_vegpont(self, uj_pont):
        self.vegpont.x = uj_pont.x
        self.vegpont.y = uj_pont.y
        self.ujraszamol()

    def ujraszamol(self):
        self.vetulet_x, self.vetulet_y = self.vetuleteket_szamol()
        self.hossz = self.hosszatszamol()

        if MIN_LIM > self.hossz > -MIN_LIM:
            self.sin = 0.0
            self.cos = 1.0
        else:
            self.sin = self.vetulet_x / self.hossz
            self.cos = self.vetulet_y / self.hossz

        if -MIN_LIM < self.vetulet_x < MIN_LIM:
            self.tan = 1000.0
        else:
            self.tan = self.vetulet_y / self.vetulet_x

        if MIN_LIM > self.vetulet_y > -MIN_LIM:
            self.ctan = 1000.0
        else:
            self.ctan = self.vetulet_x / self.vetulet_y

    def x_helyen(self, x):
        y = -1
        if self.kezdopont.x < x < self.vegpont.x or self.kezdopont.x > x > self.vegpont.x:
            y = (x-self.kezdopont.x) * self.tan
            if self.kezdopont.y < y < self.vegpont.y or self.kezdopont.y > y > self.vegpont.y:
                return y + self.kezdopont.y
        return None

    def y_helyen(self, y):
        x = -1
        if self.kezdopont.y < y < self.vegpont.y or self.kezdopont.y > y > self.vegpont.y:
            x = (y-self.kezdopont.y) * self.ctan
            if self.kezdopont.x < x < self.vegpont.x or self.kezdopont.x > x > self.vegpont.x:
                return x + self.kezdopont.x
        return None


def pont_vonal_kornyezeteben(pont, vonal, kornyezet):
    if abs(vonal.vetulet_x) >= abs(vonal.vetulet_y):
        x_metszet = vonal.x_helyen(pont.x)
        if x_metszet is None:
            return False
        min_y = x_metszet - kornyezet + vonal.kezdopont.y
        max_y = x_metszet + kornyezet + vonal.kezdopont.y
        if min_y < pont.y < max_y:
            return True
        else:
            return False
    else:
        x_metszet = vonal.y_helyen(pont.y)
        if x_metszet is None:
            return False
        min_y = x_metszet - kornyezet + vonal.kezdopont.x
        max_y = x_metszet + kornyezet + vonal.kezdopont.x
        if min_y < pont.x < max_y:
            return True
        else:
            return False


def vonalat_rajzol(vonal, kepernyo, elem = '-'):
    y = vonal.kezdopont.y
    x = vonal.kezdopont.x
    y0 = vonal.kezdopont.y
    x0 = vonal.kezdopont.x
    kepernyo.addstr(int(vonal.kezdopont.x), int(vonal.kezdopont.y), elem)
    if abs(vonal.vetulet_x) >= abs(vonal.vetulet_y):
        if vonal.vetulet_x >= 0:
            while x < vonal.vegpont.x:
                x += FELBONTAS
                y = y0 + vonal.tan * (x-x0)
                y_int = int(math.ceil(y))
                x_int = int(math.ceil(x))
                if vonal.tan < LATSZO_TAN:
                    kepernyo.addstr(x_int, y_int, elem)
                elif (y_int - y) < LATSZO_LIMIT:
                    kepernyo.addstr(x_int, y_int, elem)
        else:
            while x > vonal.vegpont.x:
                x -= FELBONTAS
                y = y0 + vonal.tan * (x-x0)
                y_int = int(math.ceil(y))
                x_int = int(math.ceil(x))
                if vonal.tan < LATSZO_TAN:
                    kepernyo.addstr(x_int, y_int, elem)
                elif (x_int - x) < LATSZO_LIMIT:
                    kepernyo.addstr(x_int, y_int, elem)
    else:
        if vonal.vetulet_y >= 0:
            while y < vonal.vegpont.y:
                y_int = int(math.ceil(y))
                x_int = int(math.ceil(x))
                if vonal.ctan < LATSZO_TAN:
                    kepernyo.addstr(x_int, y_int, elem)
                elif (x_int - x) < LATSZO_LIMIT:
                    kepernyo.addstr(x_int, y_int, elem)
                y += FELBONTAS
                x = x0 + vonal.ctan * (y-y0)
        else:
            while y > vonal.vegpont.y:
                y_int = int(math.ceil(y))
                x_int = int(math.ceil(x))
                if vonal.ctan < LATSZO_TAN:
                    kepernyo.addstr(x_int, y_int, elem)
                elif (x_int - x) < LATSZO_LIMIT:
                    kepernyo.addstr(x_int, y_int, elem)
                y -= FELBONTAS
                x = x0 + vonal.ctan * (y-y0)