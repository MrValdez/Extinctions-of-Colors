# special thanks to Enzo
# http://inventwithpython.com/extra/gorilla.py

import pygame
import sys
import math
import random
import os
import copy

from win32api import GetSystemMetrics
resolution_width = GetSystemMetrics (0)
resolution_height = GetSystemMetrics (1)

pygame.init()
pygame.font.init()
fontpath = pygame.font.get_default_font()
BigText = pygame.font.Font(fontpath, 52)
NormalText = pygame.font.Font(fontpath, 17)

#screen_size = [800, 600]
screen_size = [1024, 600]


soundBoom = pygame.mixer.Sound('boom.wav')
soundShot1 = pygame.mixer.Sound('shot1.wav')
soundShot2 = pygame.mixer.Sound('shot2.wav')
soundDead = pygame.mixer.Sound('dead.wav')
soundHit = pygame.mixer.Sound('hit.wav')
soundDrain = pygame.mixer.Sound('drain.wav')

os.environ['SDL_VIDEO_WINDOW_POS'] = "%i,%i" % ((resolution_width / 2) - (screen_size[0] / 2), ((resolution_height / 2) - (screen_size[1] / 2)))

try:
	pygame.joystick.init()
	pygame.joystick.get_init()
	joystick1=pygame.joystick.Joystick(0)
	joystick1.init()
except:
	joystick1 = None

try:
	joystick2=pygame.joystick.Joystick(1)
#	joystick2=pygame.joystick.Joystick(0)
	joystick2.init()
except:
	joystick2 = None

#screen_size = [800, 600]
screen_size = [1024, 600]

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption ("Extinction of Colors")

def isleft(stickNumber):
	if stickNumber > 1:
		return False

	joystick = [joystick1, joystick2][stickNumber]
	if joystick:
		if joystick.get_axis(0) < -0.2:
			return True
		hatposition=joystick.get_hat(0)
		if hatposition[0]==-1:
			return True
	return False

def isright(stickNumber):
	if stickNumber > 1:
		return False

	joystick = [joystick1, joystick2][stickNumber]
	if joystick:
		if joystick.get_axis(0) > 0.2:
			return True
		hatposition=joystick.get_hat(0)
		if hatposition[0]==1:
			return True
	return False

def isup (stickNumber):
	if stickNumber > 1:
		return False

	joystick = [joystick1, joystick2][stickNumber]
	if joystick:
		if joystick.get_axis(1) < -0.2:
			return True
		hatposition=joystick.get_hat(0)
		if hatposition[1]==1:
			return True
	return False

def isdown (stickNumber):
	if stickNumber > 1:
		return False

	joystick = [joystick1, joystick2][stickNumber]
	if joystick:
		if joystick.get_axis(1) > 0.2:
			return True
		hatposition=joystick.get_hat(0)
		if hatposition[1]==-1:
			return True
	return False


def isButton(stickNumber, buttonNumber):
	if stickNumber > 1:
		return False

	try:
		joystick = [joystick1, joystick2][stickNumber]
		if joystick:
			return joystick.get_button(buttonNumber)
	except:
		return False
	return False

TREE_ASCII = """
 xxx
xxxxx
xxxxx
 xxx
  x
  x
  x
  x
  x
 xxx
"""

TREE2_ASCII = """
 x
xxx
xxx  xx
 x  xx
  x  xx
  x x
  xx
  xx
  x
 xxx
"""

VOLCANO_ASCII = """
       x
      xxx
     xxxxx
    xxxxxxx
   xxxxxxxxx
  xxxxxxxxxxx
 xxxxxxxxxxxxx
xxxxxxxxxxxxxxx
"""

ROCK_ASCII = """
 x
xxx
 x
"""

FISH_ASCII = """
xxxxx  x
xx xx xx
xxxxxxxx
xxxxxxxx
 xxxx xx
xxxxx  x
"""

INVERSE_PYRAMID_ASCII = """
xxxxx
 xxx
  x
"""

