
import random

def Convert_list_to_coords(list_converted):
            return Coords(list_converted[0],list_converted[1],list_converted[2])

def Convert_tuple_to_coords(tuple_converted):
    return Convert_list_to_coords(list(tuple_converted))

class Coords():

    AXIS = [0,1,2]


    def from_tuple(coords_tuple):
        x,y,z = coords_tuple
        return Coords(x,y,z)

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.total = x + y + z

        self.coord_x = (self.x,0,0)
        self.coord_y = (0,self.y,0)
        self.coord_z = (0,0,self.z)

        self.abs = abs(x) + abs(y) + abs(z)

    def short(self):
        return (self.x,self.y)

    def __add__(self,other):
        return Coords(self.x+other.x,self.y+other.y,self.z+other.z)

    def __sub__(self,other):
        return Coords(self.x-other.x,self.y-other.y,self.z-other.z)

    def __mul__(self,other):
        if type(other) is int:
            return Coords(self.x*other,self.y*other,self.z*other)
        elif type(other) is Coords:
            return Coords(self.x*other.x,self.y*other.y,self.z*other.z)
        else:
            print("what?")
            return None

    def __rmul__(self,other):
        return __mul__(self,other)

    def tuple(self):
        return self.x,self.y,self.z

    def __hash__(self):
        return (self.x,self.y,self.z)

    def __repr__(self):
        return f"{self.x,self.y,self.z}"

    def multi_exception(self,scalar,index):
        coords = [scalar] * 3
        coords[index] = 0
        return self * Convert_list_to_coords(coords)

    def add_exception(self,scalar,index):
        coords = [scalar] * 3
        coords[index] = 0
        return self + Convert_list_to_coords(coords)

    def round(self,set_total=None):

        #No guarantee that the sum of rounded numbers will equal the same total
        #as the original numbers
        #The component with the largest change will be used to reset the total constraint
        #should only be a problem at pixel perfect selections.
        #
        #set_total used to get closest coord with that total
        #eg. Pos Corners = +1
        #    Neg Corners = -1
        #    Grid Locations = 0
        #    Roads are locations between Pos and Neg Corners so the road selected is the Road between Pos and Neg Corners!

        rx = round(self.x)
        ry = round(self.y)
        rz = round(self.z)

        x_dif = abs(rx - self.x)
        y_dif = abs(ry - self.y)
        z_dif = abs(ry - self.z)

        if x_dif > y_dif and x_dif > z_dif:
            if set_total is None:
                rx = self.total-ry-rz
            else:
                rx = set_total-ry-rz
        elif y_dif > z_dif:
            if set_total is None:
                ry = self.total-rx-rz
            else:
                ry = set_total-rx-rz
        else:
            if set_total is None:
                rz = self.total-rx-ry
            else:
                rz = set_total-rx-ry
        return Coords(rx,ry,rz)



class Corner():

    def __init__(self,grid,coords):
        self.grid = grid
        self.coords = coords
        self.sign = coords.total

    def road_coords(self,dirindex):
        other_corner_coords = self.coords.add_exception(-self.sign,dirindex)
        if self.sign == -1:
            return self.coords.short() + other_corner_coords.short()
        elif self.sign == 1:
            return other_corner_coords.short() + self.coords.short()
        else:
            return None

    def other_corner_coords(self,dirindex):
        return self.coords.add_exception(-self.sign,dirindex)

    def connected_hexes_coords(self):
        connected_hexes_coords = []
        for axis_int in Coords.AXIS:
            coord_list = [0] * 3
            coord_list[axis_int] = -self.sign
            connected_hexes_coords.append(self.coords + Coords.from_tuple(tuple(coord_list)))
        return connected_hexes_coords

class Hex():

    def __init__(self,grid,coords):
        self.grid = grid
        self.coords = coords

    def __repr__(self):
        return f"H{self.coords.tuple()}"

    def corner(self,corn_dir):
        return self.coords + corn_dir

