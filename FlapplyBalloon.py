import pygame
import time
from random import *
pygame.init()

class GameConfig :
	windowH = 750
	windowW = 1200
	blue=(113,177,227)
	white=(255,255,255)
	imgBalloon = pygame.image.load('images/hero.png')
	balloonW = 85
	balloonH = 82
	imgUpperCloud = pygame.image.load('images/balle.png')
	imgLowerCloud = pygame.image.load('images/balle.png')
	cloudW=300
	cloudH=300
	imgCrosshair = pygame.image.load('images/rsz_crosshair.png')
	crossW=20
	crossH=20

class GameState :
	def __init__(self) :
		self.balloonX=GameConfig.windowW/20
		self.balloonY=GameConfig.windowH/2 - GameConfig.balloonH/2
		self.cloudX=GameConfig.windowW
		self.cloudY=randint(-GameConfig.cloudH,120)
		self.cloudSpace = 3*GameConfig.balloonH
		self.cloudSpeed=3
		self.score=0
		self.crossX=GameConfig.windowW/5
		self.crossY=GameConfig.windowH/2 - GameConfig.crossH/2
	def draw(self,window):
		window.fill(GameConfig.blue)
		window.blit(GameConfig.imgBalloon,(self.balloonX,self.balloonY))
		window.blit(GameConfig.imgUpperCloud,(self.cloudX,self.cloudY))
		window.blit(GameConfig.imgLowerCloud,(self.cloudX,self.cloudY+self.cloudSpace+GameConfig.cloudH))
		window.blit(GameConfig.imgCrosshair,(self.crossX,self.crossY))

	def advanceState(self,nextM) :
		self.balloonY+=nextM
		self.cloudX = self.cloudX-self.cloudSpeed
		if self.cloudX < 0 - GameConfig.cloudW :
			self.cloudY=randint(-GameConfig.cloudH,120)
			self.cloudX=GameConfig.windowW
			self.score+=1
			#self.cloudSpeed+=0.2

	def isOver(self) :
		touchingEdge = self.balloonY + GameConfig.balloonH > GameConfig.windowH+10 or self.balloonY <- 10
		touchingUpperCloud = self.balloonX + GameConfig.balloonW > self.cloudX+40 and self.balloonX < self.cloudX+GameConfig.cloudW-40 and self.balloonY < self.cloudY + GameConfig.cloudH-40
		touchingLowerCloud = self.balloonX + GameConfig.balloonW > self.cloudX+40 and self.balloonX < self.cloudX+GameConfig.cloudW-40 and self.balloonY + GameConfig.balloonH > self.cloudY + GameConfig.cloudH + self.cloudSpace + 40
		return touchingEdge or touchingUpperCloud or touchingLowerCloud

class Move :
	Up = -1
	Down = 1

def gameLoop(window, horloge) :
	game_over = False
	gameState=GameState()
	nextMove=0
	while not game_over :
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				game_over = True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				nextMove=Move.Up
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				nextMove=Move.Down
			if event.type == pygame.KEYUP :
				nextMove=0
		gameState.advanceState(nextMove)
		#nextMove=getIA(gameState)
		horloge.tick(100)
		gameState.draw(window)
		displayMessage(window,"Score : "+str(gameState.score),16,30,10)

		if gameState.isOver()==True :
			displayMessage(window,"Boom!",150,GameConfig.windowW/2,GameConfig.windowH/2-50)
			displayMessage(window,"Appuyer sur une touche pour continuer",20,GameConfig.windowW/2,GameConfig.windowH/2+50)
			game_over=True

		pygame.display.update()
	if(playAgain()) :
		gameLoop(window,horloge)
		pygame.quit()
		quit()
		

	
def displayMessage(window,text,fontSize,x,y) :
	font=pygame.font.Font('BradBunR.ttf',fontSize)
	img=font.render(text,True,GameConfig.white)
	displayRect=img.get_rect()
	displayRect.center=(x,y)
	window.blit(img,displayRect)

def playAgain():
	time.sleep(0.7)
	while True :
		for event in pygame.event.get([pygame.KEYDOWN,pygame.QUIT]) :
			if event.type == pygame.QUIT :
				return False
			elif event.type == pygame.KEYDOWN :
				return True
		time.sleep(0)

def getIA(gameState):
	if gameState.cloudY + GameConfig.cloudH + 30 > gameState.balloonY :
		return Move.Down
	return Move.Up

def main() :
	window = pygame.display.set_mode((GameConfig.windowW,GameConfig.windowH))
	pygame.display.set_caption("FlappyBalloon")

	horloge = pygame.time.Clock()

	gameLoop(window, horloge)
	pygame.quit()
	quit()

main()