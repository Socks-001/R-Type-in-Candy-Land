import pygame
#from level import Level
'''from settings import SCREEN_WIDTH and SCREEN
from settings import weapon_data
'''
from settings import *
class Enemy_Weapon(pygame.sprite.Sprite):
	def __init__(self, enemy, player, groups, obstacle_sprites):
		super().__init__(groups)	

		self.player = player
		self.enemy = enemy

		# graphic
		self.sprite_type = 'enemy_shot'
		#self.weapon_index = enemy.weapon_index
		self.attack_damage = 1
		#self.direction = pygame.Vector2(0,0)
		
		#self.weapon_datas

		full_path = f'graphics/enemies/weapons/shot.png'
		self.image = pygame.image.load(full_path).convert_alpha()
		if self.enemy.direction.x < 0:
			self.image = pygame.transform.flip(self.image, True, False)

		#self.velocity = float(weapon_data[player.weapon]['projectile_speed']) + float(player.direction.x * player.speed)	
		self.velocity = 1

		# placement 
		'''self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,2))'''
		
		self.rect = self.image.get_rect(center = self.enemy.rect.center)
		self.hitbox = pygame.FRect(self.rect)
		self.direction = self.enemy.get_player_distance_direction(player)[1]

		# obstacles
		self.obstacle_sprites = obstacle_sprites

		# enemies 
		#self.entity_sprites = entity_sprites

	def move(self, velocity):

		self.hitbox.x += self.direction.x  * velocity
		self.hitbox.y += self.direction.y  * velocity
		self.rect.center = self.hitbox.center

	def check_collision(self):
		
		if self.hitbox.colliderect(self.player.hitbox) and self.player.vulnerable == True:
			pygame.mixer.Sound(self.player.hit_sound).play()
			self.player.health -= self.attack_damage
			self.player.vulnerable = False
			self.player.hit_time = pygame.time.get_ticks()

			self.kill()

		elif self.hitbox.colliderect(self.player.hitbox) and self.player.vulnerable == False:
			self.kill()

		for sprite in self.obstacle_sprites:
			if self.hitbox.colliderect(sprite.rect) or self.hitbox.x > + SCREEN_WIDTH + 4 or self.hitbox.x <= 0 or self.hitbox.y >= SCREEN_HEIGHT or self.hitbox.y <=0:
				self.kill()

	def update(self):
		self.check_collision()
		self.move(self.velocity)
		
			

		

		# Check for fireball colliding with world
		
		