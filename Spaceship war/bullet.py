import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """һ���Էɴ�������ӵ����й������"""

    def __init__(self,ai_settings,screen,ship,judge):
        super(Bullet,self).__init__()
        self.screen = screen

        # ��(0,0)������һ����ʾ�ӵ��ľ��Σ���������ȷ��λ��
        if judge:
            bullet_width = ai_settings.bullet_width_big
        else:
            bullet_width = ai_settings.bullet_width_small
        self.rect = pygame.Rect(0,0,bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # �洢��С����ʾ���ӵ�λ��
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """�����ƶ��ӵ�"""
        #���±�ʾ�ӵ�λ�õ�С��ֵ
        self.y -= self.speed_factor
        #���±�ʾ�ӵ���rect��λ��
        self.rect.y = self.y

    def draw_bullet(self):
        """����Ļ�ϻ����ӵ�"""
        pygame.draw.rect(self.screen,self.color,self.rect)