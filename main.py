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
PLAYER_IMG_PATHS = ['assets/images/robin.png', 'assets/images/player.png', 'assets/images/robin.png'] # Aufgabe 1: Ändere hier den Bild-Pfad für dein Raumschiff
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

ULT_ACTIVE = False # Aufgabe 5: Variable für den Turbo-Status
ULT_START = 0      # Aufgabe 5: Variable für die Startzeit des Turbos


# --- 2. Spiel-Einstellungen anpassen --- # Aufgabe 2: Ändere hier die Werte, um das Spiel anzupassen.
# Ändert die Zahlen, um das Spiel schwerer oder leichter zu machen.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED_X = 5          # Geschwindigkeit des Spielers nach links/rechts
PLAYER_SPEED_Y = 4          # Geschwindigkeit des Spielers nach oben/unten
BULLET_SPEED = 10           # Geschwindigkeit der Spieler-Kugeln
PLAYER_LIVES_START = 3      # Anzahl der Leben am Anfang
TEXT_COLOR = (255, 255, 255) # Farbe für Score, Level und Leben (Weiss)

# Power-Up Einstellungen
PLAYER_SIZE = (64, 64)      # Grösse des Spieler-Bildes in Pixel (Breite, Höhe)
ENEMY_SIZE = (64, 64)       # Grösse des Gegner-Bildes in Pixel (Breite, Höhe)
PLAYER_BULLET_SIZE = (32,32) # Grösse des Spieler-Kugel-Bildes in Pixel (Breite, Höhe)
ENEMY_BULLET_SIZE = (32, 32)  # Grösse des Gegner-Kugel-Bildes in Pixel (Breite, Höhe)
BOSS_SIZE = (128, 128)      # Grösse des Boss-Bildes in Pixel (Breite, Höhe)
POWERUP_SIZE = (30, 30)       # Grösse der Power-Up Bilder in Pixel (Breite, Höhe)
SHIELD_DURATION = 5000        # Dauer des Schilds in Millisekunden (5000 = 5 Sekunden)
POWERUP_DROP_CHANCE = 10      # Chance, dass ein Power-Up erscheint (1 zu 10)
INVINCIBILITY_DURATION = 2000 # Dauer der Unverwundbarkeit nach Treffer in ms (2000 = 2s)


# --- 3. Steuerung programmieren ---
# Hier könnt ihr die Tasten für die Steuerung des Spielers festlegen.

def handle_input(engine, event):
    global ULT_ACTIVE, ULT_START
    player = engine.player
    
    # Aufgabe 5: Turbo nach 2 Sekunden ausschalten
    if ULT_ACTIVE and pygame.time.get_ticks() - ULT_START > 2000:
        ULT_ACTIVE = False
        print("Turbo vorbei!")
    
    if event.type == pygame.KEYDOWN:
        if engine.game_state != engine.config.STATE_PLAYING:
            if event.key == pygame.K_RETURN:
                engine.restart_game()
            return

        # Aufgabe 4: Code für den Skin-Wechsel
        if event.key == pygame.K_e:
            global player_skin_index
            player_skin_index = (player_skin_index + 1) % len(PLAYER_IMG_PATHS)
            loaded_img = pygame.image.load(PLAYER_IMG_PATHS[player_skin_index]).convert_alpha()
            player.img = pygame.transform.scale(loaded_img, PLAYER_SIZE)

        # Aufgabe 5: Code für die Aktivierung des Turbos
        if event.key == pygame.K_u and not ULT_ACTIVE:
            ULT_ACTIVE = True
            ULT_START = pygame.time.get_ticks()
            print("Turbo aktiviert!")

        # Aufgabe 5: Geschwindigkeit verdoppeln, wenn Turbo aktiv ist
        speed = 2 if ULT_ACTIVE else 1
        # Aufgabe 3: Steuerung mit W, A, S, D (KEYDOWN)
        if event.key == pygame.K_a: player.x_change = -PLAYER_SPEED_X * speed
        if event.key == pygame.K_d: player.x_change = PLAYER_SPEED_X * speed
        if event.key == pygame.K_w: player.y_change = -PLAYER_SPEED_Y * speed
        if event.key == pygame.K_s: player.y_change = PLAYER_SPEED_Y * speed
        if event.key == pygame.K_SPACE: engine.fire_bullet(player.x, player.y)
    if event.type == pygame.KEYUP:
        # Aufgabe 3: Bewegung stoppen, wenn Tasten losgelassen werden (KEYUP)
        if event.key in (pygame.K_a, pygame.K_d): player.x_change = 0
        if event.key in (pygame.K_w, pygame.K_s): player.y_change = 0


# ===================================================================================
# HIER BEGINNT DIE SPIEL-ENGINE (Normalerweise nicht ändern)
# ===================================================================================

# --- Interne Konfiguration (nicht für Teilnehmer gedacht) ---
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

# --- Spielstart ---

if __name__ == '__main__':
    config = type('Config', (), locals())()
    game = spiel_engine.GameEngine(config, handle_input)
    loaded_img = pygame.image.load(PLAYER_IMG_PATHS[player_skin_index]).convert_alpha()
    game.player.img = pygame.transform.scale(loaded_img, PLAYER_SIZE)
    game.run()