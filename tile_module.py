import pygame
import random

import const


class Tile(pygame.sprite.Sprite):
	def __init__(self, rect_x, rect_y, board_x, board_y, tiletype, game, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.game = game

		self.tiletype = tiletype
		self.treasure = None

		self.image = None
		self.set_image()
		self.rect = self.image.get_rect(topleft=(rect_x, rect_y))

		self.board_x, self.board_y = board_x, board_y
		self.pushing = None

		self.right_open = False
		self.left_open = False
		self.top_open = False
		self.bottom_open = False
		self.set_borders()

		self.intent = None
		self.signal = None
		self.broadcast = None

	def add_marker(self, player_id):
		self.image = self.image.copy()
		self.image.blit(const.MARKER_IMAGES[player_id], (0, 0))

	def add_treasure(self, treasure):
		if not treasure:
			return
		self.treasure = treasure
		self.add_treasure_image()

	def remove_treasure(self):
		self.treasure = None
		self.set_image()
	
	def set_borders(self):
		self.right_open = False
		self.left_open = False
		self.top_open = False
		self.bottom_open = False

		if const.RIGHT in self.tiletype:
			self.right_open = True
		if const.LEFT in self.tiletype:
			self.left_open = True
		if const.TOP in self.tiletype:
			self.top_open = True
		if const.BOTTOM in self.tiletype:
			self.bottom_open = True

	def set_image(self):
		self.image = const.TILE_IMAGES[self.tiletype]
		self.add_treasure_image()

	def add_treasure_image(self):
		if self.treasure:
			self.image = self.image.copy()
			self.image.blit(const.TREASURE_IMAGES[self.treasure], (0, 0))

	def process_keyboard_input(self, key):
		if self.board_y in (-1, 7) and key == pygame.K_RIGHT:
			self.intent = const.RIGHT
		elif self.board_y in (-1, 7) and key == pygame.K_LEFT:
			self.intent = const.LEFT
		elif self.board_x in (-1, 7) and key == pygame.K_UP:
			self.intent = const.UP
		elif self.board_x in (-1, 7) and key == pygame.K_DOWN:
			self.intent = const.DOWN
		elif key == pygame.K_SPACE:
			self.intent = const.ROTATE
		elif key == pygame.K_RETURN:
			self.intent = const.PUSH_SIGNAL

	def set_broadcast(self):
		if self.intent:
			self.broadcast = ['Tile', self.intent]

	def reset_broadcast(self):
		self.broadcast = None

	def push(self):
		self.signal = const.PUSH_SIGNAL

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

	def move(self):
		# Move
		if self.intent == const.RIGHT:
			self.board_x += 2
			self.rect.x += 2 * const.TILESIZE
		elif self.intent == const.LEFT:
			self.board_x -= 2
			self.rect.x -= 2 * const.TILESIZE
		elif self.intent == const.UP:
			self.board_y -= 2
			self.rect.y -= 2 * const.TILESIZE
		elif self.intent == const.DOWN:
			self.board_y += 2
			self.rect.y += 2 * const.TILESIZE

		# Check if moved beyond board edges - snap to board
		if (self.board_x, self.board_y) == (-1, -1):
			if self.intent == const.UP:
				self.board_x += 2
				self.rect.x += 2 * const.TILESIZE
			elif self.intent == const.LEFT:
				self.board_y += 2
				self.rect.y += 2 * const.TILESIZE
		elif (self.board_x, self.board_y) == (7, -1):
			if self.intent == const.UP:
				self.board_x -= 2
				self.rect.x -= 2 * const.TILESIZE
			elif self.intent == const.RIGHT:
				self.board_y += 2
				self.rect.y += 2 * const.TILESIZE
		elif (self.board_x, self.board_y) == (7, 7):
			if self.intent == const.DOWN:
				self.board_x -= 2
				self.rect.x -= 2 * const.TILESIZE
			elif self.intent == const.RIGHT:
				self.board_y -= 2
				self.rect.y -= 2 * const.TILESIZE
		elif (self.board_x, self.board_y) == (-1, 7):
			if self.intent == const.DOWN:
				self.board_x += 2
				self.rect.x += 2 * const.TILESIZE
			elif self.intent == const.LEFT:
				self.board_y -= 2
				self.rect.y -= 2 * const.TILESIZE

	def rotate(self, random_rotation=False):
		bucket1 = [const.TOPBOTTOM, const.RIGHTLEFT]
		bucket2 = [const.TOPRIGHT, const.BOTTOMRIGHT, const.BOTTOMLEFT, const.TOPLEFT]
		bucket3 = [const.TOPRIGHTLEFT, const.TOPBOTTOMRIGHT, const.BOTTOMRIGHTLEFT, const.TOPBOTTOMLEFT]

		if self.tiletype in bucket1:
			if random_rotation:
				self.tiletype = random.choice(bucket1)
			else:
				next_rotation = (bucket1.index(self.tiletype) + 1) % len(bucket1)
				self.tiletype = bucket1[next_rotation]
		elif self.tiletype in bucket2:
			if random_rotation:
				self.tiletype = random.choice(bucket2)
			else:
				next_rotation = (bucket2.index(self.tiletype) + 1) % len(bucket2)
				self.tiletype = bucket2[next_rotation]
		elif self.tiletype in bucket3:
			if random_rotation:
				self.tiletype = random.choice(bucket3)
			else:
				next_rotation = (bucket3.index(self.tiletype) + 1) % len(bucket3)
				self.tiletype = bucket3[next_rotation]

		self.set_image()
		self.set_borders()

	def update(self, dt):
		self.signal = None

		old_rect = self.rect.copy()
		old_tiletype = self.tiletype

		if self.intent in (const.UP, const.DOWN, const.RIGHT, const.LEFT):
			self.move()
		elif self.intent == const.ROTATE:
			self.rotate()
		elif self.intent == const.PUSH_SIGNAL:
			self.push()

		if self.pushing:
			self.keep_pushing(dt)

		# True = something changed, False = things stayed the same
		# Only broadcast if something actually happened; bots only broadcast from the server side

		# This prevents pushing tiles from broadcasting
		if self == self.game.moving_tile and self.intent:
			
			# This prevents tiles that didn't update from broadcasting
			if self.signal or self.rect != old_rect or self.tiletype != old_tiletype:

				# This prevents non active players from broadcasting
				if self.game.side and self.game.side == self.game.active_player.player_id and not self.game.active_player.bot:
					self.set_broadcast()

				# This prevents clients from broadcasting bots' actions
				elif self.game.side and self.game.side == const.P1 and self.game.active_player.bot:
					self.set_broadcast()
				self.intent = None
				return True

		self.intent = None
		return False
























