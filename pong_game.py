
import pygame
import random
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

win_width = 750
win_height = 500

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

oneOrNeg = [1, -1]
y_vels = [1, 2, 3, 4]
ball_y_poses = [150, 250, 350]
rand_ball_y = random.choice(ball_y_poses)
mute = False

streak1 = False
streak2 = False
streak_score = 0
best_streak = 0
player1_score = 0
player2_score = 0

paddle_hit = pygame.mixer.Sound('assets/paddle hit.wav')
side_hit = pygame.mixer.Sound('assets/side hit.wav')
loosing = pygame.mixer.Sound('assets/loosing.wav')

def paddleHit():
	paddle_hit.play()
def sideHit():
	side_hit.play()
def loose():
	loosing.play()

class ball():
	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.right = False
		self.left = False
		self.vel = 4
		self.y_vel = 0
		self.start = False

	def draw(self):
		self.move()

		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

	def move(self):
		self.collision()

		if self.start:
			if self.left:
				self.x -= self.vel
				self.y -= self.y_vel
			elif self.right:
				self.x += self.vel
				self.y += self.y_vel

	
	def collision(self):
		global player1_score, player2_score, streak1, streak2, streak_score, best_streak

		if self.y >= bouncer1.y and self.y <= bouncer1.y + bouncer1.height:
			if self.x >= bouncer1.x and self.x <= bouncer1.x + bouncer1.width:
				if not(mute):
					paddleHit()
				self.right = True
				self.left = False
				streak1 = True
				self.y_vel = random.choice(y_vels) * random.choice(oneOrNeg)

		if self.y >= bouncer2.y and self.y <= bouncer2.y + bouncer2.height:
			if self.x >= bouncer2.x and self.x <= bouncer2.x + bouncer2.width:
				if not(mute):
					paddleHit()
				self.left = True
				self.right = False
				streak2 = True
				self.y_vel = random.choice(y_vels) * random.choice(oneOrNeg)
		



		#checking if ball goes out of court
		if self.x < 0 or self.x > win_width:
			if not(mute):
				loose()
			ball.right = False
			ball.left = False
			rand_ball_y = random.choice(ball_y_poses)

			if self.x < 0:

				player2_score += 1
				player1_point_lost = font2.render('Player 2 = Score + 1' ,1, (255, 0, 0))
				win.blit(player1_point_lost, (win_width//2 - 110, win_height//2))
				pygame.display.update()

			else:

				player1_score += 1
				player2_point_lost = font2.render('Player 1 = Score + 1' ,1, (255, 0, 0))
				win.blit(player2_point_lost, (win_width//2 - 110, win_height//2))
				pygame.display.update()


			self.x = 375
			self.y = rand_ball_y
			self.y_vel = 0
			streak_score = 0
			bouncer1.y = ((win_height) - (win_height//2) - 37)
			bouncer2.y = ((win_height) - (win_height//2) - 37)
			self.start = False


			
			i = 0
			while i < 100:
				pygame.time.delay(10)
				i += 1

		


		# seeing if ball hits edges and change direction
		if self.y > win_height - 10 or self.y < 0 + 10:
			self.y_vel = -1 * self.y_vel
			
			if not(mute):
				sideHit()

		# detrmining streaks
		if streak1 and streak2:
			streak1 = False
			streak2 = False
			streak_score += 1

			if streak_score > best_streak:
				best_streak = streak_score


class bouncer():
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.vel = 4

	def draw(self):   
		pygame.draw.rect(win, self.color, (self.x, self.y ,self.width, self.height))


def redrawGameWin():

	win.fill((0, 0, 0))
	bouncer1.draw()
	bouncer2.draw()
	pygame.draw.line(win, (255, 255, 255), (win_width//2, 0),(win_width//2, win_height))
	ball.draw()

	player1_text = font3.render('Player 1', 1, (0, 255, 0))
	player2_text = font3.render('Player 2', 1, (0, 255, 0))

	player1_score_text = font.render('Score: '+ str(player1_score), 1, (0, 255, 0))
	player2_score_text = font.render('Score: '+ str(player2_score), 1, (0, 255, 0))
	streak_score_text = font.render('Streak: '+ str(streak_score), 1, (0, 255, 0))
	best_streak_score_text = font3.render('Best: '+ str(best_streak), 1, (0, 255, 0))
	win.blit(player1_score_text, (20, 20))
	win.blit(player2_score_text, (632, 20))
	win.blit(streak_score_text, (315, 25))
	win.blit(best_streak_score_text, (332, 5))

	win.blit(player1_text, (20, 4))
	win.blit(player2_text, (632, 4))

	pygame.display.update()



font = pygame.font.SysFont('comisans', 30, True)
font2 = pygame.font.SysFont('comisans', 50)
font3 = pygame.font.SysFont('comisans', 25)

ball = ball(375, rand_ball_y, 8, (0, 0 ,255)) 
bouncer1 = bouncer((win_width - 738), ((win_height) - (win_height//2) - 37), 15, 85, (255, 0 ,0))
bouncer2 = bouncer((win_width - 25), ((win_height) - (win_height//2) - 37), 15, 85, (255, 0 ,0))

muteNum = 0
run = True
while run:
	clock.tick(120)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_m:
				if muteNum == 0:
					mute = True
					muteNum += 1
				elif muteNum == 1:
					mute = False
					muteNum = 0

	keys = pygame.key.get_pressed()


	if not(ball.start):
		if keys[pygame.K_RETURN]:
			start_dir = random.randint(0, 1)

			if start_dir == 0:
				ball.right = True
				ball.left = False
			elif start_dir == 1:
				ball.left = True
				ball.right = False

			ball.start = True

	
	if ball.start:
		if keys[pygame.K_w] and bouncer1.y > 0:
			bouncer1.y -= bouncer1.vel
			
		if keys[pygame.K_s] and bouncer1.y + bouncer1.height < win_height:
			bouncer1.y += bouncer1.vel
		

		if keys[pygame.K_UP] and bouncer2.y > 0:
			bouncer2.y -= bouncer2.vel

		if keys[pygame.K_DOWN] and bouncer2.y + bouncer2.height < win_height:
			bouncer2.y += bouncer2.vel


	redrawGameWin()

pygame.quit()
