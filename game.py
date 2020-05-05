
import pygame
import random
import math
from grid import *
from players import *

## TO DO -- BETTER WAY TO TREAT GLOBALS THAT CAN BE ACCESSED BY MAIN AND GAME
class GAME_GLOBALS():
    WHITE = (255,255,255)
    LIGHT_GRAY = (200,200,200)
    GRAY = (150,150,150)
    DARK_GRAY = (100,100,100)
    BLACK = (50,50,50)
    RED = (230,30,30)
    BLUE = (30,30,230)
    GREEN = (30,230,30)
    DARK_GREEN = (0,160,0)
    KHAKI = (240,230,140)
    OLIVE = (128,128,0)
    MOCCASIN = (255,228,181)
    LIGHT_YELLOW = (255,255,224)

    POS_X = (1,0,0)
    NEG_X = (-1,0,0)
    POS_Y = (0,1,0)
    NEG_Y = (0,-1,0)
    POS_Z = (0,0,1)
    NEG_Z = (0,0,-1)

    RESOURCE_TO_COLOR = [DARK_GREEN,RED,DARK_GRAY,KHAKI,LIGHT_GRAY,OLIVE]

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    SCREEN_CENTER = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

    GRID_SIZE = 2

    NUMBER_HEXES_WIDTH = GRID_SIZE*2+1

    HEX_DIAMETER = min(SCREEN_WIDTH/3*2,SCREEN_HEIGHT)/NUMBER_HEXES_WIDTH
    HEX_GAP = HEX_DIAMETER/3
    ALPHA = HEX_DIAMETER/4
    BETA = math.sqrt(3) * ALPHA
    G_ALPHA = (HEX_DIAMETER-HEX_GAP)/4
    G_BETA = math.sqrt(3) * G_ALPHA

    ROLL_RANK =   {
                        2:1,
                        3:2,
                        4:3,
                        5:4,
                        6:5,
                        7:0,
                        8:5,
                        9:4,
                        10:3,
                        11:2,
                        12:1
                        }

