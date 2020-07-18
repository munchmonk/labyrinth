#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import pygame
import sys
import random
import socket
import pickle
import threading


class Tile(pygame.sprite.Sprite):
	TILESIZE = 84

	DUMMY = 'DUMMY'

	# Movement
	RIGHT = 'RIGHT'
	LEFT = 'LEFT'
	UP = 'UP'
	DOWN = 'DOWN'
	ROTATE = 'ROTATE'

	# Signals
	PUSH = 'PUSH'

	# Tile orientation
	TOP = 'TOP'
	BOTTOM = 'BOTTOM'

	TOPBOTTOM = 'TOPBOTTOM'
	RIGHTLEFT = 'RIGHTLEFT'

	TOPRIGHT = 'TOPRIGHT'
	BOTTOMRIGHT = 'BOTTOMRIGHT'
	BOTTOMLEFT = 'BOTTOMLEFT'
	TOPLEFT = 'TOPLEFT'

	TOPRIGHTLEFT = 'TOPRIGHTLEFT'
	TOPBOTTOMRIGHT = 'TOPBOTTOMRIGHT'
	BOTTOMRIGHTLEFT = 'BOTTOMRIGHTLEFT'
	TOPBOTTOMLEFT = 'TOPBOTTOMLEFT'

	# Treasures
	TREASURE_1 = 'TREASURE_1'
	TREASURE_2 = 'TREASURE_2'
	TREASURE_3 = 'TREASURE_3'
	TREASURE_4 = 'TREASURE_4'
	TREASURE_5 = 'TREASURE_5'
	TREASURE_6 = 'TREASURE_6'
	TREASURE_7 = 'TREASURE_7'
	TREASURE_8 = 'TREASURE_8'
	TREASURE_9 = 'TREASURE_9'
	TREASURE_10 = 'TREASURE_10'
	TREASURE_11 = 'TREASURE_11'
	TREASURE_12 = 'TREASURE_12'
	TREASURE_13 = 'TREASURE_13'
	TREASURE_14 = 'TREASURE_14'
	TREASURE_15 = 'TREASURE_15'
	TREASURE_16 = 'TREASURE_16'
	TREASURE_17 = 'TREASURE_17'
	TREASURE_18 = 'TREASURE_18'
	TREASURE_19 = 'TREASURE_19'
	TREASURE_20 = 'TREASURE_20'
	TREASURE_21 = 'TREASURE_21'
	TREASURE_22 = 'TREASURE_22'
	TREASURE_23 = 'TREASURE_23'
	TREASURE_24 = 'TREASURE_24'

	TILE_IMAGES =  {TOPRIGHT: pygame.image.load('tiles/topright.jpeg'),
					BOTTOMRIGHT: pygame.image.load('tiles/bottomright.jpeg'),
					BOTTOMLEFT: pygame.image.load('tiles/bottomleft.jpeg'),
					TOPLEFT: pygame.image.load('tiles/topleft.jpeg'),

					TOPRIGHTLEFT: pygame.image.load('tiles/toprightleft.jpeg'),
					TOPBOTTOMRIGHT: pygame.image.load('tiles/topbottomright.jpeg'),
					BOTTOMRIGHTLEFT: pygame.image.load('tiles/bottomrightleft.jpeg'),
					TOPBOTTOMLEFT: pygame.image.load('tiles/topbottomleft.jpeg'),

					TOPBOTTOM: pygame.image.load('tiles/topbottom.jpeg'),
					RIGHTLEFT: pygame.image.load('tiles/rightleft.jpeg'),
					}

	TREASURE_IMAGES =  {TREASURE_1: pygame.image.load('treasures/treasure_1.png'),
						TREASURE_2: pygame.image.load('treasures/treasure_2.png'),
						TREASURE_3: pygame.image.load('treasures/treasure_3.png'),
						TREASURE_4: pygame.image.load('treasures/treasure_4.png'),
						TREASURE_5: pygame.image.load('treasures/treasure_5.png'),
						TREASURE_6: pygame.image.load('treasures/treasure_6.png'),
						TREASURE_7: pygame.image.load('treasures/treasure_7.png'),
						TREASURE_8: pygame.image.load('treasures/treasure_8.png'),
						TREASURE_9: pygame.image.load('treasures/treasure_9.png'),
						TREASURE_10: pygame.image.load('treasures/treasure_10.png'),
						TREASURE_11: pygame.image.load('treasures/treasure_11.png'),
						TREASURE_12: pygame.image.load('treasures/treasure_12.png'),
						TREASURE_13: pygame.image.load('treasures/treasure_13.png'),
						TREASURE_14: pygame.image.load('treasures/treasure_14.png'),
						TREASURE_15: pygame.image.load('treasures/treasure_15.png'),
						TREASURE_16: pygame.image.load('treasures/treasure_16.png'),
						TREASURE_17: pygame.image.load('treasures/treasure_17.png'),
						TREASURE_18: pygame.image.load('treasures/treasure_18.png'),
						TREASURE_19: pygame.image.load('treasures/treasure_19.png'),
						TREASURE_20: pygame.image.load('treasures/treasure_20.png'),
						TREASURE_21: pygame.image.load('treasures/treasure_21.png'),
						TREASURE_22: pygame.image.load('treasures/treasure_22.png'),
						TREASURE_23: pygame.image.load('treasures/treasure_23.png'),
						TREASURE_24: pygame.image.load('treasures/treasure_24.png')}


	def __init__(self, rect_x, rect_y, board_x, board_y, tiletype, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.tiletype = tiletype
		self.treasure = None

		self.image = None
		self.set_image()
		self.rect = self.image.get_rect(topleft=(rect_x, rect_y))

		self.board_x, self.board_y = board_x, board_y

		self.right_open = False
		self.left_open = False
		self.top_open = False
		self.bottom_open = False
		self.set_borders()

		self.intent = None
		self.signal = None

		self.broadcast = None

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

		if Tile.RIGHT in self.tiletype:
			self.right_open = True
		if Tile.LEFT in self.tiletype:
			self.left_open = True
		if Tile.TOP in self.tiletype:
			self.top_open = True
		if Tile.BOTTOM in self.tiletype:
			self.bottom_open = True

	def set_image(self):
		self.image = Tile.TILE_IMAGES[self.tiletype]
		self.add_treasure_image()

	def add_treasure_image(self):
		if self.treasure:
			self.image = self.image.copy()
			self.image.blit(Tile.TREASURE_IMAGES[self.treasure], (0, 0))

	def process_keyboard_input(self, key):
		if self.board_y in (-1, 7) and key == pygame.K_RIGHT:
			self.intent = Tile.RIGHT
		elif self.board_y in (-1, 7) and key == pygame.K_LEFT:
			self.intent = Tile.LEFT
		elif self.board_x in (-1, 7) and key == pygame.K_UP:
			self.intent = Tile.UP
		elif self.board_x in (-1, 7) and key == pygame.K_DOWN:
			self.intent = Tile.DOWN
		elif key == pygame.K_SPACE:
			self.intent = Tile.ROTATE
		elif key == pygame.K_RETURN:
			self.intent = Tile.PUSH

		self.set_broadcast()


	def set_broadcast(self):
		if self.intent:
			self.broadcast = ('Tile', self.board_x, self.board_y, self.intent)

	def reset_broadcast(self):
		self.broadcast = None

	def push(self):
		self.signal = Tile.PUSH

	def move(self):
		# Move
		if self.intent == Tile.RIGHT:
			self.board_x += 2
			self.rect.x += 2 * Tile.TILESIZE
		elif self.intent == Tile.LEFT:
			self.board_x -= 2
			self.rect.x -= 2 * Tile.TILESIZE
		elif self.intent == Tile.UP:
			self.board_y -= 2
			self.rect.y -= 2 * Tile.TILESIZE
		elif self.intent == Tile.DOWN:
			self.board_y += 2
			self.rect.y += 2 * Tile.TILESIZE

		# Check if moved beyond board edges
		if (self.board_x, self.board_y) == (-1, -1):
			if self.intent == Tile.UP:
				self.board_x += 2
				self.rect.x += 2 * Tile.TILESIZE
			elif self.intent == Tile.LEFT:
				self.board_y += 2
				self.rect.y += 2 * Tile.TILESIZE
		elif (self.board_x, self.board_y) == (7, -1):
			if self.intent == Tile.UP:
				self.board_x -= 2
				self.rect.x -= 2 * Tile.TILESIZE
			elif self.intent == Tile.RIGHT:
				self.board_y += 2
				self.rect.y += 2 * Tile.TILESIZE
		elif (self.board_x, self.board_y) == (7, 7):
			if self.intent == Tile.DOWN:
				self.board_x -= 2
				self.rect.x -= 2 * Tile.TILESIZE
			elif self.intent == Tile.RIGHT:
				self.board_y -= 2
				self.rect.y -= 2 * Tile.TILESIZE
		elif (self.board_x, self.board_y) == (-1, 7):
			if self.intent == Tile.DOWN:
				self.board_x += 2
				self.rect.x += 2 * Tile.TILESIZE
			elif self.intent == Tile.LEFT:
				self.board_y -= 2
				self.rect.y -= 2 * Tile.TILESIZE

	def rotate(self, random_rotation=False):
		bucket1 = [Tile.TOPBOTTOM, Tile.RIGHTLEFT]
		bucket2 = [Tile.TOPRIGHT, Tile.BOTTOMRIGHT, Tile.BOTTOMLEFT, Tile.TOPLEFT]
		bucket3 = [Tile.TOPRIGHTLEFT, Tile.TOPBOTTOMRIGHT, Tile.BOTTOMRIGHTLEFT, Tile.TOPBOTTOMLEFT]

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

		if self.intent in (Tile.UP, Tile.DOWN, Tile.RIGHT, Tile.LEFT):
			self.move()
		elif self.intent == Tile.ROTATE:
			self.rotate()
		elif self.intent == Tile.PUSH:
			self.push()

		self.intent = None

	def draw(self):
		pass


class Card(pygame.sprite.Sprite):
	EMPTY_CARD_PATH = 'cards/empty_card.png'
	TOP = 100
	LEFT = 800

	def __init__(self, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.image, self.rect = None, None
		self.reload_image()

	def reload_image(self):
		self.image = pygame.image.load(Card.EMPTY_CARD_PATH)
		self.rect = self.image.get_rect(topleft=(Card.LEFT, Card.TOP))
		
	def add_treasure_image(self, treasure):
		treasure_image = Tile.TREASURE_IMAGES[treasure]
		self.reload_image()
		left = self.rect.width // 2 - Tile.TILESIZE // 2
		top = self.rect.height // 2 - Tile.TILESIZE // 2
		self.image.blit(treasure_image, (left, top))		

	def update(self, dt):
		pass

	def draw(self):
		pass

class Player(pygame.sprite.Sprite):
	P1, P2 = 'P1', 'P2'
	IMAGES =   {P1: pygame.image.load('players/p1.png'),
				P2: pygame.image.load('players/p2.png')}

	# Movement
	RIGHT = 'RIGHT'
	LEFT = 'LEFT'
	UP = 'UP'
	DOWN = 'DOWN'

	# Signals
	CONFIRM_MOVEMENT = 'CONFIRM_MOVEMENT'

	def __init__(self, player_id, board_x, board_y, game, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.game = game

		self.board_x, self.board_y = board_x, board_y
		self.player_id = player_id

		self.image = Player.IMAGES[self.player_id]
		self.rect = self.image.get_rect(topleft=(Game.LEFTBOARDMARGIN + Tile.TILESIZE * self.board_x, Game.TOPBOARDMARGIN + Tile.TILESIZE * self.board_y))

		self.tile = None
		self.set_tile()

		self.treasures = []
		self.current_treasure_objective = None
		
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
		if key == pygame.K_RIGHT:
			self.intent = Player.RIGHT
		elif key == pygame.K_LEFT:
			self.intent = Player.LEFT
		elif key == pygame.K_UP:
			self.intent = Player.UP
		elif key == pygame.K_DOWN:
			self.intent = Player.DOWN
		elif key == pygame.K_RETURN:
			self.intent = Player.CONFIRM_MOVEMENT

		self.set_broadcast()

	def move(self):
		if (self.intent == Player.RIGHT and self.board_x < 6 and self.tile.right_open and
			self.game.find_tile_by_board_coord(self.board_x + 1, self.board_y).left_open):
				self.board_x += 1
				self.set_tile()
				self.rect.x += Tile.TILESIZE
		elif (self.intent == Player.LEFT and self.board_x > 0 and self.tile.left_open and
			self.game.find_tile_by_board_coord(self.board_x - 1, self.board_y).right_open):
				self.board_x -= 1
				self.set_tile()
				self.rect.x -= Tile.TILESIZE
		elif (self.intent == Player.UP and self.board_y > 0 and self.tile.top_open and
			self.game.find_tile_by_board_coord(self.board_x, self.board_y - 1).bottom_open):
				self.board_y -= 1
				self.set_tile()
				self.rect.y -= Tile.TILESIZE
		elif (self.intent == Player.DOWN and self.board_y < 6 and self.tile.bottom_open and
			self.game.find_tile_by_board_coord(self.board_x, self.board_y + 1).top_open):
				self.board_y += 1
				self.set_tile()
				self.rect.y += Tile.TILESIZE

	def start_homerun(self):
		# ---- to be continued -----
		self.signal = Player.ALL_TREASURES_TAKEN

	def check_treasure_collision(self):
		if self.current_treasure_objective == self.tile.treasure:
			self.tile.remove_treasure()

			print(self.player_id, ' obtained ', self.current_treasure_objective, '!')

			self.treasures.pop(0)
			if not self.treasures:
				self.start_homerun()
			else:
				self.current_treasure_objective = self.treasures[0]
				if self.card:
					self.card.add_treasure_image(self.current_treasure_objective)

	def set_tile(self):
		self.tile = self.game.find_tile_by_board_coord(self.board_x, self.board_y)

	def confirm_movement(self):
		self.signal = Player.CONFIRM_MOVEMENT

	def update(self, dt):
		self.signal = None

		if self.intent in (Player.UP, Player.DOWN, Player.RIGHT, Player.LEFT):
			self.move()
		elif self.intent == Player.CONFIRM_MOVEMENT:
			self.confirm_movement()

		if self.signal == Player.CONFIRM_MOVEMENT:
			self.check_treasure_collision()

		self.intent = None

	def draw(self):
		pass


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
	BASEIMAGES =   [pygame.image.load('assets/arrow.png'),
					pygame.image.load('assets/blocked_arrow.png')]

	NORMAL_IMAGES =     {Tile.UP: BASEIMAGES[0],
						Tile.RIGHT: pygame.transform.rotate(BASEIMAGES[0], 270),
						Tile.DOWN: pygame.transform.rotate(BASEIMAGES[0], 180),
						Tile.LEFT: pygame.transform.rotate(BASEIMAGES[0], 90),
						}

	BLOCKED_IMAGES =   {Tile.UP: BASEIMAGES[1],
						Tile.RIGHT: pygame.transform.rotate(BASEIMAGES[1], 270),
						Tile.DOWN: pygame.transform.rotate(BASEIMAGES[1], 180),
						Tile.LEFT: pygame.transform.rotate(BASEIMAGES[1], 90),
						}


	def __init__(self, board_x, board_y, orientation, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)

		self.board_x, self.board_y = board_x, board_y
		self.orientation = orientation
		self.blocked = False

		self.image = Arrow.NORMAL_IMAGES[self.orientation]
		self.rect = self.image.get_rect(topleft=(Game.LEFTBOARDMARGIN + board_x * Tile.TILESIZE, Game.TOPBOARDMARGIN + board_y * Tile.TILESIZE))

	def block(self):
		self.blocked = True
		self.image = Arrow.BLOCKED_IMAGES[self.orientation]

	def unblock(self):
		self.blocked = False
		self.image = Arrow.NORMAL_IMAGES[self.orientation]


class Game:
	FPS = 45
	SCRENWIDTH = 1280
	SCREEHEIGHT = 768
	LEFTBOARDMARGIN = Tile.TILESIZE
	TOPBOARDMARGIN = Tile.TILESIZE

	# States
	TILE_MOVING_STATE = 'TILE_MOVING_STATE'
	PLAYER_MOVING_STATE = 'PLAYER_MOVING_STATE'

	def __init__(self):
		# self.screen = pygame.display.set_mode((Game.SCRENWIDTH, Game.SCREEHEIGHT), pygame.FULLSCREEN)
		self.screen = pygame.display.set_mode((Game.SCRENWIDTH, Game.SCREEHEIGHT))
		self.clock = pygame.time.Clock()
		self.dt = 0

		self.allsprites = pygame.sprite.Group()
		self.alltiles = pygame.sprite.Group()
		self.allplayers = pygame.sprite.Group()
		self.allcards = pygame.sprite.Group()
		self.allarrows = pygame.sprite.Group()

		self.print_order = [self.allarrows, self.allcards, self.alltiles, self.allplayers]

		self.p1 = None
		self.p2 = None
		self.active_player = None
		self.side = None
		self.moving_tile = None
		self.last_push = None

		self.state = None

		self.client_socket = None

		self.setup()

	def broadcast(self, message):
		self.client_socket.send(pickle.dumps(message))

	def find_player_by_id(self, player_id):
		for player in self.allplayers:
			if player.player_id == player_id:
				return player

		return None

	def start_server(self):
		self.side = Player.P1

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
		print('server, cards: ', self.allcards)
		self.p1.set_treasures(self.p1.treasures)
		print('server, cards: ', self.allcards)

		ListenerThread(self, self.client_socket).start()
	
	def start_client(self):
		self.side = Player.P2

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

			if player_id == Player.P1:
				self.p1 = new_player
			else:
				self.p2 = new_player

		self.active_player = self.p1

		print('Synchronization successful.')

	def find_tile_by_board_coord(self, board_x, board_y):
		for tile in self.alltiles:
			if tile.board_x == board_x and tile.board_y == board_y:
				return tile

		return None

	def get_all_treasures(self):
		return [Tile.TREASURE_1, Tile.TREASURE_2, Tile.TREASURE_3, Tile.TREASURE_4, Tile.TREASURE_5, Tile.TREASURE_6, Tile.TREASURE_7, Tile.TREASURE_8,
				Tile.TREASURE_9, Tile.TREASURE_10, Tile.TREASURE_11, Tile.TREASURE_12, Tile.TREASURE_13, Tile.TREASURE_14, Tile.TREASURE_15, Tile.TREASURE_16,
				Tile.TREASURE_17, Tile.TREASURE_18, Tile.TREASURE_19, Tile.TREASURE_20, Tile.TREASURE_21, Tile.TREASURE_22, Tile.TREASURE_23, Tile.TREASURE_24]

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
		Tile(Game.LEFTBOARDMARGIN + 0 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 0 * Tile.TILESIZE, 0, 0, Tile.BOTTOMRIGHT, self.allsprites, self.alltiles)
		Tile(Game.LEFTBOARDMARGIN + 6 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 0 * Tile.TILESIZE, 6, 0, Tile.BOTTOMLEFT, self.allsprites, self.alltiles)
		Tile(Game.LEFTBOARDMARGIN + 6 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 6 * Tile.TILESIZE, 6, 6, Tile.TOPLEFT, self.allsprites, self.alltiles)
		Tile(Game.LEFTBOARDMARGIN + 0 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 6 * Tile.TILESIZE, 0, 6, Tile.TOPRIGHT, self.allsprites, self.alltiles)

		# Row 0
		tiles_that_need_treasure += (
		Tile(Game.LEFTBOARDMARGIN + 2 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 0 * Tile.TILESIZE, 2, 0, Tile.BOTTOMRIGHTLEFT, self.allsprites, self.alltiles),
		Tile(Game.LEFTBOARDMARGIN + 4 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 0 * Tile.TILESIZE, 4, 0, Tile.BOTTOMRIGHTLEFT, self.allsprites, self.alltiles)
		)

		# Row 2
		tiles_that_need_treasure += (
		Tile(Game.LEFTBOARDMARGIN + 0 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 2 * Tile.TILESIZE, 0, 2, Tile.TOPBOTTOMRIGHT, self.allsprites, self.alltiles),
		Tile(Game.LEFTBOARDMARGIN + 2 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 2 * Tile.TILESIZE, 2, 2, Tile.TOPBOTTOMRIGHT, self.allsprites, self.alltiles),
		Tile(Game.LEFTBOARDMARGIN + 4 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 2 * Tile.TILESIZE, 4, 2, Tile.BOTTOMRIGHTLEFT, self.allsprites, self.alltiles),
		Tile(Game.LEFTBOARDMARGIN + 6 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 2 * Tile.TILESIZE, 6, 2, Tile.TOPBOTTOMLEFT, self.allsprites, self.alltiles)
		)

		# Row 4
		tiles_that_need_treasure += (
		Tile(Game.LEFTBOARDMARGIN + 0 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 4 * Tile.TILESIZE, 0, 4, Tile.TOPBOTTOMRIGHT, self.allsprites, self.alltiles),
		Tile(Game.LEFTBOARDMARGIN + 2 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 4 * Tile.TILESIZE, 2, 4, Tile.TOPRIGHTLEFT, self.allsprites, self.alltiles),
		Tile(Game.LEFTBOARDMARGIN + 4 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 4 * Tile.TILESIZE, 4, 4, Tile.TOPBOTTOMLEFT, self.allsprites, self.alltiles),
		Tile(Game.LEFTBOARDMARGIN + 6 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 4 * Tile.TILESIZE, 6, 4, Tile.TOPBOTTOMLEFT, self.allsprites, self.alltiles)
		)

		# Row 6
		tiles_that_need_treasure += (
		Tile(Game.LEFTBOARDMARGIN + 2 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 6 * Tile.TILESIZE, 2, 6, Tile.TOPRIGHTLEFT, self.allsprites, self.alltiles),
		Tile(Game.LEFTBOARDMARGIN + 4 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 6 * Tile.TILESIZE, 4, 6, Tile.TOPRIGHTLEFT, self.allsprites, self.alltiles)
		)

		for tile in tiles_that_need_treasure:
			tile.add_treasure(self.get_random_treasure())

	def create_moving_tiles(self):
		# TOPBOTTOM tiles never have treasures
		# TOPRIGHTLEFT tiles always have treasures
		# 6 / 15 TOPLEFT tiles have treasures

		moving_tiles = []
		moving_tiles += [Tile.TOPRIGHTLEFT for i in range(6)]
		moving_tiles += [Tile.TOPBOTTOM for i in range(13)]
		moving_tiles += [Tile.TOPLEFT for i in range(15)]
		tiles_with_potential_treasure = []

		for i in range(7):
			for j in range(7):
				if not self.find_tile_by_board_coord(i, j):
					tiletype = random.choice(moving_tiles)
					moving_tiles.remove(tiletype)

					new_tile = Tile(Game.LEFTBOARDMARGIN + i * Tile.TILESIZE, Game.TOPBOARDMARGIN + j * Tile.TILESIZE, i, j, 
									tiletype, self.allsprites, self.alltiles)
					if new_tile.tiletype == Tile.TOPRIGHTLEFT:
						new_tile.add_treasure(self.get_random_treasure())
					elif new_tile.tiletype == Tile.TOPLEFT:
						tiles_with_potential_treasure.append(new_tile)
					new_tile.rotate(random_rotation=True)

		last_tile = moving_tiles[0]
		self.moving_tile = Tile(Game.LEFTBOARDMARGIN + 1 * Tile.TILESIZE, Game.TOPBOARDMARGIN + 7 * Tile.TILESIZE, 1, 7, 
								last_tile, self.allsprites, self.alltiles)	
		if self.moving_tile.tiletype == Tile.TOPRIGHTLEFT:
			self.moving_tile.add_treasure(self.get_random_treasure())	
		elif self.moving_tile.tiletype == Tile.TOPLEFT:
			tiles_with_potential_treasure.append(self.moving_tile)
		self.moving_tile.rotate(random_rotation=True)

		random.shuffle(tiles_with_potential_treasure)
		for tile in tiles_with_potential_treasure:
			tile.add_treasure(self.get_random_treasure())
		
	def create_players(self):
		self.p1 = Player(Player.P1, 0, 6, self, self.allsprites, self.allplayers)
		self.p2 = Player(Player.P2, 6, 0, self, self.allsprites, self.allplayers)

		treasures = self.get_all_treasures()
		random.shuffle(treasures)

		self.p1.set_treasures(treasures[:12])
		self.p2.set_treasures(treasures[12:])

		self.active_player = self.p1

	def set_state(self, state):
		self.state = state

		if state == Game.TILE_MOVING_STATE:
			pass
		elif state == Game.PLAYER_MOVING_STATE:
			pass

	def create_arrows(self):
		topleft_tile = self.find_tile_by_board_coord(0, 0)
		topleft_x, topleft_y = topleft_tile.board_x, topleft_tile.board_y

		# Top row
		x, y = topleft_x + 1, topleft_y - 1
		for i in range(3):
			Arrow(x, y, Tile.DOWN, self.allsprites, self.allarrows)
			x += 2

		# Bottom row
		x, y = topleft_x + 1, topleft_y + 7
		for i in range(3):
			Arrow(x, y, Tile.UP, self.allsprites, self.allarrows)
			x += 2

		# Left column
		x, y = topleft_x - 1, topleft_y + 1
		for i in range(3):
			Arrow(x, y, Tile.RIGHT, self.allsprites, self.allarrows)
			y += 2

		# Right cloumn
		x, y = topleft_x + 7, topleft_y + 1
		for i in range(3):
			Arrow(x, y, Tile.LEFT, self.allsprites, self.allarrows)
			y += 2

	def setup(self):
		for sprite in self.allsprites:
			sprite.kill()
		self.p1, self.p2 = None, None
		self.last_push = None

		self.create_fixed_tiles()
		self.create_moving_tiles()
		self.create_players()
		self.create_arrows()
		self.set_state(Game.TILE_MOVING_STATE)

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

	def set_last_push(self):
		self.last_push = self.moving_tile.board_x, self.moving_tile.board_y

		for arrow in self.allarrows:
			if arrow.blocked:
				arrow.unblock()
				break

		blocked_arrow = self.find_arrow_by_board_coord(*self.last_push)
		blocked_arrow.block()


	def push_tiles(self):
		if not self.is_push_legal():
			return

		# self.set_last_push()
		tiles_to_push = [self.moving_tile]

		# Down -> up
		if self.moving_tile.board_y == 7:
			for i in range(7):
				tiles_to_push.append(self.find_tile_by_board_coord(self.moving_tile.board_x, 6 - i))
			players_to_push = self.get_players_to_push(tiles_to_push)

			for tile in tiles_to_push:
				tile.board_y -= 1
				tile.rect.y -= Tile.TILESIZE
			for player in players_to_push:
				player.board_y -= 1
				player.rect.y -= Tile.TILESIZE
				if player.board_y == -1:
					player.board_y = 6
					player.rect.y += 7 * Tile.TILESIZE

		# Up -> down
		elif self.moving_tile.board_y == -1:
			for i in range(7):
				tiles_to_push.append(self.find_tile_by_board_coord(self.moving_tile.board_x, i))
			players_to_push = self.get_players_to_push(tiles_to_push)

			for tile in tiles_to_push:
				tile.board_y += 1
				tile.rect.y += Tile.TILESIZE
			for player in players_to_push:
				player.board_y += 1
				player.rect.y += Tile.TILESIZE
				if player.board_y == 7:
					player.board_y = 0
					player.rect.y -= 7 * Tile.TILESIZE

		# Left -> right
		elif self.moving_tile.board_x == -1:
			for i in range(7):
				tiles_to_push.append(self.find_tile_by_board_coord(i, self.moving_tile.board_y))
			players_to_push = self.get_players_to_push(tiles_to_push)

			for tile in tiles_to_push:
				tile.board_x += 1
				tile.rect.x += Tile.TILESIZE
			for player in players_to_push:
				player.board_x += 1
				player.rect.x += Tile.TILESIZE
				if player.board_x == 7:
					player.board_x = 0
					player.rect.x -= 7 * Tile.TILESIZE

		# Right -> left
		elif self.moving_tile.board_x == 7:
			for i in range(7):
				tiles_to_push.append(self.find_tile_by_board_coord(6 - i, self.moving_tile.board_y))
			players_to_push = self.get_players_to_push(tiles_to_push)

			for tile in tiles_to_push:
				tile.board_x -= 1
				tile.rect.x -= Tile.TILESIZE
			for player in players_to_push:
				player.board_x -= 1
				player.rect.x -= Tile.TILESIZE
				if player.board_x == -1:
					player.board_x = 6
					player.rect.x += 7 * Tile.TILESIZE

		self.moving_tile = tiles_to_push[-1]
		self.set_state(Game.PLAYER_MOVING_STATE)

		self.set_last_push()

	def check_signals(self):
		if self.state == Game.TILE_MOVING_STATE:
			if self.moving_tile.signal == Tile.PUSH:
				self.push_tiles()
		elif self.state == Game.PLAYER_MOVING_STATE:
			if self.active_player.signal == Player.CONFIRM_MOVEMENT:
				if self.active_player == self.p1:
					self.active_player = self.p2
				else:
					self.active_player = self.p1
				self.set_state(Game.TILE_MOVING_STATE)

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
		self.allsprites.update(self.dt)
		self.check_signals()
		self.check_broadcasts()

	def draw(self):
		self.screen.fill((0, 0, 0))

		for sprite_group in self.print_order:
			sprite_group.draw(self.screen)

		pygame.display.flip()

	def process_keyboard_input(self, key):
		if key == pygame.K_ESCAPE:
			self.quit()
		elif key == pygame.K_r:
			self.setup()
		elif key == pygame.K_s:
			self.start_server()
		elif key == pygame.K_c:
			self.start_client()
		
		if self.state == Game.TILE_MOVING_STATE:
			if key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE, pygame.K_RETURN):
				if not self.side or self.side == self.active_player.player_id:
					self.moving_tile.process_keyboard_input(key)
		elif self.state == Game.PLAYER_MOVING_STATE:
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
			self.dt = self.clock.tick(Game.FPS)


if __name__ == '__main__':
	Game().run()