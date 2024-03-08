import pygame
from settings import *
from support import *
from tile import Tile
from player import Player  
from debug import debug
from weapon import Weapon
from enemy_weapon import Enemy_Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer

class Level:   
	def __init__(self):

		#Debug Switch 
		self.debug = False 

		# timer for player
		self.player_check_timer = 60
		
		# get surface
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False
		self.lvl_counter_list = ['0', '1', 'test']
		self.lvl_counter = 0
		self.lvl = self.lvl_counter_list[self.lvl_counter]

		# sprite group setup
		self.visible_sprites = pygame.sprite.Group()
		self.obstacle_sprites = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()
		self.layer_001_shadow = pygame.sprite.Group()
		self.layer_001_sprites = pygame.sprite.Group()
		self.layer_000_sprites = pygame.sprite.Group()
		self.hazards_sprites = pygame.sprite.Group()
		self.lvl_end_sprites = pygame.sprite.Group()
		self.player_sprites = pygame.sprite.Group()
		self.weapon_sprites = pygame.sprite.Group()
		self.entity_sprites = pygame.sprite.Group()
		self.enemy_attack_sprites = pygame.sprite.Group()

		self.sg_list = [
						self.layer_001_shadow,
						self.layer_001_sprites,
						self.hazards_sprites,
						self.layer_000_sprites,
						self.lvl_end_sprites,
						self.enemy_sprites, 
						self.enemy_attack_sprites,
						self.player_sprites, 
						self.weapon_sprites
						]
		
		

		# setting up scrolling
		self.current_scroll_bg = 0
		self.current_scroll_mid = 0
		self.current_scroll_ground = 0 
		self.scroll_speed = 0.5
		self.scrolling = True

		# load bg image and give it a rect
		#self.menu_rect = self.menu_rect
		self.floor_surf = pygame.image.load('graphics/bg/bg6.png').convert()
		self.floor_rect = self.floor_surf.get_rect()
		self.floor_hitbox = pygame.FRect(self.floor_rect)

		self.keys = pygame.key.get_pressed()
		self.black_box = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
		self.black_box.fill('black')
		self.black_box.set_alpha(100)
		self.black_box_rect = self.black_box.get_rect()

		self.create_map()

		# user interface
		self.ui = UI()

		# sounds
		'''self.music = pygame.mixer.music.load('sounds/levelmusic.mp3')
		self.music.play()'''
		#pygame.mixer.music.load('audio/music/mission_000.mp3')
		#pygame.mixer.music.play()

		self.animation_player = AnimationPlayer()
	
	def create_player(self):
		self.player = Player((SCREEN_WIDTH/10,SCREEN_HEIGHT/2), 
		[self.player_sprites, self.entity_sprites], 
		self.obstacle_sprites,
		self.hazards_sprites,
		self.enemy_sprites, 
		self.enemy_attack_sprites,
		self.create_attack,
		self.activate_item,
		self.trigger_death_particles
		) 
								
	def create_menu(self):
		self.display_surface.fill()
		pygame.draw.rect(self.display_surface,'grey',(200,200))

	def create_map(self):

		
		
		#create lvl counter
		
		layouts = {
			'layer_000': import_csv_layout (f'level_data/{self.lvl}/lvl_000.csv'),
			'layer_000_hazards': import_csv_layout (f'level_data/{self.lvl}/lvl_000_hazards.csv'),
			'layer_001': import_csv_layout (f'level_data/{self.lvl}/lvl_001.csv'),
			'lvl_end': import_csv_layout (f'level_data/{self.lvl}/lvl_end.csv'),
			'player' : import_csv_layout (f'level_data/{self.lvl}/lvl_player.csv'),
			'enemies' : import_csv_layout (f'level_data/{self.lvl}/lvl_enemies.csv'),
			#'items' : import_csv_layout (f'level_data/{self.lvl_counter}/lvl_items.csv'),
		}
		graphics = {
			'layer_000': import_folder('graphics/level/lvl_001_layer_001'),
			#'layer_002': import_folder('graphics/level/lvl_001_layer_002'),
			#'decor': import_folder('graphics/level/decor/lantern'),
		}
		
		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != "-1":
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						
						if style == 'layer_000':
							surf = graphics['layer_000'][int(col)]
							Tile((x,y),[self.visible_sprites, self.obstacle_sprites, self.layer_000_sprites],'layer_000',surf)

						if style == 'layer_000_hazards':
							surf = graphics['layer_000'][int(col)]
							Tile((x,y),[self.visible_sprites, self.hazards_sprites, self.layer_000_sprites],'layer_000_hazards',surf)

						if style == 'layer_001':
							surf = graphics['layer_000'][int(col)]
							Tile((x,y),[self.visible_sprites, self.layer_001_sprites],'layer_001',surf)

						if style == 'lvl_end':
							surf = graphics['layer_000'][int(col)]
							Tile((x,y),[self.visible_sprites, self.lvl_end_sprites],'lvl_end',surf)

						if style == 'player':
							if col == '18':
								self.player = Player(
								(x,y), 
								[self.player_sprites, self.entity_sprites], 
								self.obstacle_sprites,
								self.hazards_sprites,
								self.enemy_sprites, 
								self.enemy_attack_sprites,
								self.create_attack,
								self.activate_item,
								self.trigger_death_particles
								)
						if style == 'enemies': 
							if col == '19' : monster_name = 'screaming skull'
							elif col == '20': monster_name = 'remote'
							elif col == '21' : monster_name = 'guard_fish'

							Enemy(monster_name, 
		  							(x,y),
									[self.visible_sprites, self.enemy_sprites, self.entity_sprites],
									self.obstacle_sprites, 
									self.trigger_death_particles,
									self.add_exp,
									self.create_attack_enemy,
									self.player,
									self.enemy_attack_sprites
									)
								
						
								
						'''if style == 'layer_lvl_end':
							surf = graphics['layer_000'][int(col)]
							Tile((x,y),[self.lvl_end_sprites],'lvl_end',surf)
										'''
		

			'''for tile in self.layer_001_sprites:
				
				tile_shadow_img = pygame.Surface((tile.image.get_width(), tile.image.get_height())).convert_alpha()
				tile_shadow_img.fill((50, 0, 50, 50))
				tile_shadow_pos = (tile.hitbox.x - 20, tile.hitbox.y + 20)
				shadow_tile = Tile(tile_shadow_pos,self.layer_001_shadow, 'shadow', tile_shadow_img)'''
			
			for tile in self.layer_001_sprites:
				# Create a copy of the tile's image to use as the shadow mask
				shadow_mask = tile.image.copy().convert_alpha()
				#pygame.transform.gaussian_blur(shadow_mask,10)
				#pygame.transform.invert(shadow_mask)
				
				# Fill the mask with a solid color (e.g. black) to make it a silhouette
				#shadow_mask.fill((0, 0, 0, 255))

				# Create a new surface for the shadow
				shadow_surface = pygame.Surface(tile.hitbox.size, pygame.SRCALPHA)

				# Offset the shadow position to make it appear below and to the right of the tile
				shadow_pos = (tile.hitbox.x - 60, tile.hitbox.y + 20)

				# Fill the shadow surface with a semi-transparent color
				shadow_surface.fill((0, 0, 30, 10))
				pygame.transform.gaussian_blur(shadow_mask,2)

				# Use the silhouette as a mask for the shadow surface
				shadow_surface.blit(shadow_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

				# Create a new tile object for the shadow
				shadow_tile = Tile(shadow_pos, self.layer_001_shadow, 'shadow', shadow_surface)


			# create cast shadow for level 000 				
		'''for tile in self.layer_000_sprites:
				
				tile_shadow_img = pygame.Surface((tile.image.get_width(), tile.image.get_height())).convert_alpha()
				tile_shadow_img.fill((0, 0, 0, 50))
				tile_shadow_pos = (tile.hitbox.x - 40, tile.hitbox.y + 40)
				shadow_tile = Tile(tile_shadow_pos,self.layer_000_shadow, 'shadow', tile_shadow_img)'''
				

		
		self.level_layer_group = [self.layer_000_sprites, self.layer_001_sprites]
		
	def create_attack(self):
		Weapon(self.player, [self.weapon_sprites],  self.obstacle_sprites, self.enemy_sprites)

	def create_attack_enemy(self, enemy, player, groups, obstacle_sprites):
		Enemy_Weapon(enemy, player, groups, obstacle_sprites)
		#print (len(self.enemy_attack_sprites))

	def activate_item (self, item, strength, units):
		print (item)
		print (strength)
		print (units)
	
	def add_exp(self,amount):
		self.player.exp += amount

	def toggle_menu(self):
		self.game_paused = not self.game_paused 
	
	def toggle_debug(self):
		self.debug = not self.debug 
	
	def trigger_death_particles(self,pos,particle_type):
		self.animation_player.create_particles(particle_type,pos,self.weapon_sprites)

	def lvl_change_quick (self):
			self.lvl_counter += 1
			if self.lvl_counter >= len(self.lvl_counter_list):
				self.lvl_counter = 0
			self.lvl = self.lvl_counter_list[self.lvl_counter]

			for group in self.sg_list:
				for sprite in group:
					sprite.kill()
					group.empty()
		
			self.display_surface.fill('white') 
			self.create_map()
	
	def level_end_check(self):

		for sprite in self.lvl_end_sprites:
			if sprite.hitbox.colliderect(self.player.hitbox):
				self.lvl_counter += 1
				if self.lvl_counter >= len(self.lvl_counter_list):
					self.lvl_counter = 0
				self.lvl = self.lvl_counter_list[self.lvl_counter]

				for group in self.sg_list:
					for sprite in group:
						sprite.kill()
					group.empty()
				
				self.display_surface.fill('white') 
				self.create_map()	
	
	def scroll_toggle(self):
		self.scrolling = not self.scrolling 

	def run(self):
		
		self.player_check_timer -= 1
		if self.player_check_timer <=0:
				if len(self.player_sprites) <= 0:
					if self.player.lives >=0:
						self.create_player()
					
		if self.game_paused:
			self.display_surface.blit(self.floor_surf, self.floor_rect.topleft)
			for sprite_group in self.sg_list: 
				sprite_group.draw(self.display_surface)
			self.ui.display(self.player)
			self.display_surface.blit(self.black_box, self.black_box_rect.topleft)
			# Help trying to blur
			#pygame.transform.box_blur(self.display_surface,50)
			#pygame.draw.rect(self.display_surface,(156,156,156,156), (200,200, SCREEN_WIDTH, SCREEN_HEIGHT))
			
			#pygame.mixer.music.pause()

		else:
			#pygame.mixer.music.unpause()

			# scroll bg image
			#self.floor_hitbox.centerx -= 0.1


			if self.scrolling:
				for sprite in self.enemy_sprites:
					sprite.origin.centerx -= 0.5
					

				for sprite in self.layer_000_sprites:
					sprite.hitbox.centerx -= 0.5
					sprite.rect.centerx = sprite.hitbox.centerx
				
				for sprite in self.lvl_end_sprites:
					sprite.hitbox.centerx -= 0.5
					sprite.rect.centerx = sprite.hitbox.centerx

				for sprite in self.layer_001_shadow:
					sprite.hitbox.centerx -= 0.2
					sprite.rect.centerx = sprite.hitbox.centerx

				for sprite in self.layer_001_sprites:
					sprite.hitbox.centerx -= 0.2
					sprite.rect.center = sprite.hitbox.center
				
				self.floor_hitbox.centerx -= 0.1
			self.floor_rect.center = self.floor_hitbox.center 
				
			# drawing the floor
			self.display_surface.blit(self.floor_surf, self.floor_rect.topleft)

			# draw and update sprite groups
			for enemy in self.enemy_sprites:
				enemy.enemy_update(self.player)
		
			for sprite_group in self.sg_list: 
				sprite_group.update()
				sprite_group.draw(self.display_surface)
			
			#Debug 
			#debug = True
			if self.debug == True:
				print ("true") 
			# draw enemy hitbox 
				for enemy in self.enemy_sprites:
					pygame.draw.rect(self.display_surface,'purple', enemy.hitbox, width=1)
				for shot in self.enemy_attack_sprites:
					pygame.draw.rect(self.display_surface,"white", shot.hitbox, width=1 )
			
			#Draw Player Hitbox and Rect
				for player in self.player_sprites:
					pygame.draw.rect(self.display_surface, (100,100,100,100), player.rect.inflate(2,2), width=1)
					pygame.draw.rect(self.display_surface, "white", player.hitbox, width=1)

			# draw player weapon hitbox 
				for weapon in self.weapon_sprites:
					pygame.draw.rect(self.display_surface,'red', weapon.rect, width=1)

			# draw player rect and hitbox 	
			# pygame.draw.rect(self.display_surface,'white', self.player.hitbox, width=1)
			#pygame.draw.rect(self.display_surface,'red', self.player.rect, width=1)

			'''for sprite in self.layer_000_sprites:
				pygame.draw.rect(self.display_surface, "white", sprite.hitbox, width=1)'''

			# outline background hitbox
			'''for sprite in self.layer_000_sprites and self.layer_001_sprites:
				pygame.draw.rect(self.display_surface, "white", sprite.hitbox, width=1)
				pygame.draw.rect(self.display_surface, "yellow", sprite.rect, width=1)'''
			 
			# debug 	
			self.ui.display(self.player)
			self.level_end_check()
			#debug(self.scrolling, 260, 20)
			#debug(f'lvl counter:{self.lvl_counter}', 310, 20)
			#debug(f'lvl:{self.lvl}', 350, 40)
			
		
		
			

				

