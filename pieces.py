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
        self.PawnBox = pygame.Rect(self.pos, self.size)
    

    def draw(self, screen):
        raise NotImplementedError("must be overridden by subclass")

class Pawn(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)

    def BlueMove(self, mxpos, mypos, mouseDown):
        if self.PawnBox.collidepoint(mxpos, mypos) and mouseDown:
            self.pos.y = self.pos.y - 100
            return True
    
    def BlueDraw(self, screen):#, mxpos, mypos, mouseDown):
        screen.blit(BluePawnPiece, (self.pos))

    def BlackMove(self, mxpos, mypos, mouseDown):
        if self.PawnBox.collidepoint(mxpos, mypos) and mouseDown:
            self.pos.y = self.pos.y + 100
            return True

    def Blackdraw(self, screen):
        screen.blit(BlackPawnPiece, (self.pos))


