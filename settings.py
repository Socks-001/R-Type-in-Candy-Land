# width is 16 x Tiles (16pxx16px), height is 15 x Tiles (16pxx16px)
# Test Map is 80 tiles long


#SCREEN_WIDTH = 256 # 16x16 
SCREEN_WIDTH = 426 # 16x16    
SCREEN_HEIGHT = 240 # 15x16 
# SCREEN_WIDTH = 800    
# SCREEN_HEIGHT = 600
FPS = 60
TILESIZE = 16

# ui 
BAR_HEIGHT = 10 
HEALTH_BAR_WIDTH = 100
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 20
#UI_FONT = 'graphics/font/Minecraft.ttf'
UI_FONT = 'graphics/font/joystix monospace.otf'
UI_FONT_SIZE = 10

# general colors

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#7ee4ff'
UI_BORDER_COLOR = '#4bb2cd'
TEXT_COLOR = '#fffde4'

# ui colors
HEALTH_COLOR = '#dd5929'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons 
weapon_data = {
	'fireball': {'cooldown': 450, 'damage' : 3, 'projectile_speed' : 3, 'graphic':'graphics/player/weapons/fireball.png'},
    'blue_fireball': {'cooldown': 200, 'damage' : 1, 'projectile_speed' : 3, 'graphic':'graphics/player/weapons/blue_fireball.png'}
			  } 

# items
item_data = {
	'health potion': {'strength': 5, 'cooldown': 6, 'units' : 1, 'graphic':'graphics/player/items/health_potion.png'},
    'slime': {'strength': 2, 'cooldown': 6, 'units' : 2, 'graphic':'graphics/player/items/slime.png'}
			} 

# enemy
enemy_data = {
    'screaming skull' : {'health' : 8, 'exp' : 2, 'damage' : 0.5, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 2, 'resistance' : 5, 'attack_radius' : 60, 'notice_radius': 100, 'action_type' : 'melee'},
    'eggplant' : {'health' :6, 'exp' : 10, 'damage' : 5, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 1.5, 'resistance' : 10, 'attack_radius' : 60, 'notice_radius': 100, 'action_type' : 'zone'},
    'remote' : {'health' :10, 'exp' : 5, 'damage' : 1, 'attack_type' : 'contact', 'attack_sound' : None, 'speed' : 1, 'resistance' : 5, 'attack_radius' : 60, 'notice_radius': 60, 'action_type' : 'turret'}
    	}