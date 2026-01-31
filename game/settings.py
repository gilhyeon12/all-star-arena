import pygame

# 게임 설정
# 화면 크기, 색상, 프레임 속도 등을 정의합니다.

# 시리즈별 캐릭터 분류 데이터
SERIES_DATA = {
    "Naruto": ["Naruto", "Sasuke", "Sakura"],
    "Bleach": ["Ichigo", "Inoue"],
    "Dragon Ball": ["Goku", "Vegeta"],
    "One Piece": ["Luffy", "Zoro"],
    "My Hero Academia": ["Todoroki", "Uraraka"],
    "Attack on Titan": ["Eren", "Mikasa"],
    "Demon Slayer": ["Tanjiro", "Nezuko"],
    "Chainsaw Man": ["Denji", "Power"],
    "Jujutsu Kaisen": ["Itadori", "Gojo", "Fushiguro"]
}

# 시리즈별 테마 색상 (이펙트용)
SERIES_COLORS = {
    "Naruto": (255, 140, 0), # Orange
    "Bleach": (50, 50, 255), # Blue/Black
    "Dragon Ball": (255, 215, 0), # Gold
    "One Piece": (255, 50, 50), # Red
    "My Hero Academia": (0, 255, 127), # Spring Green
    "Attack on Titan": (139, 69, 19), # Saddle Brown / Red
    "Demon Slayer": (0, 191, 255), # Deep Sky Blue
    "Chainsaw Man": (220, 20, 60), # Crimson
    "Jujutsu Kaisen": (138, 43, 226) # Blue Violet
}

# 상호작용 대사 (Cross-Talk)
# 상호작용 대사 (Cross-Talk)
INTRO_DIALOGUES = {
    frozenset(["Naruto", "Sasuke"]): {
        "Naruto": "Sasuke! Come back to the village!",
        "Sasuke": "You are annoying, Naruto."
    },
    frozenset(["Goku", "Vegeta"]): {
        "Goku": "Hey Vegeta! Let's spar!",
        "Vegeta": "Hmph. Don't hold back, Kakarot."
    },
    frozenset(["Luffy", "Zoro"]): {
        "Luffy": "Zoro! Don't get lost!",
        "Zoro": "Shut up! I know where I'm going!"
    },
    frozenset(["Deku", "Bakugo"]): {
        "Deku": "Kacchan! I won't lose!",
        "Bakugo": "Die, Deku!!"
    },
    frozenset(["Tanjiro", "Nezuko"]): {
        "Tanjiro": "Nezuko... I will protect you!",
        "Nezuko": "Mmm!"
    },
    frozenset(["Gojo", "Sukuna"]): {
        "Gojo": "Did you get lost, King of Curses?",
        "Sukuna": "Know your place, fool."
    }
}

# 기본 대사 (분석된 데이터 기반)
CHARACTER_QUOTES = {
    "Naruto": [
        "As long as you're the best ninja in the village, you can become Hokage!",
        "I'll never give up, because that is my ninja way!",
        "Alright! I've taken a path I believe in, to live without regrets!"
    ],
    "Sasuke": [
        "Too many limitations will only make us lose ourselves.",
        "I am an avenger, I was born in revenge...",
        "My loneliness is not comparable..."
    ],
    "Sakura": [
        "I am always being protected by others... this time I must protect them!",
        "I've always wished I could be a powerful ninja..."
    ],
    "Kakashi": [
        "Ninjas can't think with common sense!",
        "Don't worry, I will protect you even if I die.",
        "You can't beat me now."
    ],
    "Ichigo": [
        "Fighting by itself is for nothing but survival.",
        "I don't know why, but it all feels amazing!",
        "It's terrifying because we can't see it."
    ],
    "Rukia": [
        "People can have hope because they don't know death.",
        "Is reincarnation our fate?"
    ],
    "Renji": [
        "I vowed to save her... I made this oath to nobody, just to my soul!",
        "Woohoo, tonight, I scream again."
    ],
    "Toshiro": [
        "Don't be afraid of tricks, this world is built on lies.",
        "Don't call me Toshiro, call me Captain Hitsugaya!"
    ],
    "Luffy": [
        "I'm gonna be King of the Pirates!",
        "If you don't take risks, you can't create a future!",
         "Gum-Gum...!"
    ],
    "Zoro": [
        "Scars on the back are a swordsman's shame.",
        "If I can't even protect my captain's dream, then whatever ambition I have is nothing but talk!"
    ],
    "Tanjiro": [
        "I will never yield to demons!",
        "Water Breathing...!",
        "Nezuko is my sister!"
    ],
    "Nezuko": [
        "Mmm...!",
        "Grrr...!"
    ],
    "Goku": [
        "I'm excited! Let's do this!",
        "You look pretty strong!",
        "Kamehameha!"
    ],
    "Vegeta": [
        "I am the Prince of all Saiyans!",
        "You're nothing but a loose monkey.",
        "Final Flash!"
    ]
}

