import pygame
from game import *

def main():
    """Main program function. """
    #Initalise Pygame and set up window
    pygame.init()

    screen_size = (GAME_GLOBALS.SCREEN_WIDTH,GAME_GLOBALS.SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Settlers")
    pygame.mouse.set_visible(True)

    #Set up instance of Game class, clock and bool to end.

    done = False
    clock = pygame.time.Clock()

    scene = MainMenu()

    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done, scene = scene.process_events()

        # Update game logic
        scene.run_logic()

        # Render current frame
        scene.display_frame(screen)

        #Pause for the next frame
        clock.tick(60)

    #close window and exit
    pygame.quit()

if __name__ == "__main__":
    main()