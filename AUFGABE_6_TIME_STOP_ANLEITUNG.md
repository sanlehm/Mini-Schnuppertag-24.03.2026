# Aufgabe 6: Time Stop - Implementierungsanleitung

## 📋 Überblick
Diese Aufgabe ermöglicht es den Kindern, einen **Time-Stop-Button** zu implementieren. Wenn sie die Taste **T** drücken, wird das Spiel für 3 Sekunden eingefroren:
- Gegner bewegen sich nicht mehr
- Gegner schießen nicht mehr
- Power-Ups fallen nicht mehr
- Nur der Spieler kann sich noch bewegen und schießen

---

## 🔧 Schritt-für-Schritt Implementierung

### Schritt 1: Variable für Time Stop hinzufügen

**Wo:** In `main.py` ganz oben, bei den anderen Variablen (nach Aufgabe 5)

**Code zum Hinzufügen:**
```python
TIME_STOP_ACTIVE = False    # Aufgabe 6: Variable für den Time-Stop-Status
TIME_STOP_START = 0         # Aufgabe 6: Variable für die Startzeit des Time Stops
TIME_STOP_DURATION = 3000   # Aufgabe 6: Dauer des Time Stops in Millisekunden (3000 = 3 Sekunden)
```

---

### Schritt 2: Time Stop Aktivierung in handle_input()

**Wo:** In der `handle_input()`-Funktion, nach dem Turbo-Code (nach Aufgabe 5)

**Code zum Hinzufügen:**
```python
        # Aufgabe 6: Code für die Aktivierung des Time Stops
        if event.key == pygame.K_t and not TIME_STOP_ACTIVE:
            TIME_STOP_ACTIVE = True
            TIME_STOP_START = pygame.time.get_ticks()
            print("Time Stop aktiviert!")
```

---

### Schritt 3: Time Stop Timer in handle_input()

**Wo:** Ganz am Anfang der `handle_input()`-Funktion (vor allen Checks)

**Code zum Hinzufügen:**
```python
    # Aufgabe 6: Time Stop nach 3 Sekunden deaktivieren
    if TIME_STOP_ACTIVE and pygame.time.get_ticks() - TIME_STOP_START > TIME_STOP_DURATION:
        TIME_STOP_ACTIVE = False
        print("Time Stop vorbei!")
```

---

### Schritt 4: Time Stop in der spiel_engine.py integrieren

**Wo A:** In der `GameEngine.__init__()`-Methode, bei der Ultimate-Initialisierung (ca. Zeile 73-74)

**Code zum Hinzufügen:**
```python
        # Time Stop
        self.TIME_STOP_ACTIVE = False
        self.TIME_STOP_START = 0
```

**Wo B:** In der `update_game_state()`-Methode, am Anfang (nach dem STATE_PLAYING Check)

**Code zum Hinzufügen:**
```python
        # Aufgabe 6: Time Stop Status synchronisieren
        import main
        self.TIME_STOP_ACTIVE = main.TIME_STOP_ACTIVE
        self.TIME_STOP_START = main.TIME_STOP_START
```

**Wo C:** In der `update_game_state()`-Methode, wo die Enemy-Logik beginnt (vor `for enemy in self.enemies:`)

**Code zum Ersetzen:**
```python
        # Enemy logic (nur wenn Time Stop nicht aktiv ist)
        if not self.TIME_STOP_ACTIVE:
            for enemy in self.enemies[:]:
                # ... Rest des Enemy-Codes bleibt gleich ...
```

**Wo D:** In der `update_game_state()`-Methode, wo Enemy Bullets bewegt werden (vor `for bullet in self.enemy_bullets:`)

**Code zum Ersetzen:**
```python
        # Enemy bullet movement (nur wenn Time Stop nicht aktiv ist)
        if not self.TIME_STOP_ACTIVE:
            for bullet in self.enemy_bullets[:]:
                if bullet.y > self.config.SCREEN_HEIGHT: self.enemy_bullets.remove(bullet)
```

**Wo E:** In der `update_game_state()`-Methode, wo Power-Ups bewegt werden (vor `for pu in self.power_ups:`)

