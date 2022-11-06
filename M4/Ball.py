import random
import pygame
from Velocity import Velocity

BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = Velocity(random.randint(4, 8), random.randint(-8, 8))
        self.rect = self.image.get_rect()

    def reset(self):
        self.rect = self.image.get_rect()
        self.velocity = Velocity(random, random.randint(4, 8), random.randint(-8, 8))

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def bounce(self):
        self.velocity.x = -self.velocity.x
        self.velocity.y = random.randint(-8, 8)
