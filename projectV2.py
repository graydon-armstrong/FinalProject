# Name: Graydon Armstrong
# Date: July 25th, 2013
# Source File: projectV1.py
# Last Modified By: Graydon Armstrong
# Date Last Modified: August 15th, 2013
# Program description: A Final Project game
# Revision History: Version 2 is completing Part B

import pygame, gameEngine

#global variables to keep track of the game
stage = 1
score = 0
keepPlaying = True

#Splashscreen sprite
class Splash(gameEngine.SuperSprite):
    def __init__(self,scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("splashscreen.png")
        self.setPosition((240,320))
        self.setAngle(0)
        self.setSpeed(0) 

#Enemy Sprite
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
        
        #score based on level when killed
        global score, stage
        score += 10*self.level
        self.scene.scoreBoard.text = "Score: " + str(score) + " Level: " + str(stage)
        
        #if you arent in your final form reset in next form otherwise die
        if(self.level != 4):
            self.level += 1
            self.setImage("enemy" + str(self.level) + ".gif")
            self.setAngle(0)
            self.setSpeed((self.level-1)*1.5+5)
            self.setPosition((240,100))
        else:
            self.setPosition((240,-100))
            self.setSpeed(0)
            
#Ship Sprite for player
class Ship(gameEngine.SuperSprite):
    def __init__(self,scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("ship.gif")
        self.setAngle(0)
        self.setPosition((240,600))
        self.setBoundAction(self.STOP)
        self.canShoot = True 
        
    #Move the sprite on screen
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if(self.x > 20):
                self.moveBy((-5,0))
        if keys[pygame.K_RIGHT]:
            if(self.x < 460):
                self.moveBy((5,0))
        #if the bullet is shootable shoot it
        if keys[pygame.K_SPACE]:
            if (self.canShoot == True):
                self.scene.bullet.fire()
                self.canShoot = False
                
#BulletSprite
class Bullet(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setPosition ((-100, -100))
        self.setImage("bullet.gif")
        self.setBoundAction(self.HIDE)
        
    #when the bullet is fired set its position to the player and shoot up
    def fire(self):
        self.setPosition((self.scene.ship.x, self.scene.ship.y))
        self.setSpeed(12)
        self.setAngle(90)
        
    #When dieing put off screen
    def reset(self):
        self.setPosition ((-100, -100))
        self.setSpeed(0)
       
#The main game loop
class Game(gameEngine.Scene):
    def __init__(self):
        #Set the scene and build the player and bullet
        gameEngine.Scene.__init__(self) 
        self.ship = Ship(self)    
        self.setCaption("Space Game")
        self.background.fill((0, 0, 0))
        self.bullet = Bullet(self)
        
        #Build the score section
        self.scoreBoard = gameEngine.Label()
        self.scoreBoard.font = pygame.font.SysFont("arial",30)
        self.scoreBoard.center = (240,15)
        self.scoreBoard.size = (480,30)
        global score, stage
        self.scoreBoard.text = "Score: " + str(score) + " Level: " + str(stage)
        
        #Place enemies on screen based on stage
        self.enemies = []
        for ii in range(stage):
            for i in range(5):
                self.enemies.append(Enemy(self))
                self.enemies[(i+(ii)*5)].setPosition((40+i*40,100+ii*40))
                
        #set how many enemies have to die to end the room
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
            
#Loop for the score screen
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

#loop for the menu screen
class MenuScreen(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self) 
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
            global keepPlaying
            keepPlaying = False
            self.stop()

#loop for the splashscreen
class SplashScreen(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self) 
        self.setCaption("Space Game")
        self.time = 0
        self.splash = Splash(self)
        
        self.sprites = [self.splash]
    
    def update(self):
        self.time+=1
        
        if (self.time > 60):
            self.stop()

#Main gameloop that controls the other rooms
def main():
    #placeholder for start screen
    splashScreen = SplashScreen()
    splashScreen.start()
    while keepPlaying:
        menuScreen = MenuScreen()
        menuScreen.start()
        while keepPlaying:
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