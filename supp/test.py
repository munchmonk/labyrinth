#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3


import pygame
import sys


screen = pygame.display.set_mode((800, 600))
# screen.blit(pygame.image.load('dummy.png'), (0, 0))
bgd_img = pygame.image.load('../assets/images/backgrounds/background.png')	

p1_image = pygame.image.load('../assets/images/players/p1.png')
p2_image = pygame.image.load('../assets/images/players/p2.png')

allsprites = pygame.sprite.LayeredDirty()

allsprites.clear(screen, bgd_img)


class Player(pygame.sprite.DirtySprite):
	def __init__(self, img, x, y, *groups):
		_layer = 1
		pygame.sprite.DirtySprite.__init__(self, *groups)
		self.image = img
		self.rect = self.image.get_rect(topleft=(x, y))

	def update(self):
		pass

	def move_up(self):
		self.rect.y -= 20
		self.dirty = 1

	def move_down(self):
		self.rect.y += 20
		self.dirty = 1





p1 = Player(p1_image, 10, 30, allsprites)
p2 = Player(p2_image, 40, 80, allsprites)



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif event.key == pygame.K_UP:
				p2.move_up()
			elif event.key == pygame.K_DOWN:
				p2.move_down()



		allsprites.update()
		rects_to_update = allsprites.draw(screen)
		print(rects_to_update)

		pygame.display.update(rects_to_update)




# l = [1, 2, 3, 5, 'ciao', 'pippo']
# l.remove('ciao')
# print(l)





# l = [(0, 0), (0, 1), (0, 2)]
# l.append((0, 3))
# l += ((0, 4), (0, 5))

# print(l)







# a = ['a', 'b', 'c', 'd']

# el = a[1]

# for i in range(10):
# 	el = a[(a.index(el) + 1) % len(a)]

# 	print(el)

# print(a.pop())



