# PolyLogic.py
# Controls the logic for the game
from PolyEntities import Unit, City, Map, Tile


class GameController:
    def __init__(self, game_map):
        self.selected = None
        self.map = game_map

    def click_tile(self, location):
        print(f"clicking tile {location}")
        if isinstance(self.selected, Unit):
            self._move_unit(self.selected, location)
            print(f"moving unit to {location}")
        else:
            self.selected = self.map.tiles[location[0]][location[1]]
            print(f"selected tile {self.selected}")
            print(f"tile unit is {self.selected.unit}")
            if self.selected.unit is not None:
                self.selected = self.selected.unit
                print(f"selected unit {self.selected}")

    def _move_unit(self, unit, location):
        self.map.tiles[location[0]][location[1]].unit = self.map.tiles[unit.x][unit.y].unit
        self.map.tiles[unit.x][unit.y].unit = None
        unit.x = location[0]
        unit.y = location[1]
        self.selected = None
