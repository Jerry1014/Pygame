class Settings():
    """游戏的各项设置"""
    def __init__(self):
        # 屏幕的各项设置
        self.screen_set = (1200,800)
        self.screen_color = (230,230,230)

        # 关于蛇的设置
        self.snake_length = 8
        self.snake_color = 60,60,60
        self.snake_speed_scale = 0.8

        # 关于苹果的设置
        self.apple_length = 10
        self.apple_color = 100,100,100

        self.initialize_dynamic_settings()
        self.game_active = False

    def initialize_dynamic_settings(self):
        self.snake_speed_reciprocal = 0.005
        self.snake_level = 1

