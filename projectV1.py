# Name: Graydon Armstrong
# Date: July 25th, 2013
# Source File: projectV1.py
# Last Modified By: Graydon Armstrong
# Date Last Modified: July 25th, 2013
# Program description: A Final Project game
# Revision History: Version 1 is setting up a basic game framework

import pygame, gameEngine
       
class Enemy(gameEngine.SuperSprite):
    def __init__(self,scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.level = 1
        self.setImage("enemy" + str(self.level) + ".gif")
        self.setAngle(0)
        self.setSpeed(5)
        self.setBoundAction(self.ENEMYBOUNCE)       
    
    def reset(self):
        if(self.level != 3):
            self.level += 1
            self.setImage("enemy" + str(self.level) + ".gif")
            self.setAngle(0)
            self.setSpeed((self.level-1)*1.5+5)
            self.setPosition((240,100))
        else:
            self.setPosition((240,-100))
            self.setSpeed(0)
       
class Ship(gameEngine.SuperSprite):
    def __init__(self,scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("ship.gif")
        self.setAngle(0)
        self.setPosition((240,600))
        self.setBoundAction(self.STOP)
        self.canShoot = True 
        
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if(self.x > 20):
                self.moveBy((-5,0))
        if keys[pygame.K_RIGHT]:
            if(self.x < 460):
                self.moveBy((5,0))
        if keys[pygame.K_SPACE]:
            if (self.canShoot == True):
                self.scene.bullet.fire()
                self.canShoot = False
                
class Bullet(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setPosition ((-100, -100))
        self.setImage("bullet.gif")
        self.setBoundAction(self.HIDE)
        
    def fire(self):
        self.setPosition((self.scene.ship.x, self.scene.ship.y))
        self.setSpeed(12)
        self.setAngle(90)
        
    def reset(self):
        self.setPosition ((-100, -100))
        self.setSpeed(0)
       
class Game(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self) 
        self.ship = Ship(self)    
        self.setCaption("Space Game")
        self.background.fill((0, 0, 0))
        self.bullet = Bullet(self)
        
        self.enemies = []
        for ii in range(3):
            for i in range(5):
                self.enemies.append(Enemy(self))
                self.enemies[(i+(ii)*5)].setPosition((40+i*40,100+ii*40))
            
        self.enemyGroup = self.makeSpriteGroup(self.enemies)
        
        self.sprites = [self.ship,self.bullet, self.enemies]
        
    def update(self):
        if (self.bullet.y < 0):
            self.ship.canShoot = True
            
        enemyHitBullet = self.bullet.collidesGroup(self.enemyGroup)
        if enemyHitBullet:
            enemyHitBullet.reset()
            self.bullet.reset()

def main():   
    game = Game()    
    game.start()
    
#run the main menthod at the start
if __name__ == "__main__":
    main()