from entity import Entity
from sqlalchemy import create_engine
import mysql.connector


class Player(Entity):
    def __init__(self, strength, life, mana, name, gold=0, level=1, xp=0):
        super().__init__(strength, life, mana, name, gold, level, xp)
        self.level = level
        self.max_life = life
        self.available_points = 0
        self.inventory = []


    def check_player_exp(self):
        if self.experience > self.level:
            self.level += 1
            self.experience = 0
            self.available_points += 1
            print(f"Awansowałeś na {self.level} poziom!")

            self.add_statistic()

    def heal_player(self, value):
        if self.life + value <= self.max_life:
            self.life += value
        else:
            self.life = self.max_life

    def add_statistic(self):
        print("zdobywasz 1 pkt. statystyk, wykorzystaj go mądrze")
        print(f"""
                        | poziom : {self.level} 
                        | imie   : {self.name}
                        | życie  : {self.life} / {self.max_life} 
                        | siła   : {self.strength}
                        | mana   : {self.mana}
            """)

        add_stat = input(f"""
                    dodaj do siły = wybierz 1
                    dodaj do życia = wybierz 2
                    dodaj do many = wybierz 3
            """)

        if add_stat == '1':
            self.strength += 1
        elif add_stat == '2':
            self.max_life += 1
            self.life = self.max_life
        elif add_stat == '3':
            self.mana += 1
        else:
            print(f"Zły wybór")
            self.add_statistic()
        self.available_points -= 1

    def show_stats(self):
        print(f"""
        | doświadczenie: {self.experience}
        | poziom : {self.level} 
        | imie   : {self.name}
        | życie  : {self.life}  / {self.max_life}
        | siła   : {self.strength}
        | mana   : {self.mana}
        | złoto  : {self.gold}

        """)

    def training(self):
        add_stat = input(f"""
            Witaj za niewielką opłatą możesz zwiększyć swoje umiejętności:  

                    | życie  : {self.life}  /{self.max_life}
                    | siła   : {self.strength}
                    | mana   : {self.mana}
                    | złoto  : {self.gold}

                                dodaj do siły = wybierz 1
                                dodaj do życia = wybierz 2
                                dodaj do many = wybierz 3
                    """)
        if add_stat == '1':
            self.strength += 1
            self.gold -= 1
        elif add_stat == '2':
            self.max_life += 1
            self.life = self.max_life
            self.gold -= 1
        elif add_stat == '3':
            self.mana += 1
            self.gold -= 1
        else:
            print(f"Zły wybór")
            self.training()
    def get_inventory(self):
        print("Twoje przedmioty to")
        print(self.inventory)



    def save(self):

        xp = self.experience
        lvl = self.level
        name = self.name
        hp = self.max_life
        power = self.strength
        mana = self.mana
        gold = self.gold

        character_file = open("characters.txt", "w")
        character_file.write(xp)
        character_file.write("\n")
        character_file.write(lvl)
        character_file.write("\n")
        character_file.write(name)
        character_file.write("\n")
        character_file.write(hp)
        character_file.write("\n")
        character_file.write(power)
        character_file.write("\n")
        character_file.write(mana)
        character_file.write("\n")
        character_file.write(gold)
        character_file.close()
    def DBsave(self):
        connection = mysql.connector.connect(user='root', password='1234', host='127.0.0.1',
                                             database='rpggame', auth_plugin='mysql_native_password')
        cursor = connection.cursor()

        insertQuery = "INSERT INTO players(xp, lvl, name, hp, power, mana, gold) VALUES(%(xp)s, %(lvl)s, %(name)s, %(hp)s, %(power)s, %(mana)s, %(gold)s)"
        insertData = {
            'xp' : self.experience,
            'lvl' : self.level,
            'name' : self.name,
            'hp' : self.max_life,
            'power' : self.strength,
            'mana' : self.mana,
            'gold' : self.gold

        }
        deleteQuery = "DELETE FROM players"
        cursor.execute(deleteQuery)
        cursor.execute(insertQuery, insertData)

        connection.commit()
        connection.close()

    def shop(self):

        connection = mysql.connector.connect(user='root', password='1234', host='127.0.0.1',
                                             database='rpggame', auth_plugin='mysql_native_password')
        cursor = connection.cursor(buffered=True)

        loadAllItems = "SELECT iname, istrength, ilife, imana from items"

        loadSword = "SELECT iname, istrength, ilife, imana FROM items WHERE iname = 'miecz'"
        loadSwordName = "SELECT iname FROM items WHERE iname = 'miecz'"
        loadSwordStrength = "SELECT istrength FROM items WHERE iname = 'miecz'"
        loadSwordLife = "SELECT ilife FROM items WHERE iname = 'miecz'"
        loadSwordMana = "SELECT imana FROM items WHERE iname = 'miecz'"

        loadShield = "SELECT iname, istrength, ilife, imana FROM items WHERE iname = 'tarcza'"
        loadShieldName = "SELECT iname FROM items WHERE iname = 'tarcza'"
        loadShieldStrength = "SELECT istrength FROM items WHERE iname = 'tarcza'"
        loadShieldLife = "SELECT ilife FROM items WHERE iname = 'tarcza'"
        loadShieldMana = "SELECT imana FROM items WHERE iname = 'tarcza'"

        loadHelm = "SELECT iname, istrength, ilife, imana FROM items WHERE iname = 'helm'"
        loadHelmName = "SELECT iname FROM items WHERE iname = 'helm'"
        loadHelmStrength = "SELECT istrength FROM items WHERE iname = 'helm'"
        loadHelmLife = "SELECT ilife FROM items WHERE iname = 'helm'"
        loadHelmMana = "SELECT imana FROM items WHERE iname = 'helm'"



        print(f"Witaj, mam przedmioty pomagajace w walce (miecz, tarcza, helm)")
        cursor.execute(loadAllItems)
        print(cursor.fetchall())
        showitem = input(f"Chcesz zobaczyc co daja (w kolejnosci sila, zycie, mana)? Jak tak to podaj nazwe przedmitu: ")
        if showitem == 'miecz':
            cursor.execute(loadSword)
            myresult = cursor.fetchall()

            for m in myresult:
                print(m)
                buy = input(f"Koszt takiego cacka to tylko 1 gold. Chcesz kupic?(tak/nie)")
                if buy == 'tak':
                   self.gold -= 1
                   self.inventory.append(m)

        elif showitem == 'tarcza':
            cursor.execute(loadShield)
            myresult = cursor.fetchall()

            for t in myresult:
                print(t)
                buy = input(f"Koszt takiego cacka to tylko 1 gold. Chcesz kupic?(tak/nie)")
                if buy == 'tak':
                    self.gold -= 1
                    self.inventory.append(t)

        else:
            cursor.execute(loadHelm)
            myresult = cursor.fetchall()

            for h in myresult:
                print(h)
                buy = input(f"Koszt takiego cacka to tylko 1 gold. Chcesz kupic?(tak/nie)")
                if buy == 'tak':
                    self.gold -= 1
                    self.inventory.append(h)

        connection.commit()
        connection.close()




