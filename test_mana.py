from game.settings import *
from game.characters import Character

def test_mana_consumption():
    pygame.init()
    pygame.display.set_mode((1, 1))
    c = Character(0, 0, "game/images/naruto.png", "Naruto")
    c.mana = 50
    print(f"Initial Mana: {c.mana}")
    
    # Attack J (Basic)
    c.attack('J')
    print(f"After Attack J: {c.mana}")
    
    if c.mana == 50:
        print("Basic Attack does NOT consume mana. OK.")
    else:
        print(f"FAIL: Basic Attack consumed {50 - c.mana} mana.")
        
    # Dash
    c.mana = 50
    c.dash()
    print(f"After Dash: {c.mana}")

if __name__ == "__main__":
    test_mana_consumption()
