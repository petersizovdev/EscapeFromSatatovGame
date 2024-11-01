import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Escape from saratov')



#шрифт
font = pygame.font.SysFont('arial', 70)
font_score = pygame.font.SysFont('arial', 30)
white = (255, 255, 255)


#определение игровых переменных
tile_size = 50
game_over = 0
main_menu = True
score = 0


#загрузка текстур
bg_img = pygame.image.load('img/bg.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')



def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#получение данных о курсоре
		pos = pygame.mouse.get_pos()

		#проверьте наведение курсора мыши и условия щелчка
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#отрисовка кнопок
		screen.blit(self.image, self.rect)

		return action


class Player():
	def __init__(self, x, y):
		self.reset(x, y)



	def update(self, game_over):
		dx = 0
		dy = 0
		walk_anim_speed = 5

		if game_over == 0:
			#нажатие кнопок
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#анимация
			if self.counter > walk_anim_speed:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#гравитация
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#проверка на коллизию
			self.in_air = True
			for tile in world.tile_list:
				#коллизия по X
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#коллизия по Y
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#под
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top

						self.vel_y = 0
					#над
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#коллизия врагов
			if pygame.sprite.spritecollide(self, rob_group, False):
				game_over = -1

			#коллизия шипов
			if pygame.sprite.spritecollide(self, sip_group, False):
				game_over = -1


			#выход
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#обновление координат игрока
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image
			self.rect.y += 5

		#отрисовка игрока
		screen.blit(self.image, self.rect)

		return game_over


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'img/guy{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/fall.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True



class World():
	def __init__(self, data):
		self.tile_list = []

		#текстуры окружения
		k_img = pygame.image.load('img/k.png')
		grass_img = pygame.image.load('img/grass.png')
		platform_img = pygame.image.load('img/platform.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(k_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 4:
					img = pygame.transform.scale(platform_img, (tile_size, tile_size // 2))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size +25
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 5:
					img = pygame.transform.scale(platform_img, (tile_size, tile_size // 2))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size +50
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					rob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					rob_group.add(rob)
				if tile == 6:
					sip = Sip(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					sip_group.add(sip)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)



				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


#склассы врагов и интерактива
class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/rob.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1


class Sip(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/sip.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)



world_data = [
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 1, 0, 3, 5, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1, 1, 2, 2, 0, 0, 0, 0, 5, 1],  
[1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 1], 
[1, 4, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1],  
[1, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 1, 6, 6, 6, 6, 6, 1],  
[1, 0, 0, 0, 2, 1, 1, 0, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1],  
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 3, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 4, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1],  
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],  
[1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 6, 6, 6, 2, 2, 0, 0, 0, 0, 0, 3, 0, 7, 1],  
[1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]



player = Player(100, screen_height - 130)

rob_group = pygame.sprite.Group()
sip_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group() 

world = World(world_data)

#создание кнопок
restart_button = Button(screen_width // 2 - 150, screen_height // 2, restart_img)
start_button = Button(screen_width // 2 - 500, screen_height // 2 - 500, start_img)


run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))


	if main_menu == True:
		if start_button.draw():
			main_menu = False
	else:
		world.draw()

		if game_over == 0:
			rob_group.update()

			#сбор монет
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
			draw_text('МОНЕТЫ: ' + str(score), font_score, white, tile_size - 10, 10)

		
		rob_group.draw(screen)
		sip_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		game_over = player.update(game_over)

		#смерть модельки
		if game_over == -1:
			if restart_button.draw():
				player.reset(100, screen_height - 130)
				game_over = 0

		#выйгрыш
		if game_over == 1:
				draw_text('ВЫ ВЫБРАЛИСЬ!', font, white, (screen_width // 2) - 140, screen_height // 2)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()