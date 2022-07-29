from entity import Entity

class Enemy(Entity):
    def __init__(self,strength,life,mana,name, level=1):
        super().__init__(strength,life,mana,name, level)

