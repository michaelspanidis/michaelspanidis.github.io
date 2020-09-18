""" Load any modules necessary """
import pygame
import random

from settings import Settings
from alien import Aliens
from bullet import Bullets
from neuralnetwork import NeuralNetwork
import numpy as np
import neat

class Ship:
	""" A class to manage a single ship """

	def __init__(self, ai_game_screen):
		""" Initialize the ship attributes """
		self.settings = Settings() # Get alien information from the settings
		self.screen = ai_game_screen
		self.screen_rect = self.screen.get_rect()
		self.state = 0
		self.fitness = 0
		self.net = NeuralNetwork(self.settings.net_input, self.settings.net_hidden, self.settings.net_ouput)

		""" Prepare the alien image """
		self.image =  pygame.image.load('spaceship.png')
		self.rect = self.image.get_rect()
		self._set_position(self.settings.display_width/2, self.settings.display_height - 100)

		self.moving_right = False # At default the ship does not move unless told otherwise
		self.moving_left = False
		self.firing_bullet = False

		self.aliens = Aliens(self.screen) # Get the aliens
		self.aliens.create_alien_row()
		self.bullets = Bullets(self.screen, self.rect.midtop, self.aliens.aliens)

	def _set_position(self, x, y):
		""" Set the ships default position """
		self.rect.left = x
		self.rect.top = y

	def update(self):
		""" Update the ship's state, move the ship, etc."""
		if self.state == 0:
			self.aliens.update()
			self._check_collisions() # Pass the list of aliens
			self._get_inputs()
			self._move_position(self.settings.ship_horizontal_speed)
			for b in self.bullets.bullets:
				b.move()
			self._get_fitness()
		else:
			self.fittness -= 1

	def _get_inputs(self):
		""" Get the distance of the aliens from the ship """
		net_inputs = []
		alien_x = []
		alien_y = []
		for a in self.aliens.aliens:
			alien_x.append(self.rect.centerx - a.rect.centerx)
			alien_y.append(self.rect.centery - a.rect.centery)
		closest_alien = sorted(list(zip(alien_x, alien_y)), key = lambda coordinate: (coordinate[1], coordinate[0]), reverse = False)[0]
		if closest_alien[0] < 0:
			alien_is_left = 0
			alien_is_right = 1
		else:
			alien_is_left = 1
			alien_is_right = 0
		net_inputs.append(self._normalizer(closest_alien[0], self.screen_rect.right, self.screen_rect.left)*(0.9 - 0.1) + 0.1)
		net_inputs.append(alien_is_left)
		net_inputs.append(alien_is_right)
		return net_inputs

	def _normalizer(self, x, dist_max, dist_min):
		""" Function to normalize the inputs """
		normalized = (x - dist_min)/(dist_max - dist_min)
		return normalized

	def _check_collisions(self):
		""" Check ship-alien collisions """
		for alien in self.aliens.aliens:
			if alien.rect.colliderect(self.rect) or alien.rect.centery > self.settings.display_height:
				self.state = 1 # Kill the ship if it hits any alien or an alien passes the ship
				break

		""" Check ship-screen collisions """
		if self.rect.right > self.screen_rect.right or self.rect.left < 0:
			self.state = 1 # Kill the ship if it moves beyond the screen boundaries

	def _move_position(self, x):
		""" Move the ship """
		inputs = self._get_inputs()
		action = self.net.get_outputs(inputs)
		action = [i for i, j in enumerate(self.net.get_outputs(inputs)) if j == max(self.net.get_outputs(inputs))and i for i, j in enumerate(self.net.get_outputs(inputs)) if j > self.settings.action_chance]
		if len(action) == 0:
			action = 3 # Do nothing
		else:
			action = action[0]
		if action != 3:
			if action == 0:
				self.moving_right = True
			elif action == 1:
				self.moving_left = True
			else:
				self.firing_bullet = True

		if self.moving_right == True:
			self.rect.centerx += x
		if self.moving_left == True:
			self.rect.centerx -= x
		if self.firing_bullet == True:
			self._fire_bullet()

		self.moving_right = False # At default the ship does not move unless told otherwise
		self.moving_left = False
		self.firing_bullet = False

	def _fire_bullet(self):
		self.bullets.update(self.rect.midtop, self.aliens.aliens)

	def draw(self):
		""" Draw the ship on the dispaly """
		self.screen.blit(self.image, self.rect)

	def create_offspring(p1, p2, ai_game_screen):
		new_ship = Ship(ai_game_screen)
		new_ship.net.create_mixed_weights(p1.net, p2.net)
		return new_ship

	def _get_fitness(self):
		""" Get the fitness of the ship """
		self.fitness = self.bullets.hits

