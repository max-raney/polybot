# PolyDraw.py
import pygame
import numpy as np
from PolyEntities import Map, Tile, Unit


class Drawer:
    REFERENCE_IMAGES = {
        Tile.LandType.GRASS: pygame.image.load("Art/Terrain/Tiles/ground_1.png"),
        Tile.LandType.WATER: pygame.image.load("Art/Terrain/Tiles/ground_10.png"),

        Unit.UnitType.SCOUT: pygame.transform.scale_by(
            pygame.image.load('Art/Units/Imperius/Default/Imperius_Default_Scout.png'), 3),
        Unit.UnitType.WARRIOR: pygame.transform.scale_by(
            pygame.image.load('Art/Units/Imperius/Default/Imperius_Default_Warrior.png'), 3)
    }

    SCREEN_DIMENSIONS = [1600, 900]
    TILE_DIMENSIONS = REFERENCE_IMAGES[Tile.LandType.GRASS].get_size()
    UNIT_DIMENSIONS = REFERENCE_IMAGES[Unit.UnitType.SCOUT].get_size()

    def __init__(self, game_map):
        self.screen = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.game_map = game_map
        self.images = {}
        self._resize_images(0.1)
        self.camera_offset = [0, 0]

    def _calculate_tile_coords(self, x, y, offset=[0, 0]):
        A = np.array([[0.4975, 0.4975], [-0.31, 0.31]])
        coordinate = np.array([[x], [y]])
        offset_v = np.array([[self.camera_offset[0] + offset[0]],
                             [self.camera_offset[1] + offset[1] + self.SCREEN_DIMENSIONS[1] / 2]])
        resize_matrix = np.diag(self.TILE_DIMENSIONS) * self.scale

        return np.floor(resize_matrix @ (A @ coordinate) + offset_v).astype(int)

    def _resize_images(self, scale):
        for land_type, image in self.REFERENCE_IMAGES.items():
            self.images[land_type] = pygame.transform.scale_by(image, scale)
        self.scale = scale

    def _draw_map(self):
        map_surface = pygame.Surface(self.screen.get_size())

        for x in range(self.game_map.size - 1, -1, -1):
            for y in range(self.game_map.size):
                tile_coords = self._calculate_tile_coords(x, y)
                image = self.images[self.game_map.tiles[x][y].land_type]
                map_surface.blit(image, tile_coords.T[0])

        self.screen.blit(map_surface, (0, 0))

    # Draws all units
    def _draw_units(self):
        for unit in self.game_map.units:
            coords = self._calculate_tile_coords(unit.x, unit.y, [8, -30])
            image = self.images[unit.unit_type]
            self.screen.blit(image, coords.T[0])

    def draw_frame(self, camera_offset):
        self.camera_offset = camera_offset
        self.screen.fill((0, 0, 0))
        self._draw_map()
        self._draw_units()
        pygame.display.flip()
