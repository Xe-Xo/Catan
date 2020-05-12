from grid import Coords
import math

#testpos = Coords(-0.47290592754970234, -0.06876073911696429, 0.5416666666666666).round(1)
#print(testpos)
#testneg = Coords(-0.47290592754970234, -0.06876073911696429, 0.5416666666666666).round(-1)
#print(testneg)

#should return -1,-1,1 & 0,-1,2

test1 = Coords(0.45, -1.495, 1.04)
test2 = Coords(0.374,-1.574,1.2)

print(test1.round(1))
print(test2.round(1))


