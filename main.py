import pygame
import random
import sys
import math
import asyncio

# Inisialisasi Pygame & Mixer (Audio)
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass

# Konstanta Dimensi Layar
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car : Mini Game")
try:
    pygame.display.set_icon(pygame.image.load("favicon.png").convert_alpha())
except FileNotFoundError:
    icon_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(icon_surface, BLACK, (8, 4, 16, 24), border_radius=4)
    pygame.draw.rect(icon_surface, RED, (10, 6, 12, 20), border_radius=3)
    pygame.draw.rect(icon_surface, YELLOW, (11, 6, 3, 3), border_radius=1)
    pygame.draw.rect(icon_surface, YELLOW, (18, 6, 3, 3), border_radius=1)
    pygame.display.set_icon(icon_surface)

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
VEHICLE_COLORS = [RED, ORANGE, BLUE, PURPLE, SILVER, CYAN, WHITE, YELLOW, GREEN]

# Setup Frame Rate
clock = pygame.time.Clock()
FPS = 60

FIRST_TIME_PHASE_SCORE = 350
NEXT_TIME_PHASE_SCORE = 300
TIME_TRANSITION_SCORE = 24

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
sfx_playing = load_sfx("playing.wav")
sfx_playing_fast = load_sfx("playing_fast.wav")
sfx_playing_intense = load_sfx("playing_intense.wav")
sfx_menu = load_sfx("menu.wav")

def play_sfx(sfx):
    if sfx is not None:
        sfx.play()

def stop_sfx(sfx):
    if sfx is not None:
        sfx.stop()

def get_playing_loop(hud_score):
    if hud_score >= 900 and sfx_playing_intense is not None:
        return sfx_playing_intense
    if hud_score >= 450 and sfx_playing_fast is not None:
        return sfx_playing_fast
    return sfx_playing

def get_intensity_targets(hud_score):
    if hud_score >= 900:
        return 6.2, 46, 14.0
    if hud_score >= 450:
        return 5.0, 55, 12.0
    return 4.0, 64, 10.0

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

def create_truck(color=WHITE):
    h = int(CAR_HEIGHT * 1.4)
    s = pygame.Surface((CAR_WIDTH, h), pygame.SRCALPHA)
    pygame.draw.rect(s, color, (2, 20, CAR_WIDTH-4, h-22), border_radius=2)
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

def create_van(color=SILVER): 
    h = int(CAR_HEIGHT * 1.2)
    w = int(CAR_WIDTH * 1.1)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, color, (0, 0, w, h), border_radius=3)
    pygame.draw.rect(s, BLACK, (0, 0, w, h), 2, border_radius=3)
    pygame.draw.rect(s, BLACK, (4, 15, w-8, 20))
    pygame.draw.rect(s, BLACK, (4, 40, w-8, 30))
    return s, w, h

def create_compact(color=GREEN): 
    h = int(CAR_HEIGHT * 0.8)
    w = CAR_WIDTH
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, color, (0, 0, w, h), border_radius=8)
    pygame.draw.rect(s, BLACK, (0, 0, w, h), 2, border_radius=8)
    pygame.draw.rect(s, BLACK, (6, 12, w-12, 10))
    pygame.draw.rect(s, BLACK, (6, h-20, w-12, 10))
    return s, w, h

def create_wide_car(color):
    w = int(LANE_WIDTH * 1.75)
    h = int(CAR_HEIGHT * 1.45)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, BLACK, (0, 0, w, h), border_radius=7)
    pygame.draw.rect(s, color, (3, 24, w-6, h-27), border_radius=3)
    pygame.draw.rect(s, BLACK, (3, 24, w-6, h-27), 2, border_radius=3)
    pygame.draw.rect(s, BLUE, (12, 2, w-24, 28), border_radius=4)
    pygame.draw.rect(s, BLACK, (18, 10, w-36, 12), border_radius=2)
    pygame.draw.rect(s, BLACK, (10, 44, w-20, 6))
    pygame.draw.rect(s, BLACK, (10, h-34, w-20, 6))
    pygame.draw.rect(s, BLACK, (10, h-20, w-20, 6))
    pygame.draw.rect(s, YELLOW, (9, 3, 11, 7), border_radius=2)
    pygame.draw.rect(s, YELLOW, (w-20, 3, 11, 7), border_radius=2)
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

