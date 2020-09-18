import pygame

from settings import Settings

class ScreenStats:
	"""A class for timekeeping and other statistics"""

	def __init__(self, ai_game_screen):
		"""Initialize timekeeping attributes"""
		self.settings = Settings() # Get information from the settings
		self.screen = ai_game_screen
		self.fps_font = pygame.font.SysFont("monospace", self.settings.fps_font_size)

	def update_time(self, data, title, x, y):
		""" Write the game time on the screen"""
		self.label = self.fps_font.render('{} {}'.format(title, data), 1, self.settings.fps_font_color)
		self.screen.blit(self.label, (x, y))
		return y

	def update_time_labels(self, dt, run_time, game_time, num_iters, num_ships):
		""" Use the tick rate to determine the game time"""
		self.y_pos = 10
		self.gap = 20
		self.x_pos = 10
		self.y_pos = self.update_time(round(dt, 2), 'FPS', self.x_pos, self.y_pos + self.gap)
		self.y_pos = self.update_time(round(run_time/1000, 2), 'Total run time', self.x_pos, self.y_pos + self.gap)
		self.y_pos = self.update_time(round(game_time/1000, 2), 'Iteration run time', self.x_pos, self.y_pos + self.gap)
		self.y_pos = self.update_time(num_iters, 'Iteration', self.x_pos, self.y_pos + self.gap)
		self.y_pos = self.update_time(num_ships, 'Ships alive', self.x_pos, self.y_pos + self.gap)