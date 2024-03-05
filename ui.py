import pygame 
from settings import *

class UI:

	def __init__(self):
		
		# general

		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

		# bar setup 
		self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

		# convert weapon dict 
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)

		# convert item dict 
		self.item_graphics = []
		for item in item_data.values():
			path = item['graphic']
			item = pygame.image.load(path).convert_alpha()
			self.item_graphics.append(item)

	def show_bar (self, current, max_amount, bg_rect, color):

		# draw bg
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

		# converting stat to pixel 
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		#drawing the bar
		pygame.draw.rect(self.display_surface, color, current_rect)
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect,2)
		return bg_rect

	def show_exp(self,exp):
		text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)

		x = self.display_surface.get_size()[0] + -10
		y = self.display_surface.get_size()[1] + -20

		text_rect = text_surf.get_rect(bottomright = (x,y))
		
		#text_inflate = (0,20)
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(6,4))
		#pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,text_rect.inflate(6,2),2)
		self.display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,text_rect.inflate(6,4),2)
		
	def selection_box(self, left, top, has_switched):

		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

		if has_switched:
			pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect,2)
		else:
			pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect,2)
		
		return bg_rect
	
	def weapon_overlay(self, weapon_index, has_switched):

		bg_rect = self.selection_box(self.display_surface.get_size()[0] - 420,self.display_surface.get_size()[1] + -40, has_switched) # attack
		weapon_surf = self.weapon_graphics [weapon_index]
		weapon_rect = weapon_surf.get_rect (center = bg_rect.center)


		self.display_surface.blit(weapon_surf,weapon_rect)
	
	def item_overlay(self, item_index, has_switched):

		bg_rect = self.selection_box(self.display_surface.get_size()[0] - 395,self.display_surface.get_size()[1] + -30, has_switched) # attack
		item_surf = self.item_graphics [item_index]
		item_rect = item_surf.get_rect (center = bg_rect.center)


		self.display_surface.blit(item_surf,item_rect)

	
	def display(self, player):

		self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

		self.show_exp(player.exp)
		self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
		self.item_overlay(player.item_index, not player.can_switch_item)
		#self.lives_overlay(player.lives)
		#self.selection_box(self.display_surface.get_size()[0] - 395,self.display_surface.get_size()[1] + -30, ) # item