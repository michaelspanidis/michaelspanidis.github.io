""" Load any modules necessary """
import pygame
import random
import numpy as np

from settings import Settings

class Alien:
	""" A class to manage a single alien """

	def __init__(self, ai_game_screen, x, y):
		""" Initialize the base alien atributes """
		self.settings = Settings() # Get alien information from the settings
		self.screen = ai_game_screen # Get screen information from the main game

		""" Prepare the alien image """
		self.image = pygame.image.load('alien.png')
		self.screen_rect = self.screen.get_rect()
		self.rect = self.image.get_rect()
		self.state = 0 # N.B.: 0 implies that the sprite is alive, 1 implies that it is dead
		self._set_position(x, y)

	def _set_position(self, x, y):
		self.rect.left = x
		self.rect.top = y

	def update(self):
		""" Update the alien """
		self._update_position(self.settings.alien_vertical_speed)
	
	def _update_position(self, y):
		""" Move the alien """
		self.rect.centery += y # Move the alien y units down the screen N.B.: (0,0) is at the top left of the screen

	def draw(self):
		""" Draw the alien on the display """
		self.screen.blit(self.image, self.rect)

class Aliens:
	""" A class to manage an group of aliens """

	def __init__(self, ai_game_screen):
		""" Initialize the base alien group atributes """
		self.settings = Settings() # Get display information from the settings
		self.screen = ai_game_screen
		self.aliens = [] # Initialize the aliens list
		self.screen_rect = self.screen.get_rect()

	def create_alien_row(self):
		""" Create a row of aliens across the display """
		for a in range(4): # Create 4 aliens across the display N.B.: this is fixed because I wante the screen to be of size 1200x800 but can also be variable in the future
			""" Space the aliens evenly across the screen """
			alien = Alien(self.screen, 100, 100)
			alien.x = alien.rect.size[0] + 5 * alien.rect.size[0] * a
			alien.rect.x = alien.x
			self.aliens.append(alien) # Add aliens to the alien list

	def reset_aliens(self):
		self.aliens = []
		self.create_alien_row()

	def update(self):
		""" Update the list of aliens """
		for alien in self.aliens:
			alien.update() # Update each individual alien

		self.aliens = [alien for alien in self.aliens if alien.state == 0] # Remove aliens from the list that have been killed

		while len(self.aliens) < 4:
			self.aliens.append(Alien(self.screen, random.randint(100, self.screen_rect.right - 100), -25)) # Maintain a total of 4 aliens, generate a new alien at a random position on the screen