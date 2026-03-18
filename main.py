import pygame
import spiel_engine

# ===================================================================================
# ANPASSUNGEN FÜR DEN SCHNUPPERTAG
# ===================================================================================
# In diesem Bereich könnt ihr das Spiel nach euren Wünschen anpassen.
# Ändert die Bilder, die Geschwindigkeiten oder die Tasten für die Steuerung.
# ===================================================================================

# --- 1. Bilder und Sounds anpassen ---
# Ändert die Dateinamen, um eure eigenen Bilder und Sounds zu verwenden.
# Die Bilder müssen im selben Ordner wie diese Datei sein.
PLAYER_IMG_PATHS = ['assets/images/robin.png', 'assets/images/player.png', 'assets/images/robin.png']
player_skin_index = 0
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

ULT_ACTIVE = False
ULT_START = 0

TIME_STOP_ACTIVE = False
TIME_STOP_START = 0
TIME_STOP_DURATION = 3000


# --- 2. Spiel-Einstellungen anpassen ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED_X = 5
PLAYER_SPEED_Y = 4
BULLET_SPEED = 10
PLAYER_LIVES_START = 3
TEXT_COLOR = (255, 255, 255)

# Power-Up Einstellungen
PLAYER_SIZE = (64, 64)
ENEMY_SIZE = (64, 64)
PLAYER_BULLET_SIZE = (32,32)
ENEMY_BULLET_SIZE = (32, 32)
BOSS_SIZE = (128, 128)
POWERUP_SIZE = (30, 30)
SHIELD_DURATION = 5000
POWERUP_DROP_CHANCE = 10
INVINCIBILITY_DURATION = 2000


# --- 3. Steuerung programmieren ---
# Hier könnt ihr die Tasten für die Steuerung des Spielers festlegen.

def handle_input(engine, event):
    global ULT_ACTIVE, ULT_START, TIME_STOP_ACTIVE, TIME_STOP_START
    player = engine.player

    # Time Stop nach 3 Sekunden deaktivieren
    if TIME_STOP_ACTIVE and pygame.time.get_ticks() - TIME_STOP_START > TIME_STOP_DURATION:
        TIME_STOP_ACTIVE = False
        print("Time Stop vorbei!")

    # Turbo nach 2 Sekunden ausschalten
    if ULT_ACTIVE and pygame.time.get_ticks() - ULT_START > 2000:
        ULT_ACTIVE = False
        print("Turbo vorbei!")

    if event.type == pygame.KEYDOWN:
        if engine.game_state != engine.config.STATE_PLAYING:
            if event.key == pygame.K_RETURN:
                engine.restart_game()
            return

        # Skin-Wechsel mit E
        if event.key == pygame.K_e:
            global player_skin_index
            player_skin_index = (player_skin_index + 1) % len(PLAYER_IMG_PATHS)
            loaded_img = pygame.image.load(PLAYER_IMG_PATHS[player_skin_index]).convert_alpha()
            player.img = pygame.transform.scale(loaded_img, PLAYER_SIZE)

        # Turbo mit U
        if event.key == pygame.K_u and not ULT_ACTIVE:
            ULT_ACTIVE = True
            ULT_START = pygame.time.get_ticks()
            print("Turbo aktiviert!")

        # Time Stop mit T
        if event.key == pygame.K_t and not TIME_STOP_ACTIVE:
            TIME_STOP_ACTIVE = True
            TIME_STOP_START = pygame.time.get_ticks()
            print("Time Stop aktiviert!")

        # Geschwindigkeit verdoppeln, wenn Turbo aktiv ist
        speed = 2 if ULT_ACTIVE else 1
        # Steuerung mit W, A, S, D
        if event.key == pygame.K_a: player.x_change = -PLAYER_SPEED_X * speed
        if event.key == pygame.K_d: player.x_change = PLAYER_SPEED_X * speed
        if event.key == pygame.K_w: player.y_change = -PLAYER_SPEED_Y * speed
        if event.key == pygame.K_s: player.y_change = PLAYER_SPEED_Y * speed
        if event.key == pygame.K_SPACE: engine.fire_bullet(player.x, player.y)
    if event.type == pygame.KEYUP:
        # Bewegung stoppen, wenn Tasten losgelassen werden
        if event.key in (pygame.K_a, pygame.K_d): player.x_change = 0
        if event.key in (pygame.K_w, pygame.K_s): player.y_change = 0


# ===================================================================================
# HIER BEGINNT DIE SPIEL-ENGINE (Normalerweise nicht ändern)
# ===================================================================================


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


if __name__ == '__main__':
    config = type('Config', (), locals())()
    game = spiel_engine.GameEngine(config, handle_input)
    loaded_img = pygame.image.load(PLAYER_IMG_PATHS[player_skin_index]).convert_alpha()
    game.player.img = pygame.transform.scale(loaded_img, PLAYER_SIZE)
    game.run()