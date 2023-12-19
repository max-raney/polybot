# PolyDraw.py
# UI
import pygame
import numpy as np
import os
from PolyEntities import Map, Tile, Unit


class Drawer:
    BASE_PATH = os.path.dirname(os.path.realpath(__file__))
    MOVEMENT_RETICLE = 'movement_reticle'

    REFERENCE_IMAGES = {
        Tile.LandType.PLAINS: pygame.image.load(os.path.join(BASE_PATH, "Art", "Terrain", "Tiles", "ground_1.png")),
        Tile.LandType.OCEAN: pygame.image.load(os.path.join(BASE_PATH, "Art", "Terrain", "Tiles", "ground_11.png")),
        Tile.LandType.MOUNTAINS: pygame.image.load(os.path.join(BASE_PATH, "Art", "Terrain", "Mountains", "mountain_5.png")),

        Unit.UnitType.SCOUT: pygame.transform.scale_by(
            pygame.image.load(os.path.join(BASE_PATH, 'Art', 'Units', 'Imperius', 'Default', 'Imperius_Default_Scout.png')), 3),
        Unit.UnitType.WARRIOR: pygame.transform.scale_by(
            pygame.image.load(os.path.join(BASE_PATH, 'Art', 'Units', 'Imperius', 'Default', 'Imperius_Default_Warrior.png')), 3),
        MOVEMENT_RETICLE: pygame.image.load(os.path.join(BASE_PATH, "Art", "Misc", "moveTarget.png")),
    }

    SCREEN_DIMENSIONS = [1600, 900]
    TILE_DIMENSIONS = REFERENCE_IMAGES[Tile.LandType.PLAINS].get_size()
    UNIT_DIMENSIONS = REFERENCE_IMAGES[Unit.UnitType.SCOUT].get_size()

    def __init__(self, game_map):
        self.screen = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.game_map = game_map
        self.images = {}
        self.scale = 1
        self.camera_offset = [0, 0]

    def _tile_coordinates(self, coordinate, vertical_offset=0, horizontal_offset=0):
        offset = (horizontal_offset, -vertical_offset)
        # translates coordinates into pixel values
        translation_matrix = np.array([[507, 507], [-302.56, 302.56]]) * self.scale
        # offset from (0,0)
        offset_vector = np.array([[self.camera_offset[0] + offset[0] * self.scale],
                                  [self.camera_offset[1] + offset[1] * self.scale + self.SCREEN_DIMENSIONS[1] / 2]])
        # switch to column vector for multiplication
        coordinate = np.array([[coordinate[0]], [coordinate[1]]])

        # coordinates @ translation + offset is the pixel location
        return np.floor(translation_matrix @ coordinate + offset_vector).astype(int)

    # returns the X and Y tile coordinates based on the pixel coordinates (reverse of _tile_coordinates)
    def tile_clicked(self, pixel_coordinates):

        # translates coordinates into pixel values
        inverse_translation_matrix = np.array([[0.000986, -0.00165], [0.000986, 0.00165]]) / self.scale
        # offset from (0,0)
        offset_vector = np.array([[self.camera_offset[0]],
                                  [self.camera_offset[1] + self.SCREEN_DIMENSIONS[1] / 2]])
        # switch to column vector for multiplication
        pixel_vector = np.array([[pixel_coordinates[0]], [pixel_coordinates[1]]])

        # subtract offset, tile value to center, and reverse transformation is the coordinate
        tile_coordinate = np.round(inverse_translation_matrix @ (pixel_vector - offset_vector)).astype(int)

        # print(f"Player selected tile {tile_coordinate}")
        return tile_coordinate.flatten()

    # draws image centered on coordinate
    def _draw_image(self, image, coordinates, surface=None):
        image_offset = np.array(image.get_size()) // 2
        if surface is None:
            self.screen.blit(image, coordinates.T[0] - image_offset)
        else:
            surface.blit(image, coordinates.T[0] - image_offset)

    def _resize_images(self, scale):
        if scale != self.scale:
            for land_type, image in self.REFERENCE_IMAGES.items():
                self.images[land_type] = pygame.transform.scale_by(image, scale)
            self.scale = scale

    def _draw_map(self):
        map_surface = pygame.Surface(self.screen.get_size())

        for x in range(self.game_map.size - 1, -1, -1):
            for y in range(self.game_map.size):
                tile_coords = self._tile_coordinates((x, y))
                image = self.images[self.game_map.tiles[x][y].land_type]
                self._draw_image(image, tile_coords, map_surface)

        self.screen.blit(map_surface, (0, 0))

    # Draws all units
    def _draw_units(self):
        for unit in self.game_map.units:
            coordinates = self._tile_coordinates((unit.x, unit.y), 250)
            image = self.images[unit.unit_type]
            self._draw_image(image, coordinates)

    def draw_frame(self, camera_offset, rescale_value):
        self._resize_images(rescale_value)
        self.camera_offset = camera_offset
        self.screen.fill((0, 0, 0))
        self._draw_map()
        self._draw_units()
        pygame.display.flip()
