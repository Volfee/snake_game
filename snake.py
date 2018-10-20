import pygame
import random

white = (255,255,255)
black = (0,0,0)
red   = (255,0,0)
green = (0,155,0)

class Game(object):

	def __init__(self):
		self.DISPLAY_WIDTH = 800
		self.DISPLAY_HEIGHT = 600
		self.FPS = 60
		self.BLOCK_SIZE = 10
		self.SPEED = self.BLOCK_SIZE
		self.MAX_LEN_INCREASE = 5


		self.set_up()

		self.game_exit = False
		self.apple = None

		while not self.game_exit:
			self.run_new_game()

	def set_up(self):
		pygame.init()
		display_size = [self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT]
		self.game_display = pygame.display.set_mode(display_size)
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Snek')

	def run_new_game(self):
		self.game_over = False

		self.snake = [(self.DISPLAY_WIDTH/2, self.DISPLAY_HEIGHT/2)]
		self.apple = self.get_first_apple()

		self.acceleration = {'x': 0, 'y': 0}
		self.max_len = 20

		while not self.game_exit and not self.game_over:
			self.event_control()
				# or input_contorol #AI
			self.update_snake()
			self.check_collisions()
			self.render_game()
			self.wait()
			pygame.display.update()

	def event_control(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game_exit = True

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					self.game_exit = True

				elif event.key == pygame.K_a:
					if self.acceleration['x'] == 0:
						self.acceleration['x'] = -self.SPEED
						self.acceleration['y'] = 0
				elif event.key == pygame.K_d:
					if self.acceleration['x'] == 0:
						self.acceleration['x'] = self.SPEED
						self.acceleration['y'] = 0
				elif event.key == pygame.K_w:
					if self.acceleration['y'] == 0:
						self.acceleration['x'] = 0
						self.acceleration['y'] = -self.SPEED
				elif event.key == pygame.K_s:
					if self.acceleration['y'] == 0:
						self.acceleration['x'] = 0
						self.acceleration['y'] = self.SPEED

	def update_snake(self):
		head = self.snake[-1]
		new_position = (head[0] + self.acceleration['x'], head[1] + self.acceleration['y'])
		self.snake.append(new_position)
		if len(self.snake) > self.max_len:
			del self.snake[0]

	def get_first_apple(self):
		if self.apple == None:
			apple_x = (random.randrange(0, self.DISPLAY_WIDTH - self.BLOCK_SIZE)/20)*20
			apple_y = (random.randrange(0, self.DISPLAY_HEIGHT - self.BLOCK_SIZE)/20)*20
			while (apple_x, apple_y) in self.snake:
				apple_x = (random.randrange(0, self.DISPLAY_WIDTH - self.BLOCK_SIZE)/20)*20
				apple_y = (random.randrange(0, self.DISPLAY_HEIGHT - self.BLOCK_SIZE)/20)*20
			return apple_x, apple_y
		else:
			return self.apple

	def get_new_apple(self):
		apple_x = (random.randrange(0, self.DISPLAY_WIDTH - self.BLOCK_SIZE)/20)*20
		apple_y = (random.randrange(0, self.DISPLAY_HEIGHT - self.BLOCK_SIZE)/20)*20
		while (apple_x, apple_y) in self.snake:
			apple_x = (random.randrange(0, self.DISPLAY_WIDTH - self.BLOCK_SIZE)/20)*20
			apple_y = (random.randrange(0, self.DISPLAY_HEIGHT - self.BLOCK_SIZE)/20)*20
		return apple_x, apple_y

	def check_collisions(self):
		snake_head = self.snake[-1]
		snake_body = self.snake[:-1]

		if self.check_border_collision(snake_head):
			self.game_over = True
		elif self.check_body_collision(snake_head, snake_body):
			self.game_over = True
		elif self.check_apple_collision(snake_head, self.apple):
			self.max_len += self.MAX_LEN_INCREASE
			self.apple = self.get_new_apple()

	def check_border_collision(self, head):
		return head[0] > 780 or head[0] < 0 or head[1] > 580 or head[1] < 0
			
	def check_body_collision(self, head, body):
		return (head[0], head[1]) in body

	def check_apple_collision(self, head, apple):
		return head[0] == apple[0] and head[1] == apple[1] 

	def render_game(self):
		self.render_background()
		self.render_snake(self.snake)
		self.render_apple(self.apple)

	def render_background(self):
		self.game_display.fill(black)

	def render_snake(self, snake):
		for loc in snake:
			shape = [loc[0], loc[1], self.BLOCK_SIZE, self.BLOCK_SIZE]
			pygame.draw.rect(self.game_display, green, shape)

	def render_apple(self, apple):
		shape = [apple[0], apple[1], self.BLOCK_SIZE, self.BLOCK_SIZE]
		pygame.draw.rect(self.game_display, red, shape)

	def wait(self):
		self.clock.tick(self.FPS)


if __name__ == "__main__":
	snake = Game()