# 표시 이름 (화면 표시용)
CHARACTER_DISPLAY_NAMES = {
    "Naruto": "Naruto Uzumaki",
    "Sasuke": "Sasuke Uchiha",
    "Sakura": "Sakura Haruno",
    "Kakashi": "Kakashi Hatake",
    "Ichigo": "Kurosaki Ichigo",
    "Rukia": "Rukia Kuchiki",
    "Renji": "Renji Abarai",
    "Toshiro": "Toshiro Hitsugaya",
    "Luffy": "Monkey D. Luffy",
    "Zoro": "Roronoa Zoro",
    "Tanjiro": "Tanjiro Kamado",
    "Nezuko": "Nezuko Kamado",
    "Goku": "Son Goku",
    "Vegeta": "Vegeta IV"
}

# 전체 캐릭터 목록 (평면화)
ALL_CHAR_LIST = []
for chars in SERIES_DATA.values():
    ALL_CHAR_LIST.extend(chars)

# 보조 전용 (하위 호환성용)
ALL_SUPPORTS_LIST = ["Sasuke", "Vegeta", "Zoro", "Inoue", "Sakura", "Uraraka", "Nezuko", "Mikasa"]

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
STATE_TITLE = "title" # NEW: 타이틀 화면
STATE_MENU = "menu"
STATE_SELECT = "select"
STATE_SELECT_ROUNDS = "select_rounds"  # NEW: 라운드 선택
STATE_SELECT_SUPPORT = "select_support"
STATE_SELECT_MAP = "select_map"
STATE_BATTLE = "battle"
STATE_GAME_OVER = "game_over"
STATE_SETTINGS = "settings"
STATE_KEY_SETTINGS = "key_settings"
STATE_KEY_SETTINGS = "key_settings"
STATE_PAUSE = "pause"
STATE_INTRO = "intro" # NEW: 전투 전 인트로
STATE_EXIT_CONFIRM = "exit_confirm" # NEW: 종료 확인
STATE_TRAINING_MENU = "training_menu" # NEW: 트레이닝 설정
STATE_ARCADE_LADDER = "arcade_ladder" # NEW: 아케이드 진행 상황
STATE_ARCADE_ENDING = "arcade_ending" # NEW: 엔딩 크레딧

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
CHARACTER_WIDTH = 70
CHARACTER_HEIGHT = 100
CHARACTER_SPEED = 5
SUPPORT_CHARACTER_WIDTH = 45
SUPPORT_CHARACTER_HEIGHT = 60
JUMP_HEIGHT = 15
GRAVITY = 0.8
DASH_SPEED = 15 # 대쉬 속도
DASH_DURATION = 10 # 대쉬 지속 프레임
MAX_JUMP_COUNT = 2 # 이중 점프 허용 횟수

# 전투 설정 (기본)
ATTACK_RANGE = 60
ATTACK_COOLDOWN = 30
SUPPORT_COOLDOWN = 1200 # 20초 (태그 쿨타임으로 사용)
TAG_COOLDOWN = 600 # 10 seconds (60 FPS * 10)
KNOCKBACK_FORCE = 10
PUSH_FORCE = 20 # 가드 푸시 밀너내기 힘

# 기력 시스템 설정 (Ki)
MAX_KI = 5
KI_REGEN = 0 # 자동 회복 없음
KI_GAIN_ON_HIT = 0.5 # 타격 시 회복량


# 방어 게이지 설정
MAX_GUARD_GAUGE = 100
GUARD_REGEN = 0.2


