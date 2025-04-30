import pygame

class piece:
    def __init__(self, position, Size):
        self.pos = pygame.Vector2(position)
        self.size = pygame.Vector2(Size)
        self.isAlive = True

    def draw(self, screen):
        raise NotImplementedError("must be overridden by subclass")

class pawn(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (30,144,255), (self.pos.x, self.pos.y, 80, 80))

