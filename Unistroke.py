#!/usr/bin/env python
import sys, pygame
from pygame.locals import *
import reco as r

pygame.init()
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()
screen.fill((255,255,255))
pygame.display.set_caption ('HW3: $1 Unistroke Recognizer')

def displaytext(text, x, y):
    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))
    pygame.display.update()


position= []
done = 0
z=0
start = 0
score=0
while not done:
    clock.tick(200)
    x,y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           done = 1
           #sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            z=1      
            if start == 0:
                screen.fill((255,255,255))
                position = []
                start = 1                
        elif event.type == MOUSEBUTTONUP:
            z=0
            start = 0
            if len(position)>10:
                score=r.recognize(position,r.numcheck)
                #print(r.transform(position))
                if score[1]<0:
                    displaytext("??", 200, 0)
                    displaytext("??", 450, 0)
                else:                
                    displaytext("%s"%score[0], 200, 0)
                    displaytext("%f"%score[1], 450, 0)
            else:
                displaytext("--", 200, 0)
                displaytext("--    too small to recognize", 450, 0)
        if z == 1:
            pygame.draw.circle(screen, (255,0,0), (x,y), 4)
            position.append((x,y))
            pygame.display.update()
     
    displaytext("Number:", 100, 0)
    displaytext("Score:", 350, 0)
    
    #screen.blit(score, (220, 0))
    pygame.display.update()

#print(position)
#print(score)








    


