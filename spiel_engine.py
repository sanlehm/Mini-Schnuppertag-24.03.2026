import math
import random
import pygame
from pygame import mixer

class GameEngine:
    def __init__(self, config, input_handler):
        self.config = config
        self.input_handler = input_handler
        pygame.init()

        # Screen
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invader")
        icon = pygame.image.load(config.ICON_PATH)
        pygame.display.set_icon(icon)

        # Background and Sound
        self.background = pygame.image.load(config.BACKGROUND_IMG_PATH)
        mixer.music.load(config.BACKGROUND_SOUND_PATH)
        mixer.music.play(-1)
        self.bullet_sound = mixer.Sound(config.BULLET_SOUND_PATH)
        self.explosion_sound = mixer.Sound(config.EXPLOSION_SOUND_PATH)

        # Load Assets
        # Unterstützt sowohl PLAYER_IMG_PATH (einzelnes Bild) als auch PLAYER_IMG_PATHS (Array)
        try:
            # Versuche zuerst PLAYER_IMG_PATHS (Array) zu laden
            self.player_img = pygame.image.load(config.PLAYER_IMG_PATHS[0]).convert_alpha()
        except (AttributeError, TypeError):
            # Falls das nicht klappt, verwende PLAYER_IMG_PATH (einzelnes Bild)
            self.player_img = pygame.image.load(config.PLAYER_IMG_PATH).convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, self.config.PLAYER_SIZE)
        self.enemy_img = pygame.image.load(config.ENEMY_IMG_PATH).convert_alpha()
        self.enemy_img = pygame.transform.scale(self.enemy_img, self.config.ENEMY_SIZE)
        self.player_bullet_img = pygame.image.load(config.PLAYER_BULLET_IMG_PATH).convert_alpha()
        self.player_bullet_img = pygame.transform.scale(self.player_bullet_img, self.config.PLAYER_BULLET_SIZE)
        self.enemy_bullet_img = pygame.image.load(config.ENEMY_BULLET_IMG_PATH).convert_alpha()
        self.enemy_bullet_img = pygame.transform.scale(self.enemy_bullet_img, self.config.ENEMY_BULLET_SIZE)
        try:
            self.boss_img = pygame.image.load(config.BOSS_IMG_PATH).convert_alpha()
            self.boss_img = pygame.transform.scale(self.boss_img, self.config.BOSS_SIZE)
        except pygame.error:
            print(f"Warnung: '{config.BOSS_IMG_PATH}' nicht gefunden. Es wird ein Ersatzbild verwendet.")
            self.boss_img = self.enemy_img
        
        # Load Power-Up images, with fallback to colored squares
        try:
            self.life_powerup_img = pygame.image.load(config.LIFE_POWERUP_IMG_PATH).convert_alpha()
            self.life_powerup_img = pygame.transform.scale(self.life_powerup_img, self.config.POWERUP_SIZE)
        except pygame.error:
            print(f"Warnung: '{config.LIFE_POWERUP_IMG_PATH}' nicht gefunden. Rotes Viereck wird als Ersatz verwendet.")
            self.life_powerup_img = pygame.Surface(self.config.POWERUP_SIZE)
            self.life_powerup_img.fill((255, 0, 0))
        
        try:
            self.shield_powerup_img = pygame.image.load(config.SHIELD_POWERUP_IMG_PATH).convert_alpha()
            self.shield_powerup_img = pygame.transform.scale(self.shield_powerup_img, self.config.POWERUP_SIZE)
        except pygame.error:
            print(f"Warnung: '{config.SHIELD_POWERUP_IMG_PATH}' nicht gefunden. Blaues Viereck wird als Ersatz verwendet.")
            self.shield_powerup_img = pygame.Surface(self.config.POWERUP_SIZE)
            self.shield_powerup_img.fill((0, 0, 255))

        # Game State
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.big_font = pygame.font.Font('freesansbold.ttf', 64)
        self.game_state = self.config.STATE_PLAYING
        self.score_value = 0
        self.high_score = self.load_highscore()
        self.current_level = 1
        self.player_lives = config.PLAYER_LIVES_START
        self.last_bullet_time = 0
        
        self.player_is_shielded = False
        self.shield_start_time = 0
        self.player_is_invincible = False
        self.invincibility_start_time = 0
        
        # Ultimate/Turbo
        self.ULT_ACTIVE = False
        self.ULT_START = 0

        # Game Objects
        self.player = self.Player(self, self.player_img, 370, 480)
        self.enemies = []
        self.boss = None
        self.bullets = []
        self.enemy_bullets = []
        self.power_ups = []

    def start_level(self, level):
        self.enemies.clear(); self.bullets.clear(); self.enemy_bullets.clear(); self.power_ups.clear()
        
        # Boss level every 6 levels
        if level % 6 == 0:
            self.boss = self.Boss(self, self.boss_img)
            # Increase boss health for higher boss levels
            self.boss.health += (level / 6 - 1) * 10 
            self.enemies.append(self.boss)
        # Normal levels
        else:
            num_enemies = 3 + (level - 1)
            # Cap the number of enemies to avoid overwhelming the player
            num_enemies = min(num_enemies, 15)
            for _ in range(num_enemies):
                enemy = self.Enemy(self, self.enemy_img)
                enemy.update_speed(level)
                self.enemies.append(enemy)

    def run(self):
        self.start_level(self.current_level)
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.input_handler(self, event)

            self.update_game_state()
            self.draw_elements()
            
            pygame.display.update()

    def update_game_state(self):
        if self.game_state != self.config.STATE_PLAYING:
            return

        current_time = pygame.time.get_ticks()

        # Player movement and boundaries
        self.player.x += self.player.x_change
        self.player.y += self.player.y_change
        self.player.x = max(0, min(self.player.x, self.config.SCREEN_WIDTH - self.player.img.get_width()))
        self.player.y = max(0, min(self.player.y, self.config.SCREEN_HEIGHT - self.player.img.get_height()))
        self.player.rect.topleft = (self.player.x, self.player.y)

        # Shield and Invincibility timeout
        if self.player_is_shielded and current_time - self.shield_start_time > self.config.SHIELD_DURATION:
            self.player_is_shielded = False
        if self.player_is_invincible and current_time - self.invincibility_start_time > self.config.INVINCIBILITY_DURATION:
            self.player_is_invincible = False
        
        # Ultimate timeout
        if self.ULT_ACTIVE and current_time - self.ULT_START > 2000:
            self.ULT_ACTIVE = False
            print("Turbo vorbei!")

        # --- Collision Checks (only if not invincible) ---
        if not self.player_is_invincible:
            # Enemy collision with player
            for enemy in self.enemies[:]:
                if enemy.is_colliding(self.player):
                    self.handle_player_hit()
                    if not isinstance(enemy, self.Boss):
                        self.enemies.remove(enemy)
                    break # Stop checking after one hit
            
            # Enemy bullet collision with player
            for bullet in self.enemy_bullets[:]:
                if bullet.is_colliding(self.player):
                    self.enemy_bullets.remove(bullet)
                    self.handle_player_hit()
                    if self.game_state == self.config.STATE_GAME_OVER: return
                    break # Stop checking after one hit

        # Enemy logic
        for enemy in self.enemies[:]:
            enemy.x += enemy.x_change
            if enemy.x <= 0 or enemy.x >= self.config.SCREEN_WIDTH - enemy.img.get_width():
                enemy.x_change *= -1
                if not isinstance(enemy, self.Boss): enemy.y += enemy.y_change

            # Wenn ein normaler Gegner (kein Boss) unter den Bildschirm geht, 
            # setze ihn wieder oben (Respawn)
            if not isinstance(enemy, self.Boss) and enemy.y > self.config.SCREEN_HEIGHT:
                enemy.y = random.randint(50, 150)
                enemy.x = random.randint(0, self.config.SCREEN_WIDTH - enemy.img.get_width())

            if isinstance(enemy, self.Boss): self.boss_fire(enemy)
            else: self.enemy_fire(enemy)

            # Player bullet collision with enemy
            for bullet in self.bullets[:]:
                if enemy.is_colliding(bullet):
                    self.explosion_sound.play()
                    self.bullets.remove(bullet)
                    if isinstance(enemy, self.Boss):
                        self.boss.health -= 1
                        self.score_value += 5
                        if self.boss.health <= 0:
                            self.enemies.remove(enemy)
                            self.score_value += 50
                    else:
                        self.score_value += 1
                        enemy_x, enemy_y = enemy.x, enemy.y
                        self.enemies.remove(enemy)
                        if random.randint(1, self.config.POWERUP_DROP_CHANCE) == 1:
                            ptype = random.choice(['LIFE', 'SHIELD'])
                            img = self.life_powerup_img if ptype == 'LIFE' else self.shield_powerup_img
                            self.power_ups.append(self.PowerUp(self, enemy_x, enemy_y, ptype, img))
                    break
        
        # Bullet movement
        for bullet in self.bullets[:]:
            if bullet.y <= 0: self.bullets.remove(bullet)
            bullet.y -= bullet.y_change

        for bullet in self.enemy_bullets[:]:
            if bullet.y > self.config.SCREEN_HEIGHT: self.enemy_bullets.remove(bullet)

        # Power-up movement and collision
        for pu in self.power_ups[:]:
            if pu.y > self.config.SCREEN_HEIGHT: self.power_ups.remove(pu); continue
            if pu.is_colliding(self.player):
                if pu.type == 'LIFE': self.player_lives += 1
                elif pu.type == 'SHIELD':
                    self.player_is_shielded = True
                    self.shield_start_time = pygame.time.get_ticks()
                self.power_ups.remove(pu)

        # Level progression
        if not self.enemies:
            self.current_level += 1
            self.start_level(self.current_level)

    def draw_elements(self):
        for pu in self.power_ups: pu.draw()
        for enemy in self.enemies: enemy.draw()
        for bullet in self.bullets: bullet.draw()
        for bullet in self.enemy_bullets: bullet.draw()

        # Player blinking effect when invincible
        if self.player_is_invincible:
            if (pygame.time.get_ticks() // 200) % 2 == 0:
                self.player.draw()
        else:
            self.player.draw()

        if self.player_is_shielded:
            pygame.draw.circle(self.screen, (0, 191, 255), (int(self.player.x + self.player.img.get_width()/2), int(self.player.y + self.player.img.get_height()/2)), 40, 3)

        self.show_score(10, 10)
        self.show_level(10, 50)
        self.show_lives(10, 90)

        if self.game_state == self.config.STATE_GAME_OVER: self.game_over_text()

    def handle_player_hit(self):
        if self.player_is_invincible: return
        
        if self.player_is_shielded:
            self.player_is_shielded = False
            return

        self.player_lives -= 1
        self.player_is_invincible = True
        self.invincibility_start_time = pygame.time.get_ticks()
        
        if self.player_lives <= 0:
            self.game_state = self.config.STATE_GAME_OVER
        else:
            self.player.x, self.player.y = 370, 480

    def fire_bullet(self, x, y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_time > self.config.BULLET_COOLDOWN:
            self.last_bullet_time = current_time
            self.bullets.append(self.Bullet(self, x, y, self.player_bullet_img))
            self.bullet_sound.play()

    def enemy_fire(self, enemy):
        if random.randint(0, 200) == 1:
            self.enemy_bullets.append(self.EnemyBullet(self, enemy.x, enemy.y, self.enemy_bullet_img, self.config.ENEMY_BULLET_SPEED))

    def boss_fire(self, boss):
        if random.randint(0, 50) == 1:
            attack_type = random.choice(['normal', 'spread'])
            if attack_type == 'normal':
                self.enemy_bullets.append(self.EnemyBullet(self, boss.x + 64, boss.y + 64, self.enemy_bullet_img, self.config.BOSS_BULLET_SPEED))
            elif attack_type == 'spread':
                self.enemy_bullets.append(self.EnemyBullet(self, boss.x + 64, boss.y + 64, self.enemy_bullet_img, self.config.BOSS_BULLET_SPEED, -2))
                self.enemy_bullets.append(self.EnemyBullet(self, boss.x + 64, boss.y + 64, self.enemy_bullet_img, self.config.BOSS_BULLET_SPEED, 0))
                self.enemy_bullets.append(self.EnemyBullet(self, boss.x + 64, boss.y + 64, self.enemy_bullet_img, self.config.BOSS_BULLET_SPEED, 2))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        if self.score_value > self.high_score:
            self.high_score = self.score_value
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))

    def show_score(self, x, y): self.screen.blit(self.font.render(f"Score : {self.score_value}", True, self.config.TEXT_COLOR), (x, y))

    def show_level(self, x, y): self.screen.blit(self.font.render(f"Level : {self.current_level}", True, self.config.TEXT_COLOR), (x, y))
    def show_lives(self, x, y): self.screen.blit(self.font.render(f"Lives : {self.player_lives}", True, self.config.TEXT_COLOR), (x, y))
    def game_over_text(self): 
        self.save_highscore()
        self.screen.blit(self.big_font.render("GAME OVER", True, self.config.TEXT_COLOR), (200, 250))
        self.screen.blit(self.font.render(f"High Score : {self.high_score}", True, self.config.TEXT_COLOR), (230, 350))
        if self.score_value > self.high_score:
            self.screen.blit(self.font.render("New High Score!", True, (255, 255, 0)), (230, 400))
        self.screen.blit(self.font.render("Press Enter to Restart", True, self.config.TEXT_COLOR), (230, 450))


    def restart_game(self):
        self.save_highscore()
        self.game_state = self.config.STATE_PLAYING
        self.score_value = 0
        self.current_level = 1
        self.player_lives = self.config.PLAYER_LIVES_START
        self.player.x, self.player.y = 370, 480
        self.start_level(self.current_level)

    class Player:
        def __init__(self, engine, img_surface, x, y):
            self.engine, self.img, self.x, self.y, self.x_change, self.y_change = engine, img_surface, x, y, 0, 0
            self.rect = self.img.get_rect(topleft=(self.x, self.y))
        def draw(self): self.engine.screen.blit(self.img, (self.x, self.y))

    class Enemy:
        def __init__(self, engine, img_surface):
            self.engine = engine
            self.img = img_surface
            self.x = random.randint(0, 736)
            self.y = random.randint(50, 150)
            self.x_change = engine.config.ENEMY_SPEED_X
            self.y_change = engine.config.ENEMY_SPEED_Y
            self.rect = self.img.get_rect(topleft=(self.x, self.y))
        def update_speed(self, level): self.x_change = (abs(self.x_change) + (level - 1) * 0.5) * (1 if self.x_change > 0 else -1)
        def draw(self):
            self.rect.topleft = (self.x, self.y)
            self.engine.screen.blit(self.img, (self.x, self.y))
        def is_colliding(self, other):
            return self.rect.colliderect(other.rect)

    class Boss(Enemy):
        def __init__(self, engine, img_surface):
            super().__init__(engine, img_surface)
            self.img = img_surface
            self.rect = self.img.get_rect()
            self.x = engine.config.SCREEN_WIDTH / 2 - self.img.get_width() / 2
            self.y = 50
            self.x_change = engine.config.ENEMY_SPEED_X / 2
            self.health = engine.config.BOSS_HEALTH_START
        def draw(self):
            super().draw()
            health_ratio = self.health / self.engine.config.BOSS_HEALTH_START
            pygame.draw.rect(self.engine.screen, (255, 0, 0), (self.x, self.y - 20, self.img.get_width(), 10))
            pygame.draw.rect(self.engine.screen, (0, 255, 0), (self.x, self.y - 20, self.img.get_width() * health_ratio, 10))

    class Bullet:
        def __init__(self, engine, x, y, img_surface):
            self.engine = engine
            self.img = img_surface
            self.x = x + 16
            self.y = y + 10
            self.y_change = engine.config.BULLET_SPEED
            self.rect = self.img.get_rect(topleft=(self.x, self.y))
        def draw(self):
            self.rect.topleft = (self.x, self.y)
            self.engine.screen.blit(self.img, (self.x, self.y))
        def is_colliding(self, other):
            return self.rect.colliderect(other.rect)

    class EnemyBullet(Bullet):
        def __init__(self, engine, x, y, img_surface, speed, x_change=0):
            super().__init__(engine, x, y, img_surface)
            self.y_change = speed
            self.x_change = x_change
        def draw(self):
            self.x += self.x_change
            self.y += self.y_change
            self.rect.topleft = (self.x, self.y)
            self.engine.screen.blit(self.img, (self.x, self.y))

    class PowerUp:
        def __init__(self, engine, center_x, center_y, type, img):
            self.engine = engine
            self.type = type
            self.img = img
            self.x = center_x - self.img.get_width() / 2
            self.y = center_y
            self.rect = self.img.get_rect(topleft=(self.x, self.y))
        def draw(self):
            self.y += self.engine.config.POWERUP_SPEED
            self.rect.topleft = (self.x, self.y)
            self.engine.screen.blit(self.img, (self.x, self.y))
        def is_colliding(self, player):
            return self.rect.colliderect(player.rect)