class Ships:
	""" A class to manage the generations of ships for learning """

	def __init__(self, ai_game_screen):
		self.settings = Settings()
		self.ships = []
		self.fitness_data = []
		self.create_new_generation(ai_game_screen)

	def create_new_generation(self, ai_game_screen):
		""" Creates the generation of ships """
		self.ships = []
		for i in range(self.settings.ship_generation_size):
			self.ships.append(Ship(ai_game_screen))

	def update(self):
		""" Update the generation of ships """
		what_to_draw = max([ship.fitness for ship in self.ships])
		for s in self.ships:
			if s.state == 0:
				s.update()
			if s.fitness == what_to_draw and s.state == 0:
				s.draw()
				for b in s.bullets.bullets:
					b.draw()
				for a in s.aliens.aliens:
					a.draw()

	def evolve_population(self, ai_game_screen, iters):
		""" Evolve the ship pop """
		self.ships.sort(key = lambda x: x.fitness, reverse = True)
		self.ships_verbose = self.ships[0:10]
		print('------------------------------------')
		print('Iteration:', iters)
		for s in self.ships_verbose:
			print('Fitness:', s.fitness)
		print('------------------------------------')

		cut_off = int(len(self.ships) * 0.4)
		good_ships = self.ships[0:cut_off]
		bad_ships = self.ships[cut_off:]
		num_bad_to_take = int(len(self.ships) * 0.2)

		for s in bad_ships:
			s.net.modify_weights()

		new_ships = []

		idx_bad_to_take = np.random.choice(np.arange(len(bad_ships)), num_bad_to_take, replace = False)

		for index in idx_bad_to_take:
			new_ships.append(bad_ships[index])

		new_ships.extend(good_ships)

		children_needed = len(self.ships) - len(new_ships)

		while len(new_ships) < len(self.ships):
			idx_to_breed = np.random.choice(np.arange(len(good_ships)), 2, replace = False)
			if idx_to_breed[0] != idx_to_breed[1]:
				new_ship = Ship.create_offspring(good_ships[idx_to_breed[0]], good_ships[idx_to_breed[1]], ai_game_screen)
				if random.random() < 0.4:
					new_ship.net.modify_weights()
				new_ships.append(new_ship)

		self.ships = new_ships
		best_preformer = max([ship.fitness for ship in self.ships])
		for s in self.ships:
			s._set_position(self.settings.display_width/2, self.settings.display_height - 100)
			s.state = 0
			s.aliens.reset_aliens()
			if s.fitness == best_preformer:
				f1 = open("fitness_scores.txt", "a")
				f1.write(f'{str(iters)},{str(s.fitness)}\n')
				f1.close()
				f2 = open("wih.txt", "a")
				f2.write(f'{str(iters)},{str(s.net.weight_input_hidden)}\n')
				f2.close()
				f3 = open("who.txt", "a")
				f3.write(f'{str(iters)},{str(s.net.weight_hidden_output)}\n')
				f3.close()
				f4 = open("bh.txt", "a")
				f4.write(f'{str(iters)},{str(s.net.bias_input_hidden)}\n')
				f4.close()
				f5 = open("bo.txt", "a")
				f5.write(f'{str(iters)},{str(s.net.bias_hidden_output)}\n')
				f5.close()				
			s.bullets.hits = 0