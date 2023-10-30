# Polytopia
import numpy as np
import pygame

TILE_EMPTY = 'empty'
TILE_GRASS = 'grass'
TILE_WATER = 'water'

class Map:
    def __init__(self, size):
        # Initialize the map as a 2D array of tile types
        self.map = np.empty((size, size), dtype=Tile)
        self.size = size
        self.troop = None

        for x in range(size):
            for y in range(size):
                # Initialize each tile as empty
                self.map[x][y] = TILE_EMPTY

    def draw(self, dimensions):#screen, tile_image, screen_dims, map_coords):

        for x in range(self.size-1, -1, -1):
            for y in range(self.size):
                # Calculate the position of the tile on the screen
                # Adjust the x and y coordinates based on the map's shape
                tile_coords = index_to_pixel(x, y, dimensions)

                # Get the type of the current tile
                tile_type = self.map[x][y]

                # Scale down the tile image
                scaled_tile = pygame.transform.scale(pygame.image.load("Art/Terrain/Tiles/ground_1.png"), dimensions['tile_size'].astype(int))

                # Draw the scaled tile image at the calculated position
                dimensions['screen'].blit(scaled_tile, tile_coords.T[0])

class Tile():
    def __init__(self, land_type):
        self.land_type = land_type

class City():
    ''

class Troop():
    troop_image = 'Art/Units/Imperius/Default/Imperius_Default_Scout.png'
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, dimensions):
        coords = index_to_pixel(self.x, self.y, dimensions)

class Warrior(Troop):
    attack = 2
    defense = 2
    movement = 1
    range = 1
    
    def __init__(self, x, y):
        self.health = 10
        super(x, y)

def tile_size(tile_image):
    return np.array([tile_image.get_width(), tile_image.get_height()]) // 10

def index_to_pixel(x, y, dimensions):
    A = np.array([[0.4975, 0.4975],[-0.31, 0.31]])
    coordinate = np.array([[x], [y]])
    offset_v = np.array([[dimensions['camera_offset'][0]], [dimensions['camera_offset'][1] + dimensions['screen_dims'][1]/2]])
    resize_matrix = np.diag(dimensions['tile_size'])

    return np.floor(resize_matrix @ (A @ coordinate) + offset_v).astype(int)

def main():
    # Initialize Pygame
    pygame.init()

    dimensions = {
        'screen_dims': [1600, 900],
        'tile_size': tile_size(pygame.image.load("Art/Terrain/Tiles/ground_1.png")),
        'camera_offset': [0, 0]
    }

    # Define screen dimensions
    screen_width = 1600
    screen_height = 900

    # Create a Pygame window
    dimensions['screen'] = pygame.display.set_mode((screen_width, screen_height))

    # Set the window title
    pygame.display.set_caption("Fake Poly")

    # Load your custom tile image
    tile_image = pygame.image.load("Art/Terrain/Tiles/ground_1.png")

    # Create a map with a size of 10x10 (adjust the size as needed)
    game_map = Map(10)

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
                    dimensions['camera_offset'][0] += (y - start_y) * scroll_speed
                    start_x, start_y = x, y


        # Your game logic goes here

        # Clear the screen (fill with background color)
        dimensions['screen'].fill((0, 0, 0))

        # Draw the map
        game_map.draw(dimensions)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