EnvironmentList = [[TREE_ASCII, [28,109,110], [129, 210, 120]],
				   [TREE2_ASCII, [18,109,119], [129, 210, 120]],
				   [VOLCANO_ASCII, [128,0,0], [249, 120, 120]],
				   [ROCK_ASCII, [120,219,129], [254, 254, 254]],
				   [FISH_ASCII, [40, 50, 200], [90, 100, 255]],
				   [INVERSE_PYRAMID_ASCII, [120, 250, 200], [190, 255, 255]]]

class EnvironmentObject:
	def __init__(self, pos):
		ASCII = random.choice(EnvironmentList)
		red = random.randrange(ASCII[1][0], ASCII[2][0])
		green = random.randrange(ASCII[1][1], ASCII[2][1])
		blue = random.randrange(ASCII[1][2], ASCII[2][2])
		Color = [red, green, blue]

		self.sprite = createSurfaceFromASCII(ASCII[0], ASCII[1])
		self.sprite = self.sprite.convert_alpha()
		self.rect = pygame.Rect(pos, self.sprite.get_size())
		self.direction = +1
		self.sprite = pygame.transform.scale(self.sprite, [20 * int(random.random() + 1.5), 20 * int(random.random() + 1.0)])
		self.size = max(self.sprite.get_size()) + 4
		self.dirtyColor = None
		self.hasColors = True

	def getColor(self):
		Colors = [0, 0, 0]
		surface = pygame.PixelArray(self.sprite)
		for row in surface:
			for pixel in row:
				pixelColor = self.sprite.unmap_rgb(pixel)
				Colors[0] += pixelColor.r
				Colors[1] += pixelColor.g
				Colors[2] += pixelColor.b

		return Colors

	def drainColor(self, colorDamage, power):
		if self.hasColors == False:
			return

		originalColor = self.getColor()

		r, g, b = 0, 0, 0
		if colorDamage.r:
			r = power
		if colorDamage.g:
			g = power
		if colorDamage.b:
			b = power

		self.sprite.fill(pygame.Color(r, g, b), special_flags = pygame.BLEND_RGB_SUB)

		newColor = self.getColor()

		self.dirtyColor = [originalColor[0] - newColor[0], originalColor[1] - newColor[1], originalColor[2] - newColor[2]]

		if newColor[0] == 0 and \
		   newColor[1] == 0 and \
		   newColor[2] == 0:
			self.hasColors = False

	def update(self):
		return
		self.rect.x += self.direction
		if (self.rect.x > 600):
			self.direction = -1
		if (self.rect.x < 0):
			self.direction = +1

	def draw(self):
		screen.blit(self.sprite, self.rect)

HERO_ASCII = """
 xxx
 xxx
 xxx
 xxx
  x
xxxxx
  x
  x
  x
 xxx
 x x
 x x
"""

def createSurfaceFromASCII(ASCII, Color):
	ASCII = ASCII.split('\n')
	width = max([len(x) for x in ASCII])
	height = len(ASCII)
	surface = pygame.Surface([width, height])
	colorkey = surface.get_at((0,0))
	surface.set_colorkey(colorkey, pygame.RLEACCEL)

	surfaceArray = pygame.PixelArray(surface)
	for y in range(height):
		for x in range(len(ASCII[y])):
			if ASCII[y][x] == 'x':
				surfaceArray[x][y] = Color

	return surface

class Bullet:
	def __init__(self, playerOwner, pos, dir, power, speed, size = 1):
		#self.sprite = pygame.image.load('alien1.png')
		size = [5 * size, 5 * size]
		self.sprite = pygame.Surface(size)
		self.sprite.fill([255, 255, 255])

		self.rect = pygame.Rect(pos, size)
		self.rect.x += size[0] / 2
		self.rect.y -= size[1] / 2
		self.dir = dir
		self.power = power
		self.speed = speed
		self.playerOwner = playerOwner
		self.Damage = 1

	def update(self):
		self.rect.x += self.dir[0] * self.speed
		self.rect.y += self.dir[1] * self.speed

	def draw(self):
		screen.blit(self.sprite, self.rect)

