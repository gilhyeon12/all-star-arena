import pygame
import os
from .settings import *

class Character(pygame.sprite.Sprite):
    """
    게임 등장 캐릭터를 정의하는 기본 클래스입니다.
    """
    def __init__(self, x, y, image_path, name, sound_manager=None):
        """
        초기화 함수
        
        Args:
            x: 초기 X 위치
            y: 초기 Y 위치
            image_path: 캐릭터 이미지 파일 경로
            name: 캐릭터 이름
            sound_manager: 사운드 관리자 인스턴스 (Optional)
        """
        super().__init__()
        self.name = name
        self.sound_manager = sound_manager
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
        self.hp = 100
        self.max_hp = 100
        self.ki = 0 # Start with 0 Ki
        self.max_ki = MAX_KI
        self.ki_regen = KI_REGEN 
        
        self.guard_gauge = MAX_GUARD_GAUGE
        self.max_guard_gauge = MAX_GUARD_GAUGE
        self.guard_regen = GUARD_REGEN
        
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
        self.is_pushing = False # 가드 푸시 상태
        
        self.is_transformed = False # 변신 상태
        self.original_name = name
        self.is_temporary = False # 일시적 소환 여부 (합동 공격용)
        
        self.dash_timer = 0
        
        self.attack_timer = 0 # 공격 애니메이션 지속 시간
        self.last_skill_used = None # 메인 루프 통신용
        self.attack_timer = 0 # 공격 애니메이션 지속 시간
        self.last_skill_used = None # 메인 루프 통신용
        self.support_cooldown = 0 # 보조 캐릭터 쿨타임
        
        self.jump_count = 0 # 점프 횟수 (이중 점프용)
        self.invincible_timer = 0 # 무적 시간 타이머
        self.hit_stun = 0 # 피격 경직 타이머
        self.combo_count = 0 # 콤보 카운트
        
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
        # 방어 중일 때는 'idle' 모션 사용 (쉴드 안에서 가만히 서 있기)
        state_to_use = "idle" if self.state == "guard" else self.state
        animation_list = self.animations.get(state_to_use, self.animations['idle']) # Fallback to idle if state not found
        
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

        # [NEW] 공격 모션 처리 (Procedural Animation)
        # 이미지가 별도로 없는 경우, 기존 이미지를 회전/이동시켜 타격감 표현
        if self.is_attacking and self.attack_timer > 0:
            # simple lunge & rotate
            # 1. Rotate
            # 공격 진행도에 따라 각도 변화 (0 -> -30 -> 0)
            angle = 0
            if self.attack_timer > 10: # 초기
                 angle = -15 if self.direction == "right" else 15
            elif self.attack_timer > 5: # 중반 (타격)
                 angle = -45 if self.direction == "right" else 45
            
            if angle != 0:
                image = pygame.transform.rotate(image, angle)
            
            if angle != 0:
                image = pygame.transform.rotate(image, angle)
            
        # [NEW] 피격 모션
        if self.hit_stun > 0:
             # 피격 애니메이션이 있다면 그것을 사용, 없다면 깜빡임이나 색상 변경
             hit_anim = self.animations.get('hit', None)
             if hit_anim:
                 # 프레임 고정 (첫 프레임) 또는 반복
                 image = hit_anim[0]
                 # 방향에 따라 플립은 아래에서 처리됨

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
        
        # [NEW] Hit Stun Freeze
        if self.hit_stun > 0:
            self.change_x = 0
        
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
            self.jump_count = 0 # Reset jump count on ground

        # 쿨타임 감소
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        if self.hit_stun > 0:
            self.hit_stun -= 1
            if self.hit_stun <= 0:
                self.is_attacking = False # 피격 시 공격 캔슬 (확실히)
        
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            # 깜빡임 효과 (선택 사항)
            if self.invincible_timer % 4 < 2:
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)
        else:
             self.image.set_alpha(255) # 복구
        
        if self.ki < self.max_ki:
            self.ki += self.ki_regen
            if self.ki > self.max_ki:
                self.ki = self.max_ki
        
        # 보조 캐릭터 쿨타임 감소
        if self.support_cooldown > 0:
            self.support_cooldown -= 1
        
        # 방어 게이지 회복 및 관리
        if not self.is_guarding:
            if self.guard_gauge < self.max_guard_gauge:
                self.guard_gauge += self.guard_regen
                if self.guard_gauge > self.max_guard_gauge:
                    self.guard_gauge = self.max_guard_gauge
        elif self.guard_gauge <= 0:
            # 게이지 소진 시 방어 강제 해제
            self.is_guarding = False
            print(f"{self.name} Guard Broken!")
        
        # 대쉬 타이머
        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_timer == 0:
                self.is_dashing = False
                self.is_pushing = False # 리셋
                self.change_x = 0 # Stop horizontal movement after dash
        
        # 공격 타이머 (애니메이션 지속 시간)
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.is_attacking = False
                self.attack_rect = None
                # 일시적 소환 캐릭터는 공격 후 사라짐
                if self.is_temporary:
                    self.kill()
                    print(f"{self.name} (Support) finished attack and left.")
             
        # 상태 업데이트 (애니메이션용)
        self.update_state()
        self.update_animation()

    def update_state(self):
        """현재 행동에 따라 상태 결정"""
        if self.hit_stun > 0:
            self.state = "hit"
        elif self.is_attacking:
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

    def jump(self, can_double_jump=True):
        """점프 (이중 점프 지원)"""
        if self.is_dashing:
            return

        # 지상 점프 (항상 가능)
        if not self.is_jumping:
            self.change_y = -JUMP_HEIGHT
            self.is_jumping = True
            if self.sound_manager: self.sound_manager.play_sfx("jump")
            self.jump_count = 1
            return

        # 공중 점프 (이중 점프 - 플래그 체크)
        if can_double_jump and self.jump_count < MAX_JUMP_COUNT:
            self.change_y = -JUMP_HEIGHT
            self.jump_count += 1

    def guard(self, active):
        """방어 상태 설정"""
        if active and self.guard_gauge > 0:
             self.is_guarding = True
        else:
             self.is_guarding = False

    def dash(self):
        """대쉬 (가드 중이면 가드 푸시, 기력 소모 없음)"""
        if not self.is_dashing:
            # 기력 소모 제거 (사용자 요청)
            self.is_dashing = True
            
            # 가드 중 대쉬 -> 가드 푸시
            if self.is_guarding:
                self.is_pushing = True
                self.dash_timer = 10 # 짧게 밀치기
                speed = DASH_SPEED * 1.5 if self.direction == "right" else -DASH_SPEED * 1.5
                print(f"{self.name} used Guard Push!")
            else:
                # 대쉬 거리 증가 (지속시간 및 속도 증가)
                self.dash_timer = int(DASH_DURATION * 1.5) # 지속 시간 50% 증가
                # 속도도 약간 증가 (기존 DASH_SPEED가 15라면 충분히 빠르지만 확실한 이동을 위해)
                speed = (DASH_SPEED * 1.2) if self.direction == "right" else -(DASH_SPEED * 1.2)
                
            self.change_x = speed

    def attack(self, skill_key, modifier=None):
        """
        공격 함수 (스킬 시스템)
        캐릭터 전용 스킬이 있으면 우선 사용하고, 없으면 기본 스킬(DEFAULT_SKILLS)을 사용합니다.
        
        Args:
            skill_key: 키 입력 (J, U, I, O...)
            modifier: 방향키 조합 ('up', 'down', None)
        """
        # 데이터 가져오기 (캐릭터 전용 -> 공통 기본값 순)
        char_skills = SKILL_DATA.get(self.name, {})
        skill_info = char_skills.get(skill_key, DEFAULT_SKILLS.get(skill_key, DEFAULT_SKILLS['J']))
        
        # 반격기 (Counter) 처리
        if modifier == 'counter':
            self.perform_counter()
            return

        cost = skill_info.get('cost', 0)
        
        # 기력 무한 모드 체크
        if GAME_SETTINGS.get("infinite_resource", False):
            cost = 0

        # 대공/하단 공격 처리 (Modify skill info locally)
        attack_type = ATTACK_NORMAL
        if modifier == 'up':
            attack_type = ATTACK_AIR
            # 대공기 보정: 데미지 80%, 띄우기 효과(추후 구현)
        elif modifier == 'down':
            attack_type = ATTACK_LOW
             # 하단기 보정: 데미지 90%, 가드 무시(추후 구현 가능)

        
        if self.attack_cooldown == 0 and self.ki >= cost:
            self.is_attacking = True
            if self.sound_manager: self.sound_manager.play_sfx("attack")
            self.attack_cooldown = skill_info['cooldown']
            self.ki -= cost
            # 데미지에 배율 적용
            base_damage = skill_info['damage']
            
            # [NEW] Modifier Effects
            if attack_type == ATTACK_AIR:
                base_damage = int(base_damage * 0.8) # 대공기 데미지 감소
                self.change_y = -5 # 살짝 뜸 (Launch self)
            elif attack_type == ATTACK_LOW:
                base_damage = int(base_damage * 0.9) # 하단기 데미지 약간 감소
            
            multiplier = getattr(self, 'damage_multiplier', 1.0)
            self.current_damage = int(base_damage * multiplier)
            
            # 공격 애니메이션 시간 설정 (기본 20프레임)
            self.attack_timer = 20
            
            skill_type = skill_info.get('type', 'basic')
            
            print(f"{self.name} used {skill_key} ({skill_type})")
            self.last_skill_key = skill_key # 이펙트 참조용 키 저장
            
            # 기력 획득 (공격 성공 여부와 상관없이 시전시 약간 회복 -> 제거됨, 타격시에만)
            # if cost == 0 and self.ki < self.max_ki:
            #      self.ki += 0.1


            # 1. 투사체 (수리검, 에너지파)
            if skill_type == 'projectile':
                self.last_skill_used = 'projectile' 
                
            # 2. 소환 (분신술, 소환수)
            elif skill_type == 'summon':
                self.last_skill_used = 'summon'
            
            # 3. 돌진 공격 (나선환, 이동 타격)
            elif skill_type == 'dash_attack':
                self.is_dashing = True # 돌진 상태
                self.dash_timer = 20 # 돌진 시간
                self.current_damage = skill_info['damage']
                
                # 돌진 속도 증가
                dash_speed_mult = 1.5
                if 'blitz' in skill_info['name'].lower(): dash_speed_mult = 2.5 # 매우 빠른 돌진
                
                speed = DASH_SPEED * dash_speed_mult if self.direction == "right" else -DASH_SPEED * dash_speed_mult
                self.change_x = speed
            
            # 4. 빔 (파이널 플래시, 할로우 퍼플)
            elif skill_type == 'beam':
                self.last_skill_used = 'beam'
                # 빔은 Main에서 처리 (지속 데미지 영역 생성)
            
            # 5. 광역 (기린, 영역 전개)
            elif skill_type == 'area':
                self.last_skill_used = 'area'
                # 화면 전체 혹은 넓은 범위 공격
            
            # 6. 버프 (자가 강화)
            elif skill_type == 'buff':
                self.last_skill_used = 'buff'
                # 체력 회복이나 스탯 증가 (Main 처리)
            
            # 7. 힐 (서포트)
            elif skill_type == 'heal':
                self.last_skill_used = 'heal'
            
            # 8. 디버프 (중력 해제 등)
            elif skill_type == 'debuff':
                self.last_skill_used = 'debuff'
                
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

        if self.change_x > 0:
            self.direction = "right"
        elif self.change_x < 0:
            self.direction = "left"
        
        # 화면 경계 체크
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def move_left(self):
        """왼쪽으로 이동"""
        self.change_x = -CHARACTER_SPEED * getattr(self, 'speed_multiplier', 1.0)

    def move_right(self):
        """오른쪽으로 이동"""
        self.change_x = CHARACTER_SPEED * getattr(self, 'speed_multiplier', 1.0)

    def stop(self):
        """이동 멈춤"""
        self.change_x = 0
        
    def take_damage(self, damage=10):
        """
        피격 처리
        Args:
            damage: 입을 데미지 (기본값 10, 이제는 외부에서 전달받음)
        """
        # 무적 상태이면 데미지 무시
        if self.invincible_timer > 0:
            return

        # 콤보 카운트 및 스케일링
        if self.hit_stun > 0:
            self.combo_count += 1
        else:
            self.combo_count = 1
            
        # 스케일링 계산 (10%씩 감소, 최소 10% 데미지)
        scaling = max(0.1, 0.9 ** (self.combo_count - 1))
        
        final_damage = int(damage * scaling)
        print(f"Hit! Combo: {self.combo_count}, Scaling: {scaling:.2f}, Dmg: {damage}->{final_damage}")

        # 방어 중이면 데미지 면제 및 게이지 감소 -> 80% 감소로 변경
        if self.is_guarding and self.guard_gauge > 0:
            final_damage = int(damage * 0.2) # 80% 감소
            if final_damage < 1: final_damage = 1 # 최소 1 데미지
            
            self.guard_gauge -= damage # 게이지는 원래 데미지 만큼 감소
            print(f"{self.name} Guarded! Reduced Dmg: {final_damage} (Gauge: {self.guard_gauge})")
            if self.guard_gauge <= 0:
                 self.guard_gauge = 0
                 self.is_guarding = False # Break
        else:
            final_damage = damage
            
        self.hp -= final_damage
        if final_damage > 0:
            if self.sound_manager: self.sound_manager.play_sfx("hit")
        if self.hp < 0:
            self.hp = 0
            
        if not self.is_guarding:
            if self.direction == "right": # 맞았을 때 뒤로 밀림
               self.rect.x -= KNOCKBACK_FORCE
            else:
               self.rect.x += KNOCKBACK_FORCE * 2
            
            # 피격 경직 부여 (기본 30프레임 = 0.5초)
            # 강공격 등은 더 길게 줄 수 있음 (damage에 비례하게?)
            self.hit_stun = 20 + int(damage * 0.5) # 데미지가 클수록 경직 길어짐
            self.is_attacking = False # 공격 중단
            self.is_dashing = False # 대쉬 중단
            self.is_guarding = False # 가드 중단 (가드 브레이크가 아니더라도 맞으면 풀림? 보통은 가드 성공 시 안 맞음)
            # 가드 실패해서 들어온 데미지이므로 상태 해제

    def gain_ki(self, amount):
        """기력 획득"""
        if self.ki < self.max_ki:
            self.ki += amount
            if self.ki > self.max_ki:
                self.ki = self.max_ki
            print(f"{self.name} Gained Ki: {self.ki:.1f}")

    def transform(self):
        """캐릭터 변신"""
        if self.is_transformed:
            return

        trans_data = TRANSFORMATIONS.get(self.original_name)
        if trans_data:
            self.is_transformed = True
            
            # 비용 체크
            if not GAME_SETTINGS.get("infinite_resource", False):
                if self.ki < TRANSFORM_COST:
                    print(f"Not enough Ki for Transformation (Need {TRANSFORM_COST})")
                    self.is_transformed = False # Reset flag just in case
                    return False
                self.ki -= TRANSFORM_COST

            # 스탯 적용
            self.name = trans_data["name"]
            # 데미지는 attack 메서드에서 계산되지 않고, SKILL_DATA에 의존하지만,
            # 전체적인 데미지 계수를 추가하거나 SKILL_DATA를 수정해야 함.
            # 간단하게 current_damage가 설정될 때 multiplier를 곱하는 방식으로 처리해야 하는데,
            # attack() 메서드 수정이 필요함. 일단 속성으로 저장.
            self.damage_multiplier = trans_data.get("damage_mult", 1.2)
            # 속도 증가
            global CHARACTER_SPEED 
            # 주의: 전역 변수를 바꾸면 모두에게 적용됨. self.speed 속성을 만들어야 함.
            # 현재 move_left/right가 전역 상수를 씀.
            # 이를 위해 move 메서드를 수정해야 하거나, change_x 설정 시 상수를 안 쓰게 해야 함.
            # 여기서는 change_x에 곱해주는 방식보다, move 메서드가 multiplier를 고려하도록 수정 필요.
            self.speed_multiplier = trans_data.get("speed_mult", 1.2)
            
            # 색상 변경 (틴트)
            color = trans_data.get("color", (255, 255, 255))
            
            # 모든 애니메이션 프레임에 틴트 적용
            for action, frames in self.animations.items():
                new_frames = []
                for img in frames:
                    # 복사본 생성
                    tinted = img.copy()
                    # 색상 채우기 (BLEND_ADD 또는 BLEND_MULT)
                    # BLEND_RGBA_MULT가 자연스러움
                    # 하지만 Pygame 버전에 따라 다를 수 있음.
                    # 간단히: 색상 필터를 씌움.
                    fill_surf = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
                    fill_surf.fill((*color, 100)) # Alpha 100
                    tinted.blit(fill_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                    new_frames.append(tinted)
                self.animations[action] = new_frames
            
            print(f"{self.original_name} transformed into {self.name}!")
            # BGM Hijacking
            if GAME_SETTINGS.get("bgm_hijack", False) and self.sound_manager:
                 # 테마곡 경로 구성 (예: game/sounds/naruto_theme.wav)
                 # 파일이 없으면 재생되지 않고 경고만 출력됨 (SoundManager 처리)
                 theme_path = f"game/sounds/{self.original_name.lower()}_theme.wav"
                 self.sound_manager.play_custom_bgm(theme_path)
            
            # 컷신 효과 또는 시간 정지 등을 여기나 Main에 추가 가능
            
            return True
        return False

    def perform_counter(self):
        """반격기 사용 (U + I)"""
        if self.ki >= 1 or GAME_SETTINGS.get("infinite_resource", False):
             if not GAME_SETTINGS.get("infinite_resource", False):
                 self.ki -= 1
             
             self.is_attacking = True
             self.attack_timer = 30
             self.state = "guard" # Visual like guard but glowing?
             # 실제 반격 로직은 hit 처리에서 'counter' 상태일 때 데미지 반사를 구현해야 함
             # 여기서는 시각적 효과와 상태 설정만
             print(f"{self.name} used Explosive Counter!")
             # 이펙트 매니저가 있다면 이펙트 추가

    def perform_joint_attack(self):
        """합동 공격 (I + O)"""
        # 비용 체크 (5기)
        cost = JOINT_ATTACK_COST
        if GAME_SETTINGS.get("infinite_resource", False):
            cost = 0
            
        if self.ki >= cost:
            self.ki -= cost
            print(f"{self.name} used Joint Ultimate Attack!")
            
            # 로직:
            # 1. 컷신 연출 (화면 암전 등 - Main에서 처리하거나 상태 플래그로)
            # 2. 강력한 공격 판정 생성
            self.is_attacking = True
            self.attack_timer = 60 # 긴 시간
            self.last_skill_used = 'joint_ultimate'
            
            # 데미지 설정 (매우 강력)
            base_damage = 100
            multiplier = getattr(self, 'damage_multiplier', 1.0)
            self.current_damage = int(base_damage * multiplier)
            
            # 공격 범위: 전체 화면 (실제로는 Main에서 처리 추천)
            self.attack_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            return True
        else:
            print("Not enough Ki for Joint Attack")
            return False

    def perform_substitution(self, target):
        """바꿔치기 술 (피격 중 탈출)"""
        if self.ki >= SUBSTITUTION_COST:
            self.ki -= SUBSTITUTION_COST
            
            # 1. 이펙트 (통나무 등 - Smoke로 대체)
            # (Main에서 이펙트 생성 호출 권장, 여기서는 상태 변경만)
            
            # 2. 이동 (상대방 뒤로)
            offset = 100
            if target.direction == "right": # 상대가 오른쪽 보는 중 -> 상대 등 뒤는 왼쪽
                self.rect.x = target.rect.x - offset
                self.direction = "right" # 상대를 바라봄
            else:
                self.rect.x = target.rect.right + offset
                self.direction = "left"
            
            # 화면 경계 체크
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
            
            # 3. 무적 부여
            self.invincible_timer = INVINCIBLE_DURATION
            
            # 4. 상태 리셋 (경직 해제)
            self.state = "idle"
            self.is_attacking = False
            self.attack_timer = 0
            self.change_x = 0
            self.change_y = 0
            
            print(f"{self.name} used Substitution Jutsu!")
            return True
        return False
