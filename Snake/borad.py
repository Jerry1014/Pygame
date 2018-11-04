import pygame

class Scoreboard():
    """显示得分信息的类"""
    def __init__(self,screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.score = 0
        self.high_score = 0

        # 显示得分信息时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        # 准备最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        score_str = str(self.score)
        self.score_image = self.font.render(score_str,True,self.text_color,)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为一幅渲染的图像"""
        high_score_str = str(self.high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def draw_score(self):
        """绘制图像"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)

class Button():
    def __init__(self,screen):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (60,60,60)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        # 将msg渲染为图像，并使其在按钮上居中
        self.msg_image = self.font.render('Play!',True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)