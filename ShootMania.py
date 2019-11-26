import pygame
import time
from random import *
import math
pygame.init()

#______________________________________________________________________________
#                                  CLASSES
#______________________________________________________________________________

class GameConfig :
	windowH = 750
	windowW = 1200
	blue=(113,177,227)
	white=(255,255,255)
	imgPelouse = pygame.image.load('images/pelouse.jpg')
	imgFond = pygame.transform.scale(imgPelouse, (750, 1200))
	imgHero = pygame.image.load('images/hero.png')
	HeroW = 85
	HeroH = 82
	imgCrosshair = pygame.image.load('images/rsz_crosshair.png')
	crossW=20
	crossH=20
	level=1
	difficulty=1
	position=1
	game_over = False
	game_win = False
	balles=[None]
	#imgBalle = pygame.image.load('images/balle.png')
	balleW=24
	balleH=12
	imgBalle = pygame.image.load('images/balle.png')
	ballestirées=0
	temps=0
	ennemistués=0
	score=0
	ennemies=[None]
	imgEnnemy = pygame.image.load('images/ennemy.png')
	imgEnnemyr = pygame.transform.rotate(imgEnnemy, 90)
	EnnemiW = 60
	EnnemiH = 37
	imgCadre = pygame.image.load('images/cadre.png')
	cadreW = 1000
	cadreH = 690
	timer = 0

class GameState :
	def __init__(self) :
		self.HeroX=GameConfig.windowW/20
		self.HeroY=GameConfig.windowH/2 - GameConfig.HeroH/2
		#self.balleX=GameConfig.windowH/2
		#self.balleY=GameConfig.windowH/2 - GameConfig.balleH/2
		#self.balleSpeed=1
		self.score=0
		self.crossX=GameConfig.windowW/5
		self.crossY=GameConfig.windowH/2 - GameConfig.crossH/2
		self.cadreX=GameConfig.windowW - GameConfig.windowW/1.25 -50
		self.cadreY=GameConfig.windowH - GameConfig.windowH/1.086 - 50
		self.life=3

	def draw(self,window):
		#window.blit(GameConfig.imgFond,[0,0])
		window.blit(GameConfig.imgHero,(self.HeroX,self.HeroY))
		#window.blit(GameConfig.imgBalle,(Balle.balleX,Balle.balleY))
		window.blit(GameConfig.imgCrosshair,(self.crossX,self.crossY))
		window.blit(GameConfig.imgCadre,(self.cadreX,self.cadreY))


	def advanceState(self,nextM) :
		self.HeroY+=nextM
		'''for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
				self.balleX=GameConfig.windowW/20+GameConfig.HeroW/2
				self.balleY=GameConfig.HeroY - GameConfig.HeroH/2
				score+=2
		self.balleX = self.balleX+self.balleSpeed'''
		#self.score+=1
		#self.balleSpeed+=0.2

	def drawbackground(self,window,color):
		window.fill(color)

class Move :
	Up = -2
	Down = 2

class Balle :
	def __init__(self, gameState) :
		self.balleX=GameConfig.windowW/20+GameConfig.HeroW
		self.balleY=gameState.HeroY+GameConfig.HeroH/2 +8
		self.balleSpeed=6
		#self.angle = math.atan2(gameState.crossY+GameConfig.crossH/2-gameState.HeroY+GameConfig.HeroH/2+8,gameState.crossX+GameConfig.crossW/2 - gameState.HeroX+GameConfig.HeroW)
		self.angle = math.atan2(gameState.crossY-gameState.HeroY,gameState.crossX- gameState.HeroX)
		self.imgBalle=pygame.transform.rotate(GameConfig.imgBalle, 360 - math.degrees(self.angle))

	def update(self) :
		self.balleX += self.balleSpeed*math.cos(self.angle)
		self.balleY += self.balleSpeed*math.sin(self.angle)
		return self.balleX, self.balleY

class Ennemy :
	def __init__(self) :
		self.ennemyX=1120
		self.ennemyY=randint(120,540)

#______________________________________________________________________________
#                                  FONCTIONS
#______________________________________________________________________________

def isLost(gameState) :
	if gameState.life == 0 :
			return True
		 
def perdUneVie(gameState) :
	while compteur<array_size_ennemies() :
		if GameConfig.ennemies[compteur] is not None :
			if GameConfig.ennemies[compteur].ennemyX<gameState.cadreX : 
				gameState.life -=1
		compteur+=1		

