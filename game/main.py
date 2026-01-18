from game.settings import *
from game.characters import Character
from game.utils import draw_text
from game.effects import EffectManager # 이펙트 매니저 추가

class Game:
    """
    게임의 상태와 흐름을 관리하는 메인 클래스입니다.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_MENU
        
        # 게임 데이터
        self.player1_char = "Naruto"
        self.player2_char = "Bleach"
        self.game_mode = "2P" # "1P" or "2P"
        
        # 이펙트 시스템
        self.effect_manager = EffectManager()
        
        # 설정값 초기화
        self.difficulty = DEFAULT_DIFFICULTY
        self.bgm_volume = DEFAULT_BGM_VOLUME
        self.sfx_volume = DEFAULT_SFX_VOLUME

        # 스프라이트 및 게임 객체 (배틀 상태에서 초기화)
        self.all_sprites = None
        self.player1 = None
        self.player2 = None
        self.winner = ""

    def run(self):
        """메인 게임 루프"""
        while self.running:
            if self.state == STATE_MENU:
                self.handle_menu()
            elif self.state == STATE_SELECT:
                self.handle_select()
            elif self.state == STATE_SETTINGS:
                self.handle_settings()
            elif self.state == STATE_BATTLE:
                self.handle_battle()
            elif self.state == STATE_GAME_OVER:
                self.handle_game_over()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def handle_menu(self):
        """메인 메뉴 화면"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.game_mode = "1P"
                    self.state = STATE_SELECT
                if event.key == pygame.K_2:
                    self.game_mode = "2P"
                    self.state = STATE_SELECT
                if event.key == pygame.K_3 or event.key == pygame.K_o:
                    self.state = STATE_SETTINGS

        self.screen.fill(WHITE)
        draw_text(self.screen, "Naruto vs Bleach", 64, SCREEN_WIDTH // 2 - 180, 100, BLACK)
        draw_text(self.screen, "Press '1' for 1 Player (Bot Mode)", 32, SCREEN_WIDTH // 2 - 150, 250, RED)
        draw_text(self.screen, "Press '2' for 2 Players (PvP)", 32, SCREEN_WIDTH // 2 - 130, 300, BLUE)
        draw_text(self.screen, "Press '3' for Settings", 32, SCREEN_WIDTH // 2 - 100, 350, GRAY)
        pygame.display.flip()

    def handle_settings(self):
        """환경설정 화면"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                    self.state = STATE_MENU
                
                # 난이도 조절
                if event.key == pygame.K_1: self.difficulty = DIFFICULTY_EASY
                if event.key == pygame.K_2: self.difficulty = DIFFICULTY_NORMAL
                if event.key == pygame.K_3: self.difficulty = DIFFICULTY_HARD
                if event.key == pygame.K_4: self.difficulty = DIFFICULTY_VERY_HARD
                
                # 볼륨 조절 (단순화: 10단위)
                if event.key == pygame.K_UP: 
                    self.bgm_volume = min(100, self.bgm_volume + 10)
                if event.key == pygame.K_DOWN: 
                    self.bgm_volume = max(0, self.bgm_volume - 10)
                if event.key == pygame.K_RIGHT: 
                    self.sfx_volume = min(100, self.sfx_volume + 10)
                if event.key == pygame.K_LEFT: 
                    self.sfx_volume = max(0, self.sfx_volume - 10)

        self.screen.fill(WHITE)
        draw_text(self.screen, "SETTINGS", 48, SCREEN_WIDTH // 2 - 80, 50, BLACK)
        
        # 난이도 표시
        draw_text(self.screen, f"Difficulty: {self.difficulty}", 32, 100, 150, BLACK)
        draw_text(self.screen, "(1: Easy, 2: Normal, 3: Hard, 4: Very Hard)", 20, 100, 190, GRAY)
        
        # 볼륨 표시
        draw_text(self.screen, f"BGM Volume (Up/Down): {self.bgm_volume}%", 32, 100, 250, BLACK)
        draw_text(self.screen, f"SFX Volume (Left/Right): {self.sfx_volume}%", 32, 100, 320, BLACK)
        
        draw_text(self.screen, "Press 'ESP' or 'B' to Back", 24, SCREEN_WIDTH // 2 - 100, 500, RED)
        pygame.display.flip()

    def handle_select(self):
        """캐릭터 선택 화면"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # P1 캐릭터 변경 (A/D)
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player1_char = "Bleach" if self.player1_char == "Naruto" else "Naruto"
                
                # P2 캐릭터 변경 (Left/Right) - 2P 모드일 때만
                if self.game_mode == "2P":
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player2_char = "Bleach" if self.player2_char == "Naruto" else "Naruto"
                
                # 게임 시작 (Space)
                if event.key == pygame.K_SPACE:
                    self.init_battle()
                    self.state = STATE_BATTLE

        self.screen.fill(BLACK)
        draw_text(self.screen, "Select Character", 48, SCREEN_WIDTH // 2 - 140, 50, WHITE)
        
        # P1 선택 정보
        p1_color = ORANGE if self.player1_char == "Naruto" else BLACK
        draw_text(self.screen, "Player 1", 32, 150, 200, WHITE)
        draw_text(self.screen, f"< {self.player1_char} >", 40, 130, 250, p1_color)
        
        # P2 선택 정보
        p2_color = ORANGE if self.player2_char == "Naruto" else BLACK
        draw_text(self.screen, "Player 2", 32, 550, 200, WHITE)
        is_bot = " (Bot)" if self.game_mode == "1P" else ""
        draw_text(self.screen, f"< {self.player2_char}{is_bot} >", 40, 500, 250, p2_color)

        draw_text(self.screen, "P1: A/D to Change, Space to Start", 20, SCREEN_WIDTH // 2 - 130, 450, YELLOW)
        if self.game_mode == "2P":
             draw_text(self.screen, "P2: Arrows to Change", 20, SCREEN_WIDTH // 2 - 80, 480, YELLOW)
        pygame.display.flip()

    def init_battle(self):
        """전투 시작 전 초기화"""
        from game.objects import Projectile # 내부 임포트 to avoid circular import
        self.Projectile = Projectile

        # 선택된 캐릭터에 따라 이미지 결정
        p1_img = "game/images/naruto.png" if self.player1_char == "Naruto" else "game/images/ichigo.png"
        p2_img = "game/images/naruto.png" if self.player2_char == "Naruto" else "game/images/ichigo.png"

        
        # 난이도에 따른 봇(P2) 스탯 보정 (Very Hard)
        p2_hp = 100
        if self.game_mode == "1P" and self.difficulty == DIFFICULTY_VERY_HARD:
            p2_hp = 150 # 체력 증가 보너스

        self.player1 = Character(100, SCREEN_HEIGHT - 150, p1_img, self.player1_char)
        self.player1.direction = "right"
        self.player1.controls = {
            'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w,
            'skill_u': P1_KEY_U, 'skill_i': P1_KEY_I, 'skill_o': P1_KEY_O,
            'basic': P1_KEY_J, 'guard': P1_KEY_K, 'dash': P1_KEY_L
        }
        
        self.player2 = Character(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, p2_img, self.player2_char)
        self.player2.direction = "left"
        self.player2.hp = p2_hp 
        self.player2.max_hp = p2_hp
        
        self.player2.controls = {
            'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP,
            'skill_4': P2_KEY_4, 'skill_5': P2_KEY_5, 'skill_6': P2_KEY_6,
            'basic': P2_KEY_1, 'guard': P2_KEY_2, 'dash': P2_KEY_3
        }

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        
        self.projectiles = pygame.sprite.Group()
        self.clones = pygame.sprite.Group()
        
        # 배틀 시작 시 이펙트 초기화
        self.effect_manager = EffectManager()

    def handle_battle(self):
        """실제 전투 로직"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # P1 조작
            if event.type == pygame.KEYDOWN:
                controls = self.player1.controls
                if event.key == controls['left']: self.player1.move_left()
                if event.key == controls['right']: self.player1.move_right()
                if event.key == controls['jump']: self.player1.jump()
                
                # 스킬 및 액션
                if event.key == controls['basic']: self.player1.attack('J')
                if event.key == controls['skill_u']: self.player1.attack('U')
                if event.key == controls['skill_i']: self.player1.attack('I')
                if event.key == controls['skill_o']: self.player1.attack('O')
                
                if event.key == controls['dash']: self.player1.dash()
                if event.key == controls['guard']: self.player1.guard(True)
                
            if event.type == pygame.KEYUP:
                controls = self.player1.controls
                if event.key == controls['left'] and self.player1.change_x < 0: self.player1.stop()
                if event.key == controls['right'] and self.player1.change_x > 0: self.player1.stop()
                if event.key == controls['guard']: self.player1.guard(False)

            # P2 조작 (2P 모드일 때만)
            if self.game_mode == "2P":
                if event.type == pygame.KEYDOWN:
                    controls = self.player2.controls
                    if event.key == controls['left']: self.player2.move_left()
                    if event.key == controls['right']: self.player2.move_right()
                    if event.key == controls['jump']: self.player2.jump()
                    
                    if event.key == controls['basic']: self.player2.attack('1')
                    if event.key == controls['skill_4']: self.player2.attack('4')
                    if event.key == controls['skill_5']: self.player2.attack('5')
                    if event.key == controls['skill_6']: self.player2.attack('6')
                    
                    if event.key == controls['dash']: self.player2.dash()
                    if event.key == controls['guard']: self.player2.guard(True)

                if event.type == pygame.KEYUP:
                    controls = self.player2.controls
                    if event.key == controls['left'] and self.player2.change_x < 0: self.player2.stop()
                    if event.key == controls['right'] and self.player2.change_x > 0: self.player2.stop()
                    if event.key == controls['guard']: self.player2.guard(False)

        # 대쉬 잔상 효과 생성 (매 5프레임마다)
        current_time = pygame.time.get_ticks()
        if self.player1.is_dashing and current_time % 100 < 20: 
             self.effect_manager.create_afterimage(self.player1.rect.x, self.player1.rect.y, self.player1.image)
        if self.player2.is_dashing and current_time % 100 < 20:
             self.effect_manager.create_afterimage(self.player2.rect.x, self.player2.rect.y, self.player2.image)

        # 스킬 확인 및 처리 (투사체, 소환 등)
        self.check_special_skills(self.player1)
        if self.game_mode == "2P" or True: # 1P모드 봇도 스킬 쓴다면
             self.check_special_skills(self.player2)

        # 봇 AI update
        if self.game_mode == "1P":
            self.update_bot_ai()
            # 분신 AI 업데이트
            for clone in self.clones:
                 self.update_clone_ai(clone, self.player2 if clone.name.startswith("Player 1") else self.player1)

        # 업데이트
        self.all_sprites.update()
        self.projectiles.update()
        self.clones.update()
        self.effect_manager.update()
        
        # 충돌 및 게임 종료 체크
        self.check_collisions()

        # 그리기
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, (100, 100, 100), [0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50])
        self.all_sprites.draw(self.screen)
        self.clones.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.effect_manager.draw(self.screen)
        
        # UI (체력바 왼쪽/오른쪽 상단)
        # P1 UI
        draw_text(self.screen, f"{self.player1.name} HP: {self.player1.hp}", 20, 10, 10, RED)
        pygame.draw.rect(self.screen, RED, [10, 30, self.player1.hp * 2, 10]) 
        pygame.draw.rect(self.screen, SKY_BLUE, [10, 45, self.player1.mana * 2, 10]) 
        draw_text(self.screen, f"MP: {int(self.player1.mana)}", 15, 10, 60, BLUE)
        
        # 쿨타임 표시 (P1)
        self.draw_cooldown(self.player1, 10, 80)

        # P2 UI
        draw_text(self.screen, f"{self.player2.name} HP: {self.player2.hp}", 20, SCREEN_WIDTH - 150, 10, BLUE)
        p2_hp_width = (self.player2.hp / self.player2.max_hp) * 200
        pygame.draw.rect(self.screen, BLUE, [SCREEN_WIDTH - 210, 30, p2_hp_width, 10]) 
        pygame.draw.rect(self.screen, SKY_BLUE, [SCREEN_WIDTH - 210, 45, self.player2.mana * 2, 10]) 
        draw_text(self.screen, f"MP: {int(self.player2.mana)}", 15, SCREEN_WIDTH - 210, 60, BLUE)

        pygame.display.flip()

    def check_special_skills(self, player):
        """특수 스킬 발동 체크 및 처리"""
        if player.last_skill_used == 'projectile':
            # 수리검 생성
            proj = self.Projectile(player.rect.centerx, player.rect.centery, player.direction, player)
            self.projectiles.add(proj)
            player.last_skill_used = None
            
        elif player.last_skill_used == 'summon':
            # 분신 생성
            clone = Character(player.rect.x, player.rect.y, "game/images/naruto.png", f"{player.name} Clone")
            clone.hp = 15
            clone.max_hp = 15
            clone.direction = player.direction
            # 짙은 색으로 구분
            clone.image.set_alpha(200) 
            self.clones.add(clone)
            player.last_skill_used = None

    def draw_cooldown(self, player, x, y):
        """남은 쿨타임 표시"""
        # U, I, O 쿨타임이 있을 경우 표시
        # 원래는 각 키별 쿨타임을 관리해야 하는데, 현재 Character에는 단일 attack_cooldown만 있음.
        # 개선: Character에 skill_cooldowns 딕셔너리가 필요하지만, 
        # 현재 구조상 attack_cooldown이 모든 스킬을 공유하는 형태라면 그걸 표시.
        # 하지만 요구사항은 각 스킬별 쿨타임 출력임.
        # 일단 현재 attack_cooldown (글로벌 쿨타임)만 표시하거나, 
        # Character 구조를 바꿔야 함. 
        # (간단히 현재 쿨타임만 표시)
        if player.attack_cooldown > 0:
            secs = player.attack_cooldown / 60
            draw_text(self.screen, f"Cool: {secs:.1f}s", 15, x, y, BLACK)

    def update_clone_ai(self, clone, target):
        """분신 AI (Hard 모드 적용)"""
        # 간단한 공격형 AI
        dist = abs(clone.rect.centerx - target.rect.centerx)
        if dist > 50:
            if clone.rect.centerx > target.rect.centerx: clone.move_left()
            else: clone.move_right()
        else:
            clone.attack('J') # 기본 공격만


    def update_bot_ai(self):
        """스마트 봇 AI (난이도 적용)"""
        import random
        
        dist = abs(self.player1.rect.centerx - self.player2.rect.centerx)
        
        # 난이도별 파라미터 설정
        attack_chance = 0.05
        skill_chance = 0.05
        reaction_speed = 0.1
        
        if self.difficulty == DIFFICULTY_EASY:
            attack_chance = 0.02
            skill_chance = 0.02
            reaction_speed = 0.05
        elif self.difficulty == DIFFICULTY_HARD:
            attack_chance = 0.1
            skill_chance = 0.15
            reaction_speed = 0.3
        elif self.difficulty == DIFFICULTY_VERY_HARD:
            attack_chance = 0.2     # 매우 공격적
            skill_chance = 0.3      # 스킬 난사
            reaction_speed = 0.6    # 빠른 반응
            
        # 1. 이동 및 방어
        if dist > 300: # 멀면 접근
            if self.player2.rect.centerx > self.player1.rect.centerx: self.player2.move_left()
            else: self.player2.move_right()
        elif dist < 80:
            # 너무 가까우면 거리 벌리거나 방어
            if random.random() < reaction_speed: self.player2.guard(True)
            elif random.random() < 0.05:
                if self.player2.rect.centerx > self.player1.rect.centerx: self.player2.move_right()
                else: self.player2.move_left()
            else: self.player2.guard(False)
        else:
            self.player2.stop()
            if self.difficulty != DIFFICULTY_VERY_HARD: # Very Hard는 가드를 잘 안품
                 if random.random() > reaction_speed: 
                      self.player2.guard(False)
            else:
                 # Very Hard는 플레이어가 공격중일때만 가드 유지 시도 (예측)
                 if not self.player1.is_attacking:
                      self.player2.guard(False)
            
        # 2. 공격 로직
        if self.player2.attack_cooldown == 0:
            chance = random.random()
            # 마나가 충분하면 스킬 사용
            if dist < 150: # 근거리
                if chance < attack_chance: self.player2.attack('1') # 기본
                elif chance < attack_chance + skill_chance and self.player2.mana > 10: self.player2.attack('4') # 스킬 1
            elif dist < 400: # 중거리
                 if chance < skill_chance and self.player2.mana > 20: self.player2.attack('5') # 스킬 2
                 if chance < skill_chance * 0.5 and self.player2.mana > 40: self.player2.attack('6') # 스킬 3
            
            # 대쉬 (회피 또는 접근)
            if self.difficulty == DIFFICULTY_VERY_HARD:
                 if self.player1.is_attacking and dist < 150 and self.player2.mana > 5:
                      self.player2.dash() # 회피 대쉬
                 elif dist > 400 and self.player2.mana > 20:
                      self.player2.dash() # 접근 대쉬
            elif random.random() < 0.01 and self.player2.mana > 5:
                self.player2.dash()

    def check_collisions(self):
        """충돌 및 승패 판정"""
        # 1. 플레이어 공격 충돌 (기존 로직)
        players = [self.player1, self.player2]
        
        for p in players:
            target = self.player2 if p == self.player1 else self.player1
            if p.is_attacking and p.attack_rect:
                if p.attack_rect.colliderect(target.rect):
                    target.take_damage(p.current_damage)
                    self.effect_manager.create_hit_effect(target.rect.centerx, target.rect.centery)
                    p.is_attacking = False
                    p.attack_rect = None
            
            # 투사체 충돌 체크
            hits = pygame.sprite.spritecollide(target, self.projectiles, True) # 닿으면 사라짐
            for proj in hits:
                if proj.owner != target: # 자기가 쏜 거에 안 맞게
                    target.take_damage(proj.damage)
                    self.effect_manager.create_hit_effect(target.rect.centerx, target.rect.centery)
        
        # 2. 분신 공격 확인
        for clone in self.clones:
            target = self.player2 if clone.name.startswith("Player 1") else self.player1
            if clone.is_attacking and clone.attack_rect:
                if clone.attack_rect.colliderect(target.rect):
                    target.take_damage(clone.current_damage)
                    clone.is_attacking = False
                    clone.attack_rect = None
            
            # 분신 피격 확인 (플레이어 공격에 맞으면)
            if self.player2.attack_rect and self.player2.attack_rect.colliderect(clone.rect):
                clone.take_damage(self.player2.current_damage)
            if self.player1.attack_rect and self.player1.attack_rect.colliderect(clone.rect):
                clone.take_damage(self.player1.current_damage)
                
            if clone.hp <= 0:
                clone.kill()

        # 3. 승패 판정
        if self.player1.hp <= 0:
            self.winner = self.player2.name
            self.state = STATE_GAME_OVER
        elif self.player2.hp <= 0:
            self.winner = self.player1.name
            self.state = STATE_GAME_OVER

    def handle_game_over(self):
        """게임 오버 화면"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # 재시작
                    self.init_battle()
                    self.state = STATE_BATTLE
                if event.key == pygame.K_m: # 메인 메뉴로
                    self.state = STATE_MENU

        # 반투명 오버레이
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(10) # 투명도
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        
        draw_text(self.screen, f"GAME OVER - {self.winner} WINS!", 50, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 50, BLACK)
        draw_text(self.screen, "Press 'R' to Restart", 30, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, BLACK)
        draw_text(self.screen, "Press 'M' for Menu", 30, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, GRAY)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
