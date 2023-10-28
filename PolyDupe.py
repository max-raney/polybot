# Polytopia
import numpy as np
import pygame

TILE_EMPTY = 'empty'
TILE_GRASS = 'grass'
TILE_WATER = 'water'

class Map:
    def __init__(self, size):
        # Initialize the map as a 2D array of tile types
        self.map = np.empty((size, size), dtype=str)
        self.size = size

        for x in range(size):
            for y in range(size):
                # Initialize each tile as empty
                self.map[x][y] = TILE_EMPTY

    def draw(self, screen, tile_image, screen_width, screen_height):
        # Define the size of each tile (image size)
        tile_height = screen_height / self.size * 1.25
        tile_width = screen_height / self.size * 1.25

        for x in range(len(self.map) -1, -1, -1):
            for y in range(len(self.map[x])):
                # Calculate the position of the tile on the screen
                # Adjust the x and y coordinates based on the map's shape
                tile_x = ((x + y) / 2) * 0.95 * tile_width
                tile_y = ((y - x) / 2) * tile_height * 0.6 + screen_height / 2

                # Get the type of the current tile
                tile_type = self.map[x][y]

                # Scale down the tile image
                scaled_tile = pygame.transform.scale(tile_image, (tile_height, tile_height))

                # Draw the scaled tile image at the calculated position
                screen.blit(scaled_tile, (tile_x, tile_y))


class Tile():
    def __init__(self, land_type):
        self.land_type = land_type

class City():
    ''

class Troop():
    ''

class Warrior(Troop):
    ''

def main():
    # Initialize Pygame
    pygame.init()

    # Define screen dimensions
    screen_width = 800
    screen_height = 600

    # Create a Pygame window
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set the window title
    pygame.display.set_caption("Fake Poly")

    # Load your custom tile image
    tile_image = pygame.image.load("Art/Grass.webp")

    # Create a map with a size of 10x10 (adjust the size as needed)
    game_map = Map(10)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Your game logic goes here

        # Clear the screen (fill with background color)
        screen.fill((255, 255, 255))

        # Draw the map
        game_map.draw(screen, tile_image, screen_width, screen_height)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
