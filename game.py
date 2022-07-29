import sys,time
from sqlalchemy import create_engine,text
import random
import mysql.connector
from enemy import Enemy
from player import Player




POSSIBLE_CLASS = {
    "Wojownik": {
        "zycie": 2,
        "siła": 3,
        "mana": 1,
        "skills": {
            "uderzenie_z_wyskoku" : 'uderzenieZWyskoku()'
        }
    },
    "Mag": {
        "zycie": 1,
        "siła" : 2,
        "mana" : 3
    },
    "Nieumarły": {
        "zycie": 3,
        "siła" : 1,
        "mana" : 2
    }
}

class Game:
    """Klasa game odpowiadająca za działanie całej gry.
    Tutaj dzieje się wszystko.
    """
    def __init__(self):
        self.tour = 0
        self.player = None
        #self.actual_map = map_list
        self.is_game_started = False

    def start_game_msg(self):
        print("Wstęp")

    def main_menu(self):
        print("Zacznij gre, wybierz 1 \n"
              "Zakończ gre, wybierz 0 \n"
              "Wczytaj grę, wybierz 3 \n"
              )
        choice = input("Co chesz zrobić?")
        if choice == '1': self.is_game_started = True and self.start_game()
        if choice == '0':
            print(
                """
                 _   _   ___    _    _   _____   ____     ____
                | |/ / /  _  \ | \  | | |__ __| | ___|  /  ___|
                | ' /  | | | | |  \ | |   | |   | |__   | |
                | <    | | | | | . `  |   | |   |  __|  | |
                | . \  | |_| | | |\   |  _| |_  | |__   | |___
                |_|\_\ \ ____/ |_| \__| |_____| |____|   \____|
                
                  _____    ____    __     __
                /  ____|  |  __ \  \ \   / /
                | |  __   | |__) |  \ \_/ /
                | | |_ |  |  _  /    \   /
                | |__| |  | | \ \     | |
                \______|  |_|  \_\    |_|
                """
            )
            sys.exit()
        if choice == '3':
            self.DBload()

    def start_game(self):
        self.start_game_msg()
        print("Wybierz klase postaci :\n"
              "Wojownik: kliknij 1\n"
              "Mag: kliknij 2\n"
              "Nieumarły: kliknij 3")
        choice_num = input("Co chcesz zrobic?")
        if choice_num == '1':
            choice_class = "Wojownik"
        elif choice_num == '2':
            choice_class = "Mag"
        elif choice_num == '3':
            choice_class = "Nieumarły"
        else:

            print("Zły wybór!")
        try:
            name = input("Podaj swoje imię. ")
            self.player = Player(POSSIBLE_CLASS[choice_class]['siła'],
                                POSSIBLE_CLASS[choice_class]['zycie'],
                                POSSIBLE_CLASS[choice_class]['mana'],
                                name, level=1, gold=0, xp=0)
        except:
            self.start_game()
        self.game_tutorial()

    def game_tutorial(self):
        tutorial_enemy = Enemy(strength=1,life=1,mana=1,name="pies", level=1)
        print("pierwsza walka, powodzenia")
        print(f"""
        |   imie : {self.player.name}                   |   imie : {tutorial_enemy.name}   |
        |   siła : {self.player.strength}               |   siła : {tutorial_enemy.strength}   |
        |   życie :{self.player.life}                   |   życie : {tutorial_enemy.life}   |
        |   mana :{self.player.mana}                    |   mana : {tutorial_enemy.mana}   |
        """)
        while tutorial_enemy.life > 0:
            print("Atak: kliknij 1")
            choice = input("Co wybierasz? ")
            if choice == '1':
                self.player.atack(tutorial_enemy)

        self.player.experience += 2
        self.player.check_player_exp()

        self.game_menu()


    def game_menu(self):
        print("Co zamierzasz robić? \n"
              "Podgląd: kliknij 0\n"
              "Wyświetl ORM: kliknij 1\n"
              "Wyprawa: kliknij 2\n"
              "Trening: kliknij 3\n"
              "Inwentarz: kliknij 4\n"
              "Sklep: kliknij 5\n"
              "Uzdrowiciel: kliknij 6\n"
              "Zapis TXT: kliknij 7\n"
              "Wczytywanie TXT: kliknij 8\n"
              "Zapis DB: kliknij 9\n"
              "Wczytywanie DB: kliknij W"
              )
        choice_num = input("Wybierz akcje")
        if choice_num == '0':
            self.player.show_stats()
            self.game_menu()
        elif choice_num == '1':
            self.orm_sql()
        elif choice_num == '2':
            self.fight()
        elif choice_num == '3':
            self.training()
        elif choice_num == '4':
            self.get_inventory()
        elif choice_num == '5':
            self.shop()
        elif choice_num == '6':
            self.healer()
        elif choice_num == '7':
            self.save()
        elif choice_num == '8':
            self.load()
        elif choice_num == '9':
            self.DBsave()
        elif choice_num == 'W':
            self.DBload()
        else:
            print("Zły wybór!")
            self.game_menu()


    def fight(self):
        name_list = ["pies","mysz","kot"]
        name = random.choice(name_list)

        to_distribution = self.player.strength + self.player.max_life + self.player.mana - 3
        enemy_stats = {
            'strength': 1,
            'life': 1,
            'mana': 1
        }

        for key in enemy_stats:
            distributed = random.randint(0, to_distribution)
            enemy_stats[key] += distributed
            to_distribution -= distributed


        enemy = Enemy(strength=enemy_stats['strength'],life=enemy_stats['life'],mana=enemy_stats['mana'],name=name)
        print("walka, powodzenia")
        print(f"""
        |   imie : {self.player.name}  |   imie : {enemy.name}   |
        |   siła : {self.player.strength}  |   siła : {enemy.strength}   |
        |   życie :{self.player.life}  |   życie : {enemy.life}   |
        |   mana :{self.player.mana}  |   mana : {enemy.mana}   |
        """)

        while enemy:
            print("""Atak: kliknij 1            Ucieczka: kliknij 2""")
            choice = input("Co wybierasz? ")
            if choice == '1':
                result = self.player.atack(enemy)
                if result:
                    self.player.experience += 1
                    self.player.check_player_exp()
                    print(f"Wygrałeś walkę z {enemy.name}")
                    gold = random.randint(0, 3)
                    if gold > 0:
                        print(f"Otrzymujesz trochę złota : ", gold)
                        self.player.gold += gold
                    break
                result = enemy.atack(self.player)
                if result:
                    print(f"Przegrałeś walkę z {enemy.name}")
                    self.player.life = 1
                    break
            if choice == '2':
                result = self.player.escape()
                if result:
                    break
                result = enemy.atack(self.player)
                if result:
                    print(f"Przegrałeś walkę z {enemy.name}")
                    self.player.life = 1
                    break


        self.game_menu()


    def healer(self):
        print('Witaj ja jestem wielki czarodziej i uzdrowie cię za 10 golda')
        print("Zgadzam się: kliknij 1")
        print("Pal wroty: kliknij 2")
        choice = input("Co wybierasz?")

        if choice == '1':
            self.player.heal_player(2)
            self.game_menu()
        elif choice == '2':
            self.game_menu()
    def training(self):
        print(f"    Koszt treningu to narazie 1 gold      ")
        if self.player.gold < 1:
            print("Nie masz pieniędzy")
            self.game_menu()
        else:
            self.player.training()
            self.game_menu()
    def show_stats(self):
        self.player.show_stats()
    def get_name(enemy):
        enemy.get_name()
    def get_inventory(self):
        self.player.get_inventory()
        self.game_menu()
    def shop(self):
        self.player.shop()
        self.game_menu()
    def save(self):
        self.player.save()
        self.game_menu()
    def load(self):
        character_file = open("characters.txt", "r")

        self.experience = int(character_file.readline())
        self.level = int(character_file.readline())
        self.name = character_file.readline()
        self.max_life = int(character_file.readline())
        self.strength = int(character_file.readline())
        self.mana = int(character_file.readline())
        self.gold = int(character_file.readline())

        self.player = Player(strength=self.strength, life=self.max_life, mana=self.mana, name=self.name, gold=self.gold, level=self.level)
        character_file.close()
        self.game_menu()
    def DBsave(self):
        self.player.DBsave()
        self.game_menu()
    def DBload(self):
        connection = mysql.connector.connect(user='root', password='1234', host='127.0.0.1',
                                             database='rpggame', auth_plugin='mysql_native_password')
        cursor = connection.cursor(buffered=True)

        loadXp = "SELECT xp FROM players"
        loadLvl = "SELECT lvl FROM players"
        loadName = "SELECT name FROM players"
        loadHp = "SELECT hp FROM players"
        loadStrength = "SELECT power FROM players"
        loadMana = "SELECT mana FROM players"
        loadGold = "SELECT gold FROM players"

        cursor.execute(loadXp)
        self.experience = cursor.fetchone()
        cursor.execute(loadLvl)
        self.level = cursor.fetchone()
        cursor.execute(loadName)
        self.name = cursor.fetchone()
        cursor.execute(loadHp)
        self.max_life = cursor.fetchone()
        cursor.execute(loadStrength)
        self.strength = cursor.fetchone()
        cursor.execute(loadMana)
        self.mana = cursor.fetchone()
        cursor.execute(loadGold)
        self.gold = cursor.fetchone()


        self.player = Player(strength=self.strength, life=self.max_life, mana=self.mana, name=self.name, gold=self.gold,
                             level=self.level)
        connection.commit()
        connection.close()

        self.game_menu()
    def orm_sql(self):
        engine = create_engine('mysql+pymsql://root:1234@127.0.0.1/rpggame', echo=True) #//<username>:<password>@<host>/<dbname>
        with engine.connect() as conn:

            result = conn.execute(text("select 'hello world'"))

        print(result.all())

