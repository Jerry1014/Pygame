import pygame
from pygame.sprite import Sprite

class Snake(Sprite):
    """游戏中的贪吃蛇"""
    def __init__(self,screen,settings,last_snake_x,
                 last_snake_y,last_snake_diretion = 'd'):
        super().__init__()
        self.screen = screen

        # 关于蛇的设置
        self.direction = last_snake_diretion
        self.last_time_direction = 'd'
        self.length = settings.snake_length
        if self.direction == 'w':
            self.rect = pygame.Rect(last_snake_x,last_snake_y + self.length,
                                settings.snake_length,settings.snake_length)
        elif self.direction == 'a':
            self.rect = pygame.Rect(last_snake_x + self.length,last_snake_y,
                                settings.snake_length,settings.snake_length)
        elif self.direction == 's':
            self.rect = pygame.Rect(last_snake_x,last_snake_y - self.length,
                                settings.snake_length,settings.snake_length)
        elif self.direction == 'd':
            self.rect = pygame.Rect(last_snake_x - self.length,last_snake_y,
                                settings.snake_length,settings.snake_length)
        self.color = settings.snake_color

    def update(self):
        """更新贪吃蛇的位置"""
        if self.direction == 's':
            self.rect.y += 1
        elif self.direction == 'a':
            self.rect.x -= 1
        elif self.direction == 'w':
            self.rect.y -= 1
        elif self.direction == 'd':
            self.rect.x += 1

    def draw_snake(self):
        """绘制贪吃蛇"""
        pygame.draw.rect(self.screen,self.color,self.rect)