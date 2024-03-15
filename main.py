import pygame, sys
from settings import *
from pygame.locals import *
from debug import debug
from level import Level
#import math
# controls 
# Arrow keys or wsad = move
# spacebar = shoot
# "e" changes shot
# left cntrl uses item (items currently have no effect but can be used)
# "r" changes item
# "k" pauses game 
# "f" to fullscreen
# 'j' toggles scrolling on lvl 
# 'l' increments lvl 
# '7' Toggles "debug" boxes on rects and hitboxes for enemy, shots, and player 
# You can change between "lvl 0" and "lvl 1" by changgin level_counter in level.py to 0 or 1 
# currently 8 direction, you can change to forward and back oor just straight through weapon.py move() 
#test

class Game:                       
	def __init__(self):                         

		#General Setup
		pygame.init()
		pygame.display.set_caption('Bullets and Flying')
		self.flags = pygame.SCALED
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),self.flags)
		self.clock = pygame.time.Clock()
		self.level = Level()
		        
                            
	def run(self):
		while True:  
			for event in pygame.event.get():

				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				 
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_k:
						self.level.toggle_menu()

					if event.key == pygame.K_j:
						self.level.scroll_toggle()

					if event.key == pygame.K_l:
						self.level.lvl_change_quick()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
					pygame.display.toggle_fullscreen()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
					self.level.toggle_debug()


			self.screen.fill('black')                 
			self.level.run() 
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()

