import random,sys
from random import choice

class Entity:
    def __init__(self,strength,life,mana,name,gold,xp=0, level=1):
        self.strength = strength
        self.life = life
        self.mana = mana
        self.name = name
        self.level = level
        self.gold = gold
        self.experience = xp
        # self.inventory = []

    def atack(self, enemy):
        hit = " trafił swoim ciosem zadając, "
        die = " ginie w walce "
        miss = " nie trafił swoim ciosem "
        if random.random() > 0.50:
            enemy.life -= self.strength
            print(f"{self.name}" + hit[:] + f"{self.strength}")
            if enemy.life <= 0:
                print(f"{enemy.name}" ,die[:])
                return True
        else:
            print(f"{self.name}", miss[:])
            return False
    def escape(self):
        try_escape = " Podjęto próbe ucieczki, czy sie powiedzie?? "
        escape = " Uff udało się, nasępnym razem możesz nie mieć tyle farta "
        no_escape = "Nie udało się, tracisz kolejkę"
        print(try_escape[:])
        if random.randint(0,1) > 0:
            print(escape[:])
            return True
        else:
            print(no_escape[:])
            return False





