import pygame
import os

# 초기화
pygame.init()

# 색상 정의
TRANSPARENT = (0, 0, 0, 0)

# Naruto colors
NARUTO_ORANGE = (255, 140, 0)
NARUTO_YELLOW = (255, 215, 0)
NARUTO_SKIN = (255, 220, 177)
HEADBAND_BLUE = (0, 0, 139)
HEADBAND_METAL = (192, 192, 192)

# Ichigo colors
ICHIGO_BLACK = (20, 20, 20)
ICHIGO_ORANGE = (255, 120, 0)
ICHIGO_SKIN = (255, 227, 208)
SWORD_GRAY = (200, 200, 200)
SWORD_WRAP = (240, 240, 240)

# Goku colors
GOKU_ORANGE = (255, 100, 0)
GOKU_BLUE = (0, 100, 200)
GOKU_SKIN = (255, 200, 150)
GOKU_BLACK = (30, 30, 30)

# Luffy colors
LUFFY_RED = (220, 20, 60)
LUFFY_BLUE = (70, 130, 180)
LUFFY_SKIN = (255, 210, 180)
LUFFY_YELLOW = (255, 215, 0)

# Saitama colors
SAITAMA_YELLOW = (255, 215, 0)
SAITAMA_WHITE = (255, 255, 255)
SAITAMA_RED = (220, 20, 60)
SAITAMA_SKIN = (255, 220, 177)

# Edward colors
EDWARD_RED = (200, 0, 0)
EDWARD_BLACK = (30, 30, 30)
EDWARD_YELLOW = (255, 215, 0)
EDWARD_SKIN = (255, 220, 177)
EDWARD_METAL = (192, 192, 192)

# Todoroki colors
TODOROKI_BLUE = (100, 200, 255)
TODOROKI_RED = (255, 100, 100)
TODOROKI_WHITE = (255, 255, 255)
TODOROKI_SKIN = (255, 220, 177)
TODOROKI_GRAY = (100, 100, 100)

# Tanya colors
TANYA_BLUE = (50, 100, 200)
TANYA_YELLOW = (255, 215, 0)
TANYA_SKIN = (255, 220, 177)
TANYA_BROWN = (139, 69, 19)

# Arena (Original) colors
ARENA_PURPLE = (138, 43, 226)
ARENA_GOLD = (255, 215, 0)
ARENA_WHITE = (255, 255, 255)
ARENA_SKIN = (255, 220, 177)

# Shadow (Original) colors
SHADOW_BLACK = (20, 20, 20)
SHADOW_RED = (200, 0, 0)
SHADOW_GRAY = (80, 80, 80)
SHADOW_DARK_PURPLE = (75, 0, 130)

# Support characters
SASUKE_BLUE = (0, 0, 139)
SASUKE_WHITE = (255, 255, 255)
SASUKE_SKIN = (255, 220, 177)
SASUKE_BLACK = (30, 30, 30)

INOUE_ORANGE = (255, 140, 0)
INOUE_WHITE = (255, 255, 255)
INOUE_SKIN = (255, 220, 177)
INOUE_BROWN = (139, 69, 19)

VEGETA_BLUE = (0, 100, 200)
VEGETA_WHITE = (255, 255, 255)
VEGETA_SKIN = (255, 200, 150)
VEGETA_BLACK = (30, 30, 30)

ZORO_GREEN = (0, 128, 0)
ZORO_BLACK = (30, 30, 30)
ZORO_SKIN = (255, 210, 180)
ZORO_WHITE = (255, 255, 255)

SAKURA_PINK = (255, 192, 203)
SAKURA_RED = (220, 20, 60)
SAKURA_SKIN = (255, 220, 177)
SAKURA_BLONDE = (255, 215, 0)

URARAKA_BROWN = (139, 69, 19)
URARAKA_PINK = (255, 192, 203)
URARAKA_SKIN = (255, 220, 177)
URARAKA_WHITE = (255, 255, 255)

