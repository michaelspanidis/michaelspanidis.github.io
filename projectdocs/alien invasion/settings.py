""" Load any modules necessary """
import pygame

class Settings:
	"""A class to manage the static and dynamic settings of the game"""

	""" Display settings """
	display_height = 800 
	display_width = 1200
	fps = 30

	""" Font settings """
	fps_font_size = 18 # Font settings
	fps_font_color = (255,255,255)

	""" Alien settings """
	alien_vertical_speed = 2.5

	""" Ship settings """
	ship_horizontal_speed = 30

	""" Bullet settings """
	bullet_width = 3
	bullet_height = 15
	bullet_vertical_speed = 80
	bullet_color = (228,16,154)
	bullets_allowed = 1

	""" Neural Network settings """
	net_input = 3 # Euclidean distance between the ship and any alien, euclidean distance between the ship and the screen boundaries
	net_ouput = 3 # 1 == left, 2 == right, 3 == shoot
	net_hidden = 2
	action_chance = 0.5 # if the output is greater than 0.5, compute the action, else do nothing
	mutation_modify_chance = 0.2 # probability that a weight will be modified
	mutation_array_mix_percentage = 0.5 # mix from two arrays to create a child array
	ship_generation_size = 60