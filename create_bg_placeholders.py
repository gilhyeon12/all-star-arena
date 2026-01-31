import pygame
import os

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def create_placeholder_bg(name, color):
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill(color)
    # Add some grid lines or details
    for x in range(0, SCREEN_WIDTH, 100):
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, SCREEN_HEIGHT), 2)
    for y in range(0, SCREEN_HEIGHT, 100):
        pygame.draw.line(surface, (0, 0, 0), (0, y), (SCREEN_WIDTH, y), 2)
    
    # Save
    if not os.path.exists("game/images"):
        os.makedirs("game/images")
    pygame.image.save(surface, f"game/images/{name}.png")
    print(f"Saved {name}.png")

if __name__ == "__main__":
    create_placeholder_bg("background", (138, 43, 226)) # Temple (Purple-ish)
    create_placeholder_bg("cyberpunk", (0, 0, 139)) # Cyberpunk (Dark Blue)
    create_placeholder_bg("forest", (34, 139, 34)) # Forest (Green)
