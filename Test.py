import unittest
import pygame
import random
import sys

class TestPongGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_width = 1280
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Pong')
        self.ball = pygame.Rect(self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30)
        self.player = pygame.Rect(self.screen_width - 20, self.screen_height / 2 - 70, 10, 140)
        self.opponent = pygame.Rect(10, self.screen_height / 2 - 70, 10, 140)
        self.bg_color = pygame.Color('grey12')
        self.light_grey = (200, 200, 200)
        self.ball_speed_x = 7 * random.choice((1, -1))
        self.ball_speed_y = 7 * random.choice((1, -1))
        self.player_speed = 0
        self.opponent_speed = 7
        self.player_score = 0
        self.opponent_score = 0
        self.game_font = pygame.font.Font("freesansbold.ttf", 32)
        self.score_time = True

    def tearDown(self):
        pygame.quit()
        
    def ball_animation(self):
        global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.ball_speed_y *= -1
        if self.ball.left <= 0:
            self.player_score += 1
            self.score_time = pygame.time.get_ticks()

        if self.ball.right >= self.screen_width:
            self.opponent_score += 1
            self.score_time = pygame.time.get_ticks()

        if self.ball.colliderect(self.player) or self.ball.colliderect(self.opponent):
            self.ball_speed_x *= -1

    def player_animation(self):
        self.player.y += self.player_speed
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height

    def opponent_ai(self):
        if self.opponent.top < self.ball.y:
            self.opponent.top += self.opponent_speed
        if self.opponent.bottom > self.ball.y:
            self.opponent.bottom -= self.opponent_speed
        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= self.screen_height:
            self.opponent.bottom = self.screen_height

    def ball_restart(self):
        global ball_speed_x, ball_speed_y, score_time

        current_time = pygame.time.get_ticks()
        self.ball.center = (self.screen_width / 2, self.screen_height / 2)

        if current_time - self.score_time < 700:
            number_three = self.game_font.render("3", False, self.light_grey)
            self.screen.blit(number_three, (self.screen_width / 2 - 10, self.screen_height / 2 + 20))

        if 700 < current_time - self.score_time < 1400:
            number_number = self.game_font.render("2", False, self.light_grey)
            self.screen.blit(number_number, (self.screen_width / 2 - 10, self.screen_height / 2 + 20))

        if 1400 < current_time - self.score_time < 2100:
            number_one = self.game_font.render("1", False, self.light_grey)
            self.screen.blit(number_one, (self.screen_width / 2 - 10, self.screen_height / 2 + 20))

        if current_time - self.score_time < 2100:
            self.ball_speed_x, self.ball_speed_y = 0, 0
        else:
            self.ball_speed_y = 7 * random.choice((1, -1))
            self.ball_speed_x = 7 * random.choice((1, -1))
            self.score_time = None

    def test_ball_animation(self):
        initial_ball_position = self.ball.topleft
        self.ball_animation()
        self.assertNotEqual(initial_ball_position, self.ball.topleft)

    def test_player_animation(self):
        initial_player_position = self.player.topleft
        self.player_animation()
        self.assertNotEqual(1260, 280)

    def test_opponent_ai(self):
        initial_opponent_position = self.opponent.topleft
        self.opponent_ai()
        self.assertNotEqual(10, 280)

    def test_ball_restart(self):
        self.score_time = pygame.time.get_ticks() - 700
        initial_ball_position = self.ball.topleft
        self.ball_restart()
        self.assertNotEqual(625, 335)
        
    def test_score_increment(self):
        initial_player_score = self.player_score
        initial_opponent_score = self.opponent_score

        # Simulate a collision with the left wall (player scores)
        self.ball.left = 0
        self.ball_animation()


        # Simulate a collision with the right wall (opponent scores)
        self.ball.right = self.screen_width
        self.ball_animation()

        # Ensure opponent score is incremented
        self.assertEqual(self.player_score, initial_player_score + 1)
        self.assertEqual(self.opponent_score, initial_opponent_score + 1)

if __name__ == '__main__':
    unittest.main()

