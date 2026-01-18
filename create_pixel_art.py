import pygame
import os

# 초기화
pygame.init()

# 색상 정의
TRANSPARENT = (0, 0, 0, 0)
NARUTO_ORANGE = (255, 140, 0)
NARUTO_YELLOW = (255, 215, 0)
NARUTO_SKIN = (255, 220, 177)
HEADBAND_BLUE = (0, 0, 139)
HEADBAND_METAL = (192, 192, 192)

ICHIGO_BLACK = (20, 20, 20)
ICHIGO_ORANGE = (255, 120, 0)
ICHIGO_SKIN = (255, 227, 208)
SWORD_GRAY = (200, 200, 200)
SWORD_WRAP = (240, 240, 240)

def draw_naruto(surface, action, frame_idx):
    # 50x100 크기
    # 기본 몸체
    pygame.draw.rect(surface, NARUTO_ORANGE, (10, 30, 30, 40)) # 몸통
    pygame.draw.rect(surface, NARUTO_SKIN, (15, 15, 20, 15)) # 얼굴
    pygame.draw.polygon(surface, NARUTO_YELLOW, [(10, 15), (25, 0), (40, 15), (45, 10), (25, 5), (5, 10)]) # 머리
    pygame.draw.rect(surface, HEADBAND_BLUE, (15, 15, 20, 5)) # 서클렛
    
    # 동작별 변화
    if action == 'idle':
        # 숨쉬기: 상체가 살짝 움직임
        offset = 1 if frame_idx == 1 else 0
        pygame.draw.rect(surface, NARUTO_ORANGE, (10, 30 + offset, 30, 40))
        # 팔 (기본)
        pygame.draw.rect(surface, NARUTO_ORANGE, (5, 30 + offset, 5, 35))
        pygame.draw.rect(surface, NARUTO_ORANGE, (40, 30 + offset, 5, 35))
        # 다리
        pygame.draw.rect(surface, NARUTO_ORANGE, (10, 70, 12, 25))
        pygame.draw.rect(surface, NARUTO_ORANGE, (28, 70, 12, 25))
        
    elif action == 'walk':
        # 걷기: 다리 교차
        leg_offset = 5 if frame_idx == 0 else -5
        pygame.draw.rect(surface, NARUTO_ORANGE, (10, 70 + leg_offset, 12, 25))
        pygame.draw.rect(surface, NARUTO_ORANGE, (28, 70 - leg_offset, 12, 25))
        # 팔 흔들기
        pygame.draw.rect(surface, NARUTO_ORANGE, (5, 30 - leg_offset, 5, 35))
        pygame.draw.rect(surface, NARUTO_ORANGE, (40, 30 + leg_offset, 5, 35))
        
    elif action == 'run': # 대쉬
        # 앞으로 기울임
        pygame.draw.polygon(surface, NARUTO_ORANGE, [(15, 35), (45, 35), (35, 75), (5, 75)])
        # 다리 벌림
        pygame.draw.rect(surface, NARUTO_ORANGE, (5, 75, 15, 20))
        pygame.draw.rect(surface, NARUTO_ORANGE, (30, 75, 15, 20))
        # 팔 뒤로
        pygame.draw.rect(surface, NARUTO_ORANGE, (0, 35, 10, 30))
        
    elif action == 'attack':
        # 주먹 지르기
        pygame.draw.rect(surface, NARUTO_ORANGE, (10, 30, 30, 40))
        # 뻗은 팔
        pygame.draw.rect(surface, NARUTO_ORANGE, (40, 35, 25, 10)) # 길게 뻗음
        pygame.draw.rect(surface, NARUTO_SKIN, (65, 35, 10, 10)) # 주먹
        # 다리 기마자세
        pygame.draw.rect(surface, NARUTO_ORANGE, (5, 75, 15, 20))
        pygame.draw.rect(surface, NARUTO_ORANGE, (35, 75, 15, 20))
        
    elif action == 'guard':
        # 팔로 막기
        pygame.draw.rect(surface, NARUTO_ORANGE, (20, 35, 10, 30)) # 팔을 몸통 앞에
        pygame.draw.rect(surface, HEADBAND_METAL, (22, 38, 5, 20)) # 건틀릿 느낌
        
    elif action == 'jump':
        # 다리 굽힘
        pygame.draw.rect(surface, NARUTO_ORANGE, (10, 70, 12, 15))
        pygame.draw.rect(surface, NARUTO_ORANGE, (28, 70, 12, 15))
        # 팔 만세
        pygame.draw.rect(surface, NARUTO_ORANGE, (5, 15, 5, 35))
        pygame.draw.rect(surface, NARUTO_ORANGE, (40, 15, 5, 35))

    elif action == 'hit':
        # 뒤로 젖혀짐
        pygame.draw.polygon(surface, NARUTO_ORANGE, [(5, 30), (35, 30), (40, 70), (10, 70)])
        # 아픈 표정 (빨간 얼굴)
        pygame.draw.rect(surface, (255, 100, 100), (10, 15, 20, 15))

