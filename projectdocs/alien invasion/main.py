""" Load any modules necessary """
import sys
import pygame
import random

from settings import Settings
from screenstats import ScreenStats
from alien import Aliens
from ship import Ships

class AlienInvasion:
	""" A class to manage the main game elements """

	def __init__(self):
		""" Initialize the basic game properties """
		pygame.init() # Initialzie pygame
		self.settings = Settings() # Access the settings in the main game
		self.screen = pygame.display.set_mode((self.settings.display_width, self.settings.display_height)) # Prepare the display screen
		self.background = pygame.image.load("background.bmp")
		self.background = pygame.transform.scale(self.background, (self.settings.display_width, self.settings.display_height))
		pygame.display.set_caption("Alien Invasion")

		self.screen_statistics = ScreenStats(self.screen) # Access the timekeeping and other game statistics
		self.clock = pygame.time.Clock()
		self.dt = 0 # The change in time from a frame tick
		self.game_time = 0
		self.run_time = 0
		self.num_iters = 1 
		self.ships = Ships(self.screen) # Get the shipss

		# Initialize the random seed
		random.seed(331995)

	def run_game(self):
		""" The main game running loop """
		running = True
		while running:
			self._update_time()
			self._check_events()
			self._draw_game_assets()
			self._check_game_reset()

	def _update_time(self):
		""" Update the game time"""
		self.dt = self.clock.tick(self.settings.fps)
		self.game_time += self.dt
		self.run_time += self.dt

	def _check_events(self):
		""" Check for keyboard and mouse events """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				for s in self.ships.ships:
					f2 = open("wih.txt", "a")
					f2.write(f'{str(self.num_iters)},{str(s.net.weight_input_hidden)}\n')
					f2.close()
					f3 = open("who.txt", "a")
					f3.write(f'{str(self.num_iters)},{str(s.net.weight_hidden_output)}\n')
					f3.close()
					f4 = open("bh.txt", "a")
					f4.write(f'{str(self.num_iters)},{str(s.net.bias_input_hidden)}\n')
					f4.close()
					f5 = open("bo.txt", "a")
					f5.write(f'{str(self.num_iters)},{str(s.net.bias_hidden_output)}\n')
					f5.close()	
					sys.exit() # Stop the game if the window is closed
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event) # Check for user keyboard imputs

	def _check_keydown_events(self, event): ## Manual game override 
		"""Respond to key press."""
		if event.key == pygame.K_RIGHT:
			self.ships.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ships.moving_left = True

	def _check_keyup_events(self, event): ## Manual game override 
		""" Check for keyup events """
		if event.key == pygame.K_q:
			for s in self.ships.ships:
				f2 = open("wih.txt", "a")
				f2.write(f'{str(self.num_iters)},{str(s.net.weight_input_hidden)}\n')
				f2.close()
				f3 = open("who.txt", "a")
				f3.write(f'{str(self.num_iters)},{str(s.net.weight_hidden_output)}\n')
				f3.close()
				f4 = open("bh.txt", "a")
				f4.write(f'{str(self.num_iters)},{str(s.net.bias_input_hidden)}\n')
				f4.close()
				f5 = open("bo.txt", "a")
				f5.write(f'{str(self.num_iters)},{str(s.net.bias_hidden_output)}\n')
				f5.close()		
			sys.exit() # Exit the game if the user releaqses the Q key
		elif event.key == pygame.K_RIGHT:
			self.ships.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ships.moving_left = False

	def _draw_game_assets(self):
		""" Draw sprites and backgrounds onto the display screen """
		self.screen.blit(self.background, (0,0)) # Background image
		""" Sprites """
		self.ships.update()
		self.screen_statistics.update_time_labels(self.dt, self.run_time, self.game_time, self.num_iters, len([ship.state for ship in self.ships.ships if ship.state == 0])) # Update timekeeping information
		pygame.display.update() # Update the screen to the latest image

	def _check_game_reset(self):
		if sum([ship.state for ship in self.ships.ships]) == self.settings.ship_generation_size:
			self.ships.evolve_population(self.screen, self.num_iters) # Create a new ships and reset the bullets

			""" Update timekeeping and stats info """
			self.game_time = 0
			self.num_iters += 1

if __name__ == "__main__":
	ai = AlienInvasion()
	ai.run_game()