def niveau(window) :
	if GameConfig.position==1 :
		if GameConfig.level==1 :
			displayMessage(window,"Choisir niveau :   "+str(GameConfig.level)+" >",60,GameConfig.windowW/2,GameConfig.windowH/2-80)
		else :
			displayMessage(window,"Choisir niveau : < "+str(GameConfig.level),60,GameConfig.windowW/2,GameConfig.windowH/2-80)
	else :
		if GameConfig.level==1 :
			displayMessage(window,"Choisir niveau :   "+str(GameConfig.level)+" >",40,GameConfig.windowW/2,GameConfig.windowH/2-80)
		else :
			displayMessage(window,"Choisir niveau : < "+str(GameConfig.level),40,GameConfig.windowW/2,GameConfig.windowH/2-80)

def difficulte(window) :
	if GameConfig.position==2 :
		if GameConfig.difficulty==1 :
			displayMessage(window,"Difficulté :   Easy >",60,GameConfig.windowW/2,GameConfig.windowH/2)
		elif GameConfig.difficulty==3 :
			displayMessage(window,"Difficulté : < Hard",60,GameConfig.windowW/2,GameConfig.windowH/2)
		else :
			displayMessage(window,"Difficulté : < Medium >",60,GameConfig.windowW/2,GameConfig.windowH/2)
	else :
		if GameConfig.difficulty==1 :
			displayMessage(window,"Difficulté :   Easy >",40,GameConfig.windowW/2,GameConfig.windowH/2)
		elif GameConfig.difficulty==3 :
			displayMessage(window,"Difficulté : < Hard",40,GameConfig.windowW/2,GameConfig.windowH/2)
		else :
			displayMessage(window,"Difficulté : < Medium >",40,GameConfig.windowW/2,GameConfig.windowH/2)

def array_size_balles() :
	compteur=0
	for valeur in GameConfig.balles :
		compteur+=1
	return compteur

def array_size_ennemies() :
	compteur=0
	for valeur in GameConfig.ennemies :
		compteur+=1
	return compteur

def tirer(gameState) :
	compteur=0
	continuer=False
	while continuer==False :
		if GameConfig.balles[compteur] is None :
			GameConfig.balles[compteur]=Balle(gameState)
			GameConfig.ballestirées+=1
			if array_size_balles()-1 == compteur :
				GameConfig.balles.append(None)
			continuer=True
		else :
			compteur+=1
		
		#print(GameConfig.balles)        

def spawnEnnemy(gameState) :
	compteur=0
	continuer=False
	
	while continuer==False :
		if GameConfig.ennemies[compteur] is None :
			GameConfig.ennemies[compteur]=Ennemy()
			if array_size_ennemies()-1 == compteur :
				GameConfig.ennemies.append(None)
			continuer=True
		else :
			compteur+=1    

def printballe(window, gameState) :
	compteur=0
	while compteur<array_size_balles() :
		if GameConfig.balles[compteur] is not None :
			GameConfig.balles[compteur].update()
			#GameConfig.balles[compteur].balleX+=GameConfig.balles[compteur].balleSpeed
			#GameConfig.balles[compteur].balleY+=GameConfig.balles[compteur].balleSpeed*math.tan(GameConfig.balles[compteur].angle)
			window.blit(GameConfig.balles[compteur].imgBalle,(GameConfig.balles[compteur].balleX,GameConfig.balles[compteur].balleY))
			#print(GameConfig.balles[compteur].angle)
		compteur+=1

def printennemy(window,gameState) :
	compteur=0
	while compteur<array_size_ennemies() :
		if GameConfig.ennemies[compteur] is not None :
			#GameConfig.ennemies[compteur].ennemyX+=GameConfig.ennemies[compteur].balleSpeed
			window.blit(GameConfig.imgEnnemyr,(GameConfig.ennemies[compteur].ennemyX,GameConfig.ennemies[compteur].ennemyY))
			GameConfig.ennemies[compteur].ennemyX+=moveEnnemylevel1(gameState)
		compteur+=1

def supprimerballe() :
	compteur=0
	while compteur<array_size_balles() :
		if GameConfig.balles[compteur] is not None :
			if GameConfig.balles[compteur].balleX>GameConfig.windowW : 
				GameConfig.balles[compteur]=None
		compteur+=1

def supprimerennemmy(gameState) :
	compteur=0
	while compteur<array_size_ennemies() :
		if GameConfig.ennemies[compteur] is not None :
			if GameConfig.ennemies[compteur].ennemyX<gameState.cadreX : 
				GameConfig.ennemies[compteur]=None
		compteur+=1

def displayMessage(window,text,fontSize,x,y) :
	font=pygame.font.Font('ModerneM.ttf',fontSize)
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
	if Balle.balleY + GameConfig.balleH + 30 > gameState.HeroY :
		return Move.Down
	return Move.Up

