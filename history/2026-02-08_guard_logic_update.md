# 2026-02-08: 가드 데미지 로직 변경 (Guard Damage Logic Update)

## 목표
- 가드(Guard) 성공 시 입는 데미지를 0으로 변경 (No Chip Damage)

## 변경 사항
- [x] **game/characters.py**
    - `take_damage` 메서드 수정: `is_guarding` 상태이며 `guard_gauge`가 남아있을 경우 데미지를 완전 무효화.
