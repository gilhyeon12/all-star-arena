import pygame
import random
from game.settings import *
from game.characters import Character

class SupportCharacter(Character):
    """
    보조 캐릭터 클래스
    소환 시 나타나 스킬을 사용하고 사라집니다.
    """
    def __init__(self, owner, image_path, name):
        # 위치는 주인 옆
        start_x = owner.rect.centerx - 50 if owner.direction == "right" else owner.rect.centerx + 50
        super().__init__(start_x, owner.rect.y, image_path, name, sound_manager=getattr(owner, 'sound_manager', None))
        
        # 크기 조정
        self.image = pygame.transform.scale(self.image, (SUPPORT_CHARACTER_WIDTH, SUPPORT_CHARACTER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, owner.rect.centery)
        
        self.owner = owner
        self.hp = 999 
        self.max_hp = 999
        self.damage_multiplier = 1.0
        
        # 수명 (프레임 단위)
        self.lifetime = 120 
        
        # 이름에 따른 타입 및 스킬 자동 발동
        if name in ["Sasuke", "Vegeta", "Zoro"]:
            self.type = "offensive"
        elif name in ["Inoue", "Sakura"]:
            self.type = "healer"
        else: # Uraraka, Nezuko, Mikasa
            self.type = "balance"
            
        # 소환되자마자 스킬 실행
        self.trigger_skill()

    def update_ai(self, enemy):
        """소환된 보조 캐릭터는 별도의 AI 업데이트가 필요 없음"""
        pass

    def trigger_skill(self):
        """소환 시 즉시 발동하는 스킬"""
        if self.type == "offensive":
            self.dash()
            self.attack('J')
        elif self.type == "healer":
            self.heal_owner()
        elif self.type == "balance":
            self.attack('J')
            self.owner.hp = min(self.owner.max_hp, self.owner.hp + 5)
                 
    def heal_owner(self):
        """주인 체력 회복"""
        heal_amount = 20
        self.owner.hp = min(self.owner.max_hp, self.owner.hp + heal_amount)

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            return

        super().update()
        
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
