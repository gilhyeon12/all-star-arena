import pygame
import random
from .settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner, effect_type=None, effect_manager=None):
        super().__init__()
        self.owner = owner
        char_skill_data = SKILL_DATA.get(owner.name, {})
        skill_info = char_skill_data.get('U', DEFAULT_SKILLS['U'])
        self.damage = skill_info['damage']
        self.direction = direction
        self.power = self.damage # 클래시 승패 판정용
        
        # 시리즈별 색상 적용
        self.color = (200, 200, 200)
        for s, chars in SERIES_DATA.items():
            check_name = owner.original_name if hasattr(owner, 'original_name') else owner.name
            if check_name in chars:
                self.color = SERIES_COLORS.get(s, (200, 200, 200))
                break

        # 투사체 이미지 생성 (원형 + 꼬리 효과)
        self.image = pygame.Surface((40, 20), pygame.SRCALPHA)
        # 빛나는 코어
        pygame.draw.circle(self.image, (255, 255, 255), (20, 10), 8)
        # 외곽선 (테마 색상)
        pygame.draw.circle(self.image, self.color, (20, 10), 10, 2)
        
        # 꼬리 (방향에 따라)
        if direction == "right":
             pygame.draw.line(self.image, self.color, (0, 10), (15, 10), 3)
        else:
             pygame.draw.line(self.image, self.color, (25, 10), (40, 10), 3)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.speed = 15
        if direction == "left":
            self.speed = -15
            
        self.effect_type = effect_type
        self.effect_manager = effect_manager
        
        # Custom Visuals based on effect_type
        if self.effect_type == "spiral_blue":
             self.image.fill((0,0,0,0)) # Clear
             pygame.draw.circle(self.image, (0, 191, 255), (20, 10), 12, 2) # Outer ring
             pygame.draw.circle(self.image, (135, 206, 250), (20, 10), 8) # Inner
             pygame.draw.circle(self.image, (255, 255, 255), (20, 10), 4) # Core
             self.color = (0, 191, 255)

    def update(self):
        self.rect.x += self.speed
        
        # 화면 밖으로 나가면 제거
        # 화면 밖으로 나가면 제거
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        # Trail Effect
        if self.effect_type and self.effect_manager:
             if random.random() < 0.5: # 50% chance per frame
                 self.effect_manager.create_effect(self.rect.centerx, self.rect.centery, "charge", self.color)

class EnergyClash(pygame.sprite.Sprite):
    """
    두 투사체가 충돌했을 때 생성되는 에너지 클래시(힘겨루기) 객체
    """
    def __init__(self, p1_proj, p2_proj):
        super().__init__()
        self.p1_proj = p1_proj
        self.p2_proj = p2_proj
        
        # 초기 위치는 두 투사체의 중간
        center_x = (p1_proj.rect.centerx + p2_proj.rect.centerx) // 2
        center_y = (p1_proj.rect.centery + p2_proj.rect.centery) // 2
        
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        
        self.power_p1 = 50 # 초기 파워
        self.power_p2 = 50
        self.winner = None
        self.timer = 0
        
    def update(self):
        self.timer += 1
        
        # 힘의 균형에 따라 위치 이동
        balance = self.power_p1 - self.power_p2 # 양수면 P1 우세(오른쪽으로 밈), 음수면 P2 우세
        move_speed = balance * 0.1
        self.rect.x += move_speed
        
        # 시각 효과 (진동 및 크기 변화)
        self.image.fill((0,0,0,0)) # Clear
        
        # P1 색상 원 (왼쪽)
        radius_p1 = 30 + (self.power_p1 / 5) + random.randint(-2, 2)
        pygame.draw.circle(self.image, self.p1_proj.color, (50 - 10, 50), int(radius_p1))
        
        # P2 색상 원 (오른쪽)
        radius_p2 = 30 + (self.power_p2 / 5) + random.randint(-2, 2)
        pygame.draw.circle(self.image, self.p2_proj.color, (50 + 10, 50), int(radius_p2))
        
        # 중앙 충돌 빛
        pygame.draw.circle(self.image, (255, 255, 255), (50, 50), 20 + random.randint(-5, 5))
        
        # 승패 판정 (화면 끝에 도달하거나 파워 차이가 압도적일 때)
        if self.rect.right > SCREEN_WIDTH - 50: # P1 승리
             self.winner = 1
             self.kill()
        elif self.rect.left < 50: # P2 승리
             self.winner = 2
             self.kill()
        elif abs(self.power_p1 - self.power_p2) > 100: # 압도적 차이
             self.winner = 1 if self.power_p1 > self.power_p2 else 2
             self.kill()

    def push(self, player_num):
        """플레이어 연타 입력 처리"""
        if player_num == 1:
            self.power_p1 += 2
        else:
            self.power_p2 += 2
