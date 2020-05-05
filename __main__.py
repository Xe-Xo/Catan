import pygame
from game import GAME_GLOBALS, Game



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

    game = Game()

    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update game logic
        game.run_logic()

        # Render current frame
        game.display_frame(screen)

        #Pause for the next frame
        clock.tick(60)

    #close window and exit
    pygame.quit()

if __name__ == "__main__":
    main()