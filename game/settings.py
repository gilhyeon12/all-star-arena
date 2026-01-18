import pygame

# 게임 설정
# 화면 크기, 색상, 프레임 속도 등을 정의합니다.

# 화면 크기 (너비, 높이)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "나루토 vs 블리치: 파이썬 배틀"

# 색상 정의 (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
SKY_BLUE = (135, 206, 235) # 마나 색상

# 게임 프레임 속도 (FPS)
FPS = 60

# 게임 상태 (Game States)
STATE_MENU = "menu"
STATE_SELECT = "select"
STATE_BATTLE = "battle"
STATE_GAME_OVER = "game_over"
STATE_SETTINGS = "settings"

# 게임 환경설정
DIFFICULTY_EASY = "EASY"
DIFFICULTY_NORMAL = "NORMAL"
DIFFICULTY_HARD = "HARD"
DIFFICULTY_VERY_HARD = "VERY HARD"

# 초기 설정값
DEFAULT_DIFFICULTY = DIFFICULTY_NORMAL
DEFAULT_BGM_VOLUME = 50
DEFAULT_SFX_VOLUME = 50

# 캐릭터 설정
CHARACTER_WIDTH = 50
CHARACTER_HEIGHT = 100
CHARACTER_SPEED = 5
JUMP_HEIGHT = 15
GRAVITY = 0.8
DASH_SPEED = 15 # 대쉬 속도
DASH_DURATION = 10 # 대쉬 지속 프레임

# 전투 설정 (기본)
ATTACK_RANGE = 60
ATTACK_COOLDOWN = 30
KNOCKBACK_FORCE = 10

# 마나 시스템 설정
MAX_MANA = 100
MANA_REGEN = 0.1 # 프레임당 회복량

# 스킬 데이터 (데미지, 마나 소모)
# 키: 스킬 식별자 (U, I, O / 4, 5, 6 ...)
SKILL_DATA = {
    # 공통
    'J': {'damage': 5, 'mana': 0, 'cooldown': 10, 'type': 'basic'}, # 기본 공격
    
    # Naruto Skills (P1 Keys: U, I, O)
    'U': {'damage': 10, 'mana': 5, 'cooldown': 60, 'type': 'projectile', 'name': 'Shuriken'}, # 1초 = 60프레임
    'I': {'damage': 0, 'mana': 30, 'cooldown': 900, 'type': 'summon', 'name': 'Shadow Clone'}, # 15초
    'O': {'damage': 50, 'mana': 50, 'cooldown': 1800, 'type': 'dash_attack', 'name': 'Rasengan'}, # 30초
    
    # Bleach Skills (placeholder)
    '4': {'damage': 15, 'mana': 10, 'cooldown': 60, 'type': 'attack'},
    '5': {'damage': 25, 'mana': 20, 'cooldown': 120, 'type': 'attack'},
    '6': {'damage': 40, 'mana': 40, 'cooldown': 300, 'type': 'attack'},
    '1': {'damage': 5, 'mana': 0, 'cooldown': 10, 'type': 'basic'}, # P2 기본 공격
    
    # Common
    'DASH': {'damage': 0, 'mana': 5, 'cooldown': 30, 'type': 'movement'}
}

# 스킬 키 설정 (Player 1)
P1_KEY_U = pygame.K_u # 스킬 1
P1_KEY_I = pygame.K_i # 스킬 2
P1_KEY_O = pygame.K_o # 스킬 3
P1_KEY_J = pygame.K_j # 기본 공격 (Basic)
P1_KEY_K = pygame.K_k # 방어 (Guard)
P1_KEY_L = pygame.K_l # 대쉬 (Dash)

# 스킬 키 설정 (Player 2 - Numpad)
P2_KEY_4 = pygame.K_KP4 # 스킬 1
P2_KEY_5 = pygame.K_KP5 # 스킬 2
P2_KEY_6 = pygame.K_KP6 # 스킬 3
P2_KEY_1 = pygame.K_KP1 # 기본 공격
P2_KEY_2 = pygame.K_KP2 # 방어
P2_KEY_3 = pygame.K_KP3 # 대쉬

PARTICLE_COLOR = (255, 200, 50)
