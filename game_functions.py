import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb):
    """响应鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event, ai_settings, screen, ship, bullets, aliens, stats, sb)
        elif event.type == pygame.KEYUP:
            check_up_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, aliens, bullets, ai_settings, play_button, screen, ship, mouse_x, mouse_y, sb)


def check_up_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False
    elif event.key == pygame.K_UP:
        ship.move_up = False
    elif event.key == pygame.K_DOWN:
        ship.move_down = False


def check_down_events(event, ai_settings, screen, ship, bullets, aliens, stats, sb):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_UP:
        ship.move_up = True
    elif event.key == pygame.K_DOWN:
        ship.move_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, aliens, bullets, screen, ship, stats, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
    """发射子弹"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, ship, bullets, alien, stats, play_button, sb):
    """刷新屏幕图像"""
    screen.fill(ai_settings.color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alien.draw(screen)
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """更新子弹位置，并删除已消失的子弹"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, aliens, bullets, screen, ship, stats, sb)


def check_bullet_alien_collisions(ai_settings, aliens, bullets, screen, ship, stats, sb):
    """检查子弹和外星人碰撞，并处理相应操作"""
    # 检查是否有子弹击中外星人
    # 如果是，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, aliens, ship)


def check_high_score(stats, sb):
    """"检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_aliens(ai_settings, stats, bullets, screen, ship, aliens, sb):
    """
    检查是否有外星人位于屏幕边缘，并更新外星人位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, bullets, aliens, screen, ship, sb)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)


def create_fleet(ai_settings, screen, aliens, ship):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    """获取横向外星人数量"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (alien_width * 2))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """获取纵向外星人数量"""
    available_space_y = ai_settings.screen_height - ship_height -(3 * alien_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建单个外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, alines):
    """将整群外星人下移，并改变方向"""
    for alien in alines:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, bullets, aliens, screen, ship, sb):
    """相应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        # 更新计分牌
        sb.prep_ships()

        # 暂停
        sleep(0.5)
    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, bullets, aliens, screen, ship, sb)
            break


def check_play_button(stats, aliens, bullets, ai_settings, play_button, screen, ship, mouse_x, mouse_y, sb):
    """在玩家单机Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        start_game(ai_settings, aliens, bullets, screen, ship, stats, sb)


def start_game(ai_settings, aliens, bullets, screen, ship, stats, sb):
    # 重置游戏设置
    ai_settings.initialize_dynamic_settings()
    # 隐藏光标
    pygame.mouse.set_visible(False)
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    # 重置记分板图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()