class Road():

    def __init__(self,grid,neg_coords,pos_coords):
        self.grid = grid
        self.neg_coords = neg_coords
        self.pos_coords = pos_coords

    def coords_tuple(self):
        return self.neg_coords.x, self.neg_coords.y, self.pos_coords.x, self.pos_coords.y

    def pos_corner(self):
        return self.grid[self.pos_coords.tuple()]

    def neg_corner(self):
        return self.grid[self.neg_coords.tuple()]

    def weird_tuple(self):
        ncx, ncy, ncz = self.neg_coords.tuple()
        pcx, pcy, pcz = self.pos_coords.tuple()
        if ncx == pcx:
            return pcx*2,pcy,pcz
        elif ncy == pcy:
            return pcx, pcy*2, pcz
        elif ncz == pcz:
            return pcx, pcy, pcz*2

class Direction():

    CORN_NORTH = Coords(0,0,1)
    CORN_SOUTH = Coords(0,0,-1)
    CORN_NORTH_WEST = Coords(-1,0,0)
    CORN_SOUTH_EAST = Coords(1,0,0)
    CORN_NORTH_EAST = Coords(0,-1,0)
    CORN_SOUTH_WEST = Coords(0,1,0)

    GRID_NORTH_EAST = CORN_NORTH + CORN_NORTH_EAST
    GRID_NORTH_WEST = CORN_NORTH + CORN_NORTH_WEST
    GRID_EAST = CORN_NORTH_EAST + CORN_SOUTH_EAST
    GRID_WEST = CORN_NORTH_WEST + CORN_SOUTH_WEST
    GRID_SOUTH_EAST = CORN_SOUTH + CORN_SOUTH_EAST
    GRID_SOUTH_WEST = CORN_SOUTH + CORN_SOUTH_WEST

class Grid():
    
    def __init__(self,size):
        self.n_size = size
        self.hexes = {}
        self.corners = {}
        self.roads = {}
        self.setup_hexes()
        self.setup_corners()
        self.setup_roads()

    def setup_hexes(self):
        
        count = 0

        for x in range(-self.n_size,self.n_size+1):
            for y in range(-self.n_size,self.n_size+1):
                for z in range(-self.n_size,self.n_size+1):
                    total = x + y + z
                    if total != 0:
                        pass
                    else:
                        coord = Coords(x,y,z)
                        self.hexes[(x,y,z)] = Hex(self,coord)
                        count += 1

        print(f"{count} Hexes Created!")

    def setup_corners(self):
        
        count = 0

        for total in [-1,1]:
            for x in range(-self.n_size-1,self.n_size+2):
                for y in range(-self.n_size-1,self.n_size+2):
                    z = total - x - y
                    if abs(x) + abs(y) + abs(z) <= self.n_size*2+1:
                        count += 1
                        coords = Coords(x,y,z)
                        self.corners[(x,y,z)] = Corner(self,coords)

        print(f"{count} Corners Created!")

    def setup_roads(self):
        
        count = 0

        #sides are lines between negative total corners and positive total corners
        #nc = negative corner
        
        total = -1
        for ncx in range(-self.n_size-1,self.n_size+2):
            for ncy in range(-self.n_size-1,self.n_size+2):
                ncz = total - ncx - ncy
                if abs(ncx) + abs(ncy) + abs(ncz) <= self.n_size*2+1:
                    nc_coords = Coords(ncx,ncy,ncz)
                    nc = self.corners[nc_coords.tuple()]

                    for dirindex in range(0,3): #index in coords
                        pc_coords = nc.other_corner_coords(dirindex)
                        try:
                            pc = self.corners[pc_coords.tuple()]
                        except:
                            continue
                        
                        roadcoords = nc.road_coords(dirindex)
                        self.roads[roadcoords] = Road(self,nc.coords,pc.coords)
                        count += 1
                        
        print(f"{count} Roads Created!")                    

    def random_corner(self):
        key = random.choice(list(self.corners.keys()))
        return self.corners[key]