class Bomb:
	def __init__(self, playerOwner, pos):
		self.pos = pos
		self.timer = 30
		self.playerOwner = playerOwner
		self.Anim = True
		self.rect = pygame.Rect(pos, [10, 10])

	def update(self, delta):
		self.timer -= delta

		if self.timer < 0:
			return False

		return True

	def draw(self):
		size = self.playerOwner.sprite.get_width()
		width = size
		self.width = size
		if self.timer < 1000 and self.timer > 500:
			size = size * 3

		pos = self.pos

		up = pos[1] + (width / 2) + (size / 2)
		down = pos[1] + (width / 2)  - (size / 2)
		right = pos[0] + (width / 2) + (size / 2)
		left = pos[0] + (width / 2) - (size /2)

		pygame.draw.line(screen, [255, 255, 255], [left, up], [right, down])
		pygame.draw.line(screen, [255, 255, 255], [left, down], [right, up])
		pygame.draw.line(screen, [255, 255, 255], [left, up], [right, up])
		pygame.draw.line(screen, [255, 255, 255], [left, down], [right, down])

		self.rect = pygame.Rect(pos, [size, size])

class Explosion:
	def __init__(self, pos, size):
		self.pos = pos
		self.size = size
		self.timer = 100

	def update(self, delta):
		self.timer -= delta

	def draw(self):
		pos = self.pos
		size = self.size
		width = size

		up = pos[1] + (width / 2) + (size / 2)
		down = pos[1] + (width / 2)  - (size / 2)
		right = pos[0] + (width / 2) + (size / 2)
		left = pos[0] + (width / 2) - (size /2)

		pygame.draw.line(screen, [255, 255, 255], [left, up], [right, down])
		pygame.draw.line(screen, [255, 255, 255], [left, down], [right, up])
		pygame.draw.line(screen, [255, 255, 255], [left, pos[1] + (width / 2)], [right, pos[1] + (width / 2)])
		pygame.draw.line(screen, [255, 255, 255], [pos[0] + (width / 2), down], [pos[0] + (width / 2), up])

		self.rect = pygame.Rect(pos, [size, size])

BulletList = []
BombList = []
ExplosionList = []

