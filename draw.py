import pygame, sys
from pygame.locals import *
import math

from Grid import *

WHITE = (255,255,255)
LIGHT_GRAY = (200,200,200)
GRAY = (150,150,150)
DARK_GRAY = (100,100,100)
BLACK = (50,50,50)
RED = (230,30,30)
BLUE = (30,30,230)
GREEN = (30,230,30)
DARK_GREEN = (0,160,0)

pygame.init()
window = pygame.display.set_mode((1280,800))
window.fill(WHITE)

#D = 48*3+10

grid_size = 255
number_of_hexes_y = grid_size*2+1
D = min(1280/3*2,800)/number_of_hexes_y

gap = 0
#gap = D/3
alpha = D/4
g_alpha = (D-gap)/4
beta = math.sqrt(3) * alpha
g_beta = math.sqrt(3) * g_alpha

points = [(0,0,1),(0,-1,0),(1,0,0),(0,0,-1),(0,1,0),(-1,0,0)]

p1 = (0,-2*g_alpha) #+z
p2 = (g_beta,-g_alpha) #-y
p3 = (g_beta,g_alpha) #+x
p4 = (0,2*g_alpha) #-z
p5 = (-g_beta,g_alpha) #+y
p6 = (-g_beta,-g_alpha) #-x

center_xy = (640,400)


def coord_to_color(grid_size,coords):
    jump = 255/(grid_size+1)/2
    middle_R,middle_G,middle_B = tuple([int(255/2)]*3)
    x,y,z = coords.tuple()
    R,G,B = int(middle_R + jump*x), int(middle_G + jump*y), int(middle_B + jump*z)
    return R,G,B

def text_to_screen(screen,text,xy_tuple,size=16,color = BLACK, font_type = None):
    try:

        text = str(text)
        font = pygame.font.Font(font_type,size)
        text = font.render(text,True,color)
        x_offset = -text.get_rect().width / 2
        y_offset = -text.get_rect().height / 2
        x, y = xy_tuple
        xy_tuple = x + x_offset, y + y_offset
        screen.blit(text,xy_tuple)

    except Exception as e:
        print('Font Error')
        raise e

def coord_to_point(center_xy,x,y,z,gap=True):

    #starting center point generally the xy of 0,0,0 hexagon
    #however this changes if finding the points of a hexagon not in the center
    #returns a tuple (x,y)
    #gap (optional): renders points at approx 2/3rds back from usual render points. Useful for seeing gaps between hexes.

    if gap == True:
        pixel_x = (g_beta * x) + (-g_beta * y) + 0 * z
        pixel_y = (g_alpha * x) + (g_alpha * y) + (-2 * g_alpha * z)
    else:
        pixel_x = (beta * x) + (-beta * y) + 0 * z
        pixel_y = (alpha * x) + (alpha * y) + (-2 * alpha * z)
    return (int(pixel_x + center_xy[0]),int(pixel_y + center_xy[1]))

def hex_corners(center_xy,x,y,z):

    #finds the corner x,y points given the hex coordinates.
    #Calculates the center location of the hex then calculates the points surrounding it.

    start_center = center_xy
    hex_center = coord_to_point(start_center,x,y,z,False)
    corner_points = []
    for point_xyz in points:
        px,py,pz = point_xyz
        corner_points.append(coord_to_point(hex_center,px,py,pz))
    return corner_points
    


g = Grid(grid_size)

#draw Grid

for hex in g.hexes.values():
    hx, hy, hz = hex.coords.tuple()

    pygame.draw.polygon(window, coord_to_color(grid_size,hex.coords), hex_corners(center_xy,hx,hy,hz))
    #pygame.draw.polygon(window, GRAY, hex_corners(center_xy,hx,hy,hz))
    #text_to_screen(window,hex.coords.tuple(),coord_to_point(center_xy,hx,hy,hz,gap=False),color=RED)

for corner in g.corners.values():
    cx,cy,cz = corner.coords.tuple()
    if corner.sign == -1:
        
        #pygame.draw.circle(window, coord_to_color(grid_size,corner.coords), coord_to_point(center_xy,cx,cy,cz,gap=False),int(alpha/4))
        pass
        
        
        #pygame.draw.circle(window, LIGHT_GRAY, coord_to_point(center_xy,cx,cy,cz,gap=False),int(alpha/4))
        #text_to_screen(window,corner.coords.tuple(),coord_to_point(center_xy,cx,cy,cz,gap=False),color=BLUE)
    else:
        #pygame.draw.circle(window, coord_to_color(grid_size,corner.coords), coord_to_point(center_xy,cx,cy,cz,gap=False),int(alpha/4))
        pass
        #pygame.draw.circle(window, LIGHT_GRAY, coord_to_point(center_xy,cx,cy,cz,gap=False),int(alpha/4))
        #text_to_screen(window,corner.coords.tuple(),coord_to_point(center_xy,cx,cy,cz,gap=False),color=BLUE)

for road in g.roads.values():
    pcx, pcy, pcz = road.pos_coords.tuple()
    ncx, ncy, ncz = road.neg_coords.tuple()
    pos_point_x, pos_point_y = coord_to_point(center_xy,pcx,pcy,pcz,gap=False)
    neg_point_x, neg_point_y = coord_to_point(center_xy,ncx,ncy,ncz,gap=False)

    mid_point_x, mid_point_y = (pos_point_x + neg_point_x)/2 , (pos_point_y + neg_point_y)/2

    pos_point = pos_point_x, pos_point_y
    neg_point = neg_point_x, neg_point_y
    mid_point = mid_point_x, mid_point_y

    #pygame.draw.line(window,LIGHT_GRAY,pos_point,neg_point,3)

    #text_to_screen(window,road.coords_tuple(),mid_point,color=GREEN)


#draw text

for hex in g.hexes.values():
    hx, hy, hz = hex.coords.tuple()
    #text_to_screen(window,hex.coords.tuple(),coord_to_point(center_xy,hx,hy,hz,gap=False),color=WHITE)

for corner in g.corners.values():
    cx,cy,cz = corner.coords.tuple()
    if corner.sign == -1:
        pass
        #text_to_screen(window,corner.coords.tuple(),coord_to_point(center_xy,cx,cy,cz,gap=False),color=BLUE)
    else:
        pass
        #text_to_screen(window,corner.coords.tuple(),coord_to_point(center_xy,cx,cy,cz,gap=False),color=DARK_GREEN)

for road in g.roads.values():
    pcx, pcy, pcz = road.pos_coords.tuple()
    ncx, ncy, ncz = road.neg_coords.tuple()
    pos_point_x, pos_point_y = coord_to_point(center_xy,pcx,pcy,pcz,gap=False)
    neg_point_x, neg_point_y = coord_to_point(center_xy,ncx,ncy,ncz,gap=False)

    mid_point_x, mid_point_y = (pos_point_x + neg_point_x)/2 , (pos_point_y + neg_point_y)/2

    pos_point = pos_point_x, pos_point_y
    neg_point = neg_point_x, neg_point_y
    mid_point = mid_point_x, mid_point_y

    #text_to_screen(window,road.weird_tuple(),mid_point,color=RED,size=12)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        pygame.display.update()
    
