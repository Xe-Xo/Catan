import math

def road_rect(cx1,cy1,cx2,cy2):

    #Road dimensions
    road_length,road_thickness = 100,20


    #return list of points to draw rect

    x_delta = cx2 - cx1
    y_delta = cy2 - cy1

    print(x_delta,y_delta)    

    m = road_length
    hypot = math.sqrt(math.pow(x_delta,2) + math.pow(y_delta,2))

    print(hypot)

    n = (hypot-m)/2

    print(n)

    iX = n * x_delta/hypot
    iY = n * y_delta/hypot

    angle = math.atan(y_delta/x_delta)
    xmove = math.sin(angle) * road_thickness
    ymove = math.cos(angle) * road_thickness

    p1 = cx1 + iX - xmove, cy1 + iY + ymove
    p2 = cx1 + iX + xmove, cy1 + iY - ymove
    p3 = cx2 - iX + xmove, cy2 - iY - ymove
    p4 = cx2 - iX - xmove, cy2 - iY + ymove


    print(p1,p2,p3,p4)

road_rect(-50,0,100,200)
