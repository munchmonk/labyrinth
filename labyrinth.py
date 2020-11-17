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
import time

import const
import sprite_module
import tile_module
import player_module


class ActionThread(threading.Thread):
	def __init__(self, game):
		threading.Thread.__init__(self)

		self.game = game
		self.command_queue = []
		self.command_index = 0

	def run(self):
		while True:
			if self.command_queue:


				print('------')
				print('Command queue:')
				for command in self.command_queue:
					print(command)



				curr_command = None

				for command in self.command_queue:
					if command[0] == self.command_index:
						curr_command = command

				if curr_command:
					success = False
					sprite_type = curr_command[1]

					if sprite_type == 'Tile':
						intent = curr_command[2]
						self.game.moving_tile.intent = intent
						success = self.game.moving_tile.update(self.game.dt)

					elif sprite_type == 'Player':
						player_id = curr_command[2]
						intent = curr_command[3]

						player = self.game.find_player_by_id(player_id)
						player.intent = intent
						success = player.update(self.game.dt)

					if success:
						self.game.check_signals()
						self.command_queue.remove(curr_command)
						self.command_index += 1

					else:
						print('FAILED TO EXECUTE: ', curr_command)

				else:
					print("NO COMMAND SELECTED - command_index: ", self.command_index)


class ListenerThread(threading.Thread):
	def __init__(self, game, my_socket):
		threading.Thread.__init__(self)

		self.game = game
		self.my_socket = my_socket

		self.action_thread = ActionThread(self.game)
		self.action_thread.daemon = True
		self.action_thread.start()

	def run(self):
		while True:
			msg = self.my_socket.recv(1024)
			msg = pickle.loads(msg)

			self.action_thread.command_queue.append(msg)


