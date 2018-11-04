import pygame
from random import randint

class Apple():
    """游戏中被贪吃蛇吃的苹果"""
    def __init__(self,screen,settings):
        self.screen = screen

        # 关于苹果的设置
        self.rect = pygame.Rect(randint(5,1190),randint(5,790),settings.apple_length,settings.apple_length)
        self.color = settings.apple_color

    def update_apple(self):
        """更新苹果的位置"""
        self.rect.x = randint(5,1180)
        self.rect.y = randint(5,780)

    def draw(self):
        """绘制苹果"""
        pygame.draw.rect(self.screen,self.color,self.rect)