# Eren colors (Attack on Titan)
EREN_BROWN = (139, 69, 19)
EREN_GREEN = (0, 100, 50)
EREN_SKIN = (255, 220, 177)
EREN_WHITE = (255, 255, 255)

# Tanjiro colors (Demon Slayer)
TANJIRO_RED = (139, 0, 0)
TANJIRO_GREEN = (0, 100, 0)
TANJIRO_BLACK = (30, 30, 30)
TANJIRO_SKIN = (255, 220, 177)

# Denji colors (Chainsaw Man)
DENJI_YELLOW = (255, 215, 0)
DENJI_RED = (200, 0, 0)
DENJI_WHITE = (255, 255, 255)
DENJI_SKIN = (255, 220, 177)

# Nezuko colors (Support - Demon Slayer)
NEZUKO_PINK = (255, 192, 203)
NEZUKO_BLACK = (30, 30, 30)
NEZUKO_SKIN = (255, 220, 177)

# Mikasa colors (Support - Attack on Titan)
MIKASA_BLACK = (30, 30, 30)
MIKASA_RED = (200, 0, 0)
MIKASA_SKIN = (255, 220, 177)
MIKASA_GRAY = (100, 100, 100)

# JJK colors
ITADORI_PINK = (255, 182, 193)
ITADORI_BLACK = (20, 20, 20)
GOJO_WHITE = (255, 255, 255)
GOJO_BLUE = (100, 149, 237)
FUSHIGURO_BLACK = (10, 10, 10)
FUSHIGURO_BLUE = (25, 25, 112)

# HxH colors
GON_GREEN = (34, 139, 34)
GON_BLACK = (0, 0, 0)
KILLUA_WHITE = (245, 245, 245)
KILLUA_BLUE = (135, 206, 235)
HISOKA_PINK = (255, 105, 180)
HISOKA_PURPLE = (128, 0, 128)

# JoJo colors
JOTARO_BLUE = (0, 0, 128)
JOTARO_GOLD = (218, 165, 32)
DIO_YELLOW = (255, 215, 0)
DIO_GREEN = (50, 205, 50)

# Power colors (CSM)
POWER_PINK = (255, 182, 193)
POWER_RED = (178, 34, 34) # Horns
POWER_WHITE = (255, 250, 250)


