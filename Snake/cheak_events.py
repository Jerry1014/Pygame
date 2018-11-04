import pygame

from sys import exit
from snake import Snake
from apple import Apple

def cheak_events(play_button,settings,sb,apple,snakes,screen):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            key_down(event,snakes)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cheak_play_button(mouse_x, mouse_y,play_button,settings,sb,apple,snakes,screen)

def key_down(event,snakes):
    """响应按下按键"""
    snakes_list = snakes.sprites()
    snake_head = snakes_list[0]
    if event.key == pygame.K_w:
        snake_head.last_time_direction = snake_head.direction
        snake_head.direction = 'w'
    elif event.key == pygame.K_a:
        snake_head.last_time_direction = snake_head.direction
        snake_head.direction = 'a'
    elif event.key == pygame.K_s:
        snake_head.last_time_direction = snake_head.direction
        snake_head.direction = 's'
    elif event.key == pygame.K_d:
        snake_head.last_time_direction = snake_head.direction
        snake_head.direction = 'd'
    elif event.key == pygame.K_q:
        exit()

def cheak_play_button(mouse_x, mouse_y,play_button,settings,sb,apple,snakes,screen):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked:
        # 重置游戏
        settings.initialize_dynamic_settings()
        sb.score = 0
        snakes.empty()
        screen_rect = screen.get_rect()
        for i in range(3):
            if(i == 0):
                snake = Snake(screen,settings,screen_rect.centerx + 2*8,screen_rect.centery)
                snake_head = snake
            else:
                snake = Snake(screen,settings,last_snake_x,last_snake_y,last_snake_diretion)
            last_snake_diretion = snake.direction
            last_snake_x = snake.rect.x
            last_snake_y = snake.rect.y
            snakes.add(snake)
        apple.update_apple()
        settings.game_active = True

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()