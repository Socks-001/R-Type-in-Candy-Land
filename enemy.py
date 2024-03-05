import pygame
from settings import *
from entity import Entity
from support import *
from debug import debug


class Enemy(Entity):
	def __init__(self, name, pos, groups, obstacle_sprites, trigger_death_particles, add_exp, attack, player, enemy_attack_sprites,  ):
		# general setup
		super().__init__(groups)
		self.sprite_type = 'enemy'
		self.obstacle_sprites = obstacle_sprites
		self.visible_sprites = groups[0]
		self.shot_direction = None
		self.player = player
		self.enemy_attack_sprites = enemy_attack_sprites
		
		# graphics
		self.import_graphics(name)
		self.status = 'idle'
		self.image = self.animations[self.status][int(self.frame_index)]
		self.collision_tolerance = 5

		# movement 
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = pygame.FRect(self.rect.inflate(-6,-6))
		self.origin = self.hitbox.copy()
		#self.origin_location = pygame.math.Vector2(self.hitbox.centerx,self.hitbox.centery)
		self.obstacle_sprites = obstacle_sprites
		self.gravity = 0

		# stats
		self.health = enemy_data[name]['health'] 
		self.exp = enemy_data[name]['exp'] 
		self.damage = enemy_data[name]['damage'] 
		self.attack_type = enemy_data[name]['attack_type'] 
		self.attack_sound = enemy_data[name]['attack_sound'] 
		self.speed = enemy_data[name]['speed']
		self.resistance = enemy_data[name]['resistance'] 
		self.attack_radius = enemy_data[name]['attack_radius'] 
		self.notice_radius = enemy_data[name]['notice_radius']
		self.action_type = enemy_data[name]['action_type']
		self.trigger_death_particles = trigger_death_particles
		self.add_exp = add_exp

		# player interaction
		self.can_attack = False
		self.attack_time = pygame.time.get_ticks()
		self.attack_cooldown = None
		self.attack_cooldown = 2000
		self.hit_time = None
		self.vulnerable = True
		self.invincibility_duration = 100
		self.attack = attack

		# sounds

	def import_graphics(self,name):
		self.animations = {'idle': [], 'move': [], 'attack' : []}
		main_path = f'graphics/enemies/{name}/'
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)

	def get_player_distance_direction(self, player):
		player_vec = pygame.math.Vector2 (player.rect.center)
		enemy_vec = pygame.math.Vector2 (self.rect.center)

		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		#print (distance, direction)
		return (distance, direction)	

	def get_target_distance_direction(self, object):
		object_vec = pygame.math.Vector2 (object.center)
		enemy_vec = pygame.math.Vector2 (self.rect.center)

		distance = (object_vec - enemy_vec).magnitude()

		if distance > 0.8:
			direction = (object_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance, direction)

	def get_status(self, player):
		
		distance = self.get_player_distance_direction(player)[0]

		# set status 
		'''
		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				pass
				#self.frame_index = 0
				self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle' 
		'''
		'''
		if distance <= self.notice_radius:
			self.status = 'move'

		elif distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				pass
				#self.frame_index = 0
				self.status = 'attack'
		
		else:
			self.status = self.status
		'''
		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				pass
				#self.frame_index = 0
				self.status = 'attack'

		elif distance <= self.notice_radius:
			self.status = 'move'

		else:
			self.status = self.status

	def actions(self,player):
	
		if self.action_type == 'melee':
			
			if self.status == 'attack':
				self.attack_time = pygame.time.get_ticks()
					# print ("attack")
			elif self.status == 'move':
				self.direction = self.get_player_distance_direction(player)[1]
				#print ('move')

			else:
				self.direction = pygame.math.Vector2(-1,0)

		elif self.action_type == 'zone':

			if self.status == 'attack':
				self.attack_time = pygame.time.get_ticks()
				# print ("attack")
			elif self.status == 'move':
				self.direction = self.get_player_distance_direction(player)[1]
				#print ('move')

			else:
				#self.direction = pygame.math.Vector2(0,0)
				self.direction = self.get_target_distance_direction(self.origin)[1]
			
		elif self.action_type == 'turret':

			if self.status == 'attack':
				self.direction = pygame.math.Vector2(0,0)
				if self.can_attack:
					self.attack(self, self.player, [self.enemy_attack_sprites],  self.obstacle_sprites)
					self.can_attack = False
					self.attack_time = pygame.time.get_ticks()
				#print ("attack")

			elif self.status == 'move':
				self.direction = self.get_target_distance_direction(self.origin)[1]
				#print ('move')

			else:
				#self.direction = pygame.math.Vector2(1,0)
				self.direction = self.get_target_distance_direction(self.origin)[1]
		
		'''else:
			self.direction = pygame.math.Vector2(-1,0)'''
	
	def hit_reaction(self):
		if not self.vulnerable and self.shot_direction == 'left':
			self.direction *= -self.resistance
			#print (f'dir = {self.direction} *= {-self.resistance}')
			
		if not self.vulnerable and self.shot_direction == 'right':
			#value= pygame.math.Vector2(1,0)
			self.direction *= self.resistance
			#print (f'dir = {self.direction} *= {self.resistance}')

	
	'''def hit_reaction(self,player):
		if not self.vulnerable:
			if self.get_player_distance_direction(player)[1].x <= 0:
				self.direction *= -self.resistance
				print ('hit from left')
			else:
				self.direction *= self.resistance
				print ('hit from right')'''

	def animate(self):
		animation = self.animations[self.status]
		
		#print status
		'''print (self.rect.center , self.status)'''

		# loop over the frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			'''if self.status == 'attack':
				self.can_attack = False'''
			self.frame_index = 0 	
			
		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)	
		
		if not self.vulnerable:
			# flicker 
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
			#self.image.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGB_ADD)
			#self.image.set_alpha(alpha)
			
		else:
			self.image.set_alpha(255)
			#self.image.fill((0, 0, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
			#self.image.fill('None',)

	def check_death(self):
		if self.health <= 0:
			#print('dead')
			self.death_sound.play()
			self.add_exp(self.exp)
			self.trigger_death_particles(self.rect.center, 'explosion')
			self.kill()
		if self.rect.right < -4:
			self.kill()
	
	def cooldown(self):
		current_time = pygame.time.get_ticks()

		if not self.can_attack:
			current_time = pygame.time.get_ticks()
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True 

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True 

	def add_exp(self, player):
		player.exp += self.exp
		
	def update(self):
		self.hit_reaction()
		#self.origin.x -= 0.1
		self.move(self.speed)
		self.animate()
		self.cooldown()
		self.check_death()
		
		
		# debug(self.frame_index, 300, 10)
		# debug(self.status, 300, 40)

	def enemy_update(self,player):
		#self.hit_reaction(player)
		self.get_status(player)
		self.actions(player)

		
