#!/usr/bin/python
import pygame, sys
from pygame import *

#game modules
#-----------------------------------------
import cell

#functions
#-----------------------------------------
def getActiveCells(cells):
    active_cells = {}
    for c in cells.keys():
        if cells[c].status != None:
            active_cells[c] = cells[c]
    
    return active_cells

def clearCells():
    cells = {}
    for ix in range(160):
        for iy in range(120):
            cells[ix,iy] = cell.Cell(ix,iy)
    return cells

def readyInterface(mode):
    mode_colors = {'editor':(80,50,50),'simulation':(30,120,60)}
    
    title = font.render(mode,1,mode_colors[mode])
    title_rect = title.get_rect()
    title_rect.x = 5
    title_rect.y = 605

    return title,title_rect

#pygame
#=========================================
#window
w,h = 800,700
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption('life1')

#clock
clock = pygame.time.Clock()
TICK = 5

#media
pygame.font.init()
font = pygame.font.Font('font/Mecha_Bold.ttf',20)

#cells - make it dependant on the resolution
cells = clearCells()

#editor palette
palette = {
    None:{'color':(50,50,50),'rect':(120,605,20,20)},
    1:{'color':(100,0,0),'rect':(145,605,20,20)},
    2:{'color':(0,0,100),'rect':(170,605,20,20)},
    3:{'color':(0,100,100),'rect':(195,605,20,20)},
    4:{'color':(0,100,0),'rect':(220,605,20,20)},
    5:{'color':(255,200,50),'rect':(245,605,20,20)}
    #add more
}

#=========================================

#vars
active_cells = {}
active_cells = getActiveCells(cells)

title,title_rect = readyInterface('simulation')
EDIT_MODE = False
EDIT_paint = False
EDIT_brush = 3
EDIT_brush_size = 1
#=========================================
while 1:
    if EDIT_MODE == True:
        clock.tick(TICK)
        mx,my = pygame.mouse.get_pos()
        
        screen.fill((0,0,0))
        screen.fill((20,20,20),(0,600,800,100))
        screen.blit(title,title_rect)

        for p in palette.keys():
            screen.fill(palette[p]['color'],palette[p]['rect'])

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                TICK = 5
                active_cells = getActiveCells(cells)
                title,title_rect = readyInterface('simulation')
                EDIT_MODE = False
            
            #brush size
            elif event.type == KEYDOWN and event.key == K_KP_PLUS:
                if EDIT_brush_size <= 3:
                    EDIT_brush_size += 1
                else:
                    pass
            elif event.type == KEYDOWN and event.key == K_KP_MINUS:
                if EDIT_brush_size >= 2:
                    EDIT_brush_size -= 1
                else:
                    pass
            
            #edit cells and choose brush
            elif event.type == MOUSEBUTTONDOWN:
                if my > 600:
                    if mx in range(title_rect.x,title_rect.x+title_rect.width) and my in range(title_rect.y,title_rect.y+title_rect.height):
                        TICK = 5
                        active_cells = getActiveCells(cells)
                        title,title_rect = readyInterface('simulation')
                        EDIT_MODE = False
                    else:
                        for p in palette.keys():
                            if mx in range(palette[p]['rect'][0],palette[p]['rect'][0]+20) and my in range(palette[p]['rect'][1],palette[p]['rect'][1]+20):
                                EDIT_brush = p
                                break
                else:
                    EDIT_paint = True
            elif event.type == MOUSEBUTTONUP:
                EDIT_paint = False
            elif event.type == KEYDOWN and event.key == K_c:
                cells = clearCells()

        if EDIT_paint == True:
            try:
                cells[(mx/5,my/5)].edit(EDIT_brush)
                if EDIT_brush_size > 1:
                    try:
                        for cx in range(-1*EDIT_brush_size,EDIT_brush_size+1):
                            for cy in range(-1*EDIT_brush_size,EDIT_brush_size+1):
                                cells[(mx/5+cx,my/5+cy)].edit(EDIT_brush)
                    except Exception, e:
                        print e
            except:
                continue

        #draw cells
        for c in cells.keys():
            cells[c].draw(screen)

        pygame.display.update()

    else:
        clock.tick(TICK)
        mx,my = pygame.mouse.get_pos()
        changed_cells = []

        screen.fill((50,50,50))
        screen.fill((20,20,20),(0,600,800,100))
        screen.blit(title,title_rect)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                TICK = 60
                title,title_rect = readyInterface('editor')
                EDIT_MODE = True
            elif event.type == MOUSEBUTTONDOWN:
                if my > 600:
                    if mx in range(title_rect.x,title_rect.x+title_rect.width) and my in range(title_rect.y,title_rect.y+title_rect.height):
                        TICK = 60
                        title,title_rect = readyInterface('editor')
                        EDIT_MODE = True

        #cell state change
        for c in active_cells.keys():
            if cells[c].to_change(cells):
                changed_cells.append(c)

        for c in changed_cells:
            cells[c].change()
        
        #draw cells
        for c in active_cells.keys():
            cells[c].draw(screen)

        pygame.display.update()
