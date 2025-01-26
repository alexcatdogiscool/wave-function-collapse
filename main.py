import pygame as pg
import numpy as np
import math
import random
import time
import cv2



def neighbors(pos, size):
    n = [pos[0]-1, pos[1]]
    if size in n:
        n = [-1, -1]
    e = [pos[0], pos[1]+1]
    if size in e:
        e = [-1, -1]
    s = [pos[0]+1, pos[1]]
    if size in s:
        s = [-1, -1]
    w = [pos[0], pos[1]-1]
    if size in w:
        w = [-1, -1]
    return [n,e,s,w]

class rules:
    def __init__(self):
        self.number = 3
        self.rules = {-1: [[0,1],[0,1],[0,1],[0,1]], 0 : [[0],[1,0],[0],[1,0]], 1 : [[1],[0],[1],[0]]}# nth tile : [n,e,s,w] where n is a list of tiles allowed on the north side, e is a list of tiles allowed on the east side, etc
        self.color = {-1 : (128,128,128), 0 : (255,0,0), 1 : (0,255,0)}



class gridmap:
    def __init__(self):
        self.width = 100
        self.grid = np.zeros((self.width, self.width)) - 1


    def updateSingle(self, pos, rules):
        if self.grid[*pos] != -1:
            return
        posabilities = list(range(-1, rules.number-1))
        i = 0
        for n in neighbors(pos, self.width):
            if (n[0] == -1 or n[1] == -1):
                i += 1
                continue
            nType = self.grid[*n]
            temp = rules.rules[nType][(i+2)%4]
            posabilities = list(set(temp) & set(posabilities))
            i += 1
        if len(posabilities) == 0:
            #print("no such satisfaction :(... choosing random tile")
            self.grid[*pos] = random.randint(0, rules.number-2)
            return
        selection = posabilities[random.randint(0, len(posabilities))-1]
        self.grid[*pos] = selection

    def updateRandom(self, rules):
        pos = [random.randint(0, self.width-1), random.randint(0, self.width-1)]
        while self.grid[*pos] != -1:
            pos = [random.randint(0, self.width-1), random.randint(0, self.width-1)]
        self.updateSingle(pos, rules)

    def getBoarders(self):
        boarderList = []
        for col in range(self.width):
            for row in range(self.width):
                myType = self.grid[row, col]
                if (myType != -1):
                    for n in neighbors([row, col], self.width):
                        if (-1 in n):
                            continue
                        if (self.grid[*n] == -1):
                            boarderList.append(n)
        return boarderList
    
    def resetMask(self, mask):
        for pos in mask:
            self.grid[*pos] = -1


def displayGrid(screen, map, rules):
    width = screen.get_size()[0]
    pxSize = width/map.width
    for col in range(map.width):
        for row in range(map.width):
            myType = map.grid[row, col]
            pg.draw.rect(screen, rules.color[myType], (col*pxSize, row*pxSize, pxSize, pxSize))

def loadBrush(path):
    img = cv2.imread(path)
    return img[:,:,0]

def getBrushMask(pos, brush):
    mask = []
    halfHeight = brush.shape[0]//2
    halfWidth = brush.shape[1]//2
    
    for col in range(brush.shape[0]):
        for row in range(brush.shape[1]):
            if not brush[row,col]:#if px is black (accept it)
                mask.append([row-halfHeight+pos[0], col-halfWidth+pos[1]])
    return mask

def rotateMask(currentAngle, radius, brush, width):
    x = int((radius * math.cos(currentAngle)) + (width//2))
    y = int((radius * math.sin(currentAngle)) + (width//2))
    return getBrushMask([x,y], brush)
    





m = gridmap()
r = rules()
m.updateSingle([5,5], r)

brush = loadBrush("5block.png")



screenSize = 600
bgColor = (182, 184, 182)
screen = pg.display.set_mode((screenSize, screenSize))
screen.fill(bgColor)
pg.display.flip()

pxSize = screen.get_size()[0]/m.width

ang = 0

running = True
while running:
    m1,m2,m3 = pg.mouse.get_pressed()
    mx,my = pg.mouse.get_pos()

    ang += 0.2
    #print(((ang%360)*math.pi/180))

    


    if m1:
        newPos = [int(my/pxSize), int(mx/pxSize)]
        m.updateSingle(newPos, r)


    ##### brush
    mask = getBrushMask([int(my/pxSize), int(mx/pxSize)], brush)
    boarder = m.getBoarders()
    selectionRange = list(set(map(tuple, boarder)) & set(map(tuple, mask)))
    if len(selectionRange) != 0 and m1:
        #print(len(selectionRange))
        m.updateSingle(selectionRange[random.randint(0, len(selectionRange)-1)], r)
    if m3:
        m.resetMask(mask)
    

    #### rotation brush thingy
    mask = rotateMask(ang*math.pi/180, 30, brush, m.width)
    boarder = m.getBoarders()
    selectionRange = list(set(map(tuple, boarder)) & set(map(tuple, mask)))
    if len(selectionRange) != 0:
        m.updateSingle(selectionRange[random.randint(0, len(selectionRange)-1)], r)

    mask = rotateMask((ang+10)*math.pi/180, 30, brush, m.width)
    m.resetMask(mask)



    displayGrid(screen, m, r)







    pg.display.flip()
    #time.sleep(0.5)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
