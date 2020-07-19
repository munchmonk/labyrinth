#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import pygame
import pygame.freetype
pygame.init()
pygame.mixer.init()

import sys
import random
import socket
import pickle
import threading
import os

import const


class Player(pygame.sprite.Sprite):
	IMAGES =   {const.P1: pygame.image.load(const.PLAYER_IMAGE_PATH + 'p1.png'),
				const.P2: pygame.image.load(const.PLAYER_IMAGE_PATH + 'p2.png')}

	def __init__(self, player_id, board_x, board_y, game, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.game = game

		self.board_x, self.board_y = board_x, board_y
		self.player_id = player_id

		self.image = Player.IMAGES[self.player_id]
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
			self.card = Card(self.game.allsprites, self.game.allcards)

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
			self.broadcast = ('Player', self.player_id, self.intent)

	def reset_broadcast(self):
		self.broadcast = None

	def process_keyboard_input(self, key):
		if self.game.is_anything_pushing():
			return

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

		self.set_broadcast()

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

	def keep_pushing(self):
		step_x, step_y = 0, 0

		if self.pushing[0]:
			step_x = abs(self.pushing[0]) / self.pushing[0] * const.PUSHING_SPEED
			self.rect.x += step_x
			self.pushing[0] -= step_x
		if self.pushing[1]:
			step_y = abs(self.pushing[1]) / self.pushing[1] * const.PUSHING_SPEED
			self.rect.y += step_y
			self.pushing[1] -= step_y

		if self.pushing == [0, 0]:
			self.pushing = None
			if step_x:
				self.board_x += abs(step_x) / step_x
			if step_y:
				self.board_y += abs(step_y) / step_y

			# Warp to other side
			if self.board_y == -1:
					self.board_y = 6
					self.rect.y += 7 * const.TILESIZE
					self.set_tile()
			if self.board_y == 7:
					self.board_y = 0
					self.rect.y -= 7 * const.TILESIZE
					self.set_tile()
			if self.board_x == 7:
				self.board_x = 0
				self.rect.x -= 7 * const.TILESIZE
				self.set_tile()
			if self.board_x == -1:
					self.board_x = 6
					self.rect.x += 7 * const.TILESIZE
					self.set_tile()

	def update(self, dt):
		self.signal = None

		if self.intent in (const.UP, const.DOWN, const.RIGHT, const.LEFT):
			self.move()
		elif self.intent == const.CONFIRM_MOVEMENT_SIGNAL:
			self.confirm_movement()

			if self.homerun:
				self.check_victory()

		if self.pushing:
			self.keep_pushing()

		self.intent = None

	def draw(self):
		pass


class Tile(pygame.sprite.Sprite):
	def __init__(self, rect_x, rect_y, board_x, board_y, tiletype, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

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

		self.set_broadcast()

	def set_broadcast(self):
		if self.intent:
			self.broadcast = ('Tile', self.board_x, self.board_y, self.intent)

	def reset_broadcast(self):
		self.broadcast = None

	def push(self):
		self.signal = const.PUSH_SIGNAL

	def keep_pushing(self):
		step_x, step_y = 0, 0
		if self.pushing[0]:
			step_x = abs(self.pushing[0]) / self.pushing[0] * const.PUSHING_SPEED
			self.rect.x += step_x
			self.pushing[0] -= step_x
		if self.pushing[1]:
			step_y = abs(self.pushing[1]) / self.pushing[1] * const.PUSHING_SPEED
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

		if self.intent in (const.UP, const.DOWN, const.RIGHT, const.LEFT):
			self.move()
		elif self.intent == const.ROTATE:
			self.rotate()
		elif self.intent == const.PUSH_SIGNAL:
			self.push()

		if self.pushing:
			self.keep_pushing()

		self.intent = None

	def draw(self):
		pass


class Card(pygame.sprite.Sprite):
	def __init__(self, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.image, self.rect = None, None
		self.reload_image()

	def reload_image(self):
		self.image = const.EMPTY_CARD_IMAGE.copy()
		self.rect = self.image.get_rect(topleft=(const.CARD_LEFT, const.CARD_TOP))
		
	def add_treasure_image(self, treasure):
		treasure_image = const.TREASURE_IMAGES[treasure]
		self.reload_image()
		left = self.rect.width // 2 - const.TILESIZE // 2
		top = self.rect.height // 2 - const.TILESIZE // 2
		self.image.blit(treasure_image, (left, top))

	def set_homerun(self, player_id):
		marker_image = const.MARKER_IMAGES[player_id]
		self.reload_image()
		left = self.rect.width // 2 - const.TILESIZE // 2
		top = self.rect.height // 2 - const.TILESIZE // 2
		self.image.blit(marker_image, (left, top))


class ListenerThread(threading.Thread):
	def __init__(self, game, my_socket):
		threading.Thread.__init__(self)

		self.game = game
		self.my_socket = my_socket

	def run(self):
		while True:
			msg = self.my_socket.recv(1024)
			msg = pickle.loads(msg)

			sprite_type = msg[0]

			if sprite_type == 'Tile':
				board_x, board_y = msg[1], msg[2]
				intent = msg[3]

				tile = self.game.find_tile_by_board_coord(board_x, board_y)
				tile.intent = intent
				tile.update(self.game.dt)
				self.game.check_signals()

			elif sprite_type == 'Player':
				player_id = msg[1]
				intent = msg[2]

				player = self.game.find_player_by_id(player_id)
				player.intent = intent
				player.update(self.game.dt)
				self.game.check_signals()


class Arrow(pygame.sprite.Sprite):
	def __init__(self, board_x, board_y, orientation, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.board_x, self.board_y = board_x, board_y
		self.orientation = orientation
		self.blocked = False

		self.image = const.ARROW_NORMAL_IMAGES[self.orientation]
		self.rect = self.image.get_rect(topleft=(const.LEFTBOARDMARGIN + board_x * const.TILESIZE, const.TOPBOARDMARGIN + board_y * const.TILESIZE))

	def block(self):
		self.blocked = True
		self.image = const.ARROW_BLOCKED_IMAGES[self.orientation]

	def unblock(self):
		self.blocked = False
		self.image = const.ARROW_NORMAL_IMAGES[self.orientation]


class TextBox(pygame.sprite.Sprite):	
	def __init__(self, text, font, game, textbox_type, *groups, right=None, left=None, centerx=None, centery=None, top=None, bottom=None):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.font = font
		self.color = const.FONT_COLOR
		self.text = text
		self.image, self.rect = self.font.render(text, self.color)
		self.game = game
		self.textbox_type = textbox_type

		self.right = right
		self.left = left
		self.centerx = centerx
		self.centery = centery
		self.top = top
		self.bottom = bottom
	
		self.adjust_rect()

	def adjust_rect(self):
		if self.right:
			self.rect.right = self.right
		if self.left:
			self.rect.left = self.left
		if self.centerx:
			self.rect.centerx = self.centerx
		if self.centery:
			self.rect.centery = self.centery
		if self.top:
			self.rect.top = self.top
		if self.bottom:
			self.rect.bottom = self.bottom

	def change_text(self, new_text):
		self.image, self.rect = self.font.render(new_text, self.color)
		self.adjust_rect()

	def update(self, dt):
		msg = ''

		if self.textbox_type == const.TURN_REMINDER:
			if self.game.active_player.player_id == const.P1:
				msg += 'Player 1,'
			elif self.game.active_player.player_id == const.P2:
				msg += 'Player 2,'

			if self.game.state == const.TILE_MOVING_STATE:
				msg += ' move a tile!'
			elif self.game.state == const.PLAYER_MOVING_STATE:
				msg += ' move your character!'

		elif self.textbox_type == const.SCOREKEEPER_1:
			tot_treasures = const.TOT_TREASURES // len(self.game.allplayers)
			treasures_caught = tot_treasures - len(self.game.p1.treasures)

			msg += 'Player 1: '
			msg += str(treasures_caught)
			msg += ' / '
			msg += str(tot_treasures)

		elif self.textbox_type == const.SCOREKEEPER_2:
			tot_treasures = const.TOT_TREASURES // len(self.game.allplayers)
			treasures_caught = tot_treasures - len(self.game.p2.treasures)

			msg += 'Player 2: '
			msg += str(treasures_caught)
			msg += ' / '
			msg += str(tot_treasures)

		self.change_text(msg)


class Game:
	# Background image
	# BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'assets/images/backgrounds/')

	def __init__(self):
		# self.screen = pygame.display.set_mode((const.SCREENWIDTH, const.SCREENHEIGHT), pygame.FULLSCREEN)
		self.screen = pygame.display.set_mode((const.SCREENWIDTH, const.SCREENHEIGHT))
		self.clock = pygame.time.Clock()
		self.dt = 0
		self.fullscreen = False

		self.allsprites = pygame.sprite.Group()
		self.alltiles = pygame.sprite.Group()
		self.allplayers = pygame.sprite.Group()
		self.allcards = pygame.sprite.Group()
		self.allarrows = pygame.sprite.Group()
		self.alltextboxes = pygame.sprite.Group()

		self.print_order = [self.allarrows, self.allcards, self.alltiles, self.allplayers, self.alltextboxes]

		self.p1 = None
		self.p2 = None
		self.active_player = None
		self.side = None
		self.moving_tile = None
		self.last_push = None

		self.state = None

		self.client_socket = None

		self.setup()

	def toggle_fullscreen(self):
		self.fullscreen = not self.fullscreen

		if self.fullscreen:
			pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			pygame.mouse.set_visible(False)
		else:
			pygame.display.set_mode((const.SCREENWIDTH, const.SCREENHEIGHT))
			pygame.mouse.set_visible(True)

	def broadcast(self, message):
		self.client_socket.send(pickle.dumps(message))

	def find_player_by_id(self, player_id):
		for player in self.allplayers:
			if player.player_id == player_id:
				return player

		return None

	def start_server(self):
		self.side = const.P1

		# Setup to reset all states/variables to their starting state
		self.setup()

		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = socket.gethostname()
		port = 9999

		server_socket.bind((host, port))
		server_socket.listen()

		print('I set up a server, listening for a connection...')

		self.client_socket, client_address = server_socket.accept()

		print('I received a connection from: ' + str(client_address))

		# Send tiles
		tiles_to_send = []
		for tile in self.alltiles:
			tiles_to_send.append((tile.rect.top, tile.rect.left, tile.board_x, tile.board_y, tile.tiletype, tile.treasure))
		self.client_socket.send(pickle.dumps(tiles_to_send))

		# Receive confirmation
		while True:
			msg = self.client_socket.recv(1024).decode('ascii')
			if msg == 'TILES OK':
				break

		# Send players
		players_to_send = []
		for player in self.allplayers:
			players_to_send.append((player.player_id, player.board_x, player.board_y, player.treasures))
		self.client_socket.send(pickle.dumps(players_to_send))

		# Reload treasures on P1 (server player) to populate the card
		self.p1.set_treasures(self.p1.treasures)

		ListenerThread(self, self.client_socket).start()
	
	def start_client(self):
		self.side = const.P2

		# Setup to reset all states/variables to their starting state
		self.setup()

		# Manually remove the card on the client created by the setup() call above to avoid creating two cards
		for card in self.allcards:
			card.kill()

		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = socket.gethostname()
		port = 9999

		self.client_socket.connect((host, port))

		print('Connected to server: ' + str(host))

		# Receive tiles
		server_tiles = self.client_socket.recv(4096)
		server_tiles = pickle.loads(server_tiles)

		# Send confirmation message
		self.client_socket.send('TILES OK'.encode('ascii'))

		# Receive players
		server_players = self.client_socket.recv(4096)
		server_players = pickle.loads(server_players)

		# Synchronise tiles and players
		self.synchronise_clients(server_tiles, server_players)

		ListenerThread(self, self.client_socket).start()

	def synchronise_clients(self, new_tiles, new_players):
		# Tiles	
		for tile in self.alltiles:
			tile.kill()

		for tile in new_tiles:
			rect_x, rect_y = tile[1], tile[0]
			board_x, board_y = tile[2], tile[3]
			tiletype = tile[4]
			treasure = tile[5]

			new_tile = Tile(rect_x, rect_y, board_x, board_y, tiletype, self.allsprites, self.alltiles)
			new_tile.add_treasure(treasure)

			# Set the moving tile!
			if board_x in (-1, 7) or board_y in (-1, 7):
				self.moving_tile = new_tile

		# Players
		for player in self.allplayers:
			player.kill()
		self.p1 = None
		self.p2 = None

		for player in new_players:
			player_id = player[0]
			board_x, board_y = player[1], player[2]
			treasures = player[3]

			new_player = Player(player_id, board_x, board_y, self, self.allsprites, self.allplayers)
			new_player.set_treasures(treasures)

			if player_id == const.P1:
				self.p1 = new_player
			else:
				self.p2 = new_player

		# The markers were erased when killing the tiles at the start of this function
		self.add_markers_to_corner_tiles()

		self.active_player = self.p1

		print('Synchronization successful.')

	def find_tile_by_board_coord(self, board_x, board_y):
		for tile in self.alltiles:
			if tile.board_x == board_x and tile.board_y == board_y:
				return tile

		return None

	def get_all_treasures(self):
		return [const.TREASURE_1, const.TREASURE_2, const.TREASURE_3, const.TREASURE_4, const.TREASURE_5, const.TREASURE_6, const.TREASURE_7, const.TREASURE_8,
				const.TREASURE_9, const.TREASURE_10, const.TREASURE_11, const.TREASURE_12, const.TREASURE_13, const.TREASURE_14, const.TREASURE_15, const.TREASURE_16,
				const.TREASURE_17, const.TREASURE_18, const.TREASURE_19, const.TREASURE_20, const.TREASURE_21, const.TREASURE_22, const.TREASURE_23, const.TREASURE_24]

	def get_random_treasure(self, remaining_tiles=0, remaining_treasures=0):
		options = self.get_all_treasures()

		for tile in self.alltiles:
			if tile.treasure in options:
				options.remove(tile.treasure)

		if options:
			return random.choice(options)
		return None

	def create_fixed_tiles(self):
		tiles_that_need_treasure = []

		# Corners
		Tile(const.LEFTBOARDMARGIN + 0 * const.TILESIZE, const.TOPBOARDMARGIN + 0 * const.TILESIZE, 0, 0, const.BOTTOMRIGHT, self.allsprites, self.alltiles)
		Tile(const.LEFTBOARDMARGIN + 6 * const.TILESIZE, const.TOPBOARDMARGIN + 0 * const.TILESIZE, 6, 0, const.BOTTOMLEFT, self.allsprites, self.alltiles)
		Tile(const.LEFTBOARDMARGIN + 6 * const.TILESIZE, const.TOPBOARDMARGIN + 6 * const.TILESIZE, 6, 6, const.TOPLEFT, self.allsprites, self.alltiles)
		Tile(const.LEFTBOARDMARGIN + 0 * const.TILESIZE, const.TOPBOARDMARGIN + 6 * const.TILESIZE, 0, 6, const.TOPRIGHT, self.allsprites, self.alltiles)

		# Row 0
		tiles_that_need_treasure += (
		Tile(const.LEFTBOARDMARGIN + 2 * const.TILESIZE, const.TOPBOARDMARGIN + 0 * const.TILESIZE, 2, 0, const.BOTTOMRIGHTLEFT, self.allsprites, self.alltiles),
		Tile(const.LEFTBOARDMARGIN + 4 * const.TILESIZE, const.TOPBOARDMARGIN + 0 * const.TILESIZE, 4, 0, const.BOTTOMRIGHTLEFT, self.allsprites, self.alltiles)
		)

		# Row 2
		tiles_that_need_treasure += (
		Tile(const.LEFTBOARDMARGIN + 0 * const.TILESIZE, const.TOPBOARDMARGIN + 2 * const.TILESIZE, 0, 2, const.TOPBOTTOMRIGHT, self.allsprites, self.alltiles),
		Tile(const.LEFTBOARDMARGIN + 2 * const.TILESIZE, const.TOPBOARDMARGIN + 2 * const.TILESIZE, 2, 2, const.TOPBOTTOMRIGHT, self.allsprites, self.alltiles),
		Tile(const.LEFTBOARDMARGIN + 4 * const.TILESIZE, const.TOPBOARDMARGIN + 2 * const.TILESIZE, 4, 2, const.BOTTOMRIGHTLEFT, self.allsprites, self.alltiles),
		Tile(const.LEFTBOARDMARGIN + 6 * const.TILESIZE, const.TOPBOARDMARGIN + 2 * const.TILESIZE, 6, 2, const.TOPBOTTOMLEFT, self.allsprites, self.alltiles)
		)

		# Row 4
		tiles_that_need_treasure += (
		Tile(const.LEFTBOARDMARGIN + 0 * const.TILESIZE, const.TOPBOARDMARGIN + 4 * const.TILESIZE, 0, 4, const.TOPBOTTOMRIGHT, self.allsprites, self.alltiles),
		Tile(const.LEFTBOARDMARGIN + 2 * const.TILESIZE, const.TOPBOARDMARGIN + 4 * const.TILESIZE, 2, 4, const.TOPRIGHTLEFT, self.allsprites, self.alltiles),
		Tile(const.LEFTBOARDMARGIN + 4 * const.TILESIZE, const.TOPBOARDMARGIN + 4 * const.TILESIZE, 4, 4, const.TOPBOTTOMLEFT, self.allsprites, self.alltiles),
		Tile(const.LEFTBOARDMARGIN + 6 * const.TILESIZE, const.TOPBOARDMARGIN + 4 * const.TILESIZE, 6, 4, const.TOPBOTTOMLEFT, self.allsprites, self.alltiles)
		)

		# Row 6
		tiles_that_need_treasure += (
		Tile(const.LEFTBOARDMARGIN + 2 * const.TILESIZE, const.TOPBOARDMARGIN + 6 * const.TILESIZE, 2, 6, const.TOPRIGHTLEFT, self.allsprites, self.alltiles),
		Tile(const.LEFTBOARDMARGIN + 4 * const.TILESIZE, const.TOPBOARDMARGIN + 6 * const.TILESIZE, 4, 6, const.TOPRIGHTLEFT, self.allsprites, self.alltiles)
		)

		for tile in tiles_that_need_treasure:
			tile.add_treasure(self.get_random_treasure())

		self.add_markers_to_corner_tiles()
		
	def add_markers_to_corner_tiles(self):
		self.find_tile_by_board_coord(*const.PLAYER_STARTING_POSITIONS[const.P1]).add_marker(const.P1)
		self.find_tile_by_board_coord(*const.PLAYER_STARTING_POSITIONS[const.P2]).add_marker(const.P2)
		self.find_tile_by_board_coord(*const.PLAYER_STARTING_POSITIONS[const.P3]).add_marker(const.P3)
		self.find_tile_by_board_coord(*const.PLAYER_STARTING_POSITIONS[const.P4]).add_marker(const.P4)

	def create_moving_tiles(self):
		# TOPBOTTOM tiles never have treasures
		# TOPRIGHTLEFT tiles always have treasures
		# 6 / 15 TOPLEFT tiles have treasures

		moving_tiles = []
		moving_tiles += [const.TOPRIGHTLEFT for i in range(6)]
		moving_tiles += [const.TOPBOTTOM for i in range(13)]
		moving_tiles += [const.TOPLEFT for i in range(15)]
		tiles_with_potential_treasure = []

		for i in range(7):
			for j in range(7):
				if not self.find_tile_by_board_coord(i, j):
					tiletype = random.choice(moving_tiles)
					moving_tiles.remove(tiletype)

					new_tile = Tile(const.LEFTBOARDMARGIN + i * const.TILESIZE, const.TOPBOARDMARGIN + j * const.TILESIZE, i, j, 
									tiletype, self.allsprites, self.alltiles)
					if new_tile.tiletype == const.TOPRIGHTLEFT:
						new_tile.add_treasure(self.get_random_treasure())
					elif new_tile.tiletype == const.TOPLEFT:
						tiles_with_potential_treasure.append(new_tile)
					new_tile.rotate(random_rotation=True)

		last_tile = moving_tiles[0]
		self.moving_tile = Tile(const.LEFTBOARDMARGIN + 1 * const.TILESIZE, const.TOPBOARDMARGIN + 7 * const.TILESIZE, 1, 7, 
								last_tile, self.allsprites, self.alltiles)	
		if self.moving_tile.tiletype == const.TOPRIGHTLEFT:
			self.moving_tile.add_treasure(self.get_random_treasure())	
		elif self.moving_tile.tiletype == const.TOPLEFT:
			tiles_with_potential_treasure.append(self.moving_tile)
		self.moving_tile.rotate(random_rotation=True)

		random.shuffle(tiles_with_potential_treasure)
		for tile in tiles_with_potential_treasure:
			tile.add_treasure(self.get_random_treasure())
		
	def create_players(self):
		self.p1 = Player(const.P1, *const.PLAYER_STARTING_POSITIONS[const.P1], self, self.allsprites, self.allplayers)
		self.p2 = Player(const.P2, *const.PLAYER_STARTING_POSITIONS[const.P2], self, self.allsprites, self.allplayers)

		treasures = self.get_all_treasures()
		random.shuffle(treasures)

		self.p1.set_treasures(treasures[:12])
		self.p2.set_treasures(treasures[12:])

		self.active_player = self.p1

	def set_state(self, state):
		self.state = state

		if state == const.GAMEOVER_STATE:
			winner = 'Player 1' if self.active_player == self.p1 else 'Player 2'
			for textbox in self.alltextboxes:
				if textbox.textbox_type == const.TURN_REMINDER:
					reminder_textbox = textbox

			reminder_textbox.change_text(winner + ' won!!!')

	def create_arrows(self):
		topleft_tile = self.find_tile_by_board_coord(0, 0)
		topleft_x, topleft_y = topleft_tile.board_x, topleft_tile.board_y

		# Top row
		x, y = topleft_x + 1, topleft_y - 1
		for i in range(3):
			Arrow(x, y, const.DOWN, self.allsprites, self.allarrows)
			x += 2

		# Bottom row
		x, y = topleft_x + 1, topleft_y + 7
		for i in range(3):
			Arrow(x, y, const.UP, self.allsprites, self.allarrows)
			x += 2

		# Left column
		x, y = topleft_x - 1, topleft_y + 1
		for i in range(3):
			Arrow(x, y, const.RIGHT, self.allsprites, self.allarrows)
			y += 2

		# Right cloumn
		x, y = topleft_x + 7, topleft_y + 1
		for i in range(3):
			Arrow(x, y, const.LEFT, self.allsprites, self.allarrows)
			y += 2

	def create_reminder_textbox(self):
		last_tile = self.find_tile_by_board_coord(6, 0)
		top, left = last_tile.rect.top, last_tile.rect.left + const.TILESIZE * 2

		TextBox('', const.FONT, self, const.TURN_REMINDER, self.allsprites, self.alltextboxes, top=top, left=left)

	def create_score_textboxes(self):
		last_tile = self.find_tile_by_board_coord(6, 0)
		left = last_tile.rect.left + const.TILESIZE * 2

		top_1 = 600
		top_2 = top_1 + 100

		TextBox('score', const.FONT, self, const.SCOREKEEPER_1, self.allsprites, self.alltextboxes, top=top_1, left=left)
		TextBox('score', const.FONT, self, const.SCOREKEEPER_2, self.allsprites, self.alltextboxes, top=top_2, left=left)

	def setup(self):
		for sprite in self.allsprites:
			sprite.kill()
		self.p1, self.p2 = None, None
		self.last_push = None

		self.create_fixed_tiles()
		self.create_moving_tiles()
		self.create_players()
		self.create_arrows()
		self.create_reminder_textbox()
		self.create_score_textboxes()
		self.set_state(const.TILE_MOVING_STATE)	

	def quit(self):
		if self.client_socket:
			self.client_socket.close()
		pygame.quit()
		sys.exit()

	def get_players_to_push(self, tiles_to_push):
		players_to_push = []
		for tile in tiles_to_push:
			for player in self.allplayers:
				if (tile.board_x, tile.board_y) == (player.board_x, player.board_y):
					players_to_push.append(player)
		return players_to_push

	def is_push_legal(self):
		if not self.last_push:
			return True

		if (self.moving_tile.board_x, self.moving_tile.board_y) == (self.last_push[0], self.last_push[1]):
			return False
		return True

	def find_arrow_by_board_coord(self, board_x, board_y):
		for arrow in self.allarrows:
			if (arrow.board_x, arrow.board_y) == (board_x, board_y):
				return arrow
		return None

	def is_anything_pushing(self):
		for tile in self.alltiles:
			if tile.pushing:
				return True
		return False

	def set_last_push(self):
		# Last push will be the final position of the current moving (pushing) tile
		self.last_push = [self.moving_tile.board_x, self.moving_tile.board_y]
		if self.moving_tile.pushing[0]:
			self.last_push[0] += abs(self.moving_tile.pushing[0]) / self.moving_tile.pushing[0]
		if self.moving_tile.pushing[1]:
			self.last_push[1] += abs(self.moving_tile.pushing[1]) / self.moving_tile.pushing[1]

		for arrow in self.allarrows:
			if arrow.blocked:
				arrow.unblock()
				break

		blocked_arrow = self.find_arrow_by_board_coord(*self.last_push)
		blocked_arrow.block()

	def push_tiles(self):
		if not self.is_push_legal():
			const.ILLEGAL_PUSH_SOUND.play()
			return

		tiles_to_push = [self.moving_tile]

		# Down -> up
		if self.moving_tile.board_y == 7:
			for i in range(7):
				tiles_to_push.append(self.find_tile_by_board_coord(self.moving_tile.board_x, 6 - i))
			players_to_push = self.get_players_to_push(tiles_to_push)

			for tile in tiles_to_push:
				tile.pushing = [0, -const.TILESIZE]

			for player in players_to_push:
				player.pushing = [0, -const.TILESIZE]				

		# Up -> down
		elif self.moving_tile.board_y == -1:
			for i in range(7):
				tiles_to_push.append(self.find_tile_by_board_coord(self.moving_tile.board_x, i))
			players_to_push = self.get_players_to_push(tiles_to_push)

			for tile in tiles_to_push:
				tile.pushing = [0, const.TILESIZE]

			for player in players_to_push:
				player.pushing = [0, const.TILESIZE]				

		# Left -> right
		elif self.moving_tile.board_x == -1:
			for i in range(7):
				tiles_to_push.append(self.find_tile_by_board_coord(i, self.moving_tile.board_y))
			players_to_push = self.get_players_to_push(tiles_to_push)

			for tile in tiles_to_push:
				tile.pushing = [const.TILESIZE, 0]
				
			for player in players_to_push:
				player.pushing = [const.TILESIZE, 0]

		# Right -> left
		elif self.moving_tile.board_x == 7:
			for i in range(7):
				tiles_to_push.append(self.find_tile_by_board_coord(6 - i, self.moving_tile.board_y))
			players_to_push = self.get_players_to_push(tiles_to_push)

			for tile in tiles_to_push:
				tile.pushing = [-const.TILESIZE, 0]

			for player in players_to_push:
				player.pushing = [-const.TILESIZE, 0]

		self.moving_tile = tiles_to_push[-1]
		self.set_state(const.PLAYER_MOVING_STATE)

		self.set_last_push()
		const.MOVING_WALL_SOUND.play()

	def check_signals(self):
		if self.state == const.TILE_MOVING_STATE:
			if self.moving_tile.signal == const.PUSH_SIGNAL:
				self.push_tiles()

		elif self.state == const.PLAYER_MOVING_STATE:
			if self.active_player.signal == const.CONFIRM_MOVEMENT_SIGNAL:
				if self.active_player == self.p1:
					self.active_player = self.p2
				else:
					self.active_player = self.p1
				self.set_state(const.TILE_MOVING_STATE)

			elif self.active_player.signal == const.VICTORY_SIGNAL:
				self.set_state(const.GAMEOVER_STATE)

	def check_broadcasts(self):
		if not self.client_socket:
			return

		for tile in self.alltiles:
			if tile.broadcast:
				self.broadcast(tile.broadcast)
				tile.reset_broadcast()
		for player in self.allplayers:
			if player.broadcast:
				self.broadcast(player.broadcast)
				player.reset_broadcast()

	def update(self):
		if self.state != const.GAMEOVER_STATE:
			self.allsprites.update(self.dt)
			self.check_signals()
			self.check_broadcasts()

	def draw(self):
		self.screen.blit(const.BACKGROUND_IMAGE, (0, 0))
		for sprite_group in self.print_order:
			sprite_group.draw(self.screen)

		pygame.display.flip()

	def process_keyboard_input(self, key):
		if key == pygame.K_ESCAPE:
			self.quit()
		elif key == pygame.K_w:
			self.toggle_fullscreen()
		elif key == pygame.K_d:
			import pdb; pdb.set_trace()
		elif key == pygame.K_r and not self.side:
			self.setup()
		elif key == pygame.K_s and not self.side:
			self.start_server()
		elif key == pygame.K_c and not self.side:
				self.start_client()
		
		if self.state == const.TILE_MOVING_STATE:
			if key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE, pygame.K_RETURN):
				if not self.side or self.side == self.active_player.player_id:
					self.moving_tile.process_keyboard_input(key)
		elif self.state == const.PLAYER_MOVING_STATE:
			if key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE, pygame.K_RETURN):
				if not self.side or self.side == self.active_player.player_id:
					self.active_player.process_keyboard_input(key)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.KEYDOWN:
					self.process_keyboard_input(event.key)

			self.update()
			self.draw()
			self.dt = self.clock.tick(const.FPS)


if __name__ == '__main__':
	Game().run()