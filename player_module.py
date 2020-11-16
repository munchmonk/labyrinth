import pygame
import random
import time

import const
import sprite_module


class Player(pygame.sprite.DirtySprite):
	def __init__(self, player_id, bot, board_x, board_y, game, *groups):
		self._layer = 3
		pygame.sprite.DirtySprite.__init__(self, *groups)

		self.game = game	

		self.board_x, self.board_y = board_x, board_y
		self.player_id = player_id

		self.bot = bot
		self.path_to_target_tile = []
		self.last_bot_action = 0
		self.bot_turn_to_act = False

		self.image = const.PLAYER_IMAGES[self.player_id]
		self.rect = self.image.get_rect(topleft=(const.LEFTBOARDMARGIN + const.TILESIZE * self.board_x, const.TOPBOARDMARGIN + const.TILESIZE * self.board_y))

		self.tile = None
		self.set_tile()
		self.pushing = None

		self.treasures = []
		self.current_treasure_objective = None
		self.homerun = False
		
		# Only create a card if a connection has been established
		self.card = None
		if self.game.side and self.game.side == self.player_id:
			self.card = sprite_module.Card(self.game.allsprites, self.game.allcards)

		self.intent = None
		self.signal = None
		self.broadcast = None

	def set_treasures(self, treasures):
		self.current_treasure_objective = None
		self.treasures = treasures

		if not treasures:
			return
		
		self.current_treasure_objective = self.treasures[0]

		if self.card and self.player_id == self.game.side:
			self.card.add_treasure_image(self.current_treasure_objective)

	def set_broadcast(self):
		if self.intent:
			self.broadcast = ['Player', self.player_id, self.intent]

	def reset_broadcast(self):
		self.broadcast = None

	def process_keyboard_input(self, key):
		if key == pygame.K_RIGHT:
			self.intent = const.RIGHT
		elif key == pygame.K_LEFT:
			self.intent = const.LEFT
		elif key == pygame.K_UP:
			self.intent = const.UP
		elif key == pygame.K_DOWN:
			self.intent = const.DOWN
		elif key == pygame.K_RETURN:
			self.intent = const.CONFIRM_MOVEMENT_SIGNAL

	def move(self):
		if (self.intent == const.RIGHT and self.board_x < 6 and self.tile.right_open and
			self.game.find_tile_by_board_coord(self.board_x + 1, self.board_y).left_open):
				self.board_x += 1
				self.set_tile()
				self.rect.x += const.TILESIZE
		elif (self.intent == const.LEFT and self.board_x > 0 and self.tile.left_open and
			self.game.find_tile_by_board_coord(self.board_x - 1, self.board_y).right_open):
				self.board_x -= 1
				self.set_tile()
				self.rect.x -= const.TILESIZE
		elif (self.intent == const.UP and self.board_y > 0 and self.tile.top_open and
			self.game.find_tile_by_board_coord(self.board_x, self.board_y - 1).bottom_open):
				self.board_y -= 1
				self.set_tile()
				self.rect.y -= const.TILESIZE
		elif (self.intent == const.DOWN and self.board_y < 6 and self.tile.bottom_open and
			self.game.find_tile_by_board_coord(self.board_x, self.board_y + 1).top_open):
				self.board_y += 1
				self.set_tile()
				self.rect.y += const.TILESIZE

	def start_homerun(self):
		self.homerun = True

		if self.card:
			self.card.set_homerun(self.player_id)

	def check_treasure_collision(self):
		if self.current_treasure_objective == self.tile.treasure:
			self.tile.remove_treasure()
			self.treasures.pop(0)
			const.TREASURE_CATCH_SOUND.play()

			if not self.treasures:
				self.start_homerun()
			else:
				self.current_treasure_objective = self.treasures[0]
				if self.card:
					self.card.add_treasure_image(self.current_treasure_objective)

	def set_tile(self):
		self.tile = self.game.find_tile_by_board_coord(self.board_x, self.board_y)

	def confirm_movement(self):
		self.signal = const.CONFIRM_MOVEMENT_SIGNAL
		self.check_treasure_collision()

	def check_victory(self):
		if self.player_id == const.P1 and (self.board_x, self.board_y) == (0, 6):
			self.signal = const.VICTORY_SIGNAL
		elif self.player_id == const.P2 and (self.board_x, self.board_y) == (6, 0):
			self.signal = const.VICTORY_SIGNAL

	def keep_pushing(self, dt):
		step_x, step_y = 0, 0

		if self.pushing[0]:
			step_x = int(abs(self.pushing[0]) / self.pushing[0] * const.PUSHING_SPEED * dt)

			if self.pushing[0] > 0:
				step_x = max(step_x, 1)
				step_x = min(step_x, self.pushing[0])

			elif self.pushing[0] < 0:
				step_x = min(step_x, -1)
				step_x = max(step_x, self.pushing[0])

			self.rect.x += step_x
			self.pushing[0] -= step_x

		if self.pushing[1]:
			step_y = int(abs(self.pushing[1]) / self.pushing[1] * const.PUSHING_SPEED * dt)

			if self.pushing[1] > 0:
				step_y = max(step_y, 1)
				step_y = min(step_y, self.pushing[1])

			elif self.pushing[1] < 0:
				step_y = min(step_y, -1)
				step_y = max(step_y, self.pushing[1])			

			self.rect.y += step_y
			self.pushing[1] -= step_y

		if self.pushing == [0, 0]:
			self.pushing = None
			if step_x:
				self.board_x += abs(step_x) / step_x
			if step_y:
				self.board_y += abs(step_y) / step_y

			# Warp to other side - the tile will call Player.set_tile() because they update after the players to avoid bugs
			if self.board_y == -1:
					self.board_y = 6
					self.rect.y += 7 * const.TILESIZE

			if self.board_y == 7:
					self.board_y = 0
					self.rect.y -= 7 * const.TILESIZE

			if self.board_x == 7:
				self.board_x = 0
				self.rect.x -= 7 * const.TILESIZE

			if self.board_x == -1:
					self.board_x = 6
					self.rect.x += 7 * const.TILESIZE

	def find_reachable_tiles(self):
		reachable_tiles = []
		candidates = [self.tile]

		while candidates:
			curr_candidate = candidates.pop()
			if curr_candidate not in reachable_tiles:
				reachable_tiles.append(curr_candidate)

			for neighbour in self.find_neighbours(curr_candidate):
				if neighbour not in reachable_tiles:
					reachable_tiles.append(neighbour)
					candidates.append(neighbour)

		return reachable_tiles

	def find_neighbours(self, tile):
		neighbours = []
		left_neighbour = self.game.find_tile_by_board_coord(tile.board_x - 1, tile.board_y)
		right_neighbour = self.game.find_tile_by_board_coord(tile.board_x + 1, tile.board_y)
		top_neighbour = self.game.find_tile_by_board_coord(tile.board_x, tile.board_y - 1)
		bottom_neighbour = self.game.find_tile_by_board_coord(tile.board_x, tile.board_y + 1)

		if left_neighbour and tile.left_open and left_neighbour.right_open:
			neighbours.append(left_neighbour)
		if right_neighbour and tile.right_open and right_neighbour.left_open:
			neighbours.append(right_neighbour)
		if top_neighbour and tile.top_open and top_neighbour.bottom_open:
			neighbours.append(top_neighbour)
		if bottom_neighbour and tile.bottom_open and bottom_neighbour.top_open:
			neighbours.append(bottom_neighbour)

		return neighbours

	def find_path_to_tile(self, target_tile):
		reachable_tiles = self.find_reachable_tiles()
		if target_tile not in reachable_tiles:
			return None

		path_to_tile = [self.tile]
		visited = [self.tile]
		curr_tile = path_to_tile[-1]

		while curr_tile != target_tile:
			neighbours = self.find_neighbours(curr_tile)
			choice = None

			for neighbour in neighbours:
				if neighbour in reachable_tiles and neighbour not in visited:
					choice = neighbour
					break

			if choice:
				curr_tile = choice
				path_to_tile.append(curr_tile)
				visited.append(curr_tile)
			else:
				path_to_tile.pop()
				curr_tile = path_to_tile[-1]

		return path_to_tile		

	def find_tile_containing_treasure(self, treasure):
		for tile in self.game.alltiles:
			if tile.treasure == treasure:
				return tile
		return None

	def get_bot_tile_move(self):
		# Give RETURN a higher chance
		choice = random.choice((pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE, pygame.K_RETURN, pygame.K_RETURN, pygame.K_RETURN))
		self.game.moving_tile.process_keyboard_input(choice)

	def transform_path_into_input(self, tile_path):
		if not tile_path:
			return None

		if len(tile_path) == 1:
			return [pygame.K_RETURN]

		input_list = []
		for i in range(len(tile_path) - 1):
			curr_tile = tile_path[i]
			next_tile = tile_path[i+1]

			if next_tile.board_x > curr_tile.board_x:
				input_list.append(pygame.K_RIGHT)
			elif next_tile.board_x < curr_tile.board_x:
				input_list.append(pygame.K_LEFT)
			elif next_tile.board_y > curr_tile.board_y:
				input_list.append(pygame.K_DOWN)
			elif next_tile.board_y < curr_tile.board_y:
				input_list.append(pygame.K_UP)

		return input_list

	def get_target_tile(self):
		reachable_tiles = self.find_reachable_tiles()

		if len(reachable_tiles) == 1:
			return self.tile

		target_tile = None

		# Straightforward choice
		if self.homerun:
			target_tile = self.game.find_tile_by_board_coord(*const.PLAYER_STARTING_POSITIONS[self.player_id])
		else:
			target_tile = self.find_tile_containing_treasure(self.current_treasure_objective)

		if target_tile in reachable_tiles:
			return target_tile

		# Start heuristics
		target_x, target_y = target_tile.board_x, target_tile.board_y
		priority_list = []

		# Homerun
		if self.homerun:
			# P1
			if (target_x, target_y) == (0, 6):
				priority_list += ((1, 5), (1, 4), (2, 5))
			# P2
			elif (target_x, target_y) == (6, 0):
				priority_list += ((5, 1), (5, 2), (4, 1))
			# P3
			elif (target_x, target_y) == (6, 6):
				priority_list += ((5, 5), (4, 5), (5, 4))
			# P4
			elif (target_x, target_y) == (0, 0):
				priority_list += ((1, 1), (2, 1), (1, 2))

		# Top left 2x5 rectangle
		if target_x in (0, 1) and target_y in (0, 1, 2, 3, 4):
			priority_list += [(2, 4), (0, 2), (1, 4)]

		# Top right 5x2 rectangle
		elif target_x in (2, 3, 4, 5, 6) and target_y in (0, 1):
			priority_list += ((2, 2), (4, 0), (2, 1))

		# Bottom right 2x5 rectangle
		elif target_x in (5, 6) and target_y in (2, 3, 4, 5, 6):
			priority_list += ((4, 2), (6, 4), (5, 2))

		# Bottom left 5x2 rectangle
		elif target_x in (0, 1, 2, 3, 4) and target_y in (5, 6):
			priority_list += ((4, 4), (2, 6), (4, 5))

		# Centre 3x3 square
		elif target_x in (2, 3, 4) and target_y in (2, 3, 4):
			priority_list += ((3, 3), (3, 2), (4, 3), (3, 4), (2, 3))

		# If the above aren't reachable, try the centre
		priority_list += ((3, 3), (3, 2), (4, 3), (3, 4), (2, 3), (2, 2), (4, 2), (4, 4), (2, 4))

		# If nothing else, try for a tile with three openings
		for tile in reachable_tiles:
			if tile.tiletype in (const.TOPRIGHTLEFT, const.TOPBOTTOMRIGHT, const.BOTTOMRIGHTLEFT, const.TOPBOTTOMLEFT):
				priority_list.append((tile.board_x, tile.board_y))

		for tile_coord in priority_list:
			if self.game.find_tile_by_board_coord(*tile_coord) in reachable_tiles:
				return self.game.find_tile_by_board_coord(*tile_coord)

		# Nothing found - return a random tile
		return random.choice(reachable_tiles)

	def get_bot_player_move(self):
		if not self.path_to_target_tile:
			self.path_to_target_tile = self.transform_path_into_input(self.find_path_to_tile(self.get_target_tile()))
			self.path_to_target_tile.append(pygame.K_RETURN)

		self.process_keyboard_input(self.path_to_target_tile.pop(0))

	def get_bot_action(self):
		if self.game.state == const.TILE_MOVING_STATE:
			self.get_bot_tile_move()

		elif self.game.state == const.PLAYER_MOVING_STATE:
			self.get_bot_player_move()

	def update(self, dt):
		# Players are always drawn
		self.dirty = 1

		self.signal = None

		old_rect = self.rect.copy()

		if self.bot_turn_to_act:
			self.get_bot_action()
			self.bot_turn_to_act = False

		if self.intent in (const.UP, const.DOWN, const.RIGHT, const.LEFT):
			self.move()
		elif self.intent == const.CONFIRM_MOVEMENT_SIGNAL:
			self.confirm_movement()

			if self.homerun:
				self.check_victory()

		if self.pushing:
			self.keep_pushing(dt)

		# True = something changed, False = things stayed the same
		# Only broadcast if something actually happened; bots only broadcast from the server side

		if (self.signal or self.rect != old_rect) and self.intent:
			if self.bot and self.game.side and self.game.side == const.P1:
				self.set_broadcast()
			elif not self.bot and self.game.side and self.game.side == self.player_id:
				self.set_broadcast()
			self.intent = None
			return True

		self.intent = None
		return False























