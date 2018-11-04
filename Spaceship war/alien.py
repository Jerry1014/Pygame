import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """��ʾ���������˵���"""

    def __init__(self, ai_settings,screen):
        """��ʼ�������˲���������ʼλ��"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # ����������ͼ�񣬲�������rect����
        self.image = pygame.image.load('images/alien2.png')
        self.rect = self.image.get_rect()

        # ÿ�����������������Ļ���ϽǸ���
        self.rect.x = 0
        self.rect.y = 0

        # �洢�����˵�׼ȷλ��
        self.x = float(self.rect.x)

        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True