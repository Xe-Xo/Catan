class ResourceBunch():

    def DEVELOPMENT():
        return ResourceBunch(0,0,1,1,1)

    def SETTLEMENT():
        return ResourceBunch(1,1,0,1,1)

    def CITY():
        return ResourceBunch(0,0,3,2,0)

    def ROAD():
        return ResourceBunch(1,1,0,0,0)

    def WOOD():
        return ResourceBunch(1,0,0,0,0)
    
    def BRICK():
        return ResourceBunch(0,1,0,0,0)
    
    def ORE():
        return ResourceBunch(0,0,1,0,0)
    
    def WHEAT():
        return ResourceBunch(0,0,0,1,0)
    
    def SHEEP():
        return ResourceBunch(0,0,0,0,1)

    def from_tuple(tuple):
        return ResourceBunch(tuple[0],tuple[1],tuple[2],tuple[3],tuple[4])

    def resources_gained(r_idx,settlement,city):
        RESOURCE_INDEX = {0:ResourceBunch.WOOD(),1:ResourceBunch.BRICK(),2:ResourceBunch.ORE(),3:ResourceBunch.WHEAT(),4:ResourceBunch.SHEEP()}
        return RESOURCE_INDEX[r_idx] * (2*city+settlement) 

    def __init__(self,wood,brick,ore,wheat,sheep):
        self.wood = wood
        self.brick = brick
        self.ore = ore
        self.wheat = wheat
        self.sheep = sheep
        self.tuple = (wood,brick,ore,wheat,sheep)

    def __add__(self,other):
        return ResourceBunch(self.wood+other.wood,self.brick+other.brick,self.ore+other.ore,self.wheat+other.wheat,self.sheep+other.sheep)

    def __sub__(self,other):
        return ResourceBunch(self.wood-other.wood,self.brick-other.brick,self.ore-other.ore,self.wheat-other.wheat,self.sheep-other.sheep)

    def __mul__(self,other):
        if type(other) == int:
            return ResourceBunch(self.wood*other,self.brick*other,self.ore*other,self.wheat*other,self.sheep*other)
        elif type(other) == ResourceBunch:
            return ResourceBunch(self.wood*other.wood,self.brick*other.brick,self.ore*other.ore,self.wheat*other.wheat,self.sheep*other.sheep)
        else:
            return None

    def __eq__(self, other):
        if type(other) == ResourceBunch:
            for r_idx in range(0,len(self.tuple)):
                if self.tuple[r_idx] != other.tuple[r_idx]:
                    return False
            return True
        else:
            return False

    def __ne__(self,other):
        if type(other) == ResourceBunch:
            for r_idx in range(0,len(self.tuple)):
                if self.tuple[r_idx] == other.tuple[r_idx]:
                    return False
            return True            
        else:
            return False

    def __ge__(self,other):
        if type(other) == ResourceBunch:
            for r_idx in range(0,len(self.tuple)):
                if self.tuple[r_idx] < other.tuple[r_idx]:
                    return False
            return True
        else:
            return False

    def __le__(self,other):
        if type(other) == ResourceBunch:
            for r_idx in range(0,len(self.tuple)):
                if self.tuple[r_idx] > other.tuple[r_idx]:
                    return False
            return True
        else:
            return False

    def __gt__(self,other):
        if type(other) == ResourceBunch:
            for r_idx in range(0,len(self.tuple)):
                if self.tuple[r_idx] <= other.tuple[r_idx]:
                    return False
            return True
        else:
            return False

    def __lt__(self,other):
        if type(other) == ResourceBunch:
            for r_idx in range(0,len(self.tuple)):
                if self.tuple[r_idx] >= other.tuple[r_idx]:
                    return False
            return True
        else:
            return False  

    def __hash__(self):
        return hash(self.tuple)

    def __repr__(self):
        return f"Wd:{self.wood}, Br:{self.brick}, Or:{self.ore}, Wh:{self.wheat}, Sh:{self.sheep}"
    
    def discard(self,other):
        return ResourceBunch(self.clamp(self.wood-other.wood,0),self.clamp(self.brick-other.brick,0),self.clamp(self.ore-other.ore,0),self.clamp(self.wheat-other.wheat,0),self.clamp(self.sheep-other.sheep,0))
        
    def clamp(self,current_int,min_int=None,max_int=None):
        if min_int is not None:
            if current_int < min_int:
                return min_int
        elif max_int is not None:
            if current_int > max_int:
                return max_int
        else:
            current_int

    def any_negative(self):
        for resource in self.tuple:
            if resource < 0:
                return True
        return False

    def count(self):
        count = 0
        for resource in self.tuple:
            count += resource
        return count

    def possible_discards_to_count(self,resources_discard_to):

        #when discarding down to a specific number
        #returns list of possible resource bunches for required discard

        possible_discards = []
        for woodcount in range(0,self.wood+1):
            for brickcount in range(0,self.brick+1):
                for orecount in range(0,self.ore+1):
                    for wheatcount in range(0,self.wheat+1):
                        for sheepcount in range(0,self.sheep+1):
                            discard_rb = ResourceBunch(woodcount,brickcount,orecount,wheatcount,sheepcount)
                            remaining_rb = self - discard_rb
                            if remaining_rb.count() == resources_discard_to:
                                possible_discards.append(discard_rb)
                            else:
                                pass
        
        return possible_discards

    def possible_discards_to_rb(self,resourcebunch_to_keep):

        #when discarding down to a specific resource bunch
        #returns list of possible resource bunches to have remaining kept amount

        possible_discards = []
        for woodcount in range(0,self.wood+1):
            for brickcount in range(0,self.brick+1):
                for orecount in range(0,self.ore+1):
                    for wheatcount in range(0,self.wheat+1):
                        for sheepcount in range(0,self.sheep+1):
                            discard_rb = ResourceBunch(woodcount,brickcount,orecount,wheatcount,sheepcount)
                            remaining_rb = self - discard_rb
                            if remaining_rb >= resourcebunch_to_keep:
                                possible_discards.append(discard_rb)
                            else:
                                pass
        
        return possible_discards


if __name__ == "__main__":
    
    test = ResourceBunch(2,2,1,1,1)
    for rb in test.possible_discards_to_rb(ResourceBunch.ROAD()*2):
        print(rb,rb.count())