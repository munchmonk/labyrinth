#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3


a = ['a', 'b', 'c', 'd']

el = a[1]

for i in range(10):
	el = a[(a.index(el) + 1) % len(a)]

	print(el)

print(a.pop())



# import pygame
# import sys


# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen.blit(pygame.image.load('dummy.png'), (0, 0))

# while True:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			pygame.quit()
# 			sys.exit()
# 		elif event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_ESCAPE:
# 				pygame.quit()
# 				sys.exit()

# 		pygame.display.flip()