# 스킬 데이터
# 기본 스킬 정의 (폴백용)
DEFAULT_SKILLS = {
    'J': {'damage': 5, 'cost': 0, 'cooldown': 10, 'type': 'basic', 'name': 'Punch'},
    'U': {'damage': 15, 'cost': 0, 'cooldown': 60, 'type': 'projectile', 'name': 'Energy Blast'},
    'I': {'damage': 30, 'cost': 1, 'cooldown': 120, 'type': 'attack', 'name': 'Special Move'},
    'O': {'damage': 0, 'cost': 0, 'cooldown': 1200, 'type': 'support', 'name': 'Call Support'},
    'DASH': {'damage': 0, 'cost': 0, 'cooldown': 30, 'type': 'movement'}
}

# 캐릭터별 특수 스킬 (없으면 DEFAULT 사용)
SKILL_DATA = {
    # ---------------- NARUTO ----------------
    "Naruto": {
        'U': {'damage': 15, 'cost': 0, 'cooldown': 60, 'type': 'projectile', 'name': 'Rasengan', 'effect': 'spiral_blue'}, 
        'I': {'damage': 0, 'cost': 1, 'cooldown': 120, 'type': 'summon', 'name': 'Shadow Clone', 'effect': 'smoke'}, 
        'O': {'damage': 50, 'cost': 0, 'cooldown': 900, 'type': 'dash_attack', 'name': 'Giant Rasengan', 'effect': 'spiral_big'} 
    },
    "Sasuke": {
        'U': {'damage': 20, 'cost': 0, 'cooldown': 50, 'type': 'projectile', 'name': 'Chidori Senbon', 'effect': 'lightning'}, 
        'I': {'damage': 60, 'cost': 2, 'cooldown': 180, 'type': 'area', 'name': 'Kirin', 'effect': 'lightning_storm'}, 
        'O': {'damage': 10, 'cost': 0, 'cooldown': 900, 'type': 'projectile', 'name': 'Fireball Jutsu', 'effect': 'fire_breath'} 
    },
    "Sakura": {
        'U': {'damage': 25, 'cost': 0, 'cooldown': 70, 'type': 'attack', 'name': 'Cherry Blossom Impact', 'effect': 'impact_pink'}, 
        'I': {'damage': 0, 'cost': 2, 'cooldown': 300, 'type': 'buff', 'name': 'Creation Rebirth', 'effect': 'heal_aura'}, 
        'O': {'damage': 0, 'cost': 0, 'cooldown': 1200, 'type': 'heal', 'name': 'Katsuyu Heal', 'effect': 'heal_burst'} 
    },

    # ---------------- BLEACH ----------------
    "Ichigo": {
        'U': {'damage': 25, 'cost': 0, 'cooldown': 60, 'type': 'projectile', 'name': 'Getsuga Tensho', 'effect': 'slash_blue'},
        'I': {'damage': 60, 'cost': 1, 'cooldown': 120, 'type': 'dash_attack', 'name': 'Flash Step Slash', 'effect': 'slash_black'},
        'O': {'damage': 40, 'cost': 0, 'cooldown': 900, 'type': 'attack', 'name': 'Sword Pressure', 'effect': 'shockwave'}
    },
    "Inoue": {
        'U': {'damage': 0, 'cost': 0, 'cooldown': 180, 'type': 'buff', 'name': 'Santen Kesshun', 'effect': 'shield_orange'}, 
        'I': {'damage': 30, 'cost': 1, 'cooldown': 100, 'type': 'projectile', 'name': 'Koten Zanshun', 'effect': 'triangle_beam'}, 
        'O': {'damage': 0, 'cost': 0, 'cooldown': 1000, 'type': 'heal', 'name': 'Soten Kisshun', 'effect': 'heal_area'} 
    },

    # ---------------- DRAGON BALL ----------------
    "Goku": {
        'U': {'damage': 20, 'cost': 0, 'cooldown': 50, 'type': 'projectile', 'name': 'Kamehameha', 'effect': 'beam_charge_blue'},
        'I': {'damage': 80, 'cost': 3, 'cooldown': 300, 'type': 'projectile', 'name': 'Spirit Bomb', 'effect': 'giant_orb_blue'}, 
        'O': {'damage': 40, 'cost': 0, 'cooldown': 900, 'type': 'dash_attack', 'name': 'Kaioken Attack', 'effect': 'aura_red'}
    },
    "Vegeta": {
        'U': {'damage': 15, 'cost': 0, 'cooldown': 20, 'type': 'projectile', 'name': 'Energy Volley', 'effect': 'barrage_yellow'}, 
        'I': {'damage': 70, 'cost': 2, 'cooldown': 200, 'type': 'beam', 'name': 'Final Flash', 'effect': 'beam_charge_yellow'}, 
        'O': {'damage': 50, 'cost': 0, 'cooldown': 900, 'type': 'area', 'name': 'Big Bang Attack', 'effect': 'explosion_big'}
    },

    # ---------------- ONE PIECE ----------------
    "Luffy": {
        'U': {'damage': 25, 'cost': 0, 'cooldown': 40, 'type': 'attack', 'name': 'Gum-Gum Pistol', 'effect': 'stretch_punch'}, 
        'I': {'damage': 60, 'cost': 1, 'cooldown': 100, 'type': 'attack', 'name': 'Gum-Gum Gatling', 'effect': 'multi_punch'}, 
        'O': {'damage': 50, 'cost': 0, 'cooldown': 900, 'type': 'attack', 'name': 'Gum-Gum Bazooka', 'effect': 'impact_big'}
    },
    "Zoro": {
        'U': {'damage': 25, 'cost': 0, 'cooldown': 50, 'type': 'projectile', 'name': 'Phoenix Cannon', 'effect': 'slash_air'}, 
        'I': {'damage': 65, 'cost': 1, 'cooldown': 120, 'type': 'dash_attack', 'name': 'Lion Song', 'effect': 'slash_draw'}, 
        'O': {'damage': 45, 'cost': 0, 'cooldown': 900, 'type': 'area', 'name': 'Dragon Twister', 'effect': 'tornado_green'} 
    },

    # ---------------- MY HERO ACADEMIA ----------------
    "Todoroki": {
        'U': {'damage': 20, 'cost': 0, 'cooldown': 60, 'type': 'projectile', 'name': 'Ice Wall', 'effect': 'ice_spikes'}, 
        'I': {'damage': 70, 'cost': 2, 'cooldown': 150, 'type': 'beam', 'name': 'Flashfire Fist', 'effect': 'fire_blast'}, 
        'O': {'damage': 40, 'cost': 0, 'cooldown': 900, 'type': 'area', 'name': 'Glacier Spike', 'effect': 'ice_field'} 
    },
    "Uraraka": {
        'U': {'damage': 10, 'cost': 0, 'cooldown': 40, 'type': 'attack', 'name': 'Zero Gravity Touch', 'effect': 'float_sparkles'}, 
        'I': {'damage': 60, 'cost': 1, 'cooldown': 120, 'type': 'area', 'name': 'Meteor Storm', 'effect': 'falling_rocks'},
        'O': {'damage': 0, 'cost': 0, 'cooldown': 900, 'type': 'debuff', 'name': 'Gravity Release', 'effect': 'purple_haze'} 
    },

    # ---------------- ATTACK ON TITAN ----------------
    "Eren": {
        'U': {'damage': 30, 'cost': 0, 'cooldown': 50, 'type': 'dash_attack', 'name': 'ODM Slash', 'effect': 'slash_fast'},
        'I': {'damage': 80, 'cost': 2, 'cooldown': 200, 'type': 'attack', 'name': 'Titan Punch', 'effect': 'impact_heavy'},
        'O': {'damage': 40, 'cost': 0, 'cooldown': 900, 'type': 'attack', 'name': 'Coordinate Scream', 'effect': 'roar_wave'}
    },
    "Mikasa": {
        'U': {'damage': 25, 'cost': 0, 'cooldown': 40, 'type': 'projectile', 'name': 'Thunder Spear', 'effect': 'explosion_small'},
        'I': {'damage': 60, 'cost': 1, 'cooldown': 100, 'type': 'dash_attack', 'name': 'Ackerman Spin', 'effect': 'spin_slash'},
        'O': {'damage': 50, 'cost': 0, 'cooldown': 900, 'type': 'attack', 'name': 'Precise Cut', 'effect': 'slash_crit'}
    },

    # ---------------- DEMON SLAYER ----------------
    "Tanjiro": {
        'U': {'damage': 25, 'cost': 0, 'cooldown': 50, 'type': 'attack', 'name': 'Water Wheel', 'effect': 'water_circle'},
        'I': {'damage': 70, 'cost': 1, 'cooldown': 150, 'type': 'dash_attack', 'name': 'Hinokami Kagura', 'effect': 'fire_slash'},
        'O': {'damage': 20, 'cost': 0, 'cooldown': 600, 'type': 'projectile', 'name': 'Fire Wheel', 'effect': 'fire_circle'}
    },
    "Nezuko": {
        'U': {'damage': 25, 'cost': 0, 'cooldown': 50, 'type': 'projectile', 'name': 'Exploding Blood', 'effect': 'blood_explosion'},
        'I': {'damage': 60, 'cost': 1, 'cooldown': 100, 'type': 'attack', 'name': 'Berserk Kick', 'effect': 'impact_red'},
        'O': {'damage': 40, 'cost': 0, 'cooldown': 900, 'type': 'attack', 'name': 'Demonic Claw', 'effect': 'claw_red'}
    },

    # ---------------- CHAINSAW MAN ----------------
    "Denji": {
        'U': {'damage': 20, 'cost': 0, 'cooldown': 40, 'type': 'dash_attack', 'name': 'Chain Pull', 'effect': 'chain_spark'},
        'I': {'damage': 70, 'cost': 1, 'cooldown': 120, 'type': 'attack', 'name': 'Chainsaw Shred', 'effect': 'blood_splatter'},
        'O': {'damage': 0, 'cost': 0, 'cooldown': 900, 'type': 'buff', 'name': 'Blood Recovery', 'effect': 'heal_blood'} 
    },
    "Power": {
        'U': {'damage': 30, 'cost': 0, 'cooldown': 60, 'type': 'attack', 'name': 'Blood Hammer', 'effect': 'hammer_smash'},
        'I': {'damage': 60, 'cost': 1, 'cooldown': 100, 'type': 'projectile', 'name': 'Blood Spears', 'effect': 'spear_rain'},
        'O': {'damage': 30, 'cost': 0, 'cooldown': 800, 'type': 'attack', 'name': 'Cat Punch', 'effect': 'scratch'}
    },

    # ---------------- JUJUTSU KAISEN ----------------
    "Itadori": {
        'U': {'damage': 20, 'cost': 0, 'cooldown': 30, 'type': 'attack', 'name': 'Divergent Fist', 'effect': 'double_impact'}, 
        'I': {'damage': 80, 'cost': 1, 'cooldown': 120, 'type': 'attack', 'name': 'Black Flash', 'effect': 'black_spark'}, 
        'O': {'damage': 40, 'cost': 0, 'cooldown': 900, 'type': 'dash_attack', 'name': 'Manji Kick', 'effect': 'impact_kick'}
    },
    "Gojo": {
        'U': {'damage': 30, 'cost': 0, 'cooldown': 50, 'type': 'projectile', 'name': 'Cursed Technique: Blue', 'effect': 'orb_blue_pull'},
        'I': {'damage': 90, 'cost': 2, 'cooldown': 300, 'type': 'beam', 'name': 'Hollow Purple', 'effect': 'orb_purple_nuke'}, 
        'O': {'damage': 0, 'cost': 0, 'cooldown': 1200, 'type': 'area', 'name': 'Infinite Void', 'effect': 'void_domain'} 
    },
    "Fushiguro": {
        'U': {'damage': 25, 'cost': 0, 'cooldown': 60, 'type': 'summon', 'name': 'Divine Dog', 'effect': 'shadow_wolf'}, 
        'I': {'damage': 60, 'cost': 1, 'cooldown': 150, 'type': 'projectile', 'name': 'Nue: Electricity', 'effect': 'lightning_bird'},
        'O': {'damage': 50, 'cost': 0, 'cooldown': 900, 'type': 'area', 'name': 'Chimera Shadow Garden', 'effect': 'shadow_sludge'}
    },
    
    # NEW CHARACTERS (From updates)
    "Hisoka": {
         'U': {'damage': 20, 'cost': 0, 'cooldown': 40, 'type': 'projectile', 'name': 'Bungee Gum Cards', 'effect': 'card_throw'},
         'I': {'damage': 60, 'cost': 1, 'cooldown': 120, 'type': 'attack', 'name': 'Bungee Gum Punch', 'effect': 'gum_stick'},
         'O': {'damage': 0, 'cost': 0, 'cooldown': 900, 'type': 'debuff', 'name': 'Texture Surprise', 'effect': 'illusion_smoke'}
    },
    "Tanya": {
         'U': {'damage': 30, 'cost': 0, 'cooldown': 30, 'type': 'projectile', 'name': 'Magic Rifle', 'effect': 'bullet_trail'},
         'I': {'damage': 80, 'cost': 2, 'cooldown': 200, 'type': 'area', 'name': 'Prayer Explosion', 'effect': 'explosion_gold'},
         'O': {'damage': 0, 'cost': 0, 'cooldown': 900, 'type': 'buff', 'name': 'Type 95 Computation', 'effect': 'digital_aura'}
    },
    "Edward": {
         'U': {'damage': 25, 'cost': 0, 'cooldown': 40, 'type': 'attack', 'name': 'Alchemy Spear', 'effect': 'stone_spike'},
         'I': {'damage': 60, 'cost': 1, 'cooldown': 120, 'type': 'area', 'name': 'Cannon Transmutation', 'effect': 'cannon_blast'},
         'O': {'damage': 0, 'cost': 0, 'cooldown': 900, 'type': 'wall', 'name': 'Stone Wall', 'effect': 'wall_rise'} 
    },

    # ---------------- TRANSFORMATIONS ----------------
    "Super Saiyan Goku": {
        'J': {'damage': 15, 'cost': 0, 'cooldown': 8, 'type': 'basic', 'name': 'Super Punch', 'effect': 'impact_gold'},
        'U': {'damage': 35, 'cost': 0, 'cooldown': 40, 'type': 'projectile', 'name': 'Kamehameha (Full)', 'effect': 'beam_charge_gold'},
        'I': {'damage': 80, 'cost': 1, 'cooldown': 100, 'type': 'dash_attack', 'name': 'Instant Transmission Kamehameha', 'effect': 'teleport_beam'}
    },
    "Super Saiyan Vegeta": {
        'J': {'damage': 15, 'cost': 0, 'cooldown': 8, 'type': 'basic', 'name': 'Saiyan Strike', 'effect': 'impact_gold'},
        'U': {'damage': 30, 'cost': 0, 'cooldown': 20, 'type': 'projectile', 'name': 'Ki Barrage', 'effect': 'barrage_gold'},
        'I': {'damage': 80, 'cost': 1, 'cooldown': 120, 'type': 'beam', 'name': 'Final Flash (Full)', 'effect': 'beam_charge_gold_big'}
    },
    "Naruto (Sage Mode)": {
        'J': {'damage': 15, 'cost': 0, 'cooldown': 8, 'type': 'basic', 'name': 'Sage Punch', 'effect': 'impact_orange'},
        'U': {'damage': 45, 'cost': 0, 'cooldown': 90, 'type': 'projectile', 'name': 'Rasenshuriken', 'effect': 'shuriken_wind'},
        'I': {'damage': 70, 'cost': 1, 'cooldown': 60, 'type': 'attack', 'name': 'Frog Kumite', 'effect': 'impact_invisible'}
    },
    "Ichigo (Bankai)": {
        'J': {'damage': 20, 'cost': 0, 'cooldown': 5, 'type': 'basic', 'name': 'Tensa Zangetsu', 'effect': 'slash_black'},
        'U': {'damage': 45, 'cost': 0, 'cooldown': 50, 'type': 'projectile', 'name': 'Getsuga Tensho (Black)', 'effect': 'slash_black_big'},
        'I': {'damage': 90, 'cost': 2, 'cooldown': 150, 'type': 'dash_attack', 'name': 'Speed Blitz', 'effect': 'slash_rapid'}
    },
    "Luffy (Gear 2)": {
        'J': {'damage': 15, 'cost': 0, 'cooldown': 6, 'type': 'basic', 'name': 'Jet Pistol', 'effect': 'steam_punch'},
        'U': {'damage': 40, 'cost': 0, 'cooldown': 35, 'type': 'attack', 'name': 'Jet Whip', 'effect': 'steam_kick'},
        'I': {'damage': 80, 'cost': 1, 'cooldown': 100, 'type': 'attack', 'name': 'Jet Gatling', 'effect': 'steam_gatling'}
    },
    "Tanjiro (Hinokami)": {
        'J': {'damage': 18, 'cost': 0, 'cooldown': 8, 'type': 'basic', 'name': 'Sun Slash', 'effect': 'fire_slash_small'},
        'U': {'damage': 40, 'cost': 0, 'cooldown': 60, 'type': 'projectile', 'name': 'Fire Wheel', 'effect': 'fire_circle'},
        'I': {'damage': 85, 'cost': 1, 'cooldown': 120, 'type': 'dash_attack', 'name': 'Clear Blue Sky', 'effect': 'fire_slash_big'}
    }
}

