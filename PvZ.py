# pvz_final_corrigido.py
import pygame
import random
import sys
import os

# ------------------------------------- FUNÇÃO CRÍTICA PARA PYINSTALLER -------------------------------------
def resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso, funcionando no ambiente normal (py)
    e no ambiente empacotado do PyInstaller (exe).
    """
    try:
        # Caminho do PyInstaller (onde os assets são descompactados temporariamente)
        base_path = sys._MEIPASS
    except Exception:
        # Caminho normal do script (ambiente de desenvolvimento)
        base_path = os.path.abspath(".")

    # Concatena o caminho base com o caminho relativo (ex: 'assets/plant.png')
    return os.path.join(base_path, relative_path)
# ---------------------------------------------------------------------------------------------------------


pygame.init()
pygame.font.init()

# ------------------------------------- CONFIG -------------------------------------
LARGURA = 1200
ALTURA = 700
FPS = 60
clock = pygame.time.Clock()

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PVZ - Plants vs Zombies")

# ----------------------------------- GRID -----------------------------------------
LINHAS = 5
COLUNAS = 9
TAM = 100
OFFSET_X = 120
OFFSET_Y = 120

# ----------------------------------- CORES ----------------------------------------
GREEN1 = (110, 180, 110)
GREEN2 = (90, 160, 90)
BG = (40, 140, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
SELECT_BORDER = (255, 215, 0)

# -------------------------------- CARREGAMENTO DE IMAGENS -------------------------
def load(name, size=None):
    if os.path.exists(name):
        img = pygame.image.load(name).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    return None

# APLICANDO resource_path() A TODOS OS ASSETS
PEA = load(resource_path("assets/plant.png"), (100, 100))
ZOM = load(resource_path("assets/zombie.png"), (100, 100))
BUL = load(resource_path("assets/bullet.png"), (30, 30))
SUN = load(resource_path("assets/sun.png"), (60, 60))
WALLNUT = load(resource_path("assets/wallnut.png"), (100, 100))

# NOVO: Carregamento do Som
def load_sound(name):
    if os.path.exists(name):
        if not pygame.mixer.get_init():
             pygame.mixer.init()
        return pygame.mixer.Sound(name)
    return None

# APLICANDO resource_path() A TODOS OS SONS
# SOM DE HIT
HIT_SOUND = load_sound(resource_path("assets/hit.wav"))
if HIT_SOUND:
    HIT_SOUND.set_volume(0.3)
# SOM DE COLETA DE SOL
COLLECT_SOUND = load_sound(resource_path("assets/collect.mp3"))
if COLLECT_SOUND:
    COLLECT_SOUND.set_volume(0.3)
# SOM DO GAME OVER
GAME_OVER_SOUND = load_sound(resource_path("assets/game-over.mp3"))
if GAME_OVER_SOUND:
    GAME_OVER_SOUND.set_volume(0.5)

# -------------------------------- ENTIDADES ---------------------------------------
class Sun:
    def __init__(self):
        self.x = random.randint(OFFSET_X + 20, OFFSET_X + COLUNAS*TAM - 80)
        self.y = -70
        self.vy = 1.6
        self.w, self.h = 60, 60
        self.target_y = OFFSET_Y + LINHAS * TAM - 120
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.value = 25

    def update(self):
        if self.y < self.target_y:
            self.y += self.vy
            self.rect.y = int(self.y)

    def draw(self):
        if SUN:
            TELA.blit(SUN, (self.x, self.y))
        else:
            pygame.draw.circle(TELA, YELLOW, (int(self.x + 30), int(self.y + 30)), 30)

class Bullet:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = 8
        self.w, self.h = 30, 30
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        self.x += self.vx
        self.rect.x = int(self.x)

    def draw(self):
        if BUL:
            TELA.blit(BUL, (self.x, self.y))
        else:
            pygame.draw.circle(TELA, (30, 200, 30), (int(self.x + 15), int(self.y + 15)), 12)

class Plant:
    SHOOT = 60
    
    def __init__(self, c, l):
        self.col = c
        self.lin = l
        self.x = OFFSET_X + c * TAM
        self.y = OFFSET_Y + l * TAM
        self.hp = 6.0
        self.t = 0
        px = self.x + (TAM - 100)//2
        py = self.y + (TAM - 100)//2
        self.rect = pygame.Rect(px, py, 100, 100)

    def update(self, bullets):
        self.t += 1
        if self.t >= Plant.SHOOT:
            bx = self.x + TAM - 30
            by = self.y + TAM//2 - 15
            bullets.append(Bullet(bx, by))
            self.t = 0

    def draw(self):
        px = self.x + (TAM - 100)//2
        py = self.y + (TAM - 100)//2
        if PEA:
            TELA.blit(PEA, (px, py))
        else:
            pygame.draw.circle(TELA, (0,150,0), (px + 50, py + 50), 40)
        hp_txt = font_small.render(f"{int(self.hp)}", True, BLACK)
        TELA.blit(hp_txt, (px + 6, py + 6))

class Wallnut:
    BASE_HP = 15.0
    COST = 75

    def __init__(self, c, l):
        self.col = c
        self.lin = l
        self.x = OFFSET_X + c * TAM
        self.y = OFFSET_Y + l * TAM
        self.hp = Wallnut.BASE_HP
        self.t = 0
        
        px = self.x + (TAM - 100)//2
        py = self.y + (TAM - 100)//2
        self.rect = pygame.Rect(px, py, 100, 100)

    def update(self, bullets):
        pass

    def draw(self):
        px = self.x + (TAM - 100)//2
        py = self.y + (TAM - 100)//2
        if WALLNUT:
            TELA.blit(WALLNUT, (px, py))
        else:
            pygame.draw.rect(TELA, (180, 150, 100), (px + 10, py + 10, 80, 80), border_radius=10)
        
        hp_txt = font_small.render(f"{int(self.hp)}", True, BLACK)
        TELA.blit(hp_txt, (px + 6, py + 6))

class Zombie:
    def __init__(self, linha, hp=12, speed=0.55):
        self.linha = linha
        self.hp = float(hp)
        self.speed = speed
        self.x = LARGURA + 40
        self.vx = -self.speed
        self.y = OFFSET_Y + linha * TAM + (TAM - 100)//2
        self.w, self.h = 100, 100
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)
        self.eating = False

    def update(self):
        if not self.eating:
            self.x += self.vx
            self.rect.x = int(self.x)
        else:
            self.rect.x = int(self.x)

    def draw(self):
        if ZOM:
            TELA.blit(ZOM, (self.x, self.y))
        else:
            pygame.draw.rect(TELA, (180,40,40), (int(self.x), int(self.y), self.w, self.h))
        # hp bar
        bar_w = 60
        hp_ratio = max(0.0, min(1.0, self.hp / 12.0))
        bx = int(self.x + 20)
        by = int(self.y - 10)
        pygame.draw.rect(TELA, (0,0,0), (bx, by, bar_w, 6))
        pygame.draw.rect(TELA, (0,200,0), (bx, by, int(bar_w * hp_ratio), 6))

# ----------------------------------- ESTADO ---------------------------------------
grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]
plants = []
bullets = []
zombies = []
suns = []

sols = 150
selected = None
PLANT_COST = 100
WALLNUT_COST = 75

frame = 0
spawn_timer = 0
spawn_interval = 280
minute_ticks = 0
MIN_SPAWN_INTERVAL = 80

GAME_STATE = "PLAYING" 
GAME_OVER_SOUND_PLAYED = False

# ------------------------------ FONTES ------------------------------------------
font = pygame.font.SysFont("Arial", 22)
font_large = pygame.font.SysFont("Arial", 60, bold=True)
font_medium = pygame.font.SysFont("Arial", 30)
font_small = pygame.font.SysFont("Arial", 18)

# -------------------------------- FUNÇÕES AUX ------------------------------------
def snap(mx, my):
    if mx < OFFSET_X or my < OFFSET_Y or mx >= OFFSET_X + COLUNAS*TAM or my >= OFFSET_Y + LINHAS*TAM:
        return None, None
    return int((mx - OFFSET_X) // TAM), int((my - OFFSET_Y) // TAM)

def draw_ui():
    pygame.draw.rect(TELA, (25,25,25), (0,0,LARGURA,90))
    
    # Botão 1: Peashooter
    btn_pea = pygame.Rect(20, 10, 200, 70)
    pygame.draw.rect(TELA, (210,210,130), btn_pea, border_radius=8)
    TELA.blit(font.render(f"Peashooter ({PLANT_COST})", True, BLACK), (36, 28))
    if selected == "pea":
        pygame.draw.rect(TELA, SELECT_BORDER, btn_pea, 4, border_radius=8)

    # Botão 2: Wallnut
    btn_wallnut = pygame.Rect(230, 10, 200, 70)
    pygame.draw.rect(TELA, (210,130,130), btn_wallnut, border_radius=8)
    TELA.blit(font.render(f"Wallnut ({WALLNUT_COST})", True, BLACK), (246, 28))
    if selected == "wallnut":
        pygame.draw.rect(TELA, SELECT_BORDER, btn_wallnut, 4, border_radius=8)

    # Contador de Sol
    TELA.blit(font.render(f"Sol: {sols}", True, YELLOW), (450, 30))
    
    return {"pea": btn_pea, "wallnut": btn_wallnut}

def safe_remove(container, item):
    try:
        container.remove(item)
    except ValueError:
        pass

def reset_game():
    global grade, plants, bullets, zombies, suns, sols, selected, frame, spawn_timer, spawn_interval, minute_ticks, GAME_STATE, GAME_OVER_SOUND_PLAYED
    
    grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]
    plants = []
    bullets = []
    zombies = []
    suns = []

    sols = 150
    selected = None
    frame = 0
    spawn_timer = 0
    spawn_interval = 320
    minute_ticks = 0
    GAME_STATE = "PLAYING"
    GAME_OVER_SOUND_PLAYED = False

def draw_game_over(tela):
    # Fundo semi-transparente
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    tela.blit(overlay, (0, 0))
    
    # Título
    title_txt = font_large.render("G A M E   O V E R", True, (255, 50, 50))
    title_rect = title_txt.get_rect(center=(LARGURA // 2, ALTURA // 3))
    tela.blit(title_txt, title_rect)
    
    # Botões
    btn_w, btn_h = 300, 60
    
    # Botão 1: Recomeçar
    restart_rect = pygame.Rect(LARGURA // 2 - btn_w // 2, ALTURA // 2, btn_w, btn_h)
    pygame.draw.rect(tela, GREEN1, restart_rect, border_radius=10)
    restart_txt = font_medium.render("RECOMEÇAR", True, BLACK)
    tela.blit(restart_txt, restart_txt.get_rect(center=restart_rect.center))
    
    # Botão 2: Sair
    quit_rect = pygame.Rect(LARGURA // 2 - btn_w // 2, ALTURA // 2 + btn_h + 20, btn_w, btn_h)
    pygame.draw.rect(tela, (180, 50, 50), quit_rect, border_radius=10)
    quit_txt = font_medium.render("SAIR", True, WHITE)
    tela.blit(quit_txt, quit_txt.get_rect(center=quit_rect.center))
    
    return restart_rect, quit_rect

# ------------------------------- SPAWN ZOMBIE -----------------------------------
def spawn_zombies_logic():
    global spawn_timer, spawn_interval, minute_ticks, frame
    spawn_timer += 1
    minute_ticks += 1

    if minute_ticks >= FPS * 40:
        minute_ticks = 0
        spawn_interval = max(MIN_SPAWN_INTERVAL, spawn_interval - 40)

    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        linha = random.randint(0, LINHAS - 1)
        extra = int(frame / (FPS * 30)) 
        hp = 12 + extra 
        
        speed = 0.55 + min(0.8, extra * 0.03)
        zombies.append(Zombie(linha, hp=hp, speed=speed))


# ---------------------------------- LOOP PRINCIPAL --------------------------------
running = True
while running:
    dt = clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = pygame.mouse.get_pos()
            
            # 1. Lógica de clique na tela de Game Over
            if GAME_STATE == "GAME_OVER":
                restart_btn, quit_btn = draw_game_over(TELA) 
                
                if restart_btn.collidepoint(mx, my):
                    reset_game()
                elif quit_btn.collidepoint(mx, my):
                    running = False
                continue
            
            
            # Coletar sol
            collected = False
            for s in suns[:]:
                if s.rect.collidepoint(mx, my):
                    sols += s.value
                    safe_remove(suns, s)
                    collected = True
                    if COLLECT_SOUND:
                        COLLECT_SOUND.play()
                    break
            if collected:
                continue

            btns = draw_ui() 

            # Seleção de planta/muro
            if btns["pea"].collidepoint(mx, my):
                selected = "pea" if sols >= PLANT_COST else None
                continue
            if btns["wallnut"].collidepoint(mx, my):
                selected = "wallnut" if sols >= WALLNUT_COST else None
                continue

            col, lin = snap(mx, my)

            # Plantio
            if col is not None and grade[lin][col] is None:
                if selected == "pea" and sols >= PLANT_COST:
                    grade[lin][col] = True
                    plants.append(Plant(col, lin))
                    sols -= PLANT_COST
                    selected = None
                    continue
                
                elif selected == "wallnut" and sols >= WALLNUT_COST:
                    grade[lin][col] = True
                    plants.append(Wallnut(col, lin))
                    sols -= WALLNUT_COST
                    selected = None
                    continue

            selected = None 

    # ---- LÓGICA E DESENHO  ----
    
    if GAME_STATE == "PLAYING":
        frame += 1

        # LÓGICA DE JOGO
        spawn_zombies_logic()
        
        if frame % (FPS * 5) == 0:
            suns.append(Sun())

        for p in plants:
            p.update(bullets)

        for b in bullets[:]:
            b.update()
            if b.x > LARGURA + 200:
                safe_remove(bullets, b)

        for z in zombies[:]:
            z.eating = False

            for p in plants[:]:
                if p.lin == z.linha:
                    if z.rect.colliderect(p.rect):
                        z.eating = True
                        seconds = dt / 1000.0
                        damage_per_second = 0.8
                        p.hp -= damage_per_second * seconds
                        
                        p_right = p.rect.right
                        if z.x < p_right:
                            z.x = p_right + 2
                            z.rect.x = int(z.x)
                            
                        if p.hp <= 0:
                            grade[p.lin][p.col] = None
                            safe_remove(plants, p)
                            z.eating = False 
                        
                        break 

            z.update()

            for b in bullets[:]:
                if z.rect.colliderect(b.rect):
                    z.hp -= 2
                    safe_remove(bullets, b)
                    if HIT_SOUND:
                        HIT_SOUND.play()
                    if z.hp <= 0:
                        safe_remove(zombies, z)
                    break

            # Condição de Game Over
            if z.x < OFFSET_X - 30:
                print("GAME OVER — Um zumbi entrou na sua área!")
                GAME_STATE = "GAME_OVER"
                
        for s in suns:
            s.update()

        # DESENHO DO JOGO
        TELA.fill(BG)
        for l in range(LINHAS):
            for c in range(COLUNAS):
                x = OFFSET_X + c * TAM
                y = OFFSET_Y + l * TAM
                cor = GREEN1 if (l + c) % 2 == 0 else GREEN2
                pygame.draw.rect(TELA, cor, (x, y, TAM, TAM))

        draw_ui()

        for p in plants: p.draw()
        for b in bullets: b.draw()
        for z in zombies: z.draw()
        for s in suns: s.draw()

        # Preview ao selecionar
        if selected is not None:
            mx, my = pygame.mouse.get_pos()
            col, lin = snap(mx, my)
            if col is not None:
                px = OFFSET_X + col * TAM + (TAM - 100)//2
                py = OFFSET_Y + lin * TAM + (TAM - 100)//2
                surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                
                if selected == "pea":
                    if PEA: surf.blit(PEA, (0, 0))
                    else: pygame.draw.circle(surf, (0,150,0,180), (50, 50), 40)
                elif selected == "wallnut":
                    if WALLNUT: surf.blit(WALLNUT, (0, 0))
                    else: pygame.draw.rect(surf, (180, 150, 100, 180), (10, 10, 80, 80), border_radius=10)

                TELA.blit(surf, (px, py))

    # ---- DESENHO GAME OVER ----
    elif GAME_STATE == "GAME_OVER":
        
        draw_game_over(TELA)
        
        if not GAME_OVER_SOUND_PLAYED:
            if GAME_OVER_SOUND:
                pygame.mixer.stop()
                GAME_OVER_SOUND.play()
            GAME_OVER_SOUND_PLAYED = True

    pygame.display.update()

pygame.quit()
sys.exit()