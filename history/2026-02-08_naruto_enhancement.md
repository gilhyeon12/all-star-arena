# 2026-02-08: 나루토 캐릭터 완성 (Naruto Character Enhancement)

## 목표
- 나루토 캐릭터의 스킬 및 변신 시스템 완성
- 시각 효과 및 사운드 강화

## 변경 사항
- [x] **스킬 구현 (Skill Implementation)**
    - 나선환 (Rasengan): 투사체 이펙트 강화
    - 그림자 분신술 (Shadow Clone): AI 개선 및 소멸 이펙트
    - 대옥 나선환 (Giant Rasengan): 돌진 공격 로직 구현
- [x] **변신 시스템 (Transformation)**
    - 선인 모드 (Sage Mode): 스탯 적용 및 비주얼 변경
        - `naruto_sage_mode.png` 생성 및 적용 로직 구현 완료 (game/characters.py).
        - [Fix] 애니메이션 업데이트 루프에서 이미지가 덮어쓰여지는 문제 수정 (모든 프레임 교체).
        - [New] 나선환 사용 시 전용 스프라이트(`naruto_rasengan.png`, `naruto_sage_rasengan.png`) 적용.
        - [Fix] `Character.__init__`에서 `load_animations` 호출 시 `self.direction` 미초기화로 인한 크래시 수정.
- [x] **사운드 (Sound)**
    - 스킬 전용 효과음 적용
