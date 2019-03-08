
### 《Python编程从入门到实践》中的飞船外星人大战项目
##
涉及到知识点
* 用到的库：sys, pygame
* 用到的类和函数：
    * sys.exit()
    * 创建游戏 pygame.init() pygame.display.setmode(width, height)
    * 游戏精灵 pygame.sprite.Sprite
    * 游戏组 pygame.sprite.Group
    * 事件监控 pygame.event.get()
    * 加载图像 pygame.image.load(path)
    * 字体渲染 
        1. 获取图像 image = pygame.font.SysFont(None,48).render()
        2. 得到区域 rect = image.get_rect()
        3. 单个图像写入屏幕 screen.blit(image, rect)
        * 整组图像写入屏幕  groups.draw(screen)