def get_time_phase(hud_score):
    if hud_score < FIRST_TIME_PHASE_SCORE:
        return 0, hud_score

    elapsed = hud_score - FIRST_TIME_PHASE_SCORE
    phase_index = 1 + (elapsed // NEXT_TIME_PHASE_SCORE)
    phase_progress = elapsed % NEXT_TIME_PHASE_SCORE
    return phase_index, phase_progress

cone_img, cone_w, cone_h = create_cone()
bus_img, bus_w, bus_h = create_bus()
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
    def __init__(self, speed_modifier, is_night, advanced_difficulty):
        choices = ['car', 'cone', 'truck', 'bus', 'van', 'compact']
        weights = [3.2, 0.8, 2.0, 1.0, 2.0, 3.0]
        
        if is_night:
            choices.append('ghost')
            weights.append(3.5)

        if advanced_difficulty:
            choices.append('wide_car')
            weights.append(1.4)

        self.type = random.choices(choices, weights=weights)[0]
        self.advanced_difficulty = advanced_difficulty
        self.lane_span = 2 if self.type == 'wide_car' else 1
        
        if self.type == 'car': 
            self.image, self.w, self.h = create_car(random.choice(CAR_COLORS))
        elif self.type == 'cone': self.image, self.w, self.h = cone_img, cone_w, cone_h
        elif self.type == 'truck': self.image, self.w, self.h = create_truck(random.choice(VEHICLE_COLORS))
        elif self.type == 'bus': self.image, self.w, self.h = bus_img, bus_w, bus_h
        elif self.type == 'van': self.image, self.w, self.h = create_van(random.choice(VEHICLE_COLORS))
        elif self.type == 'compact': self.image, self.w, self.h = create_compact(random.choice(VEHICLE_COLORS))
        elif self.type == 'wide_car': self.image, self.w, self.h = create_wide_car(random.choice(VEHICLE_COLORS))
        elif self.type == 'ghost': self.image, self.w, self.h = ghost_img, ghost_w, ghost_h

        self.lane = random.randint(0, LANE_COUNT - self.lane_span)
        lane_span_width = LANE_WIDTH * self.lane_span
        lane_center_x = ROAD_LEFT + (self.lane * LANE_WIDTH) + (lane_span_width - self.w) / 2.0
        lane_padding = 6
        max_offset = max(0, int((lane_span_width - self.w) / 2) - lane_padding)
        self.lane_offset = random.randint(-max_offset, max_offset) if max_offset > 0 else 0
        self.exact_x = lane_center_x + self.lane_offset
        self.exact_y = -self.h
        self.rect = pygame.Rect(int(self.exact_x), int(self.exact_y), self.w, self.h)
        
        if self.type == 'bus' or self.type == 'truck': 
            speed_multiplier = 0.78 
        else: 
            speed_multiplier = random.uniform(0.62, 0.76)

        self.speed = speed_modifier if self.type in ['cone', 'ghost'] else speed_modifier * speed_multiplier
        
        # Variabel AI Ganti Jalur
        self.can_switch = self.type in ['car', 'truck', 'bus', 'van', 'compact', 'wide_car']
        self.switch_timer = random.randint(35, 150) if advanced_difficulty else random.randint(50, 180)
        self.is_switching = False
        self.target_x = self.exact_x
        self.previous_lane = self.lane
        
        self.base_x = self.rect.x
        self.sway = 0

    def get_lane_x(self, lane):
        lane_span_width = LANE_WIDTH * self.lane_span
        return ROAD_LEFT + (lane * LANE_WIDTH) + (lane_span_width - self.w) / 2.0 + self.lane_offset

    def can_enter_lane(self, lane, obstacles):
        target_rect = pygame.Rect(int(self.get_lane_x(lane)), self.rect.y, self.w, self.h)
        target_rect = target_rect.inflate(10, 90)
        for obstacle in obstacles:
            if obstacle is self:
                continue
            if target_rect.colliderect(obstacle.rect.inflate(10, 90)):
                return False
        return True

    def get_safe_speed(self, obstacles):
        safe_speed = self.speed
        next_rect = self.rect.copy()
        next_rect.y = int(self.exact_y + safe_speed)

        for obstacle in obstacles:
            if obstacle is self:
                continue
            same_path = (
                next_rect.right > obstacle.rect.left - 6 and
                next_rect.left < obstacle.rect.right + 6
            )
            obstacle_ahead = obstacle.rect.top >= self.rect.bottom
            if same_path and obstacle_ahead:
                gap = obstacle.rect.top - self.rect.bottom - 14
                safe_speed = min(safe_speed, max(0, gap))

        return safe_speed

    def update(self, obstacles):
        # AI Ganti Jalur untuk Mobil Musuh
        if self.can_switch and not self.is_switching:
            self.switch_timer -= 1
            if self.switch_timer <= 0:
                max_jump = 1 if self.lane_span > 1 else (3 if self.advanced_difficulty else 1)
                max_lane = LANE_COUNT - self.lane_span
                options = []
                for jump in range(1, max_jump + 1):
                    if self.lane - jump >= 0:
                        options.append(self.lane - jump)
                    if self.lane + jump <= max_lane:
                        options.append(self.lane + jump)

                safe_options = [lane for lane in options if self.can_enter_lane(lane, obstacles)]
                if self.previous_lane in safe_options and random.random() < 0.35:
                    safe_options.extend([self.previous_lane, self.previous_lane])

                switch_chance = 0.82 if self.advanced_difficulty else 0.68
                if safe_options and random.random() < switch_chance: 
                    target_lane = random.choice(safe_options)
                    self.previous_lane = self.lane
                    self.lane = target_lane
                    self.target_x = self.get_lane_x(self.lane)
                    self.is_switching = True
                else:
                    self.switch_timer = random.randint(45, 130) if self.advanced_difficulty else random.randint(65, 170)

        # Muluskan Perpindahan X
        if self.is_switching:
            diff = self.target_x - self.exact_x
            if abs(diff) > 1:
                self.exact_x += diff * 0.08 # Kecepatan belok AI
            else:
                self.exact_x = self.target_x
                self.is_switching = False
                self.switch_timer = random.randint(35, 130) if self.advanced_difficulty else random.randint(55, 170)

        self.exact_y += self.get_safe_speed(obstacles)
        self.rect.y = int(self.exact_y)
        
        if self.type == 'ghost':
            self.sway += 0.1
            self.rect.x = int(self.exact_x) + int(math.sin(self.sway) * 15)
        else:
            self.rect.x = int(self.exact_x)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def has_obstacle_space(candidate, obstacles):
    spawn_rect = candidate.rect.inflate(12, 110)
    for obstacle in obstacles:
        if spawn_rect.colliderect(obstacle.rect.inflate(12, 70)):
            return False
    return True

async def main():
    game_state = "START" 
    
    player_lane = 2
    target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
    player_x = target_x
    player_y = SCREEN_HEIGHT - 60

    scroll_speed = 4
    score = 0
    high_score = 0

    obstacles = []
    scenery = []
    obstacle_timer = 0
    scenery_timer = 0
    obstacle_frequency = 64
    
    darkness_alpha = 0 
    current_light_alpha = 0 # Intensitas cahaya (animasi)
    jumpscare_timer = 0
    jumpscare_overlay_timer = 0
    current_audio_state = None
    current_playing_loop = None
    bg_scroll = 0
    
    dino_font = pygame.font.SysFont('Consolas', 22, bold=True)
    title_font = pygame.font.SysFont('Consolas', 36, bold=True)
    blink_font = pygame.font.SysFont('Consolas', 20, bold=True)
    start_title_font = pygame.font.SysFont('Consolas', 26, bold=True)
    start_prompt_font = pygame.font.SysFont('Consolas', 14, bold=True)
    gameover_font = pygame.font.SysFont('Consolas', 50, bold=True)
    score_font = pygame.font.SysFont('Consolas', 34, bold=True)
    prompt_font = pygame.font.SysFont('Consolas', 20, bold=True)

    while True:
        current_time = pygame.time.get_ticks()

        audio_state = game_state if game_state in ["START", "PLAYING", "GAMEOVER"] else None
        if audio_state != current_audio_state:
            stop_sfx(sfx_menu)
            stop_sfx(sfx_playing)
            stop_sfx(sfx_playing_fast)
            stop_sfx(sfx_playing_intense)
            if audio_state == "START" and sfx_menu is not None:
                sfx_menu.play(-1)
                current_playing_loop = None
            elif audio_state == "PLAYING":
                current_playing_loop = get_playing_loop(int(score / 10))
                if current_playing_loop is not None:
                    current_playing_loop.play(-1)
            elif audio_state == "GAMEOVER":
                play_sfx(sfx_gameover)
                current_playing_loop = None
            current_audio_state = audio_state

        if game_state == "PLAYING":
            next_playing_loop = get_playing_loop(int(score / 10))
            if next_playing_loop is not current_playing_loop:
                stop_sfx(current_playing_loop)
                current_playing_loop = next_playing_loop
                if current_playing_loop is not None:
                    current_playing_loop.play(-1)

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
                        scroll_speed = 4
                        score = 0
                        darkness_alpha = 0
                        current_light_alpha = 0
                        player_lane = 2
                        target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
                        player_x = target_x
                        obstacle_frequency = 64
                
                elif game_state == "GAMEOVER":
                    if event.key == pygame.K_SPACE:
                        game_state = "START"
                        obstacles.clear()
                        scenery.clear()
                        scroll_speed = 4
                        score = 0
                        darkness_alpha = 0
                        current_light_alpha = 0
                        jumpscare_overlay_timer = 0
                        player_lane = 2
                        target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
                        player_x = target_x
                        obstacle_frequency = 64
                    elif event.key == pygame.K_r:
                        play_sfx(sfx_cihuy) 
                        game_state = "PLAYING"
                        obstacles.clear()
                        scenery.clear()
                        scroll_speed = 4
                        high_score = max(high_score, int(score/10))
                        score = 0
                        darkness_alpha = 0
                        current_light_alpha = 0
                        jumpscare_overlay_timer = 0
                        player_lane = 2
                        target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
                        player_x = target_x
                        obstacle_frequency = 64
                
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
                time_phase, phase_progress = get_time_phase(hud_score)
                is_night_phase = time_phase % 2 == 1
                advanced_difficulty = time_phase >= 2
                
                MAX_DARKNESS = 130 # Sedikit diturunkan agar lebih terang dari versi sebelumnya
                
                if time_phase == 0:
                    target_alpha = 0
                elif phase_progress < TIME_TRANSITION_SCORE:
                    transition_ratio = phase_progress / float(TIME_TRANSITION_SCORE)
                    if is_night_phase:
                        target_alpha = int(transition_ratio * MAX_DARKNESS)
                    else:
                        target_alpha = int((1.0 - transition_ratio) * MAX_DARKNESS)
                else:
                    target_alpha = MAX_DARKNESS if is_night_phase else 0
                    
                darkness_alpha = target_alpha
                
                # --- LOGIKA ANIMASI LAMPU NYALA (FLICKER) ---
                is_flickering = time_phase > 0 and phase_progress < TIME_TRANSITION_SCORE
                lights_on = is_night_phase and phase_progress >= TIME_TRANSITION_SCORE

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
            else:
                advanced_difficulty = False
            
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
                    for _ in range(12):
                        candidate = Obstacle(scroll_speed, is_night, advanced_difficulty)
                        if has_obstacle_space(candidate, obstacles):
                            obstacles.append(candidate)
                            break
                    obstacle_timer = 0
                    
                score += 1 
                
                if score > 0 and score % 1000 == 0: 
                    play_sfx(sfx_score)

                target_speed, target_frequency, max_speed = get_intensity_targets(int(score / 10))
                if scroll_speed < target_speed:
                    scroll_speed = min(target_speed, scroll_speed + 0.08)
                elif score % 450 == 0 and scroll_speed < max_speed:
                    scroll_speed += 0.18

                if obstacle_frequency > target_frequency:
                    obstacle_frequency = max(target_frequency, obstacle_frequency - 1)
                elif score % 550 == 0:
                    obstacle_frequency = max(34, obstacle_frequency - 2)

                for obstacle in obstacles[:]:
                    obstacle.update(obstacles)
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
                draw_retro_text(screen, prompt_font, "[R] ULANGI", left_prompt.center, WHITE, outline=BLACK, shadow=(70, 0, 30), outline_px=1)
                draw_retro_text(screen, prompt_font, "[SPACE] MENU", right_prompt.center, WHITE, outline=BLACK, shadow=(70, 0, 30), outline_px=1)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