class Player:
	def __init__(self, pos = [0,0], color = pygame.Color(255,0,0)):
		self.playerName = "Wizard"
		self.color = color

		self.original = createSurfaceFromASCII(HERO_ASCII, color)
		self.checkSize(pos)

		self.control = None
		self.drainColor = pygame.Color(255 - color.r, 255 - color.g, 255 - color.b)

		self.HP = 100
		self.MaxHP = 100
		self.Power = 1
		self.drainPower = 3
		self.cooldown = 100
		self.maxCooldown = 200
		self.cooldownRecovery = 1
		self.speed = 1
		self.charge = 0.0
		self.lookDirection = [1, 1]

		self.keyDown = False

	def update(self, keystate, EnvironmentObjectList):
		if self.control == "keyboard":
			self.checkKeyboardInput()
		if self.control == "joystick1":
			self.checkStickInput(0)
		if self.control == "joystick2":
			self.checkStickInput(1)

		if self.cooldown < 0:
			self.cooldown = 0
		self.cooldown += self.cooldownRecovery
		if self.cooldown > self.maxCooldown:
			self.cooldown = self.maxCooldown

	def checkSize(self, pos):
		#self.sprite = pygame.transform.scale(self.original, [15,20])
		#self.rect = pygame.Rect(pos, self.sprite.get_size())

		global TotalColor, MaxColor

		scale = 0
		if self.color.r > 0:
			if TotalColor[0] > 0:
				scale = TotalColor[0] / float(MaxColor[0])
		if self.color.g > 0:
			if TotalColor[1] > 0:
				scale = TotalColor[1] / float(MaxColor[1])
		if self.color.b > 0:
			if TotalColor[2] > 0:
				scale = TotalColor[2] / float(MaxColor[2])

		if self.playerName == "Green Wizard":
			self.speed = scale * 3

		scale = 1 - scale

		size = [int(125 * scale), int(120 * scale)]

		if size[0] < 15:
			size[0] = 15
		if size[1] < 20:
			size[1] = 20

		self.sprite = pygame.transform.scale(self.original, size)
		self.rect = pygame.Rect(pos, self.sprite.get_size())
		self.rect.width = self.sprite.get_width()
		self.rect.height = self.sprite.get_height()

		#self.circleSize = self.rect.width + 20
		self.circleSize = 50

	def checkKeyboardInput(self):
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_SPACE]:
			self.moveDrain()
		if keystate[pygame.K_TAB]:
			if self.keyDown == False:
				self.fireBomb()
			self.keyDown = True
		else:
			self.keyDown = False

		if keystate[pygame.K_LEFT]:
			self.movePos([-1, 0])
		if keystate[pygame.K_RIGHT]:
			self.movePos([+1, 0])
		if keystate[pygame.K_UP]:
			self.movePos([ 0,-1])
		if keystate[pygame.K_DOWN]:
			self.movePos([ 0,+1])

	def checkStickInput(self, stickNumber):
		self.checkFire(stickNumber)
		if isleft(stickNumber):
			self.movePos([-1, 0])
		if isright(stickNumber):
			self.movePos([+1, 0])
		if isup(stickNumber):
			self.movePos([ 0,-1])
		if isdown(stickNumber):
			self.movePos([ 0,+1])

		if isdown(stickNumber) and isleft(stickNumber):
			self.lookDirection = [-1, 1]
		elif isdown(stickNumber) and isright(stickNumber):
			self.lookDirection = [1, 1]
		elif isup(stickNumber) and isleft(stickNumber):
			self.lookDirection = [-1, -1]
		elif isup(stickNumber) and isright(stickNumber):
			self.lookDirection = [1, -1]
		elif isdown(stickNumber):
			self.lookDirection = [0, 1]
		elif isleft(stickNumber):
			self.lookDirection = [-1, 0]
		elif isright(stickNumber):
			self.lookDirection = [1, 0]
		elif isup(stickNumber):
			self.lookDirection = [0, -1]


		joystick = [joystick1, joystick2][stickNumber]
		if joystick and joystick.get_numaxes() > 4:
			if  joystick1.get_axis(3) < -0.3 or \
				joystick1.get_axis(3) > 0.3 or	\
				joystick1.get_axis(4) > 0.3 or	\
				joystick1.get_axis(4) < -0.3:
				firingDir = [joystick1.get_axis(4), joystick1.get_axis(3)]
				self.FireAtDir(firingDir)

			if isButton(stickNumber, 5):
				self.moveDrain()
		else:
			if isButton(stickNumber, 1):
				self.moveDrain()


	def movePos(self, pos):
		if self.charge > 0:
			return

		self.rect.x += pos[0] * self.speed
		self.rect.y += pos[1] * self.speed

		if self.rect.x < 0:
			self.rect.x = 0
		if self.rect.y < 0:
			self.rect.y = 0
		if self.rect.x > screen_size[0] - self.rect.width:
			self.rect.x = screen_size[0] - self.rect.width
		if self.rect.y > screen_size[1] - self.rect.height:
			self.rect.y = screen_size[1] - self.rect.height

	def checkFire(self, stickNumber):
		if self.control != "joystick2":
			return
		if isButton(stickNumber, 0):
			if self.charge == 0:
				self.charge = 2

			self.charge += 0.1
			if self.charge > self.cooldown:
				self.charge = self.cooldown

		if isButton(stickNumber, 0) == False and \
			self.charge > 0:

			dir = self.lookDirection
			size = int(self.charge * 0.5)
			if size > 20:
				size = 20
			bullet = Bullet(self, [self.rect.x, self.rect.y], dir, 50, 6, size = size)
			bullet.Damage = int((self.Power * (self.charge / 10.0)) + 1)
			BulletList.append(bullet)
			soundShot1.play()

			self.cooldown -= self.charge * 25
			self.charge = 0.0

	def FireAtDir(self, dir):
		if self.cooldown <= 20:
			return

		self.cooldown -= 20
		bullet = Bullet(self, [self.rect.x, self.rect.y], dir, 50, 6)
		bullet.Damage = int((self.Power * 5.0) + 1)
		BulletList.append(bullet)
		soundShot2.play()

	def fireBomb(self):
		if self.cooldown < 20:
			return
		self.cooldown -= 20

		bomb = Bomb(self, [self.rect.x, self.rect.y])
		BombList.append(bomb)

	def moveDrain(self):
		self.cooldown -= 2

		if self.cooldown <= 0:
			return

		circlePos = [self.rect.x, self.rect.y]
		circlePos[0] += self.rect.width / 2
		circlePos[1] += self.rect.height / 2
		pygame.draw.circle(screen, self.drainColor, circlePos, self.circleSize, 10)
		soundDrain.play()

		for EnvironmentObject in EnvironmentObjectList:
			distance = self.inRange(EnvironmentObject)
			if abs(distance) < EnvironmentObject.size + self.circleSize:
				EnvironmentObject.drainColor(self.drainColor, self.drainPower)

	def inRange(self, target):
		try:
			targetCenter = [target.rect.x + (target.rect.width / 2), target.rect.y + (target.rect.height / 2)]
			selfCenter = [self.rect.x + (self.rect.width / 2), self.rect.y + (self.rect.height / 2)]
			distance = math.sqrt(math.pow(selfCenter[0] - targetCenter[0], 2) + math.pow(selfCenter[1] - targetCenter[1], 2))
		except:
			return 0

		return distance

	def draw(self):
		screen.blit(self.sprite, self.rect)

		if self.charge > 0:
			target_pos = [(self.rect.x + (self.rect.width / 2)) + (self.lookDirection[0] * 10),
						  (self.rect.y + (self.rect.height / 2)) + (self.lookDirection[1] * 10)]
			pygame.draw.circle(screen, self.drainColor, target_pos, 2)


