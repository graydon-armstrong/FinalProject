# Name: Graydon Armstrong
# Date: July 25th, 2013
# Source File: projectV1.py
# Last Modified By: Graydon Armstrong
# Date Last Modified: August 15th, 2013
# Program description: A Final Project game
# Revision History: Version 2 is completing Part B

import pygame, gameEngine

stage = 1
score = 0
keepPlaying = True
       
class Enemy(gameEngine.SuperSprite):
    def __init__(self,scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.level = 1
        self.setImage("enemy" + str(self.level) + ".gif")
        self.setAngle(0)
        self.setSpeed(5)
        self.setBoundAction(self.ENEMYBOUNCE)       
    
    def reset(self):
        self.scene.enemiesLeft -= 1
        
        global score, stage
        score += 10*self.level
        self.scene.scoreBoard.text = "Score: " + str(score) + " Level: " + str(stage)
        
        if(self.level != 4):
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
        
        self.scoreBoard = gameEngine.Label()
        self.scoreBoard.font = pygame.font.SysFont("arial",30)
        self.scoreBoard.center = (240,15)
        self.scoreBoard.size = (480,30)
        global score, stage
        self.scoreBoard.text = "Score: " + str(score) + " Level: " + str(stage)
        
        self.enemies = []
        for ii in range(stage):
            for i in range(5):
                self.enemies.append(Enemy(self))
                self.enemies[(i+(ii)*5)].setPosition((40+i*40,100+ii*40))
                
        self.enemiesLeft = stage*5*4
            
        self.enemyGroup = self.makeSpriteGroup(self.enemies)
        
        self.sprites = [self.ship,self.bullet, self.enemies, self.scoreBoard]
        
    def update(self):
        if (self.bullet.y < 0):
            self.ship.canShoot = True
            
        enemyHitBullet = self.bullet.collidesGroup(self.enemyGroup)
        if enemyHitBullet:
            enemyHitBullet.reset()
            self.bullet.reset()
            
        for enemy in self.enemies:
            if (enemy.y > 550):
                global keepPlaying
                keepPlaying = False
                self.stop()
        
        if (self.enemiesLeft <= 0):
            self.stop()
            
class ScoreScreen(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self) 
        self.ship = Ship(self)    
        self.setCaption("Space Game")
        
        self.scoreBoard = gameEngine.MultiLabel()
        self.scoreBoard.font = pygame.font.SysFont("arial",30)
        self.scoreBoard.center = (240,300)
        self.scoreBoard.size = (300,60)
        global score, stage
        self.scoreBoard.textLines = ["Game Over", "Score: " + str(score) + " Level: " + str(stage)]
        
        self.Button = gameEngine.Button()
        self.Button.font = pygame.font.SysFont("arial",30)
        self.Button.center = (240,370)
        self.Button.size = (300,30)
        self.Button.text = "Play Again"
        
        self.quitButton = gameEngine.Button()
        self.quitButton.font = pygame.font.SysFont("arial",30)
        self.quitButton.center = (240,410)
        self.quitButton.size = (300,30)
        self.quitButton.text = "Quit"
        
        self.sprites = [self.scoreBoard,self.Button, self.quitButton]
        
    def update(self):
        if self.Button.clicked:
            global keepPlaying
            keepPlaying = True
            self.stop()
            
        if self.quitButton.clicked:
            self.stop()
            
class MenuScreen(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self) 
        self.ship = Ship(self)    
        self.setCaption("Space Game")
        
        self.scoreBoard = gameEngine.MultiLabel()
        self.scoreBoard.font = pygame.font.SysFont("arial",30)
        self.scoreBoard.center = (240,300)
        self.scoreBoard.size = (300,60)
        global score, stage
        self.scoreBoard.textLines = ["Space Game", "Space Invaders Tribute"]
        
        self.Button = gameEngine.Button()
        self.Button.font = pygame.font.SysFont("arial",30)
        self.Button.center = (240,370)
        self.Button.size = (300,30)
        self.Button.text = "Play Game"
        
        self.quitButton = gameEngine.Button()
        self.quitButton.font = pygame.font.SysFont("arial",30)
        self.quitButton.center = (240,410)
        self.quitButton.size = (300,30)
        self.quitButton.text = "Quit"
        
        self.sprites = [self.scoreBoard,self.Button, self.quitButton]
        
    def update(self):
        if self.Button.clicked:
            global keepPlaying, score, stage
            keepPlaying = True
            stage = 1
            score = 0
            self.stop()
            
        if self.quitButton.clicked:
            self.stop()

def main():
    #placeholder for start screen
    while keepPlaying:
        menuScreen = MenuScreen()
        menuScreen.start()
        while keepPlaying:  
            game = Game()    
            game.start()
            global stage
            stage += 1
        endscreen = ScoreScreen()
        endscreen.start()
    #placeholder for end screen
    
#run the main menthod at the start
if __name__ == "__main__":
    main()