#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import pygame
import sys
import random


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

	# Images
	BASETILES =    {TOPRIGHT: pygame.image.load('tiles/big_topright.png'),
					TOPRIGHTLEFT: pygame.image.load('tiles/big_toprightleft.png'),
					TOPBOTTOM: pygame.image.load('tiles/big_topdown.png')}

	TILE_IMAGES =  {TOPRIGHT: BASETILES[TOPRIGHT],
					BOTTOMRIGHT: pygame.transform.rotate(BASETILES[TOPRIGHT], 270),
					BOTTOMLEFT: pygame.transform.rotate(BASETILES[TOPRIGHT], 180),
					TOPLEFT: pygame.transform.rotate(BASETILES[TOPRIGHT], 90),

					TOPRIGHTLEFT: BASETILES[TOPRIGHTLEFT],
					TOPBOTTOMRIGHT: pygame.transform.rotate(BASETILES[TOPRIGHTLEFT], 270),
					BOTTOMRIGHTLEFT: pygame.transform.rotate(BASETILES[TOPRIGHTLEFT], 180),
					TOPBOTTOMLEFT: pygame.transform.rotate(BASETILES[TOPRIGHTLEFT], 90),

					TOPBOTTOM: BASETILES[TOPBOTTOM],
					RIGHTLEFT: pygame.transform.rotate(BASETILES[TOPBOTTOM], 90),

					DUMMY: pygame.image.load('tiles/dummy.png')
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

	def add_treasure(self, treasure):
		if not treasure:
			return
		self.treasure = treasure
		self.add_treasure_image()
	
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

		self.intent = None
		self.signal = None

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


			print(self.player_id, ' obtained ', self.current_treasure_objective, '!')


			self.treasures.pop(0)
			if not self.treasures:
				self.start_homerun()
			else:
				self.current_treasure_objective = self.treasures[0]

				print('New objective: ', self.current_treasure_objective)

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


class Game:
	FPS = 45
	SCRENWIDTH = 1280
	SCREEHEIGHT = 768
	LEFTBOARDMARGIN = 300
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

		self.p1 = None
		self.p2 = None
		self.active_player = None
		self.moving_tile = None

		self.state = None

		self.setup()

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
		self.p1.treasures += treasures[:12]
		self.p2.treasures += treasures[12:]

		self.p1.current_treasure_objective = self.p1.treasures[0]
		self.p2.current_treasure_objective = self.p2.treasures[0]

		self.active_player = self.p1

		print('P1 goals: ', self.p1.treasures)
		print('P2 goals: ', self.p2.treasures)
		print('P1: objective is ', self.p1.current_treasure_objective)
		print('P2: objective is ', self.p2.current_treasure_objective)

	def set_state(self, state):
		self.state = state

		if state == Game.TILE_MOVING_STATE:
			pass
		elif state == Game.PLAYER_MOVING_STATE:
			pass



	def setup(self):
		self.allsprites.empty()
		self.alltiles.empty()

		self.create_fixed_tiles()
		self.create_moving_tiles()
		self.create_players()
		self.set_state(Game.TILE_MOVING_STATE)

	def quit(self):
		pygame.quit()
		sys.exit()

	def get_players_to_push(self, tiles_to_push):
		players_to_push = []
		for tile in tiles_to_push:
			for player in self.allplayers:
				if (tile.board_x, tile.board_y) == (player.board_x, player.board_y):
					players_to_push.append(player)
		return players_to_push

	def push_tiles(self):
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

	def update(self):
		self.allsprites.update(self.dt)
		self.check_signals()

	def draw(self):
		self.screen.fill((0, 0, 0))
		self.allsprites.draw(self.screen)
		pygame.display.flip()

	def process_keyboard_input(self, key):
		if key == pygame.K_ESCAPE:
			self.quit()
		elif key == pygame.K_r:
			self.setup()

		if self.state == Game.TILE_MOVING_STATE:
			if key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE, pygame.K_RETURN):
				self.moving_tile.process_keyboard_input(key)
		elif self.state == Game.PLAYER_MOVING_STATE:
			if key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE, pygame.K_RETURN):
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