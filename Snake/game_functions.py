import pygame
from snake import Snake
from apple import Apple
from time import sleep

def update_snake(snakes,game_settings,screen):
    """更新贪吃蛇的位置"""
    snakes_list = snakes.sprites()
    snake_head = snakes_list[0]
    last_time_direction = snake_head.direction
    for snake in snakes:
        snake.direction = last_time_direction
        for i in range(game_settings.snake_length):
            snake.update()
        last_time_direction = snake.last_time_direction
        snake.last_time_direction = snake.direction

    # 检查蛇是否发生碰撞
    screen_rect = screen.get_rect()
    if not(snake_head.rect.bottom >= screen_rect.bottom or snake_head.rect.bottom <= 0
          or snake_head.rect.left <= 0 or snake_head.rect.right >= screen_rect.right):
        i = 0
        for snake in snakes:
            if snake_head.rect.centerx == snake.rect.centerx and snake_head.rect.centery == snake.rect.centery:
                i += 1
            if i > 1:
                snake_died(game_settings)
                break
    else:
            snake_died(game_settings)

def snake_died(game_settings):
    pygame.mouse.set_visible(True)
    game_settings.game_active = False

def update_apple(snakes,apple,screen,settings,sb):
    """检查蛇是否吃掉了苹果，并更新苹果的位置"""
    snakes_list = snakes.sprites()
    snake_head = snakes_list[0]
    result = pygame.sprite.collide_rect(snake_head,apple)
    if result:
        judge = True
        while judge:
            apple.update_apple()
            judge = False
            for snake in snakes:
                judge = pygame.sprite.collide_rect(snake_head,apple)
        snake_last = snakes_list[-1]
        snake = Snake(screen,settings,snake_last.rect.x,snake_last.rect.y,snake_last.direction)
        snakes.add(snake)
        settings.snake_speed_reciprocal *= settings.snake_speed_scale
        sb.score += 1
        if sb.score > sb.high_score:
            sb.high_score = sb.score
        sb.prep_score()
        sb.prep_high_score()

def update_screen(settings,snakes,apple,sb,play_button,screen):
    screen.fill(settings.screen_color)
    apple.draw()
    sb.draw_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not settings.game_active:
        play_button.draw_button()
    for snake in snakes:
        for i in range(settings.snake_length):
            sleep(settings.snake_speed_reciprocal)
            snake.draw_snake()

    pygame.display.flip()