def draw_ichigo(surface, action, frame_idx):
    # 기본 몸체
    pygame.draw.rect(surface, ICHIGO_BLACK, (10, 30, 30, 50)) # 몸통
    pygame.draw.line(surface, SWORD_WRAP, (10, 30), (40, 50), 2) # 띠
    pygame.draw.rect(surface, ICHIGO_SKIN, (15, 10, 20, 20)) # 얼굴
    pygame.draw.polygon(surface, ICHIGO_ORANGE, [(10, 10), (25, 0), (40, 10), (42, 5), (25, 2), (8, 5)]) # 머리
    
    if action == 'idle':
        offset = 1 if frame_idx == 1 else 0
        # 대검 등 뒤에
        pygame.draw.polygon(surface, SWORD_GRAY, [(45, 20+offset), (45, 80+offset), (55, 75+offset), (55, 20+offset)])
        # 다리
        pygame.draw.rect(surface, ICHIGO_BLACK, (10, 80, 13, 20))
        pygame.draw.rect(surface, ICHIGO_BLACK, (27, 80, 13, 20))
        
    elif action == 'walk':
        leg_offset = 5 if frame_idx == 0 else -5
        pygame.draw.rect(surface, ICHIGO_BLACK, (10, 80 + leg_offset, 13, 20))
        pygame.draw.rect(surface, ICHIGO_BLACK, (27, 80 - leg_offset, 13, 20))
        # 대검 흔들림
        pygame.draw.polygon(surface, SWORD_GRAY, [(45, 20+leg_offset), (45, 80+leg_offset), (55, 75+leg_offset), (55, 20+leg_offset)])

    elif action == 'run':
        # 앞으로 숙임
        pygame.draw.polygon(surface, ICHIGO_BLACK, [(15, 35), (45, 35), (35, 80), (5, 80)])
        # 대검 수평
        pygame.draw.rect(surface, SWORD_GRAY, (0, 45, 60, 10))
        
    elif action == 'attack':
        # 대검 휘드르기 (앞으로)
        pygame.draw.rect(surface, SWORD_GRAY, (40, 40, 50, 15)) # 칼날
        pygame.draw.rect(surface, ICHIGO_BLACK, (30, 40, 10, 5)) # 팔
        
    elif action == 'guard':
        # 대검으로 막기 (앞에 세움)
        pygame.draw.rect(surface, SWORD_GRAY, (35, 20, 10, 70))
        
    elif action == 'jump':
        pygame.draw.rect(surface, ICHIGO_BLACK, (10, 70, 13, 10))
        pygame.draw.rect(surface, ICHIGO_BLACK, (27, 70, 13, 10))
        # 대검 위로
        pygame.draw.rect(surface, SWORD_GRAY, (50, 0, 10, 60))

    elif action == 'hit':
        pygame.draw.polygon(surface, ICHIGO_BLACK, [(5, 30), (35, 30), (40, 70), (10, 70)])
        pygame.draw.rect(surface, (255, 100, 100), (10, 15, 20, 15))


def save_frames(character_name, action, frames):
    path = f"game/images/{character_name}_{action}"
    if not os.path.exists(path):
        os.makedirs(path) # 폴더 생성
        
    for i, surface in enumerate(frames):
        pygame.image.save(surface, f"{path}/{i}.png")
    print(f"Saved {len(frames)} frames for {character_name} {action}")

def main():
    actions = ['idle', 'walk', 'run', 'attack', 'guard', 'jump', 'hit']
    
    # Naruto
    for action in actions:
        frames = []
        count = 2 if action in ['idle', 'walk'] else 1
        for i in range(count):
            s = pygame.Surface((100, 100), pygame.SRCALPHA) # 여유 있게 100x100
            # 중심 잡기 위해 오프셋 조정 가능하지만 여기선 단순화
            draw_naruto(s, action, i)
            frames.append(s)
        save_frames("naruto", action, frames)

    # Ichigo
    for action in actions:
        frames = []
        count = 2 if action in ['idle', 'walk'] else 1
        for i in range(count):
            s = pygame.Surface((100, 100), pygame.SRCALPHA)
            draw_ichigo(s, action, i)
            frames.append(s)
        save_frames("ichigo", action, frames)

if __name__ == "__main__":
    main()
