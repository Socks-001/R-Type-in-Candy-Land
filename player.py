import pygame
from settings import *
from support import import_folder
from debug import debug
from entity import Entity 


class Player(Entity):
	def __init__(self, pos, groups, obstacle_sprites, hazard_sprites, enemy_sprites, enemy_attacks, create_attack, activate_item, trigger_death_particles):

		super().__init__(groups)
		self.image = pygame.image.load('graphics/player/flying/demon_000.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = pygame.FRect(self.rect.inflate(0,0))
		self.lives = 3
		self.sprite_type = 'player'
		self.direction = pygame.math.Vector2()
		self.lives = 3

		# graphics setup
		self.import_player_assets()
		self.status = 'flying'
		#self.wep = weaponclass()

		# movement 
		self.coolingdown = False
		self.attack_time = None
		self.obstacle_sprites = obstacle_sprites
		self.hazard_sprites = hazard_sprites
		self.gravity = 0.5
		# controller  
		pygame.joystick.init()
		joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		self.controller_found = None
		#self.previous_position = pygame.math.Vector2
		#self.can_flap = True
		'''self.flap_cooldown = None
		self.flap_cooldown_time = 800
		self.flap_power = 0'''

		# collision timer
		self.collision_tolerance = 5
		self.colliding = False
		self.collide_side = 'none'
		self.collide_cooldown = pygame.time.get_ticks()
		self.collide_cooldown_time = 100
		self.hit_cooldown = pygame.time.get_ticks()
		self.hit_cooldown_time = 800
		self.vulnerable = True
		self.trigger_death_particles = trigger_death_particles

		#stats
		self.stats = {'health' : 1, 'strength' : 2, 'speed' : 4, 'exp' : 000, 'intelligence' : 10, 'resistance' : 3}
		self.health = self.stats['health']
		self.strength = self.stats['strength']
		self.speed = self.stats['speed']
		self.exp = self.stats['exp']
		self.intelligence = self.stats['intelligence']
		self.resistance = self.stats['resistance']
		

		# weapon
		self.create_attack = create_attack
		self.weapon_index = 0 
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.weapon_switch_duration_cooldown = 100
		self.attack_cooldown = int(weapon_data[self.weapon]['cooldown'])
		self.attack_damage = self.strength + int(weapon_data[self.weapon]['damage']) 
		
		# items
		self.activate_item = activate_item
		self.item_index = 0 
		self.item = list(item_data.keys())[self.item_index]
		self.can_switch_item = True
		self.item_switch_time = None
		self.item_switch_duration_cooldown = 100
		self.enemy_sprites = enemy_sprites

		# sounds
		#self.death_sound = pygame.mixer.Sound('sounds/explosion.wav')


	def import_player_assets(self):

		character_path = 'graphics/player/'
		self.animations = {'flying' : [],'attacking':[], 'projectile':[]}
		
		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)	

	'''def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance'''

	def animation_state(self):
		animation = self.animations[self.status]

		# loop over the frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0 	

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(bottomright = self.hitbox.bottomright)

		if not self.vulnerable:
			# flicker 
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
			
		else:
			self.image.set_alpha(255)
		
	def input(self):
		# pygame.joystick.init()
		# joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		# self.joystick = pygame.joystick.Joystick(0)

		keys = pygame.key.get_pressed()
	
		'''try:
			self.joystick = pygame.joystick.Joystick(0)
			self.dpad_input_player1 = self.joystick.get_hat(0)
			self.button_input_player1 = self.joystick.get_button(0)
			self.controller_found = True
			#print('true')
		except: 
			self.controller_found = False
			#print('false')'''
		
		self.controller_found == 0
		
		if self.controller_found:
			if keys[pygame.K_UP] or self.dpad_input_player1[1] == 1:
				self.direction.y =  -1 
		
			elif (keys[pygame.K_DOWN]) or self.dpad_input_player1[1] == -1:
				self.direction.y = 1 
				
			else: 
				self.direction.y = 0

			if (keys[pygame.K_LEFT]) or self.dpad_input_player1[0] == -1:
				self.direction.x =  -1 
				
			elif (keys[pygame.K_RIGHT]) or self.dpad_input_player1[0] == 1:
				self.direction.x = 1 
				
			else: 
				self.direction.x = 0
			
			if keys[pygame.K_SPACE] or self.button_input_player1 and not self.coolingdown:
				self.coolingdown = True 
				self.status = 'attacking'
				self.shot_sound.play()
				#print ('Attacking')
				self.create_attack()
				self.attack_time = pygame.time.get_ticks()
			
		# movement controls

		if not self.controller_found: 
			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.direction.y =  -1 
			
			elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.direction.y = 1 
				
			else: 
				self.direction.y = 0

			if keys[pygame.K_LEFT] or keys[pygame.K_a]:
				self.direction.x =  -1 
				
			elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
				self.direction.x = 1 
				
			else: 
				self.direction.x = 0
			
			
		# twin stick controls
		'''if keys[pygame.K_UP] :
			self.shoot_direction_y =  -1 
		
		elif keys[pygame.K_DOWN]:
			self.shoot_direction_y = 1 
			
		else: 
			self.shoot_direction_y = 0

		if keys[pygame.K_LEFT]:
			self.shoot_direction_x =  -1 
			
		elif keys[pygame.K_RIGHT]:
			self.shoot_direction_x = 1 
			
		else: 
			self.shoot_direction_x = 0'''
		
		# attacking input	
		if keys[pygame.K_SPACE] and not self.coolingdown:
			self.coolingdown = True 
			self.status = 'attacking'
			self.shot_sound.play()
			#print ('Attacking')
			self.create_attack()
			self.attack_time = pygame.time.get_ticks()


		if keys[pygame.K_LCTRL]:
			item = list(item_data.keys())[self.item_index]
			strength = list(item_data.values())[self.item_index]['strength'] + self.intelligence
			units = list(item_data.values())[self.item_index]['units']
			self.activate_item (item, strength, units)

		if keys[pygame.K_e] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
				
				self.weapon = list(weapon_data.keys())[self.weapon_index]
				self.attack_cooldown = int(weapon_data[self.weapon]['cooldown'])
				self.attack_damage = self.strength + int(weapon_data[self.weapon]['damage'])

		if keys[pygame.K_r] and self.can_switch_item:
				self.can_switch_item = False
				self.item_switch_time = pygame.time.get_ticks()
				
				if self.item_index < len(list(item_data.keys())) - 1:
					self.item_index += 1
				else:
					self.item_index = 0
				
				item = list(item_data.keys())[self.item_index]
				strength = list(item_data.values())[self.item_index]['strength'] + self.intelligence
				units = list(item_data.values())[self.item_index]['units']
				#print (f'cooldown = {self.attack_cooldown} damage = {self.attack_damage}')		
		
	def check_death(self):
		if self.health <= 0:
			self.lives-=1
			#print('dead')
			self.death_sound.play()
			self.trigger_death_particles(self.rect.center, 'explosion')
			self.kill()
			if self.lives <= 0:
				debug('GAME OVER', SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
			
	def cooldown(self):

		current_time = pygame.time.get_ticks()

		if self.coolingdown:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.coolingdown = False
				self.status = 'flying'

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.weapon_switch_duration_cooldown:
				self.can_switch_weapon = True
		
		if not self.can_switch_item:
			if current_time - self.item_switch_time >= self.item_switch_duration_cooldown:
				self.can_switch_item = True
		
		if not self.colliding:
			if current_time - self.collide_cooldown >= self.collide_cooldown_time:
				self.colliding = True
		
		if not self.vulnerable:
			if current_time - self.hit_cooldown >= self.hit_cooldown_time:
				self.vulnerable = True
		
		'''if not  self.can_flap:
			self.flap_power = 1
			if current_time - self.flap_cooldown >= self.flap_cooldown_time:
				self.can_flap = True'''

	def update(self):
		self.check_death()
		self.input()
		self.move (self.speed)
		self.animation_state()
		
		self.cooldown()
		#debug(f'controller:{self.controller_found}', 300, 60)
		# print(self.vulnerable)
		

		