class Scene():

    """This class represents an instance of the gamestate"""
    """subclass to be used for State Machine between Main Menu, Game and GameOver screens"""

    def __init__(self):
        pass

    def move_state(self, state_index):
        if state_index == 0 and type(self) != MainMenu:
            return MainMenu()
        elif state_index == 1 and type(self) != Game:
            return Game()
        else:
            return self

    def process_events(self):
        """Process all the events. Return a True if we need to close the window"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, self
        return False, self

    def run_logic(self):
        pass

    def display_frame(self,screen):
        pygame.display.update()

    def text_to_screen(self,screen,text,xy_tuple,size=16,color = GAME_GLOBALS.BLACK, font_type = None,offset=(0,0),background_color=None):
        try:
            text = str(text)
            font = pygame.font.Font(font_type,size)
            text = font.render(text,True,color)
            x_offset, y_offset = offset
            x_offset -= text.get_rect().width / 2
            y_offset -= text.get_rect().height / 2 
            x, y = xy_tuple
            x,y = x + x_offset, y + y_offset
            if background_color is not None and type(background_color) is tuple:
                background_color = self.fix_color(background_color)
                pygame.draw.rect(screen,background_color,(x,y,text.get_rect().width, text.get_rect().height))
            screen.blit(text,(x,y))
            return x,y,text.get_rect().width, text.get_rect().height

        except Exception as e:
            print('Font Error')
            raise e

    def coord_to_point(self,center_xy,x,y,z,gap=True):
        #starting center point generally the xy of 0,0,0 hexagon
        #however this changes if finding the points of a hexagon not in the center
        #returns a tuple (x,y)
        #gap (optional): renders points at approx 2/3rds back from usual render points. Useful for seeing gaps between hexes.

        if gap == True:
            pixel_x = (GAME_GLOBALS.G_BETA * x) + (-GAME_GLOBALS.G_BETA * y) + 0 * z
            pixel_y = (GAME_GLOBALS.G_ALPHA * x) + (GAME_GLOBALS.G_ALPHA * y) + (-2 * GAME_GLOBALS.G_ALPHA * z)
        else:
            pixel_x = (GAME_GLOBALS.BETA * x) + (-GAME_GLOBALS.BETA * y) + 0 * z
            pixel_y = (GAME_GLOBALS.ALPHA * x) + (GAME_GLOBALS.ALPHA * y) + (-2 * GAME_GLOBALS.ALPHA * z)
        return (int(pixel_x + center_xy[0]),int(pixel_y + center_xy[1]))

    def hex_corners(self,center_xy,x,y,z,gap=True):

        #finds the corner x,y points given the hex coordinates.
        #Calculates the center location of the hex then calculates the points surrounding it.

        #AXIS movement heading clockwise starting at north
        points = [(0,0,1),(0,-1,0),(1,0,0),(0,0,-1),(0,1,0),(-1,0,0)]

        start_center = center_xy
        hex_center = self.coord_to_point(start_center,x,y,z,gap=False)
        corner_points = []
        for point_xyz in points:
            px,py,pz = point_xyz
            corner_points.append(self.coord_to_point(hex_center,px,py,pz,gap=gap))
        return corner_points

    def fix_color(self,color_tuple):
        new_color_list = []
        for color_int in color_tuple:
            if color_int > 255:
                new_color = 255
            elif color_int < 0:
                new_color = 0
            else:
                new_color = int(color_int)
            new_color_list.append(new_color)
        return tuple(new_color_list)

class Game(Scene):

    """This class represents an instance of the game""" 

    def __init__(self):
        super().__init__()
        """Constructor. create all our attributes and initialise the game"""
        self.game_over = False

        """Create the grid"""
        self.grid = Grid(GAME_GLOBALS.GRID_SIZE)

        """Setup grid numbers and resources"""
        self.setup_grid_numbers() #Randomly apply numbers to the board
        self.setup_grid_resources() #Randomly apply resources to the board
        self.setup_corner_ranks() #Calculate the strength of each corner

        """Setup players"""
        self.setup_players()


    def setup_players(self):
        """Setup players"""
        for playerindex in range(0,4):
            self.players.append(Human(playerindex))

        self.game_state_queue =    [
                                    (0,"place_settlement"),(0,"place_road"),
                                    (1,"place_settlement"),(1,"place_road"),
                                    (2,"place_settlement"),(2,"place_road"),
                                    (3,"place_settlement"),(3,"place_road"),
                                    (3,"place_settlement"),(3,"place_road"),
                                    (2,"place_settlement"),(2,"place_road"),
                                    (1,"place_settlement"),(1,"place_road"),
                                    (0,"place_settlement"),(0,"place_road"),
                                    ]

        self.turn, self.current_game_state = self.game_state_queue.pop(0)


    def process_events(self):
        """Process all the events. Return a True if we need to return to the Main Menu"""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, self
        return self.game_over, self

    def run_logic(self):
        pass

    def display_frame(self,screen):
        if self.current_game_state == "place_settlement":
            self.display_place_settlement(screen,self.turn)
        elif self.current_game_state == "place_road":
            self.display_place_road(self,self.turn)

        pygame.display.update()


    """Display Methods"""
    def display_place_settlement(self,screen,playerindex):
        self.draw_background(screen)
        self.draw_hexes(screen)
        #self.draw_settlements(screen)
        #self.draw_roads(screen)
        #self.draw_allowed_settlements(screen,playerindex)

    def display_place_road(self,screen,playerindex):
        self.draw_background(screen)
        self.draw_hexes(screen)
        #self.draw_settlements(screen)
        #self.draw_roads(screen)
        #self.draw_allowed_roads(screen,playerindex)

    """Player Methods"""
    def next_player_index(self,current_player_index):
        next_player_index = current_player_index + 1
        if next_player_index >= 4:
            return 0
        else:
            next_player_index

    def next_player(self,player):
        return self.players[self.next_player_index(player.playerindex)]

    """Setup Grid Methods"""

    def setup_grid_numbers(self):

        """Load self.grid_numbers and self.number_to_hex with the values"""

        self.grid_numbers = {}
        self.number_to_hex = {}
        possible_numbers = [2,3,3,4,4,5,5,6,6,7,8,8,9,9,10,10,11,11,12]
        for num in possible_numbers:
            self.number_to_hex[num] = []
        
        random.shuffle(possible_numbers)
        
        for hex in self.grid.hexes.values():
            number_picked = possible_numbers.pop(0)
            self.number_to_hex[number_picked].append(hex)
            self.grid_numbers[hex.coords.tuple()] = number_picked
        print("Grid Numbers applied!")
    
    def setup_grid_resources(self):

        """Load self.grid_resources with values"""

        resource_index = [0,1,2,3,4]
        random.shuffle(resource_index)
        resources = [resource_index.pop(0)] * 4
        resources += [resource_index.pop(0)] * 4
        resources += [resource_index.pop(0)] * 4
        resources += [resource_index.pop(0)] * 3
        resources += [resource_index.pop(0)] * 3
        random.shuffle(resources)
        self.grid_resources = {}
        for hex_tuple in self.grid.hexes.keys():
            if self.grid_numbers[hex_tuple] != 7:
                try:
                    self.grid_resources[hex_tuple] = resources.pop(0)
                except IndexError as e:
                    print(e)
            else:
                self.grid_resources[hex_tuple] = 5

        print("Grid Resources applied!")

    def calculate_resource_scarcity(self):
        resource_scarcity = []
        for resource_index in [0,1,2,3,4]:
            totalpoints = 0
            for hex_tuple in self.grid_resources.keys():
                if self.grid_resources[hex_tuple] == resource_index:
                    totalpoints += GAME_GLOBALS.ROLL_RANK[self.grid_numbers[hex_tuple]]
            resource_scarcity_points = totalpoints/58*5
            resource_scarcity.append(resource_scarcity_points)
        return resource_scarcity

    def setup_corner_ranks(self):

        self.corner_ranks = {}

        for corner in self.grid.corners.values():
            rank_value = 0
            for hex_coords in corner.connected_hexes_coords():
                try:
                    resource_index = self.grid_resources[hex_coords.tuple()]
                    try:
                        resource_scarcity = self.calculate_resouce_scarcity()[resource_index]
                    except:
                        resource_scarcity = 1
                    roll_rank_of_hex = GAME_GLOBALS.ROLL_RANK[self.grid_numbers[hex_coords.tuple()]]
                    rank_value += roll_rank_of_hex/resource_scarcity
                except KeyError as e:
                    rank_value += 0
                
            self.corner_ranks[corner.coords.tuple()] = int(rank_value)

    """Render Methods"""

    def draw_background(self,screen):
        screen.fill(GAME_GLOBALS.BLUE)

    def draw_hexes(self,screen):
        for hex in self.grid.hexes.values():
            hx, hy, hz = hex.coords.tuple()
            resource_color = GAME_GLOBALS.RESOURCE_TO_COLOR[self.grid_resources[hex.coords.tuple()]]
            pygame.draw.polygon(screen,GAME_GLOBALS.LIGHT_YELLOW, self.hex_corners(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz,gap=False))
            pygame.draw.polygon(screen,resource_color, self.hex_corners(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz))

            number = self.grid_numbers[hex.coords.tuple()]
            self.text_to_screen(screen,number,self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz,gap=False),size=20)

    def draw_hexes_scarcity(self,screen):
        for hex in self.grid.hexes.values():
            hx, hy, hz = hex.coords.tuple()
            resource_index = self.grid_resources[hx,hy,hz]
            try:
                resource_scarcity = self.calculate_resouce_scarcity()[resource_index]
            except:
                resource_scarcity = 1
            roll_rank_of_hex = GAME_GLOBALS.ROLL_RANK[self.grid_numbers[(hx,hy,hz)]]
            number = round(roll_rank_of_hex/resource_scarcity,2)
            string = "".join(int(number) * ['*'])
            self.text_to_screen(screen,string,self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz,gap=False),size=20,offset=(0,10))

    def draw_corners(self,screen):
        pass


    def draw_corners_ranks(self,screen):
        for corner in self.grid.corners.values():
            cx,cy,cz = corner.coords.tuple()
            color = self.fix_color((int(255/14*(self.corner_ranks[corner.coords.tuple()]-1)),150,150))
            
            try:
                pygame.draw.circle(screen, color, self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER, cx, cy, cz, gap=False),int(GAME_GLOBALS.ALPHA/4))
            except:
                print(color)
            self.text_to_screen(screen,self.corner_ranks[corner.coords.tuple()],self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,cx,cy,cz,gap=False),size=16)

class MainMenu(Scene):

    def __init__(self):
        super().__init__()
        self.buttons = {}
        self.grid = Grid(2)
        self.setup_background()

    def process_events(self):
        """Process all the events. Return a True if we need to close the window, return GameState should be using after events."""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, self
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_coords in self.buttons.keys():
                    x,y,w,h = button_coords
                    if self.button_check(pygame.mouse.get_pos(),x,y,w,h):
                        print(pygame.mouse.get_pos(),self.buttons.keys())
                        for function in self.buttons[button_coords]:
                            if function == "game_start":
                                return False, self.move_state(1)
                            elif function == "game_quit":
                                return True, self
        return False, self


    def run_logic(self):
        
        x, y = self.background_center

        self.background_center = x + self.move, y + self.move
        if self.background_center[0] > GAME_GLOBALS.SCREEN_WIDTH or self.background_center[0] < 0 or self.background_center[1] > GAME_GLOBALS.SCREEN_HEIGHT or self.background_center[1] < 0:
            self.move = self.move * -1


    def display_frame(self,screen):
        self.draw_background(screen)
        self.draw_menu_background(screen)
        self.draw_title(screen)
        self.draw_start_button(screen)
        pygame.display.update()    

    def setup_background(self):
        #creating the background grid
        self.background_center = (0,0)
        self.hex_colors = {}
        self.move = 1
        for hex in self.grid.hexes.values():
            self.hex_colors[hex.coords.tuple()] = random.choice(GAME_GLOBALS.RESOURCE_TO_COLOR)


    def draw_background(self,screen):
        screen.fill(GAME_GLOBALS.BLUE)

        for hex in self.grid.hexes.values():
            hx, hy, hz = hex.coords.tuple()
            resource_color = self.hex_colors[hx,hy,hz] 
            pygame.draw.polygon(screen,GAME_GLOBALS.LIGHT_YELLOW, self.hex_corners(self.background_center,hx,hy,hz,gap=False))
            pygame.draw.polygon(screen,resource_color, self.hex_corners(self.background_center,hx,hy,hz))

    def draw_title(self,screen):
        self.text_to_screen(screen,"Settlers of Catan", (GAME_GLOBALS.SCREEN_CENTER[0], 60), size=100, color=GAME_GLOBALS.GREEN)

    def draw_menu_background(self,screen):

        w, h = GAME_GLOBALS.SCREEN_WIDTH/3 , GAME_GLOBALS.SCREEN_HEIGHT/3
        x, y = GAME_GLOBALS.SCREEN_CENTER
        x = x - w/2
        y = y - h/2

        pygame.draw.rect(screen,GAME_GLOBALS.BLACK,(x,y,w,h))


    def draw_start_button(self,screen):
        center_x, center_y = GAME_GLOBALS.SCREEN_CENTER
        button_posx, button_posy = center_x, center_y - GAME_GLOBALS.SCREEN_HEIGHT/4
        self.make_button(screen,GAME_GLOBALS.BLACK,GAME_GLOBALS.WHITE,button_posx,button_posy,"START",["game_start"])

    def draw_quit_button(self,screen):
        center_x, center_y = GAME_GLOBALS.SCREEN_CENTER
        button_posx, button_posy = center_x, center_y - GAME_GLOBALS.SCREEN_HEIGHT/4
        self.make_button(screen,GAME_GLOBALS.BLACK,GAME_GLOBALS.WHITE,button_posx,button_posy,"QUIT",["game_quit"])

    def make_button(self,screen,color,text_color,x,y,text,functionalitylist):
        x,y,w,h = self.text_to_screen(screen,text,(x,y),size=32,color=text_color,background_color=color)
        self.buttons[x,y,w,h] = functionalitylist

    def button_check(self,mouse_pos,x,y,w,h):
        #mouse pos from event.pos
        #x,y where you render the button
        #x1,y1 is the width/height
        #returns true if button is clicked
        mouse_x, mouse_y = mouse_pos
        return mouse_x >= x and mouse_x < x + w and mouse_y >= y and mouse_y < y + h

