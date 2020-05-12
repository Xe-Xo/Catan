# Catan Clone
Initial work on my Settlers of Catan Clone.

## How to Start
run __main__.py to start the Game.

## Grid
The Grid uses a unique coordinate system shown below.
![Grid Layout](/readme_data/grid_layout.png?raw=true "Grid Layout")

### Coordinates
Each coordinate shown as (x,y,z) has a property noting which object it is referencing to:
* x+y+z = 0 (Grid) 
* x+y+z = 1 or -1 (Corner)

Roads are a combination of two Corners (1 x positive and 1x negative) on the grid
The coordinates shown are (neg_x, neg_y, pos_x, pos_y)
The z values can be automatically calculated from the values above.

### Hex
Each hex holds its grid coordinate and the grid it is allocated to.

### Corner
Each hex corner holds its grid coordinate, grid it is allocated to and its sign (+1/-1)
Helper methods to calculate the connected corners/hexes given the change on the axis

### Road
Each hex side holds its negative and positive coordinates and the grid it is assigned to.

### Movement across the Grid
It is important to remember that when moving across the grid the properties of the coordiate system does not change.

#### Movement from Hex to Hex
When moving from Hex to Hex, one axis will always +1 and another will always -1
eg. Moving from (0,0,0) to (1,-1,0) can be broken into:
* 1 Movement to (1,0,0) Corner (south east); and
* 1 Movement along Y Axis (north east) to (1,-1,0)




