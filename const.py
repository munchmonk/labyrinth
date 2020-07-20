import pygame
import os

# ---------------------------------------------------
# Definitions
P1, P2, P3, P4 = 'P1', 'P2', 'P3', 'P4'
RIGHT, LEFT, UP, DOWN = 'RIGHT', 'LEFT', 'UP', 'DOWN'
ROTATE = 'ROTATE'

#	- tile orientation
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

#	- treasures
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

#	- textbox types
TURN_REMINDER = 'TURN_REMINDER'
SCOREKEEPER_1 = 'SCOREKEEPER_1'
SCOREKEEPER_2 = 'SCOREKEEPER_2'
SCOREKEEPER_3 = 'SCOREKEEPER_3'
SCOREKEEPER_4 = 'SCOREKEEPER_4'

#	- game states
TILE_MOVING_STATE = 'TILE_MOVING_STATE'
PLAYER_MOVING_STATE = 'PLAYER_MOVING_STATE'
GAMEOVER_STATE = 'GAMEOVER_STATE'


# ---------------------------------------------------
# Game constants
#	- player
PLAYER_STARTING_POSITIONS =    {P1: (0, 6), P2: (6, 0), P3: (6, 6), P4: (0, 0)}
PUSHING_SPEED = 2

#	- tile
TILESIZE = 84

#	- card
CARD_TOP = TILESIZE * 2
CARD_LEFT = 850

#	- font
FONT_SIZE = 25
FONT_COLOR = (255, 0, 0)

#	- screen
SCREENWIDTH = 1280
SCREENHEIGHT = 768
LEFTBOARDMARGIN = TILESIZE
TOPBOARDMARGIN = TILESIZE

#	- bots
BOT_INPUT_COOLDOWN = 0.0005

#	- misc
FPS = 30
TOT_TREASURES = 24


# ---------------------------------------------------
# Asset paths
#	- images
PLAYER_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'assets/images/players/')
TREASURE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'assets/images/treasures/')
TILE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'assets/images/tiles/')
MARKER_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'assets/images/markers/')
CARD_PATH = os.path.join(os.path.dirname(__file__), 'assets/images/cards/')
ARROW_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'assets/images/arrows/')
BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'assets/images/backgrounds/')

#	- fonts
FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets/fonts/fff_font.ttf')

#	- sounds
SOUND_PATH = os.path.join(os.path.dirname(__file__), 'assets/sounds/')


# ---------------------------------------------------
# Assets
#	- images
PLAYER_IMAGES =    {P1: pygame.image.load(PLAYER_IMAGE_PATH + 'p1.png'),
					P2: pygame.image.load(PLAYER_IMAGE_PATH + 'p2.png'),
					P3: pygame.image.load(PLAYER_IMAGE_PATH + 'p3.png'),
					P4: pygame.image.load(PLAYER_IMAGE_PATH + 'p4.png')}

TREASURE_IMAGES =  {TREASURE_1:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_1.png'),
					TREASURE_2:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_2.png'),
					TREASURE_3:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_3.png'),
					TREASURE_4:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_4.png'),
					TREASURE_5:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_5.png'),
					TREASURE_6:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_6.png'),
					TREASURE_7:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_7.png'),
					TREASURE_8:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_8.png'),
					TREASURE_9:  pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_9.png'),
					TREASURE_10: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_10.png'),
					TREASURE_11: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_11.png'),
					TREASURE_12: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_12.png'),
					TREASURE_13: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_13.png'),
					TREASURE_14: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_14.png'),
					TREASURE_15: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_15.png'),
					TREASURE_16: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_16.png'),
					TREASURE_17: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_17.png'),
					TREASURE_18: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_18.png'),
					TREASURE_19: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_19.png'),
					TREASURE_20: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_20.png'),
					TREASURE_21: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_21.png'),
					TREASURE_22: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_22.png'),
					TREASURE_23: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_23.png'),
					TREASURE_24: pygame.image.load(TREASURE_IMAGE_PATH + 'treasure_24.png')}

TILE_IMAGES =  {TOPRIGHT: pygame.image.load(TILE_IMAGE_PATH + 'topright.png'),
				BOTTOMRIGHT: pygame.image.load(TILE_IMAGE_PATH + 'bottomright.png'),
				BOTTOMLEFT: pygame.image.load(TILE_IMAGE_PATH + 'bottomleft.png'),
				TOPLEFT: pygame.image.load(TILE_IMAGE_PATH + 'topleft.png'),

				TOPRIGHTLEFT: pygame.image.load(TILE_IMAGE_PATH + 'toprightleft.png'),
				TOPBOTTOMRIGHT: pygame.image.load(TILE_IMAGE_PATH + 'topbottomright.png'),
				BOTTOMRIGHTLEFT: pygame.image.load(TILE_IMAGE_PATH + 'bottomrightleft.png'),
				TOPBOTTOMLEFT: pygame.image.load(TILE_IMAGE_PATH + 'topbottomleft.png'),

				TOPBOTTOM: pygame.image.load(TILE_IMAGE_PATH + 'topbottom.png'),
				RIGHTLEFT: pygame.image.load(TILE_IMAGE_PATH + 'rightleft.png')}

MARKER_IMAGES =    {P1: pygame.image.load(MARKER_IMAGE_PATH + 'marker_p1.png'),
					P2: pygame.image.load(MARKER_IMAGE_PATH + 'marker_p2.png'),
					P3: pygame.image.load(MARKER_IMAGE_PATH + 'marker_p3.png'),
					P4: pygame.image.load(MARKER_IMAGE_PATH + 'marker_p4.png')}

EMPTY_CARD_IMAGE = pygame.image.load(CARD_PATH + 'empty_card.png')

BACKGROUND_IMAGE = pygame.image.load(BACKGROUND_IMAGE_PATH + 'background.png')


ARROW_NORMAL_IMAGES =  {UP: pygame.image.load(ARROW_IMAGE_PATH + 'arrow_up.png'),
						RIGHT: pygame.image.load(ARROW_IMAGE_PATH + 'arrow_right.png'),
						DOWN: pygame.image.load(ARROW_IMAGE_PATH + 'arrow_down.png'),
						LEFT: pygame.image.load(ARROW_IMAGE_PATH + 'arrow_left.png')}

ARROW_BLOCKED_IMAGES = {UP: pygame.image.load(ARROW_IMAGE_PATH + 'arrow_up_blocked.png'),
						RIGHT: pygame.image.load(ARROW_IMAGE_PATH + 'arrow_right_blocked.png'),
						DOWN: pygame.image.load(ARROW_IMAGE_PATH + 'arrow_down_blocked.png'),
						LEFT: pygame.image.load(ARROW_IMAGE_PATH + 'arrow_left_blocked.png')}

#	- fonts
FONT = pygame.freetype.Font(FONT_PATH, FONT_SIZE)

#	- sounds
MOVING_WALL_SOUND = pygame.mixer.Sound(SOUND_PATH + 'moving_wall.wav')
TREASURE_CATCH_SOUND = pygame.mixer.Sound(SOUND_PATH + 'treasure_catch.wav')
ILLEGAL_PUSH_SOUND = pygame.mixer.Sound(SOUND_PATH + 'illegal_push.wav')
VICTORY_SOUND = pygame.mixer.Sound(SOUND_PATH + 'victory.wav')


# ---------------------------------------------------
# Signals
CONFIRM_MOVEMENT_SIGNAL = 'CONFIRM_MOVEMENT_SIGNAL'
VICTORY_SIGNAL = 'VICTORY_SIGNAL'
PUSH_SIGNAL = 'PUSH_SIGNAL'