class Game:
	def __init__(self):
		self.screen = pygame.display.set_mode((const.SCREENWIDTH, const.SCREENHEIGHT))
		self.clock = pygame.time.Clock()
		self.dt = 0
		self.fullscreen = False

		self.allsprites = pygame.sprite.LayeredDirty()
		self.alltiles = pygame.sprite.LayeredDirty()
		self.allplayers = pygame.sprite.LayeredDirty()
		self.allcards = pygame.sprite.LayeredDirty()
		self.allarrows = pygame.sprite.LayeredDirty()
		self.alltextboxes = pygame.sprite.LayeredDirty()

		self.update_order = [self.allplayers, self.alltiles, self.allarrows, self.allcards, self.alltextboxes]
		self.allsprites.clear(self.screen, const.BACKGROUND_IMAGES[const.STANDARD_BACKGROUND])
		# self.alltiles.clear(self.screen, const.BACKGROUND_IMAGE)
		# self.allplayers.clear(self.screen, const.BACKGROUND_IMAGE)
		# self.allcards.clear(self.screen, const.BACKGROUND_IMAGE)
		# self.allarrows.clear(self.screen, const.BACKGROUND_IMAGE)
		# self.alltextboxes.clear(self.screen, const.BACKGROUND_IMAGE)
		# self.print_order = [self.allarrows, self.allcards, self.alltiles, self.allplayers, self.alltextboxes]

		self.p1 = None
		self.p2 = None
		self.p3 = None
		self.p4 = None
		self.active_player = None
		self.acting_order = []
		self.side = None

		self.moving_tile = None
		self.last_push = None

		self.state = None

		self.client_socket = None
		self.command_index = 0

		# Main menu buttons
		self.buttons = []

		# Server ip selection textbox
		self.server_ip_surf = None
		self.server_ip_rect = None
		self.server_ip_text = ""

	def show_starting_screen(self):
		self.set_state(const.STARTING_SCREEN_STATE)

		# Play button
		play_button_surf = const.BUTTON_IMAGES[const.PLAY]
		play_button_rect = play_button_surf.get_rect(center=(const.SCREENWIDTH / 2, const.SCREENHEIGHT / 2 - 300))
		play_button = (play_button_rect, const.PLAY)
		self.buttons.append(play_button)

		# Start server button
		start_server_button_surf = const.BUTTON_IMAGES[const.START_SERVER]
		start_server_button_rect = start_server_button_surf.get_rect(center=(const.SCREENWIDTH / 2, const.SCREENHEIGHT / 2 - 100))
		start_server_button = (start_server_button_rect, const.START_SERVER)
		self.buttons.append(start_server_button)

		# Start client button
		start_client_button_surf = const.BUTTON_IMAGES[const.START_CLIENT]
		start_client_button_rect = start_client_button_surf.get_rect(center=(const.SCREENWIDTH / 2, const.SCREENHEIGHT / 2 + 100))
		start_client_button = (start_client_button_rect, const.START_CLIENT)
		self.buttons.append(start_client_button)

		# Add bot button
		add_bot_button_surf = const.BUTTON_IMAGES[const.ADD_BOT]
		add_bot_button_rect = add_bot_button_surf.get_rect(center=(const.SCREENWIDTH / 2, const.SCREENHEIGHT / 2 + 300))
		add_bot_button = (add_bot_button_rect, const.ADD_BOT)
		self.buttons.append(add_bot_button)		

		self.screen.blit(const.BACKGROUND_IMAGES[const.STANDARD_BACKGROUND], (0, 0))
		self.screen.blit(play_button_surf, play_button_rect)
		self.screen.blit(start_server_button_surf, start_server_button_rect)
		self.screen.blit(start_client_button_surf, start_client_button_rect)
		self.screen.blit(add_bot_button_surf, add_bot_button_rect)

		pygame.display.flip()

	def get_server_ip_address(self):
		self.set_state(const.SERVER_IP_SELECTION_STATE)

		self.server_ip_surf, self.server_ip_rect = const.FONT.render(self.server_ip_text, const.FONT_COLOR)
		self.server_ip_rect.center = (const.SCREENWIDTH / 2, const.SCREENHEIGHT / 2)

	def toggle_fullscreen(self):
		self.fullscreen = not self.fullscreen

		if self.fullscreen:
			pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			pygame.mouse.set_visible(False)
		else:
			pygame.display.set_mode((const.SCREENWIDTH, const.SCREENHEIGHT))
			pygame.mouse.set_visible(True)

	def broadcast(self, message):
		message.insert(0, self.command_index)
		self.command_index += 1

		self.client_socket.send(pickle.dumps(message))


		print('-----')
		print('Sending:')
		print(message)

	def find_player_by_id(self, player_id):
		for player in self.allplayers:
			if player.player_id == player_id:
				return player

		return None

	def start_server(self):
		self.side = const.P1

		number_of_bots = len(self.allplayers) - 2

		# Setup to reset all states/variables to their starting state
		self.setup()

		# Add bots back if applicable
		for i in range(number_of_bots):
			self.add_bot()

		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# The below commented out line doesn't allow other machines to connect. Use '' instead
		# host = socket.gethostbyname("localhost")
		host = ''
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

		t = ListenerThread(self, self.client_socket)
		t.daemon = True
		t.start()

	def start_client(self):
		self.side = const.P2

		# Setup to reset all states/variables to their starting state
		self.setup()

		# Manually remove the card on the client created by the setup() call above to avoid creating two cards
		for card in self.allcards:
			card.kill()

		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Uncomment to quickly test locally - 192.168.1.15/19
		# host = socket.gethostbyname("localhost")
		host = self.server_ip_text
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

			new_tile = tile_module.Tile(rect_x, rect_y, board_x, board_y, tiletype, self, self.allsprites, self.alltiles)
			new_tile.add_treasure(treasure)

			# Set the moving tile!
			if board_x in (-1, 7) or board_y in (-1, 7):
				self.moving_tile = new_tile

		# Players
		for player in self.allplayers:
			player.kill()
		self.p1 = None
		self.p2 = None
		self.p3 = None
		self.p4 = None

		for player in new_players:
			player_id = player[0]
			board_x, board_y = player[1], player[2]
			treasures = player[3]

			bot = False
			if player_id in (const.P3, const.P4):
				bot = True
			new_player = player_module.Player(player_id, bot, board_x, board_y, self, self.allsprites, self.allplayers)
			new_player.set_treasures(treasures)

			if player_id == const.P1:
				self.p1 = new_player
			elif player_id == const.P2:
				self.p2 = new_player
			elif player_id == const.P3:
				self.p3 = new_player
			elif player_id == const.P4:
				self.p4 = new_player

		self.acting_order = [self.p1, self.p2]

		if self.p3:
			self.acting_order.append(self.p3)
		if self.p4:
			self.acting_order.append(self.p4)

		# Recreate textboxes in case there are now more than 2 players (i.e. bots)
		self.create_score_textboxes()

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
		tile_module.Tile(const.LEFTBOARDMARGIN + 0 * const.TILESIZE, const.TOPBOARDMARGIN + 0 * const.TILESIZE, 0, 0, const.BOTTOMRIGHT, self, self.allsprites, self.alltiles)
		tile_module.Tile(const.LEFTBOARDMARGIN + 6 * const.TILESIZE, const.TOPBOARDMARGIN + 0 * const.TILESIZE, 6, 0, const.BOTTOMLEFT, self, self.allsprites, self.alltiles)
		tile_module.Tile(const.LEFTBOARDMARGIN + 6 * const.TILESIZE, const.TOPBOARDMARGIN + 6 * const.TILESIZE, 6, 6, const.TOPLEFT, self, self.allsprites, self.alltiles)
		tile_module.Tile(const.LEFTBOARDMARGIN + 0 * const.TILESIZE, const.TOPBOARDMARGIN + 6 * const.TILESIZE, 0, 6, const.TOPRIGHT, self, self.allsprites, self.alltiles)

		# Row 0
		tiles_that_need_treasure += (
		tile_module.Tile(const.LEFTBOARDMARGIN + 2 * const.TILESIZE, const.TOPBOARDMARGIN + 0 * const.TILESIZE, 2, 0, const.BOTTOMRIGHTLEFT, self, self.allsprites, self.alltiles),
		tile_module.Tile(const.LEFTBOARDMARGIN + 4 * const.TILESIZE, const.TOPBOARDMARGIN + 0 * const.TILESIZE, 4, 0, const.BOTTOMRIGHTLEFT, self, self.allsprites, self.alltiles)
		)

		# Row 2
		tiles_that_need_treasure += (
		tile_module.Tile(const.LEFTBOARDMARGIN + 0 * const.TILESIZE, const.TOPBOARDMARGIN + 2 * const.TILESIZE, 0, 2, const.TOPBOTTOMRIGHT, self, self.allsprites, self.alltiles),
		tile_module.Tile(const.LEFTBOARDMARGIN + 2 * const.TILESIZE, const.TOPBOARDMARGIN + 2 * const.TILESIZE, 2, 2, const.TOPBOTTOMRIGHT, self, self.allsprites, self.alltiles),
		tile_module.Tile(const.LEFTBOARDMARGIN + 4 * const.TILESIZE, const.TOPBOARDMARGIN + 2 * const.TILESIZE, 4, 2, const.BOTTOMRIGHTLEFT, self, self.allsprites, self.alltiles),
		tile_module.Tile(const.LEFTBOARDMARGIN + 6 * const.TILESIZE, const.TOPBOARDMARGIN + 2 * const.TILESIZE, 6, 2, const.TOPBOTTOMLEFT, self, self.allsprites, self.alltiles)
		)

		# Row 4
		tiles_that_need_treasure += (
		tile_module.Tile(const.LEFTBOARDMARGIN + 0 * const.TILESIZE, const.TOPBOARDMARGIN + 4 * const.TILESIZE, 0, 4, const.TOPBOTTOMRIGHT, self, self.allsprites, self.alltiles),
		tile_module.Tile(const.LEFTBOARDMARGIN + 2 * const.TILESIZE, const.TOPBOARDMARGIN + 4 * const.TILESIZE, 2, 4, const.TOPRIGHTLEFT, self, self.allsprites, self.alltiles),
		tile_module.Tile(const.LEFTBOARDMARGIN + 4 * const.TILESIZE, const.TOPBOARDMARGIN + 4 * const.TILESIZE, 4, 4, const.TOPBOTTOMLEFT, self, self.allsprites, self.alltiles),
		tile_module.Tile(const.LEFTBOARDMARGIN + 6 * const.TILESIZE, const.TOPBOARDMARGIN + 4 * const.TILESIZE, 6, 4, const.TOPBOTTOMLEFT, self, self.allsprites, self.alltiles)
		)

		# Row 6
		tiles_that_need_treasure += (
		tile_module.Tile(const.LEFTBOARDMARGIN + 2 * const.TILESIZE, const.TOPBOARDMARGIN + 6 * const.TILESIZE, 2, 6, const.TOPRIGHTLEFT, self, self.allsprites, self.alltiles),
		tile_module.Tile(const.LEFTBOARDMARGIN + 4 * const.TILESIZE, const.TOPBOARDMARGIN + 6 * const.TILESIZE, 4, 6, const.TOPRIGHTLEFT, self, self.allsprites, self.alltiles)
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

					new_tile = tile_module.Tile(const.LEFTBOARDMARGIN + i * const.TILESIZE, const.TOPBOARDMARGIN + j * const.TILESIZE, i, j, 
									tiletype, self, self.allsprites, self.alltiles)
					if new_tile.tiletype == const.TOPRIGHTLEFT:
						new_tile.add_treasure(self.get_random_treasure())
					elif new_tile.tiletype == const.TOPLEFT:
						tiles_with_potential_treasure.append(new_tile)
					new_tile.rotate(random_rotation=True)

		last_tile = moving_tiles[0]
		self.moving_tile = tile_module.Tile(const.LEFTBOARDMARGIN + 1 * const.TILESIZE, const.TOPBOARDMARGIN + 7 * const.TILESIZE, 1, 7, 
								last_tile, self, self.allsprites, self.alltiles)	
		if self.moving_tile.tiletype == const.TOPRIGHTLEFT:
			self.moving_tile.add_treasure(self.get_random_treasure())	
		elif self.moving_tile.tiletype == const.TOPLEFT:
			tiles_with_potential_treasure.append(self.moving_tile)
		self.moving_tile.rotate(random_rotation=True)

		random.shuffle(tiles_with_potential_treasure)
		for tile in tiles_with_potential_treasure:
			tile.add_treasure(self.get_random_treasure())
		
	def create_players(self):
		self.p1 = player_module.Player(const.P1, False, *const.PLAYER_STARTING_POSITIONS[const.P1], self, self.allsprites, self.allplayers)
		self.p2 = player_module.Player(const.P2, False, *const.PLAYER_STARTING_POSITIONS[const.P2], self, self.allsprites, self.allplayers)

		treasures = self.get_all_treasures()
		random.shuffle(treasures)

		self.p1.set_treasures(treasures[:12])
		self.p2.set_treasures(treasures[12:])

		self.acting_order = [self.p1, self.p2]
		self.active_player = self.acting_order[0]

	def add_bot(self):
		if not self.p3:
			self.p3 = player_module.Player(const.P3, True, *const.PLAYER_STARTING_POSITIONS[const.P3], self, self.allsprites, self.allplayers)
			self.acting_order.append(self.p3)

			treasures = self.get_all_treasures()
			random.shuffle(treasures)

			self.p1.set_treasures(treasures[:8])
			self.p2.set_treasures(treasures[8:16])
			self.p3.set_treasures(treasures[16:])

			self.create_score_textboxes()

		elif not self.p4:
			self.p4 = player_module.Player(const.P4, True, *const.PLAYER_STARTING_POSITIONS[const.P4], self, self.allsprites, self.allplayers)
			self.acting_order.append(self.p4)

			treasures = self.get_all_treasures()
			random.shuffle(treasures)

			self.p1.set_treasures(treasures[:6])
			self.p2.set_treasures(treasures[6:12])
			self.p3.set_treasures(treasures[12:18])
			self.p4.set_treasures(treasures[18:])

			self.create_score_textboxes()

		else:
			print('Max number of players reached (4).')

	def set_state(self, state):
		self.state = state

		if state == const.GAMEOVER_STATE:
			# if self.active_player == self.p1:
			# 	winner = 'Player 1'
			# elif self.active_player == self.p2:
			# 	winner = 'Player 2'
			# elif self.active_player == self.p3:
			# 	winner = 'Player 3'
			# elif self.active_player == self.p4:
			# 	winner = 'Player 4'

			# for textbox in self.alltextboxes:
			# 	if textbox.textbox_type == const.TURN_REMINDER:
			# 		reminder_textbox = textbox
			# 		break

			# reminder_textbox.change_text(winner + ' won!!!')
			const.VICTORY_SOUND.play()

	def create_arrows(self):
		topleft_tile = self.find_tile_by_board_coord(0, 0)
		topleft_x, topleft_y = topleft_tile.board_x, topleft_tile.board_y

		# Top row
		x, y = topleft_x + 1, topleft_y - 1
		for i in range(3):
			sprite_module.Arrow(x, y, const.DOWN, self.allsprites, self.allarrows)
			x += 2

		# Bottom row
		x, y = topleft_x + 1, topleft_y + 7
		for i in range(3):
			sprite_module.Arrow(x, y, const.UP, self.allsprites, self.allarrows)
			x += 2

		# Left column
		x, y = topleft_x - 1, topleft_y + 1
		for i in range(3):
			sprite_module.Arrow(x, y, const.RIGHT, self.allsprites, self.allarrows)
			y += 2

		# Right column
		x, y = topleft_x + 7, topleft_y + 1
		for i in range(3):
			sprite_module.Arrow(x, y, const.LEFT, self.allsprites, self.allarrows)
			y += 2

	def create_reminder_textbox(self):
		last_tile = self.find_tile_by_board_coord(6, 0)
		top, left = last_tile.rect.top, last_tile.rect.left + const.TILESIZE * 2

		sprite_module.TextBox('', const.FONT, self, const.TURN_REMINDER, self.allsprites, self.alltextboxes, top=top, left=left)

	def create_score_textboxes(self):
		textboxes_to_kill = []
		for textbox in self.alltextboxes:
			if textbox.textbox_type in (const.SCOREKEEPER_1, const.SCOREKEEPER_2, const.SCOREKEEPER_3, const.SCOREKEEPER_4):
				textboxes_to_kill.append(textbox)
		for textbox in textboxes_to_kill:
			textbox.kill()

		last_tile = self.find_tile_by_board_coord(6, 0)

		left_1 = last_tile.rect.left + const.TILESIZE * 2
		left_2 = left_1
		left_3 = left_1 + 250
		left_4 = left_3

		top_1 = 600
		top_2 = top_1 + 100
		top_3 = top_1
		top_4 = top_2

		sprite_module.TextBox('score', const.FONT, self, const.SCOREKEEPER_1, self.allsprites, self.alltextboxes, top=top_1, left=left_2)
		sprite_module.TextBox('score', const.FONT, self, const.SCOREKEEPER_2, self.allsprites, self.alltextboxes, top=top_2, left=left_2)

		if self.p3:
			sprite_module.TextBox('score', const.FONT, self, const.SCOREKEEPER_3, self.allsprites, self.alltextboxes, top=top_3, left=left_3)
		if self.p4:
			sprite_module.TextBox('score', const.FONT, self, const.SCOREKEEPER_4, self.allsprites, self.alltextboxes, top=top_4, left=left_4)

	def setup(self):
		for sprite in self.allsprites:
			sprite.kill()
		self.p1, self.p2, self.p3, self.p4 = None, None, None, None
		self.last_push = None
		self.command_index = 0

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
		for player in self.allplayers:
			if player.pushing:
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

				# Cycles through the acting_order list
				self.active_player = self.acting_order[(self.acting_order.index(self.active_player) + 1) % len(self.acting_order)]
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

	def update_bots(self):
		# Only calculate bot actions on server side or in single player mode
		if self.side and self.side != const.P1:
			return

		if self.active_player.bot and time.time() - self.active_player.last_bot_action > const.BOT_INPUT_COOLDOWN:
			if self.state in (const.TILE_MOVING_STATE, const.PLAYER_MOVING_STATE) and not self.is_anything_pushing():
				self.active_player.bot_turn_to_act = True
				self.active_player.last_bot_action = time.time()

	def update(self):
		if self.state in (const.TILE_MOVING_STATE, const.PLAYER_MOVING_STATE):
			self.update_bots()
			for sprite_group in self.update_order:
				sprite_group.update(self.dt)
			self.check_signals()
			self.check_broadcasts()

	def draw(self):

		# -------------- BUG:
		# for some reason when the tiles are drawn,the whole 1280x768 screen is returned as a rect that needs updating
		# if this actually worked, some sprites wouldn't get drawn as I haven't set their dirty behaviour yet
		# This means that as of now I purposefully left the game bugged (by not defining the sprites' dirty behaviour)
		# so that it's easier to tell if this actual bug still exists or not

		if self.state in (const.TILE_MOVING_STATE, const.PLAYER_MOVING_STATE):
			rects_to_update = self.allsprites.draw(self.screen)
			pygame.display.update(rects_to_update)

		elif self.state == const.SERVER_IP_SELECTION_STATE:
			self.screen.blit(const.BACKGROUND_IMAGES[const.SERVER_IP_SELECTION_BACKGROUND], (0, 0))
			self.screen.blit(self.server_ip_surf, self.server_ip_rect)
			pygame.display.flip()

	def process_mouse_input(self, button):
		# button is a tuple (rect, mouse_button_index)
		# 1 = left click, 3 = right click
		if self.state == const.STARTING_SCREEN_STATE and button == 1:
			for button in self.buttons:
				if button[0].collidepoint(pygame.mouse.get_pos()):
					if button[1] == const.PLAY:
						self.set_state(const.TILE_MOVING_STATE)
						self.buttons = []
					elif button[1] == const.START_SERVER:
						self.start_server()
						self.buttons = []
						print('Started server!')
					elif button[1] == const.START_CLIENT:
						self.get_server_ip_address()
						self.buttons = []
					elif button[1] == const.ADD_BOT:
						self.add_bot()
						print('Added one bot!')

	def process_keyboard_input(self, key):
		if key == pygame.K_ESCAPE:
			self.quit()

		# ---- Deprecated keyboard inputs

		# elif key == pygame.K_o and self.state == const.STARTING_SCREEN_STATE:
		# 	self.set_state(const.TILE_MOVING_STATE)

		elif key == pygame.K_w:
			self.toggle_fullscreen()
		elif key == pygame.K_d:
			import pdb; pdb.set_trace()

		# ---- Deprecated keyboard inputs

		# elif key == pygame.K_a and not self.side:
		# 	self.add_bot()
		# elif key == pygame.K_r and not self.side:
		# 	self.setup()
		# elif key == pygame.K_s and not self.side:
		# 	self.start_server()
		# elif key == pygame.K_c and not self.side:
		# 	self.start_client()

		if self.state in (const.PLAYER_MOVING_STATE, const.TILE_MOVING_STATE):
			if not self.active_player.bot and (not self.side or self.side == self.active_player.player_id):
				if key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE, pygame.K_RETURN):
					if not self.is_anything_pushing():
						if self.state == const.TILE_MOVING_STATE:
							self.moving_tile.process_keyboard_input(key)
						elif self.state == const.PLAYER_MOVING_STATE:
							self.active_player.process_keyboard_input(key)

		elif self.state == const.SERVER_IP_SELECTION_STATE:
			if key == pygame.K_BACKSPACE and self.server_ip_text:
				self.server_ip_text = self.server_ip_text[:-1]
			elif key in const.PYGAME_KEYS.keys():
				self.server_ip_text += const.PYGAME_KEYS[key]
			elif key == pygame.K_RETURN:
				self.start_client()
					
			self.server_ip_surf, self.server_ip_rect = const.FONT.render(self.server_ip_text, const.FONT_COLOR)
			self.server_ip_rect.center = (const.SCREENWIDTH / 2, const.SCREENHEIGHT / 2)

	def run(self):
		self.setup()
		self.show_starting_screen()

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.KEYDOWN:
					self.process_keyboard_input(event.key)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.process_mouse_input(event.button)

			self.update()
			self.draw()
			self.dt = self.clock.tick(const.FPS)


if __name__ == '__main__':
	Game().run()