def create_simple_character(surface, primary_color, secondary_color, skin_color, special_feature='none'):
    """간단한 캐릭터 스프라이트 생성"""
    # 머리
    pygame.draw.circle(surface, skin_color, (50, 30), 15)
    
    # 머리카락 (특징)
    if special_feature == 'spiky':  # Goku, Vegeta
        pygame.draw.polygon(surface, secondary_color, [(35, 25), (50, 10), (65, 25)])
        pygame.draw.polygon(surface, secondary_color, [(40, 30), (50, 15), (60, 30)])
    elif special_feature == 'hat':  # Luffy
        pygame.draw.circle(surface, secondary_color, (50, 25), 18, 3)
        pygame.draw.rect(surface, secondary_color, (32, 22, 36, 5))
    elif special_feature == 'bald':  # Saitama
        pygame.draw.circle(surface, skin_color, (50, 30), 16)
    elif special_feature == 'ponytail':  # Edward
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
        pygame.draw.circle(surface, secondary_color, (68, 35), 8)
    elif special_feature == 'split':  # Todoroki
        pygame.draw.circle(surface, (255, 255, 255), (40, 30), 15)
        pygame.draw.circle(surface, (255, 100, 100), (60, 30), 15)
    elif special_feature == 'short':  # Tanya
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
    elif special_feature == 'hood':  # Shadow
        pygame.draw.circle(surface, primary_color, (50, 30), 18)
        pygame.draw.rect(surface, primary_color, (35, 25, 30, 15))
    elif special_feature == 'helmet':  # Arena
        pygame.draw.circle(surface, primary_color, (50, 30), 16)
        pygame.draw.rect(surface, secondary_color, (42, 28, 16, 3))
    elif special_feature == 'messy':  # Eren
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
        pygame.draw.polygon(surface, secondary_color, [(40, 20), (50, 15), (60, 20)])
    elif special_feature == 'redblack':  # Tanjiro
        # 빨간 머리카락
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
        # 이마에 흉터 표시
        pygame.draw.rect(surface, (200, 0, 0), (48, 25, 4, 8))
    elif special_feature == 'chainsaw':  # Denji
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
        # 체인소 표시 (머리 위)
        pygame.draw.rect(surface, (150, 150, 150), (45, 15, 10, 5))
    elif special_feature == 'bamboo':  # Nezuko
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
        # 대나무 입마개
        pygame.draw.rect(surface, (139, 69, 19), (45, 35, 10, 5))
    elif special_feature == 'scarf':  # Mikasa
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
        # 빨간 스카프
        pygame.draw.rect(surface, (200, 0, 0), (40, 40, 20, 8))
    elif special_feature == 'horns':  # Power
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
        # 빨간 뿔
        pygame.draw.polygon(surface, (178, 34, 34), [(40, 20), (42, 5), (45, 20)])
        pygame.draw.polygon(surface, (178, 34, 34), [(60, 20), (58, 5), (55, 20)])
    elif special_feature == 'blindfold':  # Gojo
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
        # 안대
        pygame.draw.rect(surface, (20, 20, 20), (35, 25, 30, 8))
    else:  # Default hair
        pygame.draw.circle(surface, secondary_color, (50, 30), 15)
    
    # 몸통
    pygame.draw.rect(surface, primary_color, (35, 45, 30, 35))
    
    # 팔
    pygame.draw.rect(surface, primary_color, (25, 50, 10, 25))
    pygame.draw.rect(surface, primary_color, (65, 50, 10, 25))
    
    # 다리
    pygame.draw.rect(surface, primary_color, (35, 80, 12, 20))
    pygame.draw.rect(surface, primary_color, (53, 80, 12, 20))
    
    # 눈
    pygame.draw.circle(surface, (0, 0, 0), (45, 30), 2)
    pygame.draw.circle(surface, (0, 0, 0), (55, 30), 2)


def draw_naruto(surface, action, frame_idx):
    # 기존 나루토 그리기 함수 유지
    pygame.draw.rect(surface, NARUTO_ORANGE, (10, 30, 30, 40))
    pygame.draw.rect(surface, NARUTO_SKIN, (15, 15, 20, 15))
    pygame.draw.polygon(surface, NARUTO_YELLOW, [(10, 15), (25, 0), (40, 15), (45, 10), (25, 5), (5, 10)])
    pygame.draw.rect(surface, HEADBAND_BLUE, (15, 15, 20, 5))
    
    if action == 'idle':
        offset = 1 if frame_idx == 1 else 0
        pygame.draw.rect(surface, NARUTO_ORANGE, (10, 30 + offset, 30, 40))
        pygame.draw.rect(surface, NARUTO_ORANGE, (5, 30 + offset, 5, 35))
        pygame.draw.rect(surface, NARUTO_ORANGE, (40, 30 + offset, 5, 35))
        pygame.draw.rect(surface, NARUTO_ORANGE, (10, 70, 12, 25))
        pygame.draw.rect(surface, NARUTO_ORANGE, (28, 70, 12, 25))


