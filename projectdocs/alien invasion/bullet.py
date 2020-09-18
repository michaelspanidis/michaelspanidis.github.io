""" Load any modules necessary """
import pygame

from settings import Settings


class Bullet:
	""" A class to manage the bullet """

	def __init__(self, ai_game_screen, ship_rect_midtop, ai_game_aliens):
		""" initialize the bullet attributes """

		self.settings = Settings() # Get the settings
		self.screen = ai_game_screen
		self.aliens = ai_game_aliens # Get the aliens
		self.color = self.settings.bullet_color
		self.state = 0 # Initialize the bullet as "alive"
		self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height) # Set the bullet dimensions
		self._set_position(ship_rect_midtop)
		self.hit_counter = 0

	def _set_position(self, ship_rect_midtop):
		""" Generate a bullet at the mid top of the ship's location """
		self.rect.midtop = ship_rect_midtop

	def update(self):
		""" Update the bullet """
		self._check_collisions(self.aliens)
	
	def move(self):
		self.rect.top -= self.settings.bullet_vertical_speed # N.B.: Negative because the bullet travels upward

	def _check_collisions(self, aliens):
		""" Check if the bullet has hit an alien or it collides with the top of the screen"""
		if self.rect.top < 0: # If the bullet exceeds the top of the screen
			self.state = 1

		for alien in aliens:
			if alien.rect.colliderect(self.rect):
				self.state = 1 # Kill the bullet if it hits an alien
				alien.state = 1 # Kill the alien if it hits a bullet
				self.hit_counter = 1
				break

	def draw(self):
		""" Draw the bullet on the display """
		pygame.draw.rect(self.screen, self.color, self.rect)

class Bullets:
	""" A class to manage the list of bullets """

	def __init__(self, ai_game_screen, ship_rect_midtop, ai_game_aliens):
		""" Initialize the list of bullet attributes """
		self.settings = Settings()
		self.screen = ai_game_screen
		self.bullets = []
		self.hits = 0
		self._create_bullets(ship_rect_midtop, ai_game_aliens) # Add amo to the cartridge

	def _create_bullets(self, ship_rect_midtop, ai_game_aliens):
		""" Manage amo """
		self.bullet = Bullet(self.screen, ship_rect_midtop, ai_game_aliens)
		self.bullets.append(self.bullet)
			
	def update(self, ship_rect_midtop, ai_game_aliens):
		for bullet in self.bullets:
			bullet.update()
			self.hits += bullet.hit_counter

		while len(self.bullets) < self.settings.bullets_allowed:
			self._create_bullets(ship_rect_midtop, ai_game_aliens)

		self.bullets = [bullet for bullet in self.bullets if bullet.state == 0] # Remove bullets that fly past the screen or that collide with aliens