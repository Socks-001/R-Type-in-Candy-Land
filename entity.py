import pygame
from math import sin
from debug import debug

class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.frame_index = 0
		self.animation_speed = 0.25
		self.display_surface = pygame.display.get_surface()
		self.screen_size = self.display_surface.get_size()
		self.direction = pygame.math.Vector2()

		# sounds
		self.death_sound = pygame.mixer.Sound('sounds/explosion001.wav')
		self.hit_sound = pygame.mixer.Sound('sounds/hitHurt.wav')
		self.shot_sound = pygame.mixer.Sound('sounds/shot.wav')

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed	
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self, direction):
		
		# out of bounds damage
		if self.sprite_type == 'player':
			
			if self.hitbox.right < -1 or self.hitbox.left > self.screen_size[0]  or self.hitbox.top > self.screen_size[1]  or self.hitbox.bottom < -1:	
				if self.vulnerable:
					self.hit_sound.play()
					self.health -= 1
					self.hit_cooldown = pygame.time.get_ticks()
					self.vulnerable = False
				

			for enemy in self.enemy_sprites:
					if enemy.hitbox.colliderect(self.hitbox):
						if self.vulnerable:
							self.hit_sound.play()
							self.health -= enemy.damage
							self.hit_cooldown = pygame.time.get_ticks()
							self.vulnerable = False
			
			for hazard in self.hazard_sprites:
					if hazard.hitbox.colliderect(self.hitbox):
						if self.vulnerable:
							self.hit_sound.play()
							self.health -= 80
							self.hit_cooldown = pygame.time.get_ticks()
							self.vulnerable = False
							

		for sprite in self.obstacle_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.sprite_type == 'player':	
					self.colliding = True

				if direction == 'horizontal':
					if abs(self.hitbox.right - sprite.rect.left) <= self.collision_tolerance : #moving right
						self.hitbox.right = sprite.rect.left #- self.collision_tolerance 
						if self.sprite_type == 'player':
							self.collide_side = 'right'
						#print('collided right')
						
					if abs(self.hitbox.left - sprite.rect.right) <= self.collision_tolerance : #moving left
						self.hitbox.left = sprite.rect.right #+ self.collision_tolerance
						#self.non_collide_time = True
						if self.sprite_type == 'player':
							self.collide_side = 'left'
						#print('collided left')

				if direction == 'vertical':
					if abs(self.hitbox.bottom - sprite.rect.top) <= self.collision_tolerance : #moving down
						self.hitbox.bottom = sprite.hitbox.top #- self.collision_tolerance
						#self.non_collide_time = True
						if self.sprite_type == 'player':
							self.collide_side = 'bottom'
						#print('collided bottom')

					if abs(self.hitbox.top - sprite.rect.bottom) <= self.collision_tolerance : #moving up
						self.hitbox.top = sprite.rect.bottom #+ self.collision_tolerance
						self.colliding = True
						if self.sprite_type == 'player':
							self.collide_side = 'top'

						#print('collided top')	


	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >=0:
			return 255
		else:
			return 0			
				
					

			

	

	