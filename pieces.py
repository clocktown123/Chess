import pygame

BluePawnPiece = pygame.image.load("BluePawn.png")
BluePawnPiece.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)

BlackPawnPiece = pygame.image.load("BlackPawn.png")
BlackPawnPiece.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)

class piece:
    def __init__(self, position, Size):
        self.pos = pygame.Vector2(position)
        self.size = pygame.Vector2(Size)
        self.isAlive = True

    def draw(self, screen):
        raise NotImplementedError("must be overridden by subclass")

class BluePawn(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
    
    def draw(self, screen):
        screen.blit(BluePawnPiece, (self.pos))

class BlackPawn(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
    
    def draw(self, screen):
        screen.blit(BlackPawnPiece, (self.pos))