def GenerateEnvironment():
	TotalColor = [0,0,0]
	EnvironmentObjectList = []
	for x in range(random.randrange(15, 30)):
#	for x in range(2):
		pos = [random.randrange(0, screen_size[0] - 50),random.randrange(0, screen_size[1] - 100)]
		obj = EnvironmentObject(pos)

		objColors = obj.getColor()
		TotalColor[0] += objColors[0]
		TotalColor[1] += objColors[1]
		TotalColor[2] += objColors[2]

		EnvironmentObjectList.append(obj)
	return EnvironmentObjectList, TotalColor

EnvironmentObjectList, TotalColor = GenerateEnvironment()
MaxColor = copy.copy(TotalColor)

startingPointOffset = 70

playerList = []

redPlayer = Player([startingPointOffset, startingPointOffset], pygame.Color(255, 0, 0))
greenPlayer = Player([(screen_size[0] - 150) / 2, screen_size[1] - startingPointOffset - 150], pygame.Color(0, 255, 0))
bluePlayer = Player([screen_size[0] - startingPointOffset - 150, startingPointOffset], pygame.Color(0, 0, 255))

redPlayer.playerName = "Red Wizard"
greenPlayer.playerName = "Green Wizard"
bluePlayer.playerName = "Blue Wizard"

greenPlayer.control = "keyboard"
bluePlayer.control = "joystick1"
redPlayer.control = "joystick2"

redPlayer.speed = 2
greenPlayer.speed = 2
bluePlayer.speed = 2

playerList.append(redPlayer)
playerList.append(greenPlayer)
playerList.append(bluePlayer)

