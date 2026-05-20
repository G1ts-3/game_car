import pygame
import random
import sys
import math

# Inisialisasi Pygame
pygame.init()

# Konstanta Dimensi Layar
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Car Git")

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
SILVER = (192, 192, 192)
CYAN = (0, 255, 255)

# Setup Frame Rate
clock = pygame.time.Clock()
FPS = 60

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
    pygame.draw.rect(s, CYAN, (4, 8, w-8, 12)) # Kaca depan
    for i in range(25, h-10, 20):
        pygame.draw.rect(s, BLACK, (2, i, 8, 12)) # Jendela kiri
        pygame.draw.rect(s, BLACK, (w-10, i, 8, 12)) # Jendela kanan
    return s, w, h

def create_van(): # Alphard style
    h = int(CAR_HEIGHT * 1.2)
    w = int(CAR_WIDTH * 1.1)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, SILVER, (0, 0, w, h), border_radius=3)
    pygame.draw.rect(s, BLACK, (0, 0, w, h), 2, border_radius=3)
    pygame.draw.rect(s, BLACK, (4, 15, w-8, 20)) # Kaca depan besar
    pygame.draw.rect(s, BLACK, (4, 40, w-8, 30)) # Kaca penumpang
    return s, w, h

def create_compact(): # Brio style
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

# Varian Pohon untuk Hutan
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

cone_img, cone_w, cone_h = create_cone()
truck_img, truck_w, truck_h = create_truck()
bus_img, bus_w, bus_h = create_bus()
van_img, van_w, van_h = create_van()
compact_img, compact_w, compact_h = create_compact()
ghost_img, ghost_w, ghost_h = create_ghost()

# Cache gambar pohon
scenery_images = {
    'oak': create_oak_tree(),
    'pine': create_pine_tree(),
    'bush': create_bush()
}
jumpscare_img = create_jumpscare()


