# Polytopia
import numpy as np
import pygame


class Map:
    def __init__(self, size):
        # Initialize the map as a 2D array of tile types
        self.tiles = np.empty((size, size), dtype=Tile)
        self.size = size
        self.troop = None

        for x in range(size):
            for y in range(size):
                # self.tiles[x][y] = Tile('grass')
                if (x + y) % 2 == 0:
                    self.tiles[x][y] = Tile('grass')
                else:
                    self.tiles[x][y] = Tile('water')

    def draw(self, dimensions):

        map_surface = pygame.Surface(dimensions['screen'].get_size())

        for x in range(self.size-1, -1, -1):
            for y in range(self.size):
                # Calculate the position of the tile on the screen
                tile_coords = index_to_pixel(x, y, dimensions)

                scaled_tile = pygame.transform.scale(self.tiles[x][y].image, dimensions['tile_size'].astype(int))


                # Draw the scaled tile image at the calculated position
                map_surface.blit(scaled_tile, tile_coords.T[0])
        
        dimensions['screen'].blit(map_surface, (0, 0))

class Tile():
    def __init__(self, land_type):
        self.land_type = land_type
        if land_type == 'grass':
            self.image = pygame.image.load("Art/Terrain/Tiles/ground_1.png")
        else:
            self.image = pygame.image.load("Art/Terrain/Tiles/ground_10.png")

class City():
    ''

class Unit():
    unit_image = pygame.image.load('Art/Units/Imperius/Default/Imperius_Default_Scout.png')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, dimensions):
        coords = index_to_pixel(self.x, self.y, dimensions, [8, -30])
        scaled_image = pygame.transform.scale(self.unit_image, dimensions['unit_size'].astype(int))

        dimensions['screen'].blit(scaled_image, coords.T[0])

class Warrior(Unit):
    attack = 2
    defense = 2
    movement = 1
    range = 1

    unit_image = pygame.image.load('Art/Units/Imperius/Default/Imperius_Default_Warrior.png')
    
    def __init__(self, x, y):
        self.health = 10
        super().__init__(x, y)

def scaled_size(image, dimensions):
    return np.array([image.get_width(), image.get_height()]) // dimensions['scale']

def index_to_pixel(x, y, dimensions, offset = [0,0]):
    A = np.array([[0.4975, 0.4975],[-0.31, 0.31]])
    coordinate = np.array([[x], [y]])
    offset_v = np.array([[dimensions['camera_offset'][0] + offset[0]], [dimensions['camera_offset'][1] + offset[1] + dimensions['screen_dims'][1]/2]])
    resize_matrix = np.diag(dimensions['tile_size'])

    return np.floor(resize_matrix @ (A @ coordinate) + offset_v).astype(int)

def main():
    # Initialize Pygame
    pygame.init()

    dimensions = {
        'screen_dims': [1600, 900],
        'camera_offset': [0, 0],
        'scale': 10
    }


    # Create a Pygame window
    dimensions['screen'] = pygame.display.set_mode(dimensions['screen_dims'])
    dimensions['tile_size'] = scaled_size(pygame.image.load("Art/Terrain/Tiles/ground_1.png"), dimensions)
    dimensions['unit_size'] = scaled_size(pygame.image.load('Art/Units/Imperius/Default/Imperius_Default_Warrior.png'), dimensions) * 3


    # Set the window title
    pygame.display.set_caption("Fake Poly")

    # Load your custom tile image
    tile_image = pygame.image.load("Art/Terrain/Tiles/ground_1.png")

    # Create a map with a size of 10x10 (adjust the size as needed)
    game_map = Map(20)

    # Initialize two warriors
    warrior_1 = Warrior(0, 0)
    warrior_2 = Warrior(4, 5)

    # Initial variables for click-and-drag
    dragging = False
    start_x, start_y = 0, 0
    scroll_speed = 1

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    start_x, start_y = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    x, y = event.pos
                    # Calculate the difference in mouse position and move the map accordingly
                    dimensions['camera_offset'][0] += (x - start_x) * scroll_speed
                    dimensions['camera_offset'][1] += (y - start_y) * scroll_speed
                    start_x, start_y = x, y


        # Your game logic goes here

        # Clear the screen (fill with background color)
        dimensions['screen'].fill((0, 0, 0))

        # Draw the map
        game_map.draw(dimensions)
        warrior_1.draw(dimensions)
        warrior_2.draw(dimensions)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
