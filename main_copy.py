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
PLAYER_IMG_PATH = ''  #Aufgabe 1 ToDo: Füge hier dein eigenes Bild ein
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


# --- Aufgabe 2. Spiel-Einstellungen anpassen ---
# Ändert die Zahlen, um das Spiel schwerer oder leichter zu machen.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED_X = 50          
PLAYER_SPEED_Y = 40          
BULLET_SPEED = 50          
PLAYER_LIVES_START = 3      
TEXT_COLOR = (255, 255, 255) 

# Power-Up Einstellungen
PLAYER_SIZE = (64, 100)    
ENEMY_SIZE = (64, 40)       
PLAYER_BULLET_SIZE = (32,32) 
ENEMY_BULLET_SIZE = (32, 32)  
BOSS_SIZE = (128, 200)      
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


# --- Aufgabe 3. Steuerung programmieren ---
# Hier könnt ihr die Tasten für die Steuerung des Spielers festlegen.
def handle_input(engine, event):
    player = engine.player
    if event.type == pygame.KEYDOWN:
        if engine.game_state != engine.config.STATE_PLAYING:
            if event.key == pygame.K_RETURN:
                engine.restart_game()
            return

        # Aufgabe 4
        
        if event.key == pygame.K_RIGHT: player.x_change = -PLAYER_SPEED_X
        if event.key == pygame.K_LEFT: player.x_change = PLAYER_SPEED_X
        if event.key == pygame.K_UP: player.y_change = -PLAYER_SPEED_Y
        if event.key == pygame.K_DOWN: player.y_change = PLAYER_SPEED_Y
        if event.key == pygame.K_SPACE: engine.fire_bullet(player.x, player.y)
    if event.type == pygame.KEYUP:
        if event.key in (pygame.K_RIGHT, pygame.K_d): player.x_change = 0
        if event.key in (pygame.K_UP, pygame.K_s): player.y_change = 0




# --- Spielstart ---

if __name__ == '__main__':
    config = type('Config', (), locals())()
    game = spiel_engine.GameEngine(config, handle_input)
    game.run()