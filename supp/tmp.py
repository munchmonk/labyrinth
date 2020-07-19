class Tile(pygame.sprite.Sprite):
	TILESIZE = 84

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

	MARKER_P1 = 'MARKER_P1'
	MARKER_P2 = 'MARKER_P2'
	MARKER_P3 = 'MARKER_P3'
	MARKER_P4 = 'MARKER_P4'

	TILE_IMAGES =  {TOPRIGHT: pygame.image.load('assets/images/tiles/topright.png'),
					BOTTOMRIGHT: pygame.image.load('assets/images/tiles/bottomright.png'),
					BOTTOMLEFT: pygame.image.load('assets/images/tiles/bottomleft.png'),
					TOPLEFT: pygame.image.load('assets/images/tiles/topleft.png'),

					TOPRIGHTLEFT: pygame.image.load('assets/images/tiles/toprightleft.png'),
					TOPBOTTOMRIGHT: pygame.image.load('assets/images/tiles/topbottomright.png'),
					BOTTOMRIGHTLEFT: pygame.image.load('assets/images/tiles/bottomrightleft.png'),
					TOPBOTTOMLEFT: pygame.image.load('assets/images/tiles/topbottomleft.png'),

					TOPBOTTOM: pygame.image.load('assets/images/tiles/topbottom.png'),
					RIGHTLEFT: pygame.image.load('assets/images/tiles/rightleft.png'),
					}

	TREASURE_IMAGES =  {TREASURE_1: pygame.image.load('assets/images/treasures/treasure_1.png'),
						TREASURE_2: pygame.image.load('assets/images/treasures/treasure_2.png'),
						TREASURE_3: pygame.image.load('assets/images/treasures/treasure_3.png'),
						TREASURE_4: pygame.image.load('assets/images/treasures/treasure_4.png'),
						TREASURE_5: pygame.image.load('assets/images/treasures/treasure_5.png'),
						TREASURE_6: pygame.image.load('assets/images/treasures/treasure_6.png'),
						TREASURE_7: pygame.image.load('assets/images/treasures/treasure_7.png'),
						TREASURE_8: pygame.image.load('assets/images/treasures/treasure_8.png'),
						TREASURE_9: pygame.image.load('assets/images/treasures/treasure_9.png'),
						TREASURE_10: pygame.image.load('assets/images/treasures/treasure_10.png'),
						TREASURE_11: pygame.image.load('assets/images/treasures/treasure_11.png'),
						TREASURE_12: pygame.image.load('assets/images/treasures/treasure_12.png'),
						TREASURE_13: pygame.image.load('assets/images/treasures/treasure_13.png'),
						TREASURE_14: pygame.image.load('assets/images/treasures/treasure_14.png'),
						TREASURE_15: pygame.image.load('assets/images/treasures/treasure_15.png'),
						TREASURE_16: pygame.image.load('assets/images/treasures/treasure_16.png'),
						TREASURE_17: pygame.image.load('assets/images/treasures/treasure_17.png'),
						TREASURE_18: pygame.image.load('assets/images/treasures/treasure_18.png'),
						TREASURE_19: pygame.image.load('assets/images/treasures/treasure_19.png'),
						TREASURE_20: pygame.image.load('assets/images/treasures/treasure_20.png'),
						TREASURE_21: pygame.image.load('assets/images/treasures/treasure_21.png'),
						TREASURE_22: pygame.image.load('assets/images/treasures/treasure_22.png'),
						TREASURE_23: pygame.image.load('assets/images/treasures/treasure_23.png'),
						TREASURE_24: pygame.image.load('assets/images/treasures/treasure_24.png')
						}

	MARKER_IMAGES =    {MARKER_P1: pygame.image.load('assets/images/markers/marker_p1.png'),
						MARKER_P2: pygame.image.load('assets/images/markers/marker_p2.png'),
						MARKER_P3: pygame.image.load('assets/images/markers/marker_p3.png'),
						MARKER_P4: pygame.image.load('assets/images/markers/marker_p2.png')
						}

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

	def add_marker(self, marker):
		self.image = self.image.copy()
		self.image.blit(Tile.MARKER_IMAGES[marker], (0, 0))

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




















		def set_last_push(self):
		self.last_push = self.moving_tile.board_x, self.moving_tile.board_y
		import pdb; pdb.set_trace()

		for arrow in self.allarrows:
			if arrow.blocked:
				arrow.unblock()
				break

		blocked_arrow = self.find_arrow_by_board_coord(*self.last_push)
		blocked_arrow.block()






















class Player(pygame.sprite.Sprite):
	P1, P2 = 'P1', 'P2'
	IMAGES =   {P1: pygame.image.load('assets/images/players/p1.png'),
				P2: pygame.image.load('assets/images/players/p2.png')}

	# Movement
	RIGHT = 'RIGHT'
	LEFT = 'LEFT'
	UP = 'UP'
	DOWN = 'DOWN'

	# Signals
	CONFIRM_MOVEMENT = 'CONFIRM_MOVEMENT'
	VICTORY = 'VICTORY'

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
		self.homerun = True

	def check_treasure_collision(self):
		if self.current_treasure_objective == self.tile.treasure:
			self.tile.remove_treasure()
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
		self.check_treasure_collision()

	def check_victory(self):
		if self.player_id == Player.P1 and (self.board_x, self.board_y) == (0, 6):
			self.signal = Player.VICTORY
		elif self.player_id == Player.P2 and (self.board_x, self.board_y) == (6, 0):
			self.signal = Player.VICTORY

	def update(self, dt):
		self.signal = None

		if self.intent in (Player.UP, Player.DOWN, Player.RIGHT, Player.LEFT):
			self.move()
		elif self.intent == Player.CONFIRM_MOVEMENT:
			self.confirm_movement()

			if self.homerun:
				self.check_victory()

		self.intent = None

	def draw(self):
		pass