def start(window, gameState) :
	gameState.drawbackground(window,GameConfig.blue)
	gameState.draw(window)
	displayMessage(window,"Niveau : "+str(GameConfig.level)+"  /  Difficulté : "+str(GameConfig.difficulty),14,100,10)

'''def angle(gameState) : 
	#return (gameState.crossY-gameState.HeroY) / (gameState.crossX - gameState.HeroX)
	tan = (abs(gameState.crossY-gameState.HeroY) / abs(gameState.crossX - gameState.HeroX))
	angle = math.atan(tan) * (180 / math.pi)
	return angle
'''	
def inZone(gameState) :
	if gameState.crossX > GameConfig.windowW - GameConfig.windowW/1.25 -50 and gameState.crossX<GameConfig.windowW - GameConfig.windowW/1.25 -50+GameConfig.cadreW and gameState.crossY>GameConfig.windowH - GameConfig.windowH/1.086 - 50 and gameState.crossY< GameConfig.windowH - GameConfig.windowH/1.086 - 50 + GameConfig.cadreH : 
		return True
	return False

def moveEnnemylevel1(gameState) :
	move = 0
	if GameConfig.difficulty==1 :
		move = -1
	elif GameConfig.difficulty==2 :
		move =  -1.5
	else :
		move = -2
	return move

def moveEnnemylevel2(gameState) :
	if GameConfig.difficulty==1 :
		Up = -2
		Down = 2
	elif GameConfig.difficulty==2 :
		Up = -3
		Down = 3
	else :
		Up = -4
		Down = 4

#______________________________________________________________________________
#                                  FENETRES
#______________________________________________________________________________

def settings_game(window, horloge) :
	continuer = False
	gameState=GameState()
	while not continuer :
		#choisir_niveau()
		#choisir_difficulte()
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				continuer = True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
				continuer=True

			if GameConfig.position==1 :
				if GameConfig.level>1 and event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT :
					GameConfig.level-=1
				if GameConfig.level<2 and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT :
					GameConfig.level +=1
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN :
					GameConfig.position=2
			
			if GameConfig.position==2 :
				if GameConfig.difficulty>1 and event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT :
					GameConfig.difficulty-=1
				if GameConfig.difficulty<3 and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT :
					GameConfig.difficulty +=1
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
						GameConfig.position=1
			
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
				pygame.quit()
				quit()
				
		horloge.tick(100)
		gameState.drawbackground(window,GameConfig.blue)
		#displayMessage(window,"Choisir niveau : ",40,GameConfig.windowW/2,GameConfig.windowH/2-50)
		#displayMessage(window,"Score : "+str(gameState.score),16,30,10)
		niveau(window)
		difficulte(window)
		pygame.display.update()
		
