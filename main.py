import pygame
import random
import sys
import math

# Inisialisasi Pygame & Mixer (Audio)
pygame.init()
pygame.mixer.init()

# Konstanta Dimensi Layar
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car : Mini Game")

# Palet Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
ORANGE = (255, 140, 0)
DARK_GREY = (45, 45, 45)
LIGHT_GREY = (180, 180, 180)
GREEN = (34, 139, 34)
DARK_GREEN = (20, 80, 20)
PINE_GREEN = (15, 60, 25)
YELLOW = (255, 215, 0)
BLUE = (30, 144, 255)
BROWN = (92, 64, 51)
PURPLE = (128, 0, 128)
SILVER = (192, 192, 192)
CYAN = (0, 255, 255)

# Daftar warna acak untuk mobil rintangan
CAR_COLORS = [RED, ORANGE, BLUE, PURPLE, SILVER, CYAN, WHITE, YELLOW]

# Setup Frame Rate
clock = pygame.time.Clock()
FPS = 60

# --- FUNGSI LOAD SOUND EFFECT ---
def load_sfx(filename):
    try:
        return pygame.mixer.Sound(filename)
    except:
        return None

# Silakan tambahkan file .wav ini di folder yang sama agar ada suaranya
sfx_move = load_sfx("move.wav")
sfx_crash = load_sfx("crash.wav")
sfx_score = load_sfx("score.wav")
sfx_jumpscare = load_sfx("jumpscare.wav")
sfx_cihuy = load_sfx("cihuy.wav") 
sfx_gameover = load_sfx("gameover.wav")

def play_sfx(sfx):
    if sfx is not None:
        sfx.play()

# --- KONFIGURASI JALUR ---
LANE_COUNT = 5
ROAD_LEFT = 70
ROAD_RIGHT = SCREEN_WIDTH - 70
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

CAR_WIDTH = int(LANE_WIDTH * 0.6)
CAR_HEIGHT = int(CAR_WIDTH * 1.6)

# Memuat Aset Pemain
try:
    player_image = pygame.image.load('image_0.png').convert_alpha()
    player_image = pygame.transform.scale(player_image, (CAR_WIDTH, CAR_HEIGHT))
except FileNotFoundError:
    player_image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(player_image, RED, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=5)
    pygame.draw.rect(player_image, BLACK, (0, 0, CAR_WIDTH, CAR_HEIGHT), 3, border_radius=5)
    pygame.draw.rect(player_image, BLACK, (6, 15, CAR_WIDTH-12, 15))
    pygame.draw.rect(player_image, BLACK, (6, CAR_HEIGHT-30, CAR_WIDTH-12, 15))

# MENAMBAHKAN LAMPU DEPAN KE MOBIL PEMAIN
pygame.draw.rect(player_image, YELLOW, (4, 0, 8, 6), border_radius=2)
pygame.draw.rect(player_image, YELLOW, (CAR_WIDTH - 12, 0, 8, 6), border_radius=2)

headlight_img = pygame.Surface((300, 400), pygame.SRCALPHA)

# --- FUNGSI PEMBUAT ASET RINTANGAN & SCENERY ---

