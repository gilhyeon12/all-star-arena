import pygame
import random
from game.settings import *

class Particle(pygame.sprite.Sprite):
    """
    스킬 이펙트나 타격 효과를 위한 파티클 클래스
    """
    def __init__(self, x, y, color, velocity_x, velocity_y, lifetime=30):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = lifetime
        self.age = 0

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.age += 1
        
        # 시간이 지날수록 투명해지거나 작아지는 효과 (여기서는 단순 제거)
        if self.age >= self.lifetime:
            self.kill()

class Afterimage(pygame.sprite.Sprite):
    """
    대쉬 잔상 효과
    """
    def __init__(self, x, y, image, lifetime=15):
        super().__init__()
        self.image = image.copy()
        self.image.set_alpha(128) # 반투명
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lifetime = lifetime
        self.age = 0

    def update(self):
        self.age += 1
        if self.age >= self.lifetime:
            self.kill()
        else:
             # 점점 흐려짐
             alpha = 128 * (1 - self.age / self.lifetime)
             self.image.set_alpha(int(alpha))

class EffectManager:
    """
    파티클 생성 및 관리를 담당하는 클래스
    """
    def __init__(self):
        self.particles = pygame.sprite.Group()

    def create_attack_effect(self, x, y, color):
        """공격 시 파티클 폭발 효과"""
        for _ in range(10): # 파티클 10개 생성
            vx = random.uniform(-3, 3)
            vy = random.uniform(-3, 3)
            particle = Particle(x, y, color, vx, vy, random.randint(20, 40))
            self.particles.add(particle)

    def create_hit_effect(self, x, y):
        """피격 시 빨간 파티클 효과"""
        for _ in range(15):
            vx = random.uniform(-5, 5)
            vy = random.uniform(-5, 5)
            particle = Particle(x, y, RED, vx, vy, 20)
            self.particles.add(particle)

    def create_afterimage(self, x, y, image):
        """대쉬 잔상 생성"""
        afterimage = Afterimage(x, y, image)
        self.particles.add(afterimage)

    def create_effect(self, x, y, effect_type, color=None):
        """다양한 이펙트 생성 (smoke, block, skill_cast 등)"""
        if effect_type == "smoke":
            # 연기 이펙트 (회색)
            for _ in range(20):
                vx = random.uniform(-2, 2)
                vy = random.uniform(-2, 2)
                c = (150, 150, 150) # Gray
                particle = Particle(x, y, c, vx, vy, random.randint(30, 50))
                self.particles.add(particle)
        elif effect_type == "block":
            # 막기/변신 이펙트 (노란색/하얀색 섬광)
            for _ in range(20):
                vx = random.uniform(-4, 4)
                vy = random.uniform(-4, 4)
                c = (255, 255, 200) # Pale Yellow
                particle = Particle(x, y, c, vx, vy, random.randint(20, 40))
                self.particles.add(particle)
        elif effect_type == "charge":
             # 기 모으기 (위로 솟구치는 파티클)
             c = color if color else (255, 255, 0)
             for _ in range(5):
                 vx = random.uniform(-1, 1)
                 vy = random.uniform(-5, -1)
                 particle = Particle(x + random.randint(-20, 20), y + 40, c, vx, vy, random.randint(20, 40))
                 self.particles.add(particle)
        else:
            # Fallback to unique interpreter if generic type not found
            self.create_unique_effect(x, y, effect_type)

    def create_unique_effect(self, x, y, effect_name, direction="right"):
        """스킬별 고유 이펙트 생성 로직"""
        
        # 1. Color Parsing
        c = WHITE
        if "blue" in effect_name: c = (0, 191, 255)
        elif "red" in effect_name: c = RED
        elif "green" in effect_name: c = GREEN
        elif "gold" in effect_name or "yellow" in effect_name: c = (255, 215, 0)
        elif "black" in effect_name: c = (30, 30, 30)
        elif "pink" in effect_name: c = (255, 105, 180)
        elif "orange" in effect_name: c = ORANGE
        elif "purple" in effect_name: c = (128, 0, 128)
        
        # 2. Pattern Matching
        if "spiral" in effect_name:
            # 나선형 (Rasengan)
            for i in range(30):
                vx = random.uniform(-5, 5)
                vy = random.uniform(-5, 5)
                particle = Particle(x, y, c, vx, vy, 20)
                self.particles.add(particle)
                
        elif "lightning" in effect_name:
            # 번개 (Chidori) - 빠르고 불규칙
            for i in range(20):
                vx = random.uniform(-10, 10)
                vy = random.uniform(-10, 10)
                p = Particle(x, y, (200, 200, 255), vx, vy, 10)
                self.particles.add(p)

        elif "fire" in effect_name or "explosion" in effect_name:
            # 화염/폭발
            count = 50 if "big" in effect_name else 20
            color_fire = RED if "red" in effect_name else ORANGE
            for i in range(count):
                vx = random.uniform(-6, 6)
                vy = random.uniform(-6, 6)
                p = Particle(x, y, color_fire, vx, vy, 40)
                self.particles.add(p)

        elif "slash" in effect_name:
            # 참격 (방향성)
            dir_mod = 1 if direction == "right" else -1
            for i in range(20):
                vx = random.uniform(2, 10) * dir_mod
                vy = random.uniform(-5, 5)
                p = Particle(x, y, c, vx, vy, 15)
                self.particles.add(p)

        elif "beam" in effect_name or "orb" in effect_name:
            # 빔/구체 (모이는 느낌 or 쏘는 느낌)
            for i in range(30):
                vx = random.uniform(-2, 2)
                vy = random.uniform(-2, 2)
                p = Particle(x + random.randint(-20, 20), y + random.randint(-20, 20), c, vx, vy, 30)
                self.particles.add(p)
        
        elif "heal" in effect_name or "aura" in effect_name:
             # 치유/오라 (위로 천천히)
            for i in range(20):
                vx = random.uniform(-1, 1)
                vy = random.uniform(-3, -1)
                p = Particle(x + random.randint(-20, 20), y + 20, GREEN if "heal" in effect_name else c, vx, vy, 60)
                self.particles.add(p)
                
        else:
            # Default Impact
            for i in range(10):
                vx = random.uniform(-3, 3)
                vy = random.uniform(-3, 3)
                p = Particle(x, y, c, vx, vy, 20)
                self.particles.add(p)

    def update(self):
        self.particles.update()

    def draw(self, screen):
        self.particles.draw(screen)