def draw_ichigo(surface, action, frame_idx):
    # 기존 이치고 그리기 함수 유지
    pygame.draw.rect(surface, ICHIGO_BLACK, (10, 30, 30, 50))
    pygame.draw.line(surface, SWORD_WRAP, (10, 30), (40, 50), 2)
    pygame.draw.rect(surface, ICHIGO_SKIN, (15, 10, 20, 20))
    pygame.draw.polygon(surface, ICHIGO_ORANGE, [(10, 10), (25, 0), (40, 10), (42, 5), (25, 2), (8, 5)])
    
    if action == 'idle':
        offset = 1 if frame_idx == 1 else 0
        pygame.draw.polygon(surface, SWORD_GRAY, [(45, 20+offset), (45, 80+offset), (55, 75+offset), (55, 20+offset)])
        pygame.draw.rect(surface, ICHIGO_BLACK, (10, 80, 13, 20))
        pygame.draw.rect(surface, ICHIGO_BLACK, (27, 80, 13, 20))


def save_single_image(character_name, surface):
    """단일 캐릭터 이미지 저장"""
    path = f"game/images/{character_name}.png"
    if os.path.exists(path):
        print(f"Skipping {character_name}.png (already exists)")
        return
    pygame.image.save(surface, path)
    print(f"Saved {character_name}.png")


def save_support_image(character_name, surface):
    """보조 캐릭터 이미지 저장 (작은 크기)"""
    # 50x50으로 축소
    small_surface = pygame.transform.scale(surface, (50, 50))
    path = f"game/images/{character_name}.png"
    pygame.image.save(small_surface, path)
    print(f"Saved support character {character_name}.png")


