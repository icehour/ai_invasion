import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """初始化飞船"""
    def __init__(self, screen, ai_setting):
        #super(Ship, self).__init__()
        super().__init__()
        self.setting = ai_setting
        self.screen = screen
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        #设置飞船位置
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #飞船移动标志位
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

        # 由于rect只能存储整数值，而移动可能时小数，因此先用个存小数的变量进行移动，再把变量赋值给rect，rect只取整数部分
        self.centery = float(self.rect.centery)
        self.centerx = float(self.rect.centerx)

    def update(self):
        """更新飞船移动位置"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.setting.ship_speed_factor
        elif self.move_left and self.rect.left > 0:
            self.centerx -= self.setting.ship_speed_factor
        elif self.move_up and self.rect.top > 0:
            self.centery -= self.setting.ship_speed_factor
        elif self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.setting.ship_speed_factor

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船置中"""
        self.rect.bottom = self.screen_rect.bottom
        self.centerx = self.screen_rect.centerx
        self.centery = self.rect.centery

