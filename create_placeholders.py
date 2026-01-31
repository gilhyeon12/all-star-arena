#!/usr/bin/env python3
import pygame

pygame.init()

# Create Ichigo placeholder (Orange/Black theme)
ichigo = pygame.Surface((100, 100))
ichigo.fill((255, 140, 0))  # Orange
pygame.draw.rect(ichigo, (0, 0, 0), [30, 20, 40, 60])  # Black body
pygame.draw.circle(ichigo, (255, 200, 150), (50, 25), 15)  # Head
pygame.image.save(ichigo, "game/images/ichigo.png")

# Create Sasuke placeholder (Blue/Dark theme)
sasuke = pygame.Surface((80, 80))
sasuke.fill((50, 50, 150))  # Dark blue
pygame.draw.rect(sasuke, (0, 0, 0), [25, 15, 30, 50])  # Black outfit
pygame.draw.circle(sasuke, (255, 220, 180), (40, 20), 12)  # Head
pygame.image.save(sasuke, "game/images/sasuke.png")

# Create Inoue placeholder (Orange/White theme)
inoue = pygame.Surface((80, 80))
inoue.fill((255, 200, 100))  # Light orange
pygame.draw.rect(inoue, (255, 255, 255), [25, 15, 30, 50])  # White dress
pygame.draw.circle(inoue, (255, 220, 180), (40, 20), 12)  # Head
pygame.image.save(inoue, "game/images/inoue.png")

print("Placeholder images created successfully!")
