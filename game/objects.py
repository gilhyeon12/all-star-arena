import pygame
from .settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner):
        super().__init__()
        self.owner = owner
        self.damage = SKILL_DATA['U']['damage']
        self.direction = direction
        
        # 간단한 수리검 그리기 (나중에는 이미지로 대체 가능)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (50, 50, 50), (10, 10), 5) # 중심
        # 십자 모양
        pygame.draw.line(self.image, (200, 200, 200), (10, 0), (10, 20), 2)
        pygame.draw.line(self.image, (200, 200, 200), (0, 10), (20, 10), 2)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.speed = 15
        if direction == "left":
            self.speed = -15

    def update(self):
        self.rect.x += self.speed
        
        # 화면 밖으로 나가면 제거
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