**Code zum Ersetzen:**
```python
        # Power-up movement and collision (nur wenn Time Stop nicht aktiv ist)
        if not self.TIME_STOP_ACTIVE:
            for pu in self.power_ups[:]:
                if pu.y > self.config.SCREEN_HEIGHT: self.power_ups.remove(pu); continue
                if pu.is_colliding(self.player):
                    if pu.type == 'LIFE': self.player_lives += 1
                    elif pu.type == 'SHIELD':
                        self.player_is_shielded = True
                        self.shield_start_time = pygame.time.get_ticks()
                    self.power_ups.remove(pu)
```

---

### Schritt 5: Visueller Effekt im draw_elements()

**Wo:** In der `draw_elements()`-Methode der `GameEngine`, nach der Zeit-Anzeige (am Ende, vor `if self.game_state == ...`)

**Code zum Hinzufügen:**
```python
        # Aufgabe 6: Time Stop Effekt anzeigen
        if self.TIME_STOP_ACTIVE:
            remaining_time = max(0, (3000 - (pygame.time.get_ticks() - self.TIME_STOP_START)) / 1000)
            time_stop_text = self.font.render(f"TIME STOP: {remaining_time:.1f}s", True, (0, 255, 255))
            self.screen.blit(time_stop_text, (self.config.SCREEN_WIDTH - 350, 10))
```

---

## 📝 Word-Dokument Aufgabe 6 Text

```
Aufgabe 6: Time Stop - Dein Spiel einfrieren! ❄️

Ziel: Erweitere das Spiel um eine neue Spezialfähigkeit! 
Wenn du die Taste T drückst, werden alle Gegner und deren Schüsse 
für 3 Sekunden eingefroren - aber du kannst dich noch bewegen und schießen!

Umsetzung:

1. Neue Variablen hinzufügen
   Ganz oben in deinem main.py, nach Aufgabe 5, schreibst du:
   
   [FB6.1]
   TIME_STOP_ACTIVE = False
   TIME_STOP_START = 0
   TIME_STOP_DURATION = 3000


2. Time Stop Aktivierung
   In der handle_input() Funktion, nach dem Turbo-Code, füge hinzu:
   
   [FB6.2]
   if event.key == pygame.K_t and not TIME_STOP_ACTIVE:
       TIME_STOP_ACTIVE = True
       TIME_STOP_START = pygame.time.get_ticks()
       print("Time Stop aktiviert!")


3. Time Stop Timer
   Am Anfang der handle_input() Funktion, füge hinzu:
   
   [FB6.3]
   if TIME_STOP_ACTIVE and pygame.time.get_ticks() - TIME_STOP_START > TIME_STOP_DURATION:
       TIME_STOP_ACTIVE = False
       print("Time Stop vorbei!")


4. Spiel-Engine anpassen
   Öffne die spiel_engine.py und suche in der update_game_state() Methode 
   den Part mit der Enemy-Logik (for enemy in self.enemies:).
   
   Ersetze:
   [FB6.4]
   for enemy in self.enemies[:]:
   
   Mit:
   [FB6.5]
   if not self.TIME_STOP_ACTIVE:
       for enemy in self.enemies[:]:
   
   (Das gleiche machst du auch für die enemy_bullets und power_ups!)

Tipp: Experimentiere mit verschiedenen TIME_STOP_DURATION Werten! 
Ist 3 Sekunden zu kurz? Probiere 5000 aus!
```

---

## 🎮 Spieler-Info

**Taste zum Aktivieren:** T  
**Dauer:** 3 Sekunden  
**Effekt:** 
- ✅ Gegner bleiben stehen
- ✅ Gegner schießen nicht mehr
- ✅ Power-Ups bleiben stehen
- ✅ Der Spieler kann sich noch bewegen und schießen

---

## 🐛 Troubleshooting

**Problem:** Time Stop wird nicht aktiviert?
- Stelle sicher, dass du `pygame.K_t` (nicht `pygame.K_T`) verwendest
- Check, dass die Variable `TIME_STOP_ACTIVE` in `main.py` weit oben deklariert ist

**Problem:** Gegner bewegen sich trotzdem?
- Überprüfe, ob du wirklich `if not self.TIME_STOP_ACTIVE:` VOR der Enemy-Logik eingefügt hast
- Achte auf die Einrückung (Indentation)!

**Problem:** Time Stop läuft nicht ab?
- Stelle sicher, dass der Timer-Check am Anfang von `handle_input()` ist
- Kontrolliere die TIME_STOP_DURATION - ist sie in Millisekunden?

