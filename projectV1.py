# Name: Graydon Armstrong
# Date: July 25th, 2013
# Source File: projectV1.py
# Last Modified By: Graydon Armstrong
# Date Last Modified: July 25th, 2013
# Program description: A Final Project game
# Revision History: Version 1 is setting up a basic game framework

import pygame, random
pygame.init()

screen = pygame.display.set_mode((640,480))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
       
def main():   
    keepGoing = True    
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            keepGoing = False 
#run the main menthod at the start
if __name__ == "__main__":
    main()