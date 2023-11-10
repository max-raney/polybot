# Polytopia
import numpy as np
import pygame
from PolyEntities import Map, Warrior
from PolyDraw import Drawer



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

    # Create a Drawer instance
    drawer = Drawer(dimensions)

    # Create a map with a size of 10x10 (adjust the size as needed)
    game_map = Map(20, drawer)

    # Initialize two warriors
    warrior_1 = Warrior(0, 0, drawer)
    warrior_2 = Warrior(4, 5, drawer)

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
            
        # Clear the screen (fill with background color)
        dimensions['screen'].fill((0, 0, 0))

        # Draw the map
        game_map.draw()
        warrior_1.draw()
        warrior_2.draw()

        # Update the display
        drawer.draw_frame()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
