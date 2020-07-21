import pygame

import const

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
			elif self.game.active_player.player_id == const.P3:
				msg += 'Player 3,'
			elif self.game.active_player.player_id == const.P4:
				msg += 'Player 4,'

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

		elif self.textbox_type == const.SCOREKEEPER_3:
			tot_treasures = const.TOT_TREASURES // len(self.game.allplayers)
			treasures_caught = tot_treasures - len(self.game.p3.treasures)

			msg += 'Player 3: '
			msg += str(treasures_caught)
			msg += ' / '
			msg += str(tot_treasures)

		elif self.textbox_type == const.SCOREKEEPER_4:
			tot_treasures = const.TOT_TREASURES // len(self.game.allplayers)
			treasures_caught = tot_treasures - len(self.game.p4.treasures)			

			msg += 'Player 4: '
			msg += str(treasures_caught)
			msg += ' / '
			msg += str(tot_treasures)

		self.change_text(msg)





















		