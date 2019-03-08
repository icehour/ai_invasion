import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("AI INVASION")
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)
    stats = GameStats(ai_settings)

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建计分牌
    sb = ScoreBoard(screen, ai_settings, stats)

    while True:
        gf.check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(ai_settings, stats, bullets, screen, ship, aliens, sb)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb)

run_game()
