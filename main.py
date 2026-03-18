import pygame
import spiel_engine

# Aufgabe 1: Trage hier den Dateinamen deines Raumschiff-Bildes ein
PLAYER_IMG_PATH = 'assets/images/player.png'

ENEMY_IMG_PATH = 'assets/images/enemy.png'
PLAYER_BULLET_IMG_PATH = 'assets/images/Laser_payer.png'
ENEMY_BULLET_IMG_PATH = 'assets/images/Laser_enemy.png'
BOSS_IMG_PATH = 'assets/images/Boss.png'
ICON_PATH = 'assets/images/enemy.png'
BACKGROUND_IMG_PATH = 'assets/images/background.png'
LIFE_POWERUP_IMG_PATH = 'assets/images/life_powerup.png'
SHIELD_POWERUP_IMG_PATH = 'assets/images/shield_powerup.png'

BACKGROUND_SOUND_PATH = 'assets/sounds/background.wav'
BULLET_SOUND_PATH = 'assets/sounds/laser.wav'
EXPLOSION_SOUND_PATH = 'assets/sounds/explosion.wav'

# Aufgabe 5: HIER Turbo-Variablen einfügen (ULT_ACTIVE, ULT_START)

# HIER Zeit-Stopp-Variablen einfügen (TIME_STOP_ACTIVE, TIME_STOP_START, TIME_STOP_DURATION)

# Aufgabe 2: Passe diese Werte an
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED_X = 5
PLAYER_SPEED_Y = 4
BULLET_SPEED = 10
PLAYER_LIVES_START = 3
TEXT_COLOR = (255, 255, 255)

PLAYER_SIZE = (64, 64)
ENEMY_SIZE = (64, 64)
PLAYER_BULLET_SIZE = (32, 32)
ENEMY_BULLET_SIZE = (32, 32)
BOSS_SIZE = (128, 128)
POWERUP_SIZE = (30, 30)
SHIELD_DURATION = 5000
POWERUP_DROP_CHANCE = 10
INVINCIBILITY_DURATION = 2000

ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 40
ENEMY_BULLET_SPEED = 7
BOSS_BULLET_SPEED = 10
POWERUP_SPEED = 3
NUM_OF_ENEMIES = 6
GAME_OVER_Y_LIMIT = 440
BOSS_HEALTH_START = 25
BULLET_COOLDOWN = 300
STATE_PLAYING, STATE_GAME_OVER, STATE_VICTORY = 0, 1, 2


def handle_input(engine, event):
    player = engine.player

    # Aufgabe 5: HIER Turbo-Timer prüfen (läuft er noch?)

    # HIER Zeit-Stopp-Timer prüfen (läuft er noch?)

    if event.type == pygame.KEYDOWN:
        if engine.game_state != engine.config.STATE_PLAYING:
            if event.key == pygame.K_RETURN:
                engine.restart_game()
            return

        # Aufgabe 3: Ersetze K_LEFT/K_RIGHT durch K_a/K_d und K_UP/K_DOWN durch K_w/K_s
        if event.key == pygame.K_LEFT:  player.x_change = -PLAYER_SPEED_X
        if event.key == pygame.K_RIGHT: player.x_change = PLAYER_SPEED_X
        if event.key == pygame.K_UP:    player.y_change = -PLAYER_SPEED_Y
        if event.key == pygame.K_DOWN:  player.y_change = PLAYER_SPEED_Y
        if event.key == pygame.K_SPACE: engine.fire_bullet(player.x, player.y)

        # Aufgabe 4: HIER Skin-Wechsel (E-Taste) einfügen

        # HIER Zeit-Stopp (T-Taste) einfügen

        # Aufgabe 5: HIER Turbo (U-Taste) einfügen

    if event.type == pygame.KEYUP:
        # Aufgabe 3: Passe auch hier K_LEFT/K_RIGHT auf K_a/K_d an (usw.)
        if event.key in (pygame.K_LEFT, pygame.K_RIGHT): player.x_change = 0
        if event.key in (pygame.K_UP, pygame.K_DOWN):    player.y_change = 0


if __name__ == '__main__':
    config = type('Config', (), locals())()
    game = spiel_engine.GameEngine(config, handle_input)
    # Aufgabe 4: HIER neues Bild laden und setzen
    game.run()
