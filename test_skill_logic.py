import pygame
from game.settings import *
from game.characters import Character
from game.main import Game

# Mock pygame setup
pygame.init()
pygame.display.set_mode((1, 1))

def test_projectile_logic():
    print("Testing Projectile Logic...")
    
    # Setup
    c = Character(0, 0, "game/images/naruto.png", "Naruto")
    c.mana = 100 # Give mana
    
    # Trigger Attack
    print(f"Before Attack: last_skill_used = {c.last_skill_used}")
    c.attack('U')
    print(f"After Attack: last_skill_used = {c.last_skill_used}")
    
    if c.last_skill_used != 'projectile':
        print("FAIL: last_skill_used is not 'projectile'")
        return

    # Mock Game check
    g = Game()
    g.Projectile = lambda x, y, d, o: "ProjectileObject" # Mock Projectile class
    g.projectiles = pygame.sprite.Group()
    
    g.check_special_skills(c)
    
    if len(g.projectiles) == 1:
        print("SUCCESS: Projectile added to group")
    else:
        print(f"FAIL: Projectile group size is {len(g.projectiles)}")

if __name__ == "__main__":
    test_projectile_logic()