def gameLoop(window, horloge) :
	gameState=GameState()
	nextMove=0
	timer=0
	
	start(window,gameState)
	displayMessage(window,"3",100,GameConfig.windowW/2,GameConfig.windowH/2)
	pygame.display.update()
	time.sleep(1)
	
	start(window,gameState)
	displayMessage(window,"2",100,GameConfig.windowW/2,GameConfig.windowH/2)
	pygame.display.update()
	time.sleep(1)
	
	start(window,gameState)
	displayMessage(window,"1",100,GameConfig.windowW/2,GameConfig.windowH/2)
	pygame.display.update()
	time.sleep(1)
	
	start(window,gameState)
	displayMessage(window,"GO",100,GameConfig.windowW/2,GameConfig.windowH/2)
	pygame.display.update()
	time.sleep(0.4)

	spawnEnnemy(gameState);
	
	while GameConfig.game_over==False and GameConfig.game_win==False :
		pygame.mouse.set_visible(False)
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				GameConfig.game_over = True

			if event.type == pygame.MOUSEMOTION : 
				#if event.pos[1] > GameConfig.windowW - GameConfig.windowW/1.25 -50 and event.pos[1]<GameConfig.windowW - GameConfig.windowW/1.25 -50+GameConfig.cadreW and event.pos[0]>GameConfig.windowH - GameConfig.windowH/1.086 - 50 and event.pos[0]< GameConfig.windowH - GameConfig.windowH/1.086 - 50 + GameConfig.cadreH :
				if event.pos[0] > gameState.HeroX + GameConfig.HeroW :
					#SDL_WM_GrabInput(SDL_GRAB_ON)
    				#SDL_ShowCursor(SDL_DISABLE)
					gameState.crossX = event.pos[0]
					gameState.crossY = event.pos[1]
				#print(event.pos[1]) #permet d'afficher coord du curseur
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1  :
				tirer(gameState)
				#Balle.balleX=event.pos[0]
				#Balle.balleY=event.pos[1]
				#print(angle(gameState))

			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
			 		nextMove=0
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN :
					nextMove=0
			if event.type == pygame.KEYUP :
				nextMove=0

			if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
				GameConfig.game_over = True
			if GameConfig.ballestirées==20:
				GameConfig.game_win = True
				
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
				pygame.quit()
				quit()

		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP] :
			if gameState.HeroY <= -5 :
				nextMove=0
			else :
				nextMove=Move.Up
		if keys[pygame.K_DOWN] :
			if gameState.HeroY >= 668 :
				nextMove=0
			else :
				nextMove=Move.Down

		if timer%250==0  :
			spawnEnnemy(gameState)		
		supprimerballe()
		supprimerennemmy(gameState)
		#Balle.balleX += Balle.balleSpeed    
		gameState.advanceState(nextMove)
		#nextMove=getIA(gameState)
		horloge.tick(100)
		timer+=1
		print(timer)
		gameState.drawbackground(window,GameConfig.blue)
		gameState.draw(window)
		printennemy(window, gameState)
		printballe(window, gameState)
		displayMessage(window,"Vies restantes : "+str(gameState.life),20,GameConfig.windowW/2,GameConfig.windowH-20)
		displayMessage(window,"Niveau : "+str(GameConfig.level)+"  /  Difficulté : "+str(GameConfig.difficulty),14,100,10)
		#displayMessage(window,"Score : "+str(gameState.score),16,30,10)

		'''if gameState.isOver()==True :
			displayMessage(window,"You lose!",30,GameConfig.windowW/2,GameConfig.windowH/2-50)
			displayMessage(window,"Appuyer sur espace pour recommencer",20,GameConfig.windowW/2,GameConfig.windowH/2+50)'''
		
		pygame.display.update()
	'''if(playAgain()) :
		gameLoop(window,horloge)
		displayMessage(window,"Appuyer sur une touche pour continuer",20,GameConfig.windowW/2,GameConfig.windowH/2+50)
		pygame.quit()
		quit()'''
		
def end_game(window,horloge) :
	continuer = False
	gameState=GameState()
	while not continuer :
		horloge.tick(100)
		gameState.drawbackground(window,GameConfig.blue)
		if GameConfig.game_win == True :
			displayMessage(window,"Bravo vous avez gagné !",35,GameConfig.windowW/2,50)
		else : 
			displayMessage(window,"Dommage vous avez perdu !",35,GameConfig.windowW/2,50)
		displayMessage(window,"Appuyez sur une touche pour recommencer",30,GameConfig.windowW/2,140)
		displayMessage(window,"Statistiques :",30,GameConfig.windowW/2,240)
		displayMessage(window,"Temps : "+str(GameConfig.temps),22,GameConfig.windowW/2,300)
		displayMessage(window,"Balles tirées : "+str(GameConfig.ballestirées),22,GameConfig.windowW/2,340)
		displayMessage(window,"Ennemis tués : "+str(GameConfig.ennemistués),22,GameConfig.windowW/2,380)
		displayMessage(window,"Score : "+str(GameConfig.score),22,GameConfig.windowW/2,420)
		pygame.display.update()
		time.sleep(3)
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				continuer = True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
				pygame.quit()
				quit()
			'''if event.type == pygame.KEYDOWN :
				settings_game(window,horloge)'''
		
		
			
#______________________________________________________________________________
#                                  MAIN
#______________________________________________________________________________
	
def main() :
	window = pygame.display.set_mode((GameConfig.windowW,GameConfig.windowH))
	pygame.display.set_caption("ShootMania")

	horloge = pygame.time.Clock()
	settings_game(window, horloge)
	gameLoop(window, horloge)
	end_game(window,horloge)
	#displayMessage(window,"Appuyer sur une touche pour continuer",20,GameConfig.windowW/2,GameConfig.windowH/2+50)
	pygame.quit()
	quit()

main()

#______________________________________________________________________________
#                                  BONUS
#______________________________________________________________________________
	
'''def choisir_difficulte() :
		for event in pygame.event.get() :
			if GameConfig.position==2 :
				if GameConfig.difficulty>1 and event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT :
					GameConfig.difficulty-=1
				if GameConfig.difficulty<3 and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT :
					GameConfig.difficulty +=1
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
						GameConfig.position=1'''

'''def choisir_niveau() :
	for event in pygame.event.get() :
		if GameConfig.position==1 :
			if GameConfig.level>1 and event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT :
				GameConfig.level-=1
			if GameConfig.level<5 and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT :
				GameConfig.level +=1
		if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN :
				GameConfig.position=2'''