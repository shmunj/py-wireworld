import pygame
from pygame import *

#status = 1 - pos, 2 - neg, None - none, 3 - conductor
COLOR = {
    1:(100,0,0),
    2:(0,0,100),
    3:(0,100,100),
    None:(50,50,50),
    4:(0,100,0),
    5:(255,200,50)
}

class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.status = None
        self.newstatus = self.status

    def draw(self,screen):
        screen.fill(COLOR[self.status],((self.x*5),(self.y*5),4,4))

    def to_change(self,cells):
        self.newstatus = self.status
        
        if self.status == 1:
            self.newstatus = 2
        elif self.status == 2:
            self.newstatus = 3
        elif self.status == 3:
            eh_neighbours = self.getNeighbours(cells,1)
            if eh_neighbours in range (1,3):
                self.newstatus = 1
            else:
                self.newstatus = 3
        elif self.status == 4:
            eh_neighbours = self.getNeighbours(cells,1)
            if eh_neighbours >= 2:
                self.newstatus = None
            elif eh_neighbours == 1:
                self.newstatus = 1
            else:
                self.newstatus = 4
        elif self.status == 5:
            eh_neighbours = self.getNeighbours(cells,4)
            if eh_neighbours >=3:
                self.newstatus = 4
            else:
                self.status = 5
        else:
            self.newstatus = None
        
        if self.status != self.newstatus:
            return True

    def change(self):
        self.status = self.newstatus

    def edit(self,newstatus):
        self.newstatus = newstatus
        self.status = self.newstatus

    def getNeighbours(self,cells,target_type):
        eh_count = 0
        for mx in range(-1,2):
            for my in range(-1,2):
                if mx == 0 and my == 0:
                    continue
                else:
                    try:
                        if cells[self.x+mx,self.y+my].status == target_type:
                            eh_count += 1
                    except:
                        continue
        return eh_count
