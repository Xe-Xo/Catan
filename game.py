
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

    #RGB codes sourced from https://www.pinterest.com.au/pin/238339005262876109/

    BEAUTIFUL_BLUE = (0,104,132)
    BEAUTIFUL_AQUA = (0,144,158)
    BEAUTIFUL_LIGHT_BLUE = (137,219,236)
    BEAUTIFUL_RED = (237,0,38)
    BEAUTIFUL_ORANGE = (250, 157, 0)
    BEAUTIFUL_SAND = (255,208,141)
    BEAUTIFUL_ROSE = (176,0,81)
    BEAUTIFUL_PEACH = (246,131,112)
    BEAUTIFUL_PINK = (254,171,185)
    BEAUTIFUL_PURPLE = (110,0,108)
    BEAUTIFUL_LIGHT_PURPLE = (145,39,143)
    BEAUTIFUL_GREEN = (149,212,122)
    BEAUTIFUL_YELLOW = (254,226,62)

    PLAYER_COLORS = [BEAUTIFUL_BLUE,BEAUTIFUL_GREEN,BEAUTIFUL_RED,BEAUTIFUL_YELLOW]

    ORE_COLOR = (145,134,126)
    WHEAT_COLOR = (201,194,127)
    SHEEP_COLOR = (178,200,145)
    BRICK_COLOR = (228,153,105)
    WOOD_COLOR = (116,161,142)
    ROBBER_COLOR = (185,156,107)

    POS_X = (1,0,0)
    NEG_X = (-1,0,0)
    POS_Y = (0,1,0)
    NEG_Y = (0,-1,0)
    POS_Z = (0,0,1)
    NEG_Z = (0,0,-1)

    RESOURCE_TO_COLOR = [WOOD_COLOR,BRICK_COLOR,ORE_COLOR,WHEAT_COLOR,SHEEP_COLOR,ROBBER_COLOR]

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    SCREEN_CENTER = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

    GRID_SIZE = 2

    NUMBER_HEXES_WIDTH = GRID_SIZE*2+1

    HEX_DIAMETER = min(SCREEN_WIDTH/3*2,SCREEN_HEIGHT)/NUMBER_HEXES_WIDTH
    HEX_GAP = HEX_DIAMETER/4
    G_HEX_DIAMETER = HEX_DIAMETER - HEX_GAP
    ALPHA = HEX_DIAMETER/4
    BETA = math.sqrt(3) * ALPHA
    G_ALPHA = (G_HEX_DIAMETER)/4
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

    def point_to_grid_coord(self,center_xy,xy_point,set_sign=None):

        mouse_x, mouse_y = xy_point #Location of mouse in window
        center_x, center_y = center_xy #Location of the centerpoint of the grid
        pixel_x, pixel_y = mouse_x-center_x,mouse_y-center_y #x,y to be turned into grid coords
        
        #coord to point uses matrix multiplication for calculation of x,y
        #after rearranging formula into a square matrix (subsistute x = 0 - y - z) we can calculate the inverse matrix that can be multiplied by pixel_x, pixel_y
        #see https://www.wolframalpha.com/input/?i=24*%7B%7B-sqrt%283%29%2C1%7D%2C%7B0%2C2%7D%7D*%7Bx%2Cy%7D+
        #See Readme notes for detailed breakdown
        
        hex_y = -2*pixel_x/(math.sqrt(3)*GAME_GLOBALS.HEX_DIAMETER) + (2*pixel_y)/(3*GAME_GLOBALS.HEX_DIAMETER)
        hex_z = 0*pixel_x + -4*pixel_y/(3*GAME_GLOBALS.HEX_DIAMETER)
        hex_x = 0 - hex_y - hex_z
        return Coords(hex_x,hex_y,hex_z).round(set_total=set_sign) 

    def point_to_corner_coord(self,center_xy,xy_point):

        pointx, pointy = xy_point
        nx, ny, nz = self.point_to_grid_coord(center_xy,xy_point,set_sign=-1).tuple()
        px, py, pz = self.point_to_grid_coord(center_xy,xy_point,set_sign=1).tuple()
        negposx, negposy = self.coord_to_point(center_xy,nx,ny,nz,gap=False)
        posposx, posposy = self.coord_to_point(center_xy,px,py,pz,gap=False)

        negdistance = math.pow(pointx - negposx,2) + math.pow(pointy - negposy,2) 
        posdisance = math.pow(pointx - posposx,2) + math.pow(pointy - posposy,2)

        if negdistance < posdisance:
            return self.point_to_grid_coord(center_xy,xy_point,set_sign=-1)
        else:
            return self.point_to_grid_coord(center_xy,xy_point,set_sign=1)

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

        self.debug = False
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
        self.setup_settlements()
        self.setup_ports()
        self.setup_roads()

    def process_events(self):
        """Process all the events. Return a True if we need to close the Window"""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, self
            elif self.current_game_state == "place_settlement":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    coord_pointing = self.point_to_corner_coord(GAME_GLOBALS.SCREEN_CENTER,pygame.mouse.get_pos()).round()
                    print(coord_pointing,self.valid_settlement(self.turn,coord_pointing))
                    if self.valid_settlement(self.turn,coord_pointing):
                        self.place_settlement(self.turn,coord_pointing)
                        self.next_game_state()
                        return False,self
            elif self.current_game_state == "place_road":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    coord_pointing_neg = self.point_to_grid_coord(GAME_GLOBALS.SCREEN_CENTER,pygame.mouse.get_pos(),set_sign=-1)
                    coord_pointing_pos = self.point_to_grid_coord(GAME_GLOBALS.SCREEN_CENTER,pygame.mouse.get_pos(),set_sign=1)
                    road_pos = (coord_pointing_neg.x, coord_pointing_neg.y, coord_pointing_pos.x, coord_pointing_pos.y)
                    if self.valid_road(self.turn,road_pos):
                        self.place_road(self.turn, road_pos)
                        self.next_game_state()
                        return False,self
        return self.game_over, self

    def run_logic(self):

        #temporary skip logic
        if self.current_game_state == "place_road":
            self.next_game_state()

    def display_frame(self,screen):
        if self.debug == True:
            self.display_debug(screen)
        elif self.current_game_state == "place_settlement":
            self.display_place_settlement(screen,self.turn)
        elif self.current_game_state == "place_road":
            self.display_place_road(screen,self.turn)
        elif self.current_game_state == "player_turn":
            self.display_player_turn(screen,self.turn)
        pygame.display.update()


    """Display Methods"""

    def display_debug(self,screen):
        pass

    def display_place_settlement(self,screen,playerindex):
        self.draw_background(screen)
        self.draw_hexes(screen)
        self.draw_hexes_scarcity(screen)
        self.draw_game_state(screen)
        self.draw_roads(screen)
        self.draw_valid_settlements(screen,playerindex)
        self.draw_corners_ranks(screen)
        self.draw_settlements(screen)

    def display_place_road(self,screen,playerindex):
        self.draw_background(screen)
        self.draw_hexes(screen)
        self.draw_hexes_scarcity(screen)
        self.draw_game_state(screen)
        self.draw_settlements(screen)
        self.draw_roads(screen)
        self.draw_valid_roads(screen,playerindex)

    def display_player_turn(self,screen,player_index):
        self.draw_background(screen)
        self.draw_hexes(screen)
        self.draw_hexes_scarcity(screen)
        self.draw_game_state(screen)
        self.draw_corners_ranks(screen)
        self.draw_settlements(screen)
        self.draw_roads(screen)

    """Player Methods"""

    def setup_players(self):
        """Setup players"""
        self.players = []
        for playerindex in range(0,4):
            self.players.append(Human(playerindex))

        self.game_state_queue =    [(0,"place_settlement"),(0,"place_road"),(1,"place_settlement"),(1,"place_road"),
                                    (2,"place_settlement"),(2,"place_road"),(3,"place_settlement"),(3,"place_road"),
                                    (3,"place_settlement"),(3,"place_road"),(2,"place_settlement"),(2,"place_road"),
                                    (1,"place_settlement"),(1,"place_road"),(0,"place_settlement"),(0,"place_road")
                                    ]

        self.next_game_state()

    def next_player_index(self,current_player_index):
        next_player_index = current_player_index + 1
        if next_player_index >= 4:
            return 0
        return next_player_index

    def next_player(self,player):
        return self.players[self.next_player_index(player.playerindex)]

    def place_settlement(self,player_index,coords):
        self.settlements[coords.tuple()] = player_index

    """Game State Methods"""

    def next_game_state(self):
        try:
            self.turn, self.current_game_state = self.game_state_queue.pop(0)
        except:
            self.turn, self.current_game_state = self.next_player_index(self.turn), "player_turn"

    def valid_settlement(self,player_id,coords,limit_by_road=False):

        #TO DO - this is complicated when it really shouldnt be.
        #clean up this trainwreck

        try:
            corner_selected = self.grid.corners[coords.tuple()]
            for other_corners_coords in corner_selected.connected_corner_coords():
                try:
                    if self.settlements[other_corners_coords.tuple()] != -1: 
                        return False
                except:
                    pass
            if limit_by_road:
                for road_coords in corner_selected.connected_road_coords():
                    if self.roads[road_coords] == player_id:
                        return True
                return False
            else:
                return True

        except KeyError:
            print("KeyError")
            return False

    def valid_road(self,player_id,roadcoords):
        pass

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

        #from 36 rolls with even distribution
        #the probability of each resource being given out

        #resouce scarcity = SUM(Possible ways number can be rolled 

        #eg. 2 can be rolled 1 way and there is one placement on board.
        #    3 can be rolled 2 ways and there is two placements on board.
        # 
        # sum of this (2x1+2x2+3x2+.....) = 58

        resource_scarcity = []
        for resource_index in [0,1,2,3,4]:
            totalpoints = 0
            for hex_tuple in self.grid_resources.keys():
                if self.grid_resources[hex_tuple] == resource_index:
                    totalpoints += GAME_GLOBALS.ROLL_RANK[self.grid_numbers[hex_tuple]]/58
            resource_scarcity.append(totalpoints)
        return resource_scarcity

    def setup_corner_ranks(self):

        #Calculates the strength of a corner given the overall resource scarcity
        #

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

    def setup_settlements(self):
        self.settlements = {}
        for corner_tuple in self.grid.corners.keys():
            self.settlements[corner_tuple] = -1

    def setup_roads(self):
        self.roads = {}
        for road_tuple in self.grid.roads.keys():
            self.roads[road_tuple] = -1

    def setup_ports(self):
        self.ports = {}

        possible_ports = [
                        ((),("sheep",2)),
                        ((),("wood",2)),
                        ((),("brick",2)),
                        ((),("ore",2)),
                        ((),("wheat",2)),
                        ((),("any",3)),
                        ((),("any",3)),
                        ((),("any",3))
                        ]

    """Render Methods"""

    def draw_background(self,screen):
        screen.fill(GAME_GLOBALS.BLUE)

    def draw_hexes(self,screen):
        for hex in self.grid.hexes.values():
            hx, hy, hz = hex.coords.tuple()
            resource_color = GAME_GLOBALS.RESOURCE_TO_COLOR[self.grid_resources[hex.coords.tuple()]]
            pygame.draw.polygon(screen,GAME_GLOBALS.LIGHT_YELLOW, self.hex_corners(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz,gap=False))
            pygame.draw.polygon(screen,GAME_GLOBALS.BLACK, self.hex_corners(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz,gap=False),2)
            pygame.draw.polygon(screen,resource_color, self.hex_corners(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz))


            number = self.grid_numbers[hex.coords.tuple()]
            self.text_to_screen(screen,number,self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz,gap=False),size=20,color=GAME_GLOBALS.WHITE)

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
            self.text_to_screen(screen,string,self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,hx,hy,hz,gap=False),size=20,offset=(0,10),color=GAME_GLOBALS.WHITE)

    def draw_settlements(self,screen):
        for corner in self.grid.corners.values():
            try:
                settlementplayer = self.settlements[corner.coords.tuple()]
                if settlementplayer != -1:
                    pygame.draw.circle(screen, GAME_GLOBALS.PLAYER_COLORS[settlementplayer],self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,corner.coords.x,corner.coords.y,corner.coords.z,gap=False),int(GAME_GLOBALS.ALPHA/4))
            except KeyError as e:
                print(corner.tuple())
    
    def draw_roads(self,screen):
        pass

    def draw_game_state(self,screen):
        self.text_to_screen(screen,self.current_game_state,(100,100),size=32,color=GAME_GLOBALS.RED)
        self.text_to_screen(screen,self.turn,(150,150),size=32,color=GAME_GLOBALS.RED)
    
    def draw_corners_ranks(self,screen):
        for corner in self.grid.corners.values():
            cx,cy,cz = corner.coords.tuple()
            if self.valid_settlement(1,corner.coords):
                color = self.fix_color((int(255/14*(self.corner_ranks[corner.coords.tuple()]-1)),150,150))
            
                try:
                    pygame.draw.circle(screen, color, self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER, cx, cy, cz, gap=False),int(GAME_GLOBALS.ALPHA/4),2)
                except:
                    print(color)
                self.text_to_screen(screen,self.corner_ranks[corner.coords.tuple()],self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,cx,cy,cz,gap=False),size=16)

    def draw_valid_settlements(self,screen,player_index):
        for corner in self.grid.corners.values():
            if self.valid_settlement(player_index,corner.coords,limit_by_road=False):
                pygame.draw.circle(screen, GAME_GLOBALS.LIGHT_GRAY,self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,corner.coords.x,corner.coords.y,corner.coords.z,gap=False),int(GAME_GLOBALS.ALPHA/4))

    def draw_valid_roads(self,screen,player_index):
        pass


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

        