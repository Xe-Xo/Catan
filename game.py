
import pygame
import random
import math

from grid import *

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

class Game():

    """This class represents an instance of the game""" 

    def __init__(self):
        """Constructor. create all our attributes and initialise the game"""
        self.game_over = False

        """Create the grid"""
        self.grid = Grid(GAME_GLOBALS.GRID_SIZE)

        """Setup grid numbers and resources"""
        self.setup_grid_numbers() #Randomly apply numbers to the board
        self.setup_grid_resources() #Randomly apply resources to the board
        self.setup_corner_ranks() #Calculate the strength of each corner
        self.calculate_resource_scarcity()

        """Setup players"""

    def process_events(self):
        """Process all the events. Return a True if we need to close the window"""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            return self.game_over

    def run_logic(self):
        pass

    def display_frame(self,screen):
        self.draw_background(screen)
        self.draw_hexes(screen)
        self.draw_hexes_scarcity(screen)
        self.draw_corners(screen)

        pygame.display.update()


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
        for corner in self.grid.corners.values():
            cx,cy,cz = corner.coords.tuple()
            color = self.fix_color((int(255/14*(self.corner_ranks[corner.coords.tuple()]-1)),150,150))
            
            try:
                pygame.draw.circle(screen, color, self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER, cx, cy, cz, gap=False),int(GAME_GLOBALS.ALPHA/4))
            except:
                print(color)
            self.text_to_screen(screen,self.corner_ranks[corner.coords.tuple()],self.coord_to_point(GAME_GLOBALS.SCREEN_CENTER,cx,cy,cz,gap=False),size=16)

    def text_to_screen(self,screen,text,xy_tuple,size=16,color = GAME_GLOBALS.BLACK, font_type = None,offset=(0,0)):
        try:
            text = str(text)
            font = pygame.font.Font(font_type,size)
            text = font.render(text,True,color)
            x_offset, y_offset = offset
            x_offset -= text.get_rect().width / 2
            y_offset -= text.get_rect().height / 2 
            x, y = xy_tuple
            xy_tuple = x + x_offset, y + y_offset
            screen.blit(text,xy_tuple)

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













    #
    #resources_possible = [4,4,3,3]

    #resource_strings = {
    #                    "WOOD": (1,0,0,0,0),
    #                    "BRICK":(0,1,0,0,0),
    #                    "ORE":  (0,0,1,0,0),
    #                    "WHEAT":(0,0,0,1,0),
    #                    "SHEEP":(0,0,0,0,1)
    #                    }

    #build = {
    #        "Road":(1,1,0,0,0),
    #        "Settlement":(1,1,0,1,1),
    #        "City":(0,0,3,2,0),
    #        "Development":(0,0,1,1,1)
    #        }

