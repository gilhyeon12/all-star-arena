import pygame
from .settings import *

# 유틸리티 함수
# 게임 전반에서 재사용되는 도구 함수들을 정의합니다.

def draw_text(surface, text, size, x, y, color=BLACK):
    """
    화면에 텍스트를 그리는 함수입니다.
    
    Args:
        surface: 텍스트를 그릴 대상 화면 (pygame.Surface)
        text: 표시할 문자열 (str)
        size: 글자 크기 (int)
        x: X 좌표 (int)
        y: Y 좌표 (int)
        color: 글자 색상 (tuple, 기본값: 검정색)
    """
    font = pygame.font.SysFont("malgungothic", size) # 한글 지원 폰트 사용 시도 (시스템에 따라 다를 수 있음)
    if not font:
        font = pygame.font.Font(None, size) # 기본 폰트
        
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