class Obstacle:
    def __init__(self, speed_modifier, is_night):
        # Lambo (sportscar) dihapus, Cone tetap ada di list rintangan
        choices = ['cone', 'truck', 'bus', 'van', 'compact']
        weights = [2, 1.5, 1, 1.5, 2]
        
        if is_night:
            choices.append('ghost')
            weights.append(3.5)

        self.type = random.choices(choices, weights=weights)[0]
        
        if self.type == 'cone': self.image, self.w, self.h = cone_img, cone_w, cone_h
        elif self.type == 'truck': self.image, self.w, self.h = truck_img, truck_w, truck_h
        elif self.type == 'bus': self.image, self.w, self.h = bus_img, bus_w, bus_h
        elif self.type == 'van': self.image, self.w, self.h = van_img, van_w, van_h
        elif self.type == 'compact': self.image, self.w, self.h = compact_img, compact_w, compact_h
        elif self.type == 'ghost': self.image, self.w, self.h = ghost_img, ghost_w, ghost_h

        self.lane = random.randint(0, LANE_COUNT - 1)
        x_pos = ROAD_LEFT + (self.lane * LANE_WIDTH) + (LANE_WIDTH - self.w) // 2
        self.rect = pygame.Rect(x_pos, -self.h, self.w, self.h)
        
        # Kecepatan relatif berbeda tiap kendaraan besar/kecil
        if self.type == 'bus' or self.type == 'truck': 
            speed_multiplier = 0.9 # Lambat
        else: 
            speed_multiplier = random.uniform(0.7, 0.85)

        self.speed = speed_modifier if self.type in ['cone', 'ghost'] else speed_modifier * speed_multiplier
        self.base_x = self.rect.x
        self.sway = 0

    def update(self):
        self.rect.y += self.speed
        if self.type == 'ghost':
            self.sway += 0.1
            self.rect.x = self.base_x + int(math.sin(self.sway) * 15)

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
    jumpscare_timer = 0
    bg_scroll = 0
    
    dino_font = pygame.font.SysFont('Consolas', 22, bold=True)
    title_font = pygame.font.SysFont('Consolas', 36, bold=True)
    blink_font = pygame.font.SysFont('Consolas', 20, bold=True)

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game_state == "START":
                    if event.key == pygame.K_SPACE: game_state = "PLAYING"
                
                elif game_state == "GAMEOVER":
                    if event.key in [pygame.K_SPACE, pygame.K_r]:
                        game_state = "PLAYING"
                        obstacles.clear()
                        scenery.clear()
                        scroll_speed = 5
                        high_score = max(high_score, int(score/10))
                        score = 0
                        darkness_alpha = 0
                        player_lane = 2
                        target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)
                        player_x = target_x
                        obstacle_frequency = 90
                
                elif game_state == "PLAYING":
                    if event.key == pygame.K_LEFT and player_lane > 0: 
                        player_lane -= 1
                    if event.key == pygame.K_RIGHT and player_lane < LANE_COUNT - 1: 
                        player_lane += 1
                    target_x = ROAD_LEFT + (player_lane * LANE_WIDTH) + (LANE_WIDTH / 2)

        # Animasi geser biasa (tanpa rotasi)
        diff_x = target_x - player_x
        if abs(diff_x) > 1:
            player_x += diff_x * 0.25 
        else:
            player_x = target_x
            
        player_rect = player_image.get_rect(center=(int(player_x), player_y))

        # --- UPDATE LINGKUNGAN ---
        if game_state in ["START", "PLAYING"]:
            bg_scroll = (bg_scroll + (scroll_speed if game_state=="PLAYING" else 2)) % 40
            
            # Siklus Siang/Malam (Malam tidak terlalu gelap, max alpha 100)
            if game_state == "PLAYING":
                hud_score = int(score / 10)
                cycle_val = hud_score % 750 
                
                if cycle_val < 480: 
                    target_alpha = 0 
                elif cycle_val < 500: 
                    target_alpha = int(((cycle_val - 480) / 20.0) * 100) 
                elif cycle_val < 730: 
                    target_alpha = 100 
                else: 
                    target_alpha = int(((750 - cycle_val) / 20.0) * 100)
                    
                darkness_alpha = target_alpha
            
            is_night = darkness_alpha > 50

            # Spawn Dekorasi Hutan
            scenery_timer += 1
            if scenery_timer > 6: 
                side = random.choice(['left', 'right'])
                tree_type = random.choices(['oak', 'pine', 'bush'], weights=[3, 4, 2])[0]
                
                if side == 'left':
                    x_pos = random.randint(-10, ROAD_LEFT - 30)
                else:
                    x_pos = random.randint(ROAD_RIGHT + 5, SCREEN_WIDTH - 20)
                
                scenery.append({'type': tree_type, 'x': x_pos, 'y': -80})
                scenery_timer = 0

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
                            game_state = "JUMPSCARE"
                            jumpscare_timer = 60
                        else:
                            game_state = "GAMEOVER"

        # --- RENDER KE LAYAR ---
        screen.fill(GREEN)
        
        for s in scenery:
            screen.blit(scenery_images[s['type']], (s['x'], s['y']))

        pygame.draw.rect(screen, DARK_GREY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT, 0, 4, SCREEN_HEIGHT))
        pygame.draw.rect(screen, WHITE, (ROAD_RIGHT - 4, 0, 4, SCREEN_HEIGHT))
        for l in range(1, LANE_COUNT):
            x_pos = ROAD_LEFT + (l * LANE_WIDTH)
            for y in range(-40, SCREEN_HEIGHT + 40, 40):
                pygame.draw.rect(screen, LIGHT_GREY, (x_pos - 2, y + bg_scroll, 4, 20))

        for obstacle in obstacles: 
            obstacle.draw(screen)
            
        screen.blit(player_image, player_rect.topleft)

        # --- EFEK MALAM TANPA SENTER ---
        if darkness_alpha > 0:
            dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            dark_surface.fill((10, 10, 25, int(darkness_alpha))) 
            screen.blit(dark_surface, (0, 0))

        # UI & HUD
        if game_state == "START":
            title_text = title_font.render("Gits Car", True, YELLOW)
            screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
            if (current_time // 500) % 2 == 0:
                start_text = blink_font.render("TEKAN [SPACE] UNTUK GAS!", True, WHITE)
                screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2 + 10))

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
            go_text = title_font.render("G A M E  O V E R", True, RED)
            screen.blit(go_text, (SCREEN_WIDTH//2 - go_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            if (current_time // 500) % 2 == 0:
                restart_text = blink_font.render("TEKAN [SPACE] MULAI LAGI", True, WHITE)
                screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()