def main():
    # 메인 캐릭터 생성 (100x100)
    
    # Goku
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, GOKU_ORANGE, GOKU_BLACK, GOKU_SKIN, 'spiky')
    save_single_image("goku", s)
    
    # Luffy
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, LUFFY_RED, LUFFY_BLUE, LUFFY_SKIN, 'hat')
    save_single_image("luffy", s)
    
    # Saitama
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, SAITAMA_YELLOW, SAITAMA_WHITE, SAITAMA_SKIN, 'bald')
    # 망토 추가
    pygame.draw.polygon(s, SAITAMA_WHITE, [(30, 50), (70, 50), (75, 95), (25, 95)])
    save_single_image("saitama", s)
    
    # Edward
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, EDWARD_RED, EDWARD_YELLOW, EDWARD_SKIN, 'ponytail')
    # 기계팔 표시
    pygame.draw.rect(s, EDWARD_METAL, (65, 50, 10, 25))
    save_single_image("edward", s)
    
    # Todoroki
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, TODOROKI_GRAY, TODOROKI_WHITE, TODOROKI_SKIN, 'split')
    save_single_image("todoroki", s)
    
    # Tanya
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, TANYA_BLUE, TANYA_YELLOW, TANYA_SKIN, 'short')
    save_single_image("tanya", s)
    
    # Arena (Original Character)
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, ARENA_PURPLE, ARENA_GOLD, ARENA_SKIN, 'helmet')
    # 갑옷 디테일
    pygame.draw.rect(s, ARENA_GOLD, (35, 45, 30, 5))
    pygame.draw.rect(s, ARENA_GOLD, (35, 60, 30, 3))
    save_single_image("arena", s)
    
    # Shadow (Original Character)
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, SHADOW_BLACK, SHADOW_GRAY, (100, 100, 100), 'hood')
    # 빨간 눈
    pygame.draw.circle(s, SHADOW_RED, (45, 30), 3)
    pygame.draw.circle(s, SHADOW_RED, (55, 30), 3)
    save_single_image("shadow", s)
    
    # NEW: Eren (Attack on Titan)
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, EREN_GREEN, EREN_BROWN, EREN_SKIN, 'messy')
    # 초록 망토
    pygame.draw.polygon(s, EREN_GREEN, [(30, 45), (70, 45), (75, 90), (25, 90)])
    save_single_image("eren", s)
    
    # NEW: Tanjiro (Demon Slayer)
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, TANJIRO_BLACK, TANJIRO_RED, TANJIRO_SKIN, 'redblack')
    # 녹색 체크무늬 하오리 (간단히 표현)
    pygame.draw.rect(s, TANJIRO_GREEN, (35, 45, 30, 35))
    pygame.draw.line(s, TANJIRO_BLACK, (35, 55), (65, 55), 2)
    pygame.draw.line(s, TANJIRO_BLACK, (35, 65), (65, 65), 2)
    save_single_image("tanjiro", s)
    
    # NEW: Denji (Chainsaw Man)
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, DENJI_WHITE, DENJI_YELLOW, DENJI_SKIN, 'chainsaw')
    save_single_image("denji", s)
    
    # --- 기존 보조 캐릭터들을 메인 크기로 생성 ---
    
    # Sasuke
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, SASUKE_BLUE, SASUKE_BLACK, SASUKE_SKIN, 'short')
    save_single_image("sasuke", s)
    
    # Inoue
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, INOUE_ORANGE, INOUE_ORANGE, INOUE_SKIN, 'short')
    save_single_image("inoue", s)
    
    # Vegeta
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, VEGETA_BLUE, VEGETA_BLACK, VEGETA_SKIN, 'spiky')
    save_single_image("vegeta", s)
    
    # Zoro
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, ZORO_GREEN, ZORO_GREEN, ZORO_SKIN, 'short')
    pygame.draw.line(s, (200, 200, 200), (20, 60), (20, 80), 2)
    save_single_image("zoro", s)
    
    # Sakura
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, SAKURA_PINK, SAKURA_BLONDE, SAKURA_SKIN, 'short')
    save_single_image("sakura", s)
    
    # Uraraka
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, URARAKA_BROWN, URARAKA_BROWN, URARAKA_SKIN, 'short')
    save_single_image("uraraka", s)
    
    # Nezuko
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, NEZUKO_PINK, NEZUKO_BLACK, NEZUKO_SKIN, 'bamboo')
    save_single_image("nezuko", s)
    
    # Mikasa
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, MIKASA_GRAY, MIKASA_BLACK, MIKASA_SKIN, 'scarf')
    save_single_image("mikasa", s)

    # --- 신규 캐릭터 생성 ---
    
    # Gon
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, GON_GREEN, GON_BLACK, SAITAMA_SKIN, 'spiky')
    save_single_image("gon", s)
    
    # Killua
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, KILLUA_WHITE, KILLUA_WHITE, SAITAMA_SKIN, 'spiky')
    save_single_image("killua", s)
    
    # Hisoka
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, HISOKA_PINK, HISOKA_PINK, SAITAMA_SKIN, 'messy')
    save_single_image("hisoka", s)
    
    # Itadori
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, ITADORI_BLACK, ITADORI_PINK, SAITAMA_SKIN, 'short')
    save_single_image("itadori", s)
    
    # Gojo
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, ITADORI_BLACK, GOJO_WHITE, SAITAMA_SKIN, 'blindfold')
    save_single_image("gojo", s)
    
    # Fushiguro
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, FUSHIGURO_BLUE, FUSHIGURO_BLACK, SAITAMA_SKIN, 'spiky')
    save_single_image("fushiguro", s)
    
    # Jotaro
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, JOTARO_BLUE, JOTARO_GOLD, SAITAMA_SKIN, 'hat')
    save_single_image("jotaro", s)
    
    # DIO
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, DIO_YELLOW, DIO_YELLOW, SAITAMA_SKIN, 'messy')
    save_single_image("dio", s)
    
    # Power
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, POWER_WHITE, POWER_PINK, SAITAMA_SKIN, 'horns')
    save_single_image("power", s)

    # 기본 나루토/이치고도 일반화된 이미지로 하나씩 생성 (백업용)
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, NARUTO_ORANGE, NARUTO_YELLOW, NARUTO_SKIN, 'short')
    save_single_image("naruto", s) 
    
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    create_simple_character(s, ICHIGO_BLACK, ICHIGO_ORANGE, ICHIGO_SKIN, 'spiky')
    save_single_image("ichigo", s)

    print("\n✅ All character images created successfully!")



if __name__ == "__main__":
    main()
