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

    def update(self):
        self.particles.update()

    def draw(self, screen):
        self.particles.draw(screen)