# 스킬 키 설정 (Player 1)
P1_KEY_U = pygame.K_u # 원거리 공격 (Ranged)
P1_KEY_I = pygame.K_i # 필살기 (Special/Ultimate)
P1_KEY_O = pygame.K_o # 보조 캐릭터 스킬 (Support Skill)
P1_KEY_J = pygame.K_j # 기본 공격 (Basic)
P1_KEY_K = pygame.K_k # 점프 (Jump)
P1_KEY_S = pygame.K_s # 방어 (Guard)
P1_KEY_L = pygame.K_l # 대쉬 (Dash)

# 스킬 키 설정 (Player 2 - Numpad)
P2_KEY_4 = pygame.K_KP4 # 스킬 1
P2_KEY_5 = pygame.K_KP5 # 스킬 2
P2_KEY_6 = pygame.K_KP6 # 스킬 3
P2_KEY_1 = pygame.K_KP1 # 기본 공격
P2_KEY_2 = pygame.K_KP2 # 방어
P2_KEY_3 = pygame.K_KP3 # 대쉬

PARTICLE_COLOR = (255, 200, 50)

# 변신 시스템 설정
TRANSFORM_COST = 3
JOINT_ATTACK_COST = 5

# 바꿔치기 술 (Substituion) 설정
SUBSTITUTION_COST = 1.0 # 기력 소모량
SUBSTITUTION_COOLDOWN = 60 # 쿨타임 (프레임)
INVINCIBLE_DURATION = 30 # 무적 시간 (프레임)

TRANSFORMATIONS = {
    "Goku": {
        "name": "Super Saiyan Goku", 
        "damage_mult": 1.5, 
        "speed_mult": 1.3, 
        "color": (255, 215, 0) # Gold
    },
    "Vegeta": {
        "name": "Super Saiyan Vegeta", 
        "damage_mult": 1.4, 
        "speed_mult": 1.2, 
        "color": (255, 215, 0) # Gold
    },
    "Naruto": {
        "name": "Naruto (Sage Mode)", 
        "damage_mult": 1.3, 
        "speed_mult": 1.2, 
        "color": (255, 100, 0) # Orange
    },
    "Ichigo": {
        "name": "Ichigo (Bankai)", 
        "damage_mult": 1.4, 
        "speed_mult": 1.5, 
        "color": (50, 0, 0) # Dark Red
    },
    "Luffy": {
        "name": "Luffy (Gear 2)",
        "damage_mult": 1.3,
        "speed_mult": 1.6,
        "color": (255, 100, 100) # Reddish
    },
    "Tanjiro": {
        "name": "Tanjiro (Hinokami)",
        "damage_mult": 1.4,
        "speed_mult": 1.2,
    }
}

# ---------------------------------------------------------
# NEW SETTINGS from USAGE.md
# ---------------------------------------------------------

# Attack Types for character logic
ATTACK_NORMAL = "normal"
ATTACK_AIR = "air"
ATTACK_LOW = "low"
ATTACK_COUNTER = "counter"

# Game Settings Storage
GAME_SETTINGS = {
    "camera_shake": 50,          # 0-100%
    "rendering_style": "Modern", # Classic/Modern
    "ult_skip": "Short",         # Full/Short/Skip
    "bgm_hijack": True,          # True/False
    "sfx_type": "Comic",         # Heavy/Comic
    "infinite_resource": False,  # True/False (Aura/Ki)
    "support_cooldown_mult": 1.0 # Multiplier (0.5 = Faster)
}

# Rendering Styles
RENDER_CLASSIC = "Classic"
RENDER_MODERN = "Modern"

# Ult Skip Options
ULT_FULL = "Full"
ULT_SHORT = "Short"
ULT_SKIP = "Skip"

# SFX Types
SFX_HEAVY = "Heavy"
SFX_COMIC = "Comic"
