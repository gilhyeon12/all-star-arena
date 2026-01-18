import pygame
import os
from .settings import *

class Character(pygame.sprite.Sprite):
    """
    게임 등장 캐릭터를 정의하는 기본 클래스입니다.
    """
    def __init__(self, x, y, image_path, name):
        """
        초기화 함수
        
        Args:
            x: 초기 X 위치
            y: 초기 Y 위치
            image_path: 캐릭터 이미지 파일 경로
            name: 캐릭터 이름
        """
        super().__init__()
        self.name = name
        self.animations = {}
        self.load_animations(name)
        
        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        
        # 초기 이미지 설정
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # 기존 속성 유지
        self.hp = 100
        self.max_hp = 100
        self.mana = 50 # Start with 50 MP
        self.max_mana = 100
        self.mana_regen = 0.05 # Changed from MANA_REGEN constant
        
        self.change_x = 0
        self.change_y = 0
        self.direction = "right" 
        
        # 전투 관련
        self.attack_cooldown = 0
        self.is_attacking = False
        self.attack_rect = None
        self.current_damage = 0
        
        self.is_guarding = False
        self.is_dashing = False
        self.is_guarding = False
        self.is_dashing = False
        self.dash_timer = 0
        
        self.attack_timer = 0 # 공격 애니메이션 지속 시간
        self.last_skill_used = None # 메인 루프 통신용
        
        # Removed: self.controls = {}

    def load_animations(self, name):
        """캐릭터별 애니메이션 로드"""
        actions = ['idle', 'walk', 'run', 'attack', 'guard', 'jump', 'hit']
        base_path = "game/images"
        
        for action in actions:
            path = f"{base_path}/{name.lower()}_{action}"
            animation_list = []
            if os.path.exists(path):
                file_count = len(os.listdir(path))
                for i in range(file_count):
                    img_path = f"{path}/{i}.png"
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
                    animation_list.append(img)
            else:
                # 폴더 없으면 기본 이미지(또는 에러 방지용) 사용
                # Fallback to a single image if animation folder doesn't exist
                default_img_path = f"{base_path}/{name.lower()}.png"
                if os.path.exists(default_img_path):
                    default_img = pygame.image.load(default_img_path).convert_alpha()
                    default_img = pygame.transform.scale(default_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
                    animation_list.append(default_img)
                else:
                    # If even the default single image doesn't exist, create a placeholder
                    print(f"Warning: No animation or default image found for {name} {action}. Creating placeholder.")
                    placeholder_img = pygame.Surface((CHARACTER_WIDTH, CHARACTER_HEIGHT), pygame.SRCALPHA)
                    placeholder_img.fill((100, 100, 100, 150)) # Semi-transparent gray
                    animation_list.append(placeholder_img)
            
            self.animations[action] = animation_list

    def update_animation(self):
        """상태에 따른 애니메이션 프레임 업데이트"""
        animation_list = self.animations.get(self.state, self.animations['idle']) # Fallback to idle if state not found
        
        # 애니메이션 속도 조절
        now = pygame.time.get_ticks()
        if now - self.last_update > 150: # 150ms 마다 프레임 변경
            self.last_update = now
            self.frame_index += 1
            if self.frame_index >= len(animation_list):
                 self.frame_index = 0
        
        # 이미지 변경
        try:
             image = animation_list[self.frame_index]
        except IndexError:
             self.frame_index = 0
             image = animation_list[0]
             
        if self.direction == "left":
            self.image = pygame.transform.flip(image, True, False)
        else:
            self.image = image

    def update(self):
        """
        캐릭터의 상태를 업데이트하는 함수입니다.
        중력 적용, 이동, 공격 쿨타임 등을 처리합니다.
        """
        # 중력 적용
        self.calc_grav()
        
        # 좌우 이동
        self.rect.x += self.change_x
        
        # 이동 방향에 따라 보는 방향 업데이트 (only if moving)
        if self.change_x > 0:
            self.direction = "right"
        elif self.change_x < 0:
            self.direction = "left"
        
        # 화면 경계 체크
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.y += self.change_y

        # 바닥 충돌 체크
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.change_y = 0
            self.is_jumping = False # Reset jump state when on ground

        # 쿨타임 감소
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # 마나 자동 회복
        if self.mana < self.max_mana:
            self.mana += self.mana_regen
            if self.mana > self.max_mana:
                self.mana = self.max_mana
        
        # 대쉬 타이머
        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_timer == 0:
                self.is_dashing = False
                self.change_x = 0 # Stop horizontal movement after dash
        
        # 공격 타이머 (애니메이션 지속 시간)
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.is_attacking = False
                self.attack_rect = None
             
        # 상태 업데이트 (애니메이션용)
        self.update_state()
        self.update_animation()

    def update_state(self):
        """현재 행동에 따라 상태 결정"""
        if self.is_attacking:
            self.state = "attack"
        elif self.is_guarding:
            self.state = "guard"
        elif self.is_dashing:
            self.state = "run" # Dash might use run animation or a dedicated dash animation
        elif self.change_y != 0: # If moving vertically, assume jumping/falling
            self.state = "jump"
        elif self.change_x != 0: # If moving horizontally
            self.state = "walk"
        else:
            self.state = "idle"

    def calc_grav(self):
        """
        중력을 계산하여 Y축 이동 속도에 더합니다.
        """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY
            
        # 바닥에 있을 경우 미세한 떨림 방지
        if self.rect.bottom >= SCREEN_HEIGHT - 50 and self.change_y >= 0:
            self.change_y = 0
            self.rect.bottom = SCREEN_HEIGHT - 50

    def jump(self):
        """점프"""
        if not self.is_jumping and not self.is_dashing:
            self.change_y = -JUMP_HEIGHT
            self.is_jumping = True

    def guard(self, active):
        """방어 상태 설정"""
        self.is_guarding = active

    def dash(self):
        """대쉬"""
        if not self.is_dashing and self.mana >= SKILL_DATA['DASH']['mana']:
            self.mana -= SKILL_DATA['DASH']['mana']
            self.is_dashing = True
            self.dash_timer = DASH_DURATION
            # 바라보는 방향으로 빠르게 이동
            speed = DASH_SPEED if self.direction == "right" else -DASH_SPEED
            self.change_x = speed

    def attack(self, skill_key):
        """
        공격 함수 (스킬 시스템)
        Args:
            skill_key: 사용된 스킬 키 식별자
        """
        # 데이터 가져오기 (없는 키면 기본 공격 처리)
        skill_info = SKILL_DATA.get(skill_key, SKILL_DATA['J']) 
        
        if self.attack_cooldown == 0 and self.mana >= skill_info['mana']:
            self.is_attacking = True
            self.attack_cooldown = skill_info['cooldown']
            self.mana -= skill_info['mana']
            self.current_damage = skill_info['damage']
            
            # 공격 애니메이션 시간 설정 (기본 20프레임)
            self.attack_timer = 20
            
            skill_type = skill_info.get('type', 'basic')
            
            print(f"{self.name} used {skill_key} ({skill_type})")

            # 1. 투사체 (수리검)
            if skill_type == 'projectile':
                # 투사체 생성은 메인 루프에서 처리하기 위해 이벤트를 반환하거나 
                # 여기서 직접 생성하려면 main에서 sprite group을 인자로 받아야 함.
                # 구조상 여기서는 플래그/속성만 설정하고 Main에서 감지하는 게 깔끔함.
                self.last_skill_used = 'projectile' 
                
            # 2. 소환 (분신술)
            elif skill_type == 'summon':
                self.last_skill_used = 'summon'
                
            # 3. 돌진 공격 (나선환)
            elif skill_type == 'dash_attack':
                self.is_dashing = True # 돌진 상태
                self.dash_timer = 20 # 돌진 시간
                self.current_damage = skill_info['damage'] # 높은 데미지 설정
                # 돌진 속도 증가
                speed = DASH_SPEED * 1.5 if self.direction == "right" else -DASH_SPEED * 1.5
                self.change_x = speed
                
                # 나선환 이펙트는 Main에서 처리
                
            # 4. 일반 근접 공격
            else:
                # 공격 범위 설정
                attack_width = ATTACK_RANGE
                
                # 스킬별 범위 조절 (예시)
                if skill_info['damage'] >= 40: # 필살기
                    attack_width = ATTACK_RANGE * 2.5
                elif skill_info['damage'] >= 25: # 중급 스킬
                    attack_width = ATTACK_RANGE * 1.5
    
                if self.direction == "right":
                    self.attack_rect = pygame.Rect(self.rect.right, self.rect.y, attack_width, CHARACTER_HEIGHT)
                else:
                    self.attack_rect = pygame.Rect(self.rect.left - attack_width, self.rect.y, attack_width, CHARACTER_HEIGHT)

    def move_left(self):
        """왼쪽으로 이동"""
        self.change_x = -CHARACTER_SPEED

    def move_right(self):
        """오른쪽으로 이동"""
        self.change_x = CHARACTER_SPEED

    def stop(self):
        """이동 멈춤"""
        self.change_x = 0
        
    def take_damage(self, damage=10):
        """
        피격 처리
        Args:
            damage: 입을 데미지 (기본값 10, 이제는 외부에서 전달받음)
        """
        final_damage = damage
        
        # 방어 중이면 데미지 감소
        if self.is_guarding:
            final_damage = int(damage * 0.2) # 80% 감소
            print(f"{self.name} Blocked! ({damage} -> {final_damage})")
            
        self.hp -= final_damage
        if self.hp < 0:
            self.hp = 0
            
        # 넉백 (방어 중이면 넉백 없음)
        if not self.is_guarding:
            if self.direction == "right": # 맞았을 때 뒤로 밀림
               self.rect.x -= KNOCKBACK_FORCE
            else:
               self.rect.x += KNOCKBACK_FORCE * 2