Clock = pygame.time.Clock()

tmpHUD = pygame.Surface([200, 200])

def drawInfo(player, GUIPos):
	if player.HP <= 0:
		return

	HUD = tmpHUD
	HUDWidth = HUD.get_width()

	#name
	HUD.fill([0, 0, 0])
	text = NormalText.render(player.playerName, True, [255, 255, 255])
	pos = [0, 0]
	HUD.blit(text, pos)
	colorkey = [0,0,0]
	HUD.set_colorkey(colorkey, pygame.RLEACCEL)

	#HP
	LifeBar = pygame.Rect([0,text.get_height() + 5],[(player.HP / float(player.MaxHP)) * HUDWidth, 10])
	Pos = LifeBar
	LifeColor = player.color
	pygame.draw.rect(HUD, LifeColor, LifeBar)

	#Cooldown
	Cooldown = pygame.Rect([0,LifeBar.height + 5],[(player.cooldown / float(player.maxCooldown)) * HUDWidth, 10])
	Cooldown.y += Pos[1]

	LifeColor = player.color
	pygame.draw.rect(HUD, LifeColor, Cooldown)

	#blit
	if GUIPos[0] + HUDWidth > screen_size[0]:
		GUIPos[0] -= HUDWidth + 20
	screen.blit(HUD, GUIPos)

def drawGUI():
	global playerList, redPlayer, greenPlayer, bluePlayer

	drawInfo(redPlayer, 	[10, 10])
	drawInfo(bluePlayer, 	[screen_size[0] - 10, 10])
	drawInfo(greenPlayer, 	[(screen_size[0] - 150) / 2, screen_size[1] - 100])


while True:
	screen.fill ([0, 0, 0])
	Clock.tick(60)

	eventList = pygame.event.get()
	keystate = None

	for event in eventList:
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			keystate = pygame.key.get_pressed()

	RecheckSize = False
	for EnvironmentObject in EnvironmentObjectList:
		EnvironmentObject.update()
		EnvironmentObject.draw()

		if EnvironmentObject.dirtyColor:
			TotalColor[0] -= EnvironmentObject.dirtyColor[0]
			TotalColor[1] -= EnvironmentObject.dirtyColor[1]
			TotalColor[2] -= EnvironmentObject.dirtyColor[2]
			EnvironmentObject.dirtyColor = None
			RecheckSize = True

	if RecheckSize:
		for player in playerList:
			if player.HP <= 0:
				continue

			#check size and power
			player.checkSize([player.rect.x, player.rect.y])

	for bullet in BulletList:
		bullet.update()
		bullet.draw()

		if bullet.rect.x <= 0 or \
		   bullet.rect.x >= screen_size[0] or \
		   bullet.rect.y <= 0 or \
		   bullet.rect.y >= screen_size[1]:
			BulletList.remove(bullet)

	for bomb in BombList:
		bomb.update(1)
		bomb.draw()

		if bomb.timer <= 0:
			for player in playerList:
				if bomb.playerOwner != player and \
				   bomb.rect.colliderect(player.rect):
					player.HP -= bomb.playerOwner.circleSize * 0.4
			ExplosionList.append(Explosion(bomb.pos, bomb.rect.width))
			BombList.remove(bomb)


	for boom in ExplosionList:
		boom.update(1)
		boom.draw()

		if boom.timer <= 0:
			soundBoom.play()
			ExplosionList.remove(boom)

	for player in playerList:
		if player.HP <= 0:
			continue

		for bullet in BulletList:
			if bullet.playerOwner != player and \
			   bullet.rect.colliderect(player.rect):
				soundHit.play()
				player.HP -= bullet.Damage
				BulletList.remove(bullet)

				if player.HP < 0:
					soundDead.play()

	for player in playerList:
		if player.HP > 0:
			player.update(keystate, EnvironmentObjectList)
			player.draw()

	drawGUI()
	pygame.display.update()
