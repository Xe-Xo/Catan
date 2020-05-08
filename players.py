from resources import ResourceBunch
import random
from game import *


class Player():
    def __init__(self,playerindex):
        self.resources = ResourceBunch(0,0,0,0,0)
        self.playerindex = playerindex

    def add_resouces(self,resourcebunch):
        self.resources = self.resources + resourcebunch

    def discard_resouces(self,resourcebunch):
        self.resources = self.resources.discard(resourcebunch)

class Human(Player):

    def __init__(self,playerindex):
        super().__init__(playerindex)

class Bot(Player):

    def __init__(self,playerindex):
        super().__init__(playerindex)
