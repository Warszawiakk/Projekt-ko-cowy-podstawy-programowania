import os
import time
import keyboard

class Map:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.cache: list[list[str]] = []
        self.clear()

    def clear(self):
        self.cache = []
        char = "X"
        self.cache.append([char] * (self.y + 2))
        for _ in range(self.x):
            self.cache.append([char] + self.y * [" "] + [char])
        self.cache.append([char] * (self.y + 2))

    def set_char(self, x, y, char):
        self.cache[x + 1][y + 1] = char

    def __repr__(self) -> str:
        napis = ""
        for row in self.cache:
            napis += "".join(row) + "\n"
        return napis
# Kod z lekcji /\

class Ball:
    def __init__(self) -> None:
        self.speedX = 1
        self.speedY = 1
        self.posX = 7
        self.posY = 0
# Kod z lekcji /\

    def update_position(self, map: Map, p1, p2): # Funkcja po części z lekcji
        self.posX += self.speedX
        self.posY += self.speedY
        if self.posX >= map.x or self.posX <= 0: # dodaję segment, który dodaje punkty do odpowiedniego gracza w zależności od tego, czy udało odbić się piłkę
            self.speedX *= -1
        if self.posY >= map.y: # jeżeli posy jest większe lub równe map.y, wtedy self.speed odwraca się (efekt odbicia), wtedy również zostają dodane punkty dla gracza1
            self.speedY *= -1
            p1.points += 1
        elif self.posY < 0:     # vice versa
            self.speedY *= -1
            p2.points += 1
        if self.posY == p1.posY and p1.posX <= self.posX < p1.posX + 3: # mechanizm odbijania od paletek (potrzebny do naliczania punktów). Działa na takiej samej
            self.speedY *= -1                                           # zasadzie co odbijanie od granicy 
        if self.posY == p2.posY and p2.posX <= self.posX < p2.posX + 3:
            self.speedY *= -1

    def draw_on(self, map: Map):
        map.set_char(self.posX, self.posY, 'O')

class Palette:
    def __init__(self, x: int, y: int) -> None:
        self.posX = x
        self.posY = y
        self.points = 0

    def draw_on(self, map: Map):
        for offset in range(3):
            map.set_char(self.posX + offset, self.posY, '|')

    def move_up(self, limit: int):
        if self.posX > 1:
            self.posX -= 1

    def move_down(self, limit: int):
        if self.posX < limit - 3:
            self.posX += 1

x = 35
y = 15
m = Map(y, x)
b = Ball()
p1 = Palette(1, 0)
p2 = Palette(1, 34)

while True:
    m.clear()
    b.update_position(m, p1, p2)

    b.draw_on(m)
    p1.draw_on(m)
    p2.draw_on(m)

    if keyboard.is_pressed("w"):
        p1.move_up(m.x)
    elif keyboard.is_pressed("s"):
        p1.move_down(m.x)
    elif keyboard.is_pressed("t"):
        p2.move_up(m.x)
    elif keyboard.is_pressed("g"):
        p2.move_down(m.x)

    os.system('cls')
    print(m)
    print(f"Player 1: {p1.points} | Player 2: {p2.points}")
    time.sleep(0.3)
