# -*- coding:utf-8 -*-
import pygame
from pygame.sprite import Group
from cheak_events import cheak_events
from game_functions import update_snake,update_apple,update_screen
from snake import Snake
from borad import Button,Scoreboard
from apple import Apple

from settings import Settings

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(game_settings.screen_set)
    pygame.display.set_caption("Gluttonous Snake")

    snakes = Group()
    for i in range(3):
        screen_rect = screen.get_rect()
        if(i == 0):
            snake = Snake(screen,game_settings,screen_rect.centerx - 9,screen_rect.centery)
        else:
            snake = Snake(screen,game_settings,last_snake_x,last_snake_y,last_snake_diretion)
        last_snake_diretion = snake.direction
        last_snake_x = snake.rect.x
        last_snake_y = snake.rect.y
        snakes.add(snake)
    play_button = Button(screen)
    sb = Scoreboard(screen)
    apple = Apple(screen,game_settings)

    # 开始游戏的主循环
    while True:
        cheak_events(play_button,game_settings,sb,apple,snakes,screen)
        if game_settings.game_active:
            update_snake(snakes,game_settings,screen)
            update_apple(snakes,apple,screen,game_settings,sb)
        update_screen(game_settings,snakes,apple,sb,play_button,screen)

run_game()