def create_cone():
    sz = int(LANE_WIDTH * 0.5)
    s = pygame.Surface((sz, sz), pygame.SRCALPHA)
    pygame.draw.rect(s, BLACK, (2, sz-6, sz-4, 4))
    pygame.draw.polygon(s, ORANGE, [(sz//2, 2), (4, sz-6), (sz-4, sz-6)])
    pygame.draw.polygon(s, WHITE, [(sz//2, sz//3), (sz//3 + 2, sz//2 + 2), (sz - sz//3 - 2, sz//2 + 2)])
    return s, sz, sz

def create_car(color):
    s = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(s, BLACK, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=6)
    pygame.draw.rect(s, color, (2, 2, CAR_WIDTH-4, CAR_HEIGHT-4), border_radius=4)
    pygame.draw.rect(s, BLACK, (6, 16, CAR_WIDTH-12, 12))
    pygame.draw.rect(s, BLACK, (6, CAR_HEIGHT-28, CAR_WIDTH-12, 12))
    return s, CAR_WIDTH, CAR_HEIGHT

def create_truck():
    h = int(CAR_HEIGHT * 1.4)
    s = pygame.Surface((CAR_WIDTH, h), pygame.SRCALPHA)
    pygame.draw.rect(s, WHITE, (2, 20, CAR_WIDTH-4, h-22), border_radius=2)
    pygame.draw.rect(s, BLACK, (2, 20, CAR_WIDTH-4, h-22), 2)
    pygame.draw.rect(s, BLUE, (4, 0, CAR_WIDTH-8, 22), border_radius=4)
    pygame.draw.rect(s, BLACK, (6, 8, CAR_WIDTH-12, 10))
    return s, CAR_WIDTH, h

def create_bus():
    h = int(CAR_HEIGHT * 1.6)
    w = int(CAR_WIDTH * 1.1)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, YELLOW, (0, 0, w, h), border_radius=4)
    pygame.draw.rect(s, BLACK, (0, 0, w, h), 2, border_radius=4)
    pygame.draw.rect(s, CYAN, (4, 8, w-8, 12))
    for i in range(25, h-10, 20):
        pygame.draw.rect(s, BLACK, (2, i, 8, 12))
        pygame.draw.rect(s, BLACK, (w-10, i, 8, 12))
    return s, w, h

def create_van(): 
    h = int(CAR_HEIGHT * 1.2)
    w = int(CAR_WIDTH * 1.1)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, SILVER, (0, 0, w, h), border_radius=3)
    pygame.draw.rect(s, BLACK, (0, 0, w, h), 2, border_radius=3)
    pygame.draw.rect(s, BLACK, (4, 15, w-8, 20))
    pygame.draw.rect(s, BLACK, (4, 40, w-8, 30))
    return s, w, h

def create_compact(): 
    h = int(CAR_HEIGHT * 0.8)
    w = CAR_WIDTH
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, GREEN, (0, 0, w, h), border_radius=8)
    pygame.draw.rect(s, BLACK, (0, 0, w, h), 2, border_radius=8)
    pygame.draw.rect(s, BLACK, (6, 12, w-12, 10))
    pygame.draw.rect(s, BLACK, (6, h-20, w-12, 10))
    return s, w, h

def create_ghost():
    s = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 255, 255, 150), (CAR_WIDTH//2, CAR_WIDTH//2), CAR_WIDTH//2)
    pygame.draw.polygon(s, (255, 255, 255, 150), [(0, CAR_WIDTH//2), (CAR_WIDTH, CAR_WIDTH//2), (CAR_WIDTH//2, CAR_HEIGHT)])
    pygame.draw.circle(s, (0, 0, 0, 200), (CAR_WIDTH//3, CAR_WIDTH//2.5), 4)
    pygame.draw.circle(s, (0, 0, 0, 200), (CAR_WIDTH - CAR_WIDTH//3, CAR_WIDTH//2.5), 4)
    return s, CAR_WIDTH, CAR_HEIGHT

# POV Atas - Lampu Tol Pinggir Jalan
def create_street_lamp(is_left):
    s = pygame.Surface((70, 40), pygame.SRCALPHA)
    if is_left:
        pygame.draw.rect(s, (60, 60, 60), (10, 15, 8, 25)) # Tiang di rumput kiri
        pygame.draw.rect(s, (90, 90, 90), (15, 15, 38, 6)) # Lengan pendek ke pinggir jalan
        pygame.draw.rect(s, (40, 40, 40), (48, 12, 16, 12), border_radius=3) # Kap lampu di pinggir aspal
    else:
        pygame.draw.rect(s, (60, 60, 60), (52, 15, 8, 25)) # Tiang di rumput kanan
        pygame.draw.rect(s, (90, 90, 90), (17, 15, 38, 6)) # Lengan pendek ke pinggir jalan
        pygame.draw.rect(s, (40, 40, 40), (6, 12, 16, 12), border_radius=3) # Kap lampu
    return s

def create_oak_tree():
    s = pygame.Surface((50, 60), pygame.SRCALPHA)
    pygame.draw.rect(s, BROWN, (20, 30, 10, 30))
    pygame.draw.circle(s, DARK_GREEN, (25, 25), 25)
    return s

def create_pine_tree():
    s = pygame.Surface((40, 70), pygame.SRCALPHA)
    pygame.draw.rect(s, BROWN, (16, 50, 8, 20))
    pygame.draw.polygon(s, PINE_GREEN, [(20, 0), (0, 55), (40, 55)])
    return s

def create_bush():
    s = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(s, (34, 120, 34), (15, 15), 15)
    return s

def create_jumpscare():
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, int(255 * 0.7)))
    cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
    pygame.draw.circle(s, (200, 200, 200, 200), (cx, cy), 120)
    pygame.draw.circle(s, RED, (cx - 40, cy - 20), 25)
    pygame.draw.circle(s, BLACK, (cx - 40, cy - 20), 10)
    pygame.draw.circle(s, RED, (cx + 40, cy - 20), 25)
    pygame.draw.circle(s, BLACK, (cx + 40, cy - 20), 10)
    pygame.draw.ellipse(s, BLACK, (cx - 30, cy + 30, 60, 70))
    return s

def draw_retro_text(surface, font, text, center, color, outline=BLACK, shadow=(70, 0, 30), outline_px=2):
    x, y = center
    shadow_surf = font.render(text, False, shadow)
    shadow_rect = shadow_surf.get_rect(center=(x + 4, y + 4))
    surface.blit(shadow_surf, shadow_rect)

    outline_surf = font.render(text, False, outline)
    for ox, oy in [(-outline_px, 0), (outline_px, 0), (0, -outline_px), (0, outline_px),
                   (-outline_px, -outline_px), (outline_px, -outline_px),
                   (-outline_px, outline_px), (outline_px, outline_px)]:
        outline_rect = outline_surf.get_rect(center=(x + ox, y + oy))
        surface.blit(outline_surf, outline_rect)

    text_surf = font.render(text, False, color)
    text_rect = text_surf.get_rect(center=center)
    surface.blit(text_surf, text_rect)
    return text_rect

def draw_scanlines(surface, alpha=28, gap=4):
    scanline = pygame.Surface((SCREEN_WIDTH, 1), pygame.SRCALPHA)
    scanline.fill((0, 0, 0, alpha))
    for y in range(0, SCREEN_HEIGHT, gap):
        surface.blit(scanline, (0, y))

cone_img, cone_w, cone_h = create_cone()
truck_img, truck_w, truck_h = create_truck()
bus_img, bus_w, bus_h = create_bus()
van_img, van_w, van_h = create_van()
compact_img, compact_w, compact_h = create_compact()
ghost_img, ghost_w, ghost_h = create_ghost()

scenery_images = {
    'oak': create_oak_tree(),
    'pine': create_pine_tree(),
    'bush': create_bush(),
    'lamp_left': create_street_lamp(True),
    'lamp_right': create_street_lamp(False)
}
jumpscare_img = create_jumpscare()

class Obstacle:
    def __init__(self, speed_modifier, is_night):
        choices = ['car', 'cone', 'truck', 'bus', 'van', 'compact']
        weights = [2.5, 1.5, 1.5, 1, 1.5, 2]
        
        if is_night:
            choices.append('ghost')
            weights.append(3.5)

        self.type = random.choices(choices, weights=weights)[0]
        
        if self.type == 'car': 
            self.image, self.w, self.h = create_car(random.choice(CAR_COLORS))
        elif self.type == 'cone': self.image, self.w, self.h = cone_img, cone_w, cone_h
        elif self.type == 'truck': self.image, self.w, self.h = truck_img, truck_w, truck_h
        elif self.type == 'bus': self.image, self.w, self.h = bus_img, bus_w, bus_h
        elif self.type == 'van': self.image, self.w, self.h = van_img, van_w, van_h
        elif self.type == 'compact': self.image, self.w, self.h = compact_img, compact_w, compact_h
        elif self.type == 'ghost': self.image, self.w, self.h = ghost_img, ghost_w, ghost_h

        self.lane = random.randint(0, LANE_COUNT - 1)
        self.exact_x = ROAD_LEFT + (self.lane * LANE_WIDTH) + (LANE_WIDTH - self.w) / 2.0
        self.rect = pygame.Rect(int(self.exact_x), -self.h, self.w, self.h)
        
        if self.type == 'bus' or self.type == 'truck': 
            speed_multiplier = 0.9 
        else: 
            speed_multiplier = random.uniform(0.7, 0.85)

        self.speed = speed_modifier if self.type in ['cone', 'ghost'] else speed_modifier * speed_multiplier
        
        # Variabel AI Ganti Jalur
        self.can_switch = self.type in ['car', 'truck', 'bus', 'van', 'compact']
        self.switch_timer = random.randint(60, 250) 
        self.is_switching = False
        self.target_x = self.exact_x
        
        self.base_x = self.rect.x
        self.sway = 0

    def update(self):
        # AI Ganti Jalur untuk Mobil Musuh
        if self.can_switch and not self.is_switching:
            self.switch_timer -= 1
            if self.switch_timer <= 0:
                options = []
                if self.lane > 0: options.append(-1)
                if self.lane < LANE_COUNT - 1: options.append(1)
                # 60% probabilitas benar-benar pindah, 40% tetap lurus
                if options and random.random() < 0.6: 
                    self.lane += random.choice(options)
                    self.target_x = ROAD_LEFT + (self.lane * LANE_WIDTH) + (LANE_WIDTH - self.w) / 2.0
                    self.is_switching = True
                else:
                    self.switch_timer = random.randint(100, 300)

        # Muluskan Perpindahan X
        if self.is_switching:
            diff = self.target_x - self.exact_x
            if abs(diff) > 1:
                self.exact_x += diff * 0.08 # Kecepatan belok AI
            else:
                self.exact_x = self.target_x
                self.is_switching = False
                self.switch_timer = random.randint(120, 350) 

        self.rect.y += self.speed
        
        if self.type == 'ghost':
            self.sway += 0.1
            self.rect.x = int(self.exact_x) + int(math.sin(self.sway) * 15)
        else:
            self.rect.x = int(self.exact_x)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def main():
    game_state = "START" 
    
    player_lane = 2
    target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
    player_x = target_x
    player_y = SCREEN_HEIGHT - 60

    scroll_speed = 5
    score = 0
    high_score = 0

    obstacles = []
    scenery = []
    obstacle_timer = 0
    scenery_timer = 0
    obstacle_frequency = 90
    
    darkness_alpha = 0 
    current_light_alpha = 0 # Intensitas cahaya (animasi)
    jumpscare_timer = 0
    jumpscare_overlay_timer = 0
    bg_scroll = 0
    
    dino_font = pygame.font.SysFont('Consolas', 22, bold=True)
    title_font = pygame.font.SysFont('Consolas', 36, bold=True)
    blink_font = pygame.font.SysFont('Consolas', 20, bold=True)
    start_title_font = pygame.font.SysFont('Consolas', 30, bold=True)
    start_prompt_font = pygame.font.SysFont('Consolas', 15, bold=True)
    gameover_font = pygame.font.SysFont('Consolas', 50, bold=True)
    score_font = pygame.font.SysFont('Consolas', 34, bold=True)
    prompt_font = pygame.font.SysFont('Consolas', 20, bold=True)

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game_state == "START":
                    if event.key == pygame.K_SPACE:
                        game_state = "PLAYING"
                        obstacles.clear()
                        scenery.clear()
                        scroll_speed = 5
                        score = 0
                        darkness_alpha = 0
                        current_light_alpha = 0
                        player_lane = 2
                        target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
                        player_x = target_x
                        obstacle_frequency = 90
                
                elif game_state == "GAMEOVER":
                    if event.key == pygame.K_SPACE:
                        game_state = "START"
                        obstacles.clear()
                        scenery.clear()
                        scroll_speed = 5
                        score = 0
                        darkness_alpha = 0
                        current_light_alpha = 0
                        jumpscare_overlay_timer = 0
                        player_lane = 2
                        target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
                        player_x = target_x
                        obstacle_frequency = 90
                    elif event.key == pygame.K_r:
                        play_sfx(sfx_cihuy) 
                        game_state = "PLAYING"
                        obstacles.clear()
                        scenery.clear()
                        scroll_speed = 5
                        high_score = max(high_score, int(score/10))
                        score = 0
                        darkness_alpha = 0
                        current_light_alpha = 0
                        jumpscare_overlay_timer = 0
                        player_lane = 2
                        target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
                        player_x = target_x
                        obstacle_frequency = 90
                
                elif game_state == "PLAYING":
                    if event.key in [pygame.K_LEFT, pygame.K_a] and player_lane > 0: 
                        player_lane -= 1
                        play_sfx(sfx_move)
                    if event.key in [pygame.K_RIGHT, pygame.K_d] and player_lane < LANE_COUNT - 1: 
                        player_lane += 1
                        play_sfx(sfx_move)
                    target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)

        diff_x = target_x - player_x
        if abs(diff_x) > 1:
            player_x += diff_x * 0.25 
        else:
            player_x = target_x
            
        player_rect = player_image.get_rect(center=(int(player_x), player_y))

        # --- UPDATE LINGKUNGAN ---
        if game_state in ["START", "PLAYING"]:
            bg_scroll = (bg_scroll + (scroll_speed if game_state=="PLAYING" else 2)) % 40
            
            if game_state == "PLAYING":
                hud_score = int(score / 10)
                cycle_val = hud_score % 750 
                
                MAX_DARKNESS = 130 # Sedikit diturunkan agar lebih terang dari versi sebelumnya
                
                if cycle_val < 480: 
                    target_alpha = 0 
                elif cycle_val < 500: 
                    target_alpha = int(((cycle_val - 480) / 20.0) * MAX_DARKNESS) 
                elif cycle_val < 730: 
                    target_alpha = MAX_DARKNESS 
                else: 
                    target_alpha = int(((750 - cycle_val) / 20.0) * MAX_DARKNESS)
                    
                darkness_alpha = target_alpha
                
                # --- LOGIKA ANIMASI LAMPU NYALA (FLICKER) ---
                is_flickering = (485 <= cycle_val <= 495) or (735 <= cycle_val <= 745)
                lights_on = cycle_val > 495 and cycle_val < 735

                if is_flickering:
                    # Kedap-kedip
                    if random.random() < 0.4:
                        current_light_alpha = 150
                    else:
                        current_light_alpha = 0
                elif lights_on:
                    current_light_alpha = 150
                else:
                    current_light_alpha = 0
            
            is_night = darkness_alpha > 50

            # Spawn Dekorasi Hutan & Lampu
            scenery_timer += 1
            if scenery_timer % 6 == 0: 
                side = random.choice(['left', 'right'])
                tree_type = random.choices(['oak', 'pine', 'bush'], weights=[3, 4, 2])[0]
                if side == 'left':
                    x_pos = random.randint(-20, ROAD_LEFT - 40)
                else:
                    x_pos = random.randint(ROAD_RIGHT + 10, SCREEN_WIDTH - 20)
                scenery.append({'type': tree_type, 'x': x_pos, 'y': -80})
            
            # Spawn Lampu Pinggir Jalan Tol Tiap Berapa Detik
            if scenery_timer % 60 == 0:
                scenery.append({'type': 'lamp_left', 'x': ROAD_LEFT - 20, 'y': -80})
                scenery.append({'type': 'lamp_right', 'x': ROAD_RIGHT - 50, 'y': -80})

            for s in scenery[:]:
                s['y'] += (scroll_speed if game_state=="PLAYING" else 2)
                if s['y'] > SCREEN_HEIGHT:
                    scenery.remove(s)

            # Update Obstacles
            if game_state == "PLAYING":
                obstacle_timer += 1
                if obstacle_timer > obstacle_frequency:
                    obstacles.append(Obstacle(scroll_speed, is_night))
                    obstacle_timer = 0
                    
                score += 1 
                
                if score > 0 and score % 1000 == 0: 
                    play_sfx(sfx_score)

                if score % 400 == 0 and scroll_speed < 20:
                    scroll_speed += 1
                    obstacle_frequency = max(30, obstacle_frequency - 4)

                for obstacle in obstacles[:]:
                    obstacle.update()
                    if obstacle.rect.top > SCREEN_HEIGHT:
                        obstacles.remove(obstacle)
                    
                    hitbox = player_rect.inflate(-12, -12) 
                    if hitbox.colliderect(obstacle.rect):
                        if obstacle.type == 'ghost':
                            jumpscare_overlay_timer = 60
                            obstacles.remove(obstacle)
                            play_sfx(sfx_jumpscare)
                        else:
                            high_score = max(high_score, int(score/10))
                            game_state = "GAMEOVER"
                            play_sfx(sfx_crash)
                            play_sfx(sfx_gameover)

        # --- RENDER KE LAYAR ---
        # 1. Base Layer (Rumput)
        screen.fill(GREEN)

        # 2. Jalan Aspal
        pygame.draw.rect(screen, DARK_GREY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT, 0, 4, SCREEN_HEIGHT))
        pygame.draw.rect(screen, WHITE, (ROAD_RIGHT - 4, 0, 4, SCREEN_HEIGHT))
        for l in range(1, LANE_COUNT):
            x_pos = ROAD_LEFT + (l * LANE_WIDTH)
            for y in range(-40, SCREEN_HEIGHT + 40, 40):
                pygame.draw.rect(screen, LIGHT_GREY, (x_pos - 2, y + bg_scroll, 4, 20))

        # 3. Kendaraan
        for obstacle in obstacles: 
            obstacle.draw(screen)
        screen.blit(player_image, player_rect.topleft)

        # 4. Scenery (Pohon & Tiang Lampu ditaruh di atas mobil biar ada efek kedalaman 3D)
        for s in scenery:
            screen.blit(scenery_images[s['type']], (s['x'], s['y']))

        # 5. EFEK MALAM & LAMPU
        if darkness_alpha > 0:
            dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            dark_surface.fill((10, 10, 25, int(darkness_alpha))) 
            
            # Area senter dibuat transparan di overlay gelap, jadi yang terlihat
            # benar-benar tampilan normal seperti siang hari.
            beam_top_y = max(0, player_rect.top - 430)
            beam_center_x = player_rect.centerx
            soft_beam = [
                (beam_center_x - 28, player_rect.top),
                (beam_center_x + 28, player_rect.top),
                (beam_center_x + 180, beam_top_y),
                (beam_center_x - 180, beam_top_y)
            ]
            clear_beam = [
                (beam_center_x - 18, player_rect.top),
                (beam_center_x + 18, player_rect.top),
                (beam_center_x + 125, beam_top_y),
                (beam_center_x - 125, beam_top_y)
            ]
            pygame.draw.polygon(dark_surface, (10, 10, 25, int(darkness_alpha * 0.35)), soft_beam)
            pygame.draw.polygon(dark_surface, (0, 0, 0, 0), clear_beam)

            # Lampu pinggir jalan juga membuka kegelapan, seperti area kecil yang
            # terlihat siang, lalu diberi glow tipis setelah overlay digambar.
            if current_light_alpha > 0:
                for s in scenery:
                    if s['type'] == 'lamp_left':
                        lamp_x = s['x'] + 56
                    elif s['type'] == 'lamp_right':
                        lamp_x = s['x'] + 14
                    else:
                        continue
                    lamp_y = s['y'] + 18
                    pygame.draw.circle(dark_surface, (10, 10, 25, int(darkness_alpha * 0.45)), (lamp_x, lamp_y), 46)
                    pygame.draw.circle(dark_surface, (0, 0, 0, 0), (lamp_x, lamp_y), 24)
            screen.blit(dark_surface, (0, 0))
            
            # Jika animasi lampu sedang menyala
            if current_light_alpha > 0 and game_state in ["PLAYING", "GAMEOVER", "JUMPSCARE"]:
                # Cahaya tipis sebagai penanda arah senter; visibilitas utama dari lubang overlay gelap.
                hl_opacity = int(10 * (current_light_alpha / 150.0)) 
                headlight_img.fill((0,0,0,0))
                pygame.draw.polygon(headlight_img, (255, 255, 200, hl_opacity), [(150-18, 400), (150+18, 400), (300, 0), (0, 0)])
                screen.blit(headlight_img, (player_rect.centerx - 150, player_rect.top - 400))
                
                # Cahaya untuk Tiang Lampu Pinggir Jalan
                for s in scenery:
                    if s['type'] == 'lamp_left':
                        lamp_glow = pygame.Surface((80, 80), pygame.SRCALPHA)
                        pygame.draw.circle(lamp_glow, (255, 255, 150, int(current_light_alpha * 0.08)), (40, 40), 40)
                        pygame.draw.circle(lamp_glow, (255, 255, 200, int(current_light_alpha * 0.18)), (40, 40), 15)
                        screen.blit(lamp_glow, (s['x'] + 56 - 40, s['y'] + 18 - 40))
                    elif s['type'] == 'lamp_right':
                        lamp_glow = pygame.Surface((80, 80), pygame.SRCALPHA)
                        pygame.draw.circle(lamp_glow, (255, 255, 150, int(current_light_alpha * 0.08)), (40, 40), 40)
                        pygame.draw.circle(lamp_glow, (255, 255, 200, int(current_light_alpha * 0.18)), (40, 40), 15)
                        screen.blit(lamp_glow, (s['x'] + 14 - 40, s['y'] + 18 - 40))

        if jumpscare_overlay_timer > 0:
            screen.blit(jumpscare_img, (0, 0))
            jumpscare_overlay_timer -= 1

        # UI & HUD
        if game_state == "START":
            title_y = SCREEN_HEIGHT//2 - 100
            insert_y = SCREEN_HEIGHT//2 - 44
            prompt_y = SCREEN_HEIGHT//2 + 22

            start_dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            start_dim.fill((0, 0, 0, 45))
            screen.blit(start_dim, (0, 0))
            draw_scanlines(screen, alpha=18, gap=5)

            marquee = pygame.Rect(ROAD_LEFT + 38, title_y - 29, ROAD_WIDTH - 76, 58)
            pygame.draw.rect(screen, (18, 18, 18), marquee)
            pygame.draw.rect(screen, YELLOW, marquee, 3)
            pygame.draw.rect(screen, RED, marquee.inflate(-10, -10), 1)

            draw_retro_text(
                screen,
                start_title_font,
                "CAR : MINI GAME",
                (SCREEN_WIDTH//2, title_y),
                YELLOW,
                outline=BLACK,
                shadow=(80, 45, 0),
                outline_px=2
            )

            if (current_time // 450) % 2 == 0:
                draw_retro_text(
                    screen,
                    blink_font,
                    "INSERT COIN",
                    (SCREEN_WIDTH//2, insert_y),
                    RED,
                    outline=BLACK,
                    shadow=(70, 0, 30),
                    outline_px=1
                )

            prompt_box = pygame.Rect(ROAD_LEFT + 58, prompt_y, ROAD_WIDTH - 116, 42)
            pygame.draw.rect(screen, (20, 20, 20), prompt_box)
            pygame.draw.rect(screen, WHITE, prompt_box, 2)
            pygame.draw.rect(screen, YELLOW, prompt_box.inflate(-8, -8), 1)
            if (current_time // 500) % 2 == 0:
                draw_retro_text(
                    screen,
                    start_prompt_font,
                    "TEKAN [SPACE] UNTUK GAS!",
                    prompt_box.center,
                    WHITE,
                    outline=BLACK,
                    shadow=(70, 0, 30),
                    outline_px=1
                )

        elif game_state == "PLAYING":
            hud_score = int(score / 10)
            score_surf = dino_font.render(f"HI {high_score:05d}  {hud_score:05d}", True, WHITE)
            screen.blit(score_surf, (SCREEN_WIDTH - score_surf.get_width() - 20, 20))

        elif game_state == "JUMPSCARE":
            screen.blit(jumpscare_img, (0, 0))
            jumpscare_timer -= 1
            if jumpscare_timer <= 0:
                game_state = "GAMEOVER"

        elif game_state == "GAMEOVER":
            gameover_dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            gameover_dim.fill((0, 0, 0, 125))
            screen.blit(gameover_dim, (0, 0))

            final_score = int(score / 10)
            draw_retro_text(
                screen,
                score_font,
                f"SCORE {final_score:05d}",
                (SCREEN_WIDTH//2, 125),
                YELLOW,
                outline=BLACK,
                shadow=(80, 45, 0),
                outline_px=2
            )
            draw_retro_text(
                screen,
                gameover_font,
                "GAME OVER",
                (
                    SCREEN_WIDTH//2 + random.randint(-2, 2),
                    225 + (2 if (current_time // 120) % 2 == 0 else -1)
                ),
                RED if (current_time // 90) % 3 else YELLOW,
                outline=BLACK,
                shadow=(80, 0, 35),
                outline_px=3
            )
            draw_scanlines(screen, alpha=20, gap=4)

            prompt_y = 390
            prompt_w = 170
            prompt_h = 42
            left_prompt = pygame.Rect(SCREEN_WIDTH//2 - prompt_w - 10, prompt_y, prompt_w, prompt_h)
            right_prompt = pygame.Rect(SCREEN_WIDTH//2 + 10, prompt_y, prompt_w, prompt_h)
            for rect in [left_prompt, right_prompt]:
                pygame.draw.rect(screen, (18, 18, 18), rect)
                pygame.draw.rect(screen, YELLOW, rect, 3)
                pygame.draw.rect(screen, RED, rect.inflate(-8, -8), 1)

            if (current_time // 500) % 2 == 0:
                draw_retro_text(screen, prompt_font, "R ULANGI", left_prompt.center, WHITE, outline=BLACK, shadow=(70, 0, 30), outline_px=1)
                draw_retro_text(screen, prompt_font, "SPACE MENU", right_prompt.center, WHITE, outline=BLACK, shadow=(70, 0, 30), outline_px=1)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
