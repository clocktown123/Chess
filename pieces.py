import pygame

import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

BluePawnPiece = pygame.image.load(resource_path("ChessImages/BluePawn.png"))
BluePawnPiece.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)

BlackPawnPiece = pygame.image.load(resource_path("ChessImages/BlackPawn.png"))
BlackPawnPiece.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)

BlueBishop = pygame.image.load(resource_path("ChessImages/BlueBishop.png"))
BlueBishop.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)

BlackBishop = pygame.image.load(resource_path("ChessImages/BlackBishop.png"))
BlackBishop.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)

class piece:
    def __init__(self, position, Size):
        self.pos = pygame.Vector2(position)
        self.size = pygame.Vector2(Size)
        self.isAlive = True
        self.PawnBox = pygame.Rect(self.pos, self.size)
        self.selecting = False
        self.wait = False
    

    def draw(self, screen):
        raise NotImplementedError("must be overridden by subclass")

class Pawn(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
        self.FirstMove = True
        self.selected = False

    def update_rect(self):
        self.PawnBox = pygame.Rect(self.pos, self.size)

    def BlueMove(self, mxpos, mypos, mouseDown, enemies):
        self.update_rect()
        if self.PawnBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selected = True
            return False

        if self.selected and mouseDown:
            # Move one step forward
            self.one_step = pygame.Rect(self.pos.x, self.pos.y - 100, self.size.x, self.size.y)
            self.two_step = pygame.Rect(self.pos.x, self.pos.y - 200, self.size.x, self.size.y)
            self.TopLeft = pygame.Rect(self.pos.x-100, self.pos.y-100, 100, 100)
            self.TopRight = pygame.Rect(self.pos.x+100, self.pos.y-100, 100, 100)

            for i in enemies:
                if i.PawnBox.colliderect(self.TopLeft):
                    if self.TopLeft.collidepoint(mxpos, mypos) and mouseDown:
                        self.pos.y -= 100
                        self.pos.x -= 100
                        self.selected = False
                        i.isAlive = False
                        return True

                elif i.PawnBox.colliderect(self.TopRight):
                    if self.TopRight.collidepoint(mxpos, mypos) and mouseDown:
                        self.pos.y -= 100
                        self.pos.x += 100
                        self.selected = False
                        i.isAlive = False
                        return True

            if self.FirstMove and self.two_step.collidepoint(mxpos, mypos):
                self.pos.y -= 200
                self.FirstMove = False
                self.selected = False
                return True
            elif self.one_step.collidepoint(mxpos, mypos):
                self.pos.y -= 100
                self.FirstMove = False
                self.selected = False
                return True

        return False

    def BlueDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BluePawnPiece, self.pos)

    def BlackMove(self, mxpos, mypos, mouseDown, enemies):
        self.update_rect()
        if self.PawnBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selected = True
            return False

        if self.selected and mouseDown:
            self.one_step = pygame.Rect(self.pos.x, self.pos.y + 100, self.size.x, self.size.y)
            self.two_step = pygame.Rect(self.pos.x, self.pos.y + 200, self.size.x, self.size.y)
            self.BottomLeft = pygame.Rect(self.pos.x-100, self.pos.y+100, 100, 100)
            self.BottomRight = pygame.Rect(self.pos.x+100, self.pos.y+100, 100, 100)

            for i in enemies:
                if i.PawnBox.colliderect(self.BottomLeft):
                    if self.BottomLeft.collidepoint(mxpos, mypos) and mouseDown:
                        self.pos.y += 100
                        self.pos.x -= 100
                        self.selected = False
                        i.isAlive = False
                        return True

                elif i.PawnBox.colliderect(self.BottomRight):
                    if self.BottomRight.collidepoint(mxpos, mypos) and mouseDown:
                        self.pos.y += 100
                        self.pos.x += 100
                        self.selected = False
                        i.isAlive = False
                        return True

            if self.FirstMove and self.two_step.collidepoint(mxpos, mypos):
                self.pos.y += 200
                self.FirstMove = False
                self.selected = False
                return True
            elif self.one_step.collidepoint(mxpos, mypos):
                self.pos.y += 100
                self.FirstMove = False
                self.selected = False
                return True

        return False

    def Blackdraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackPawnPiece, self.pos)
                

class Bishop(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
        self.BishopBox = pygame.Rect(self.pos, self.size)

    def update_rect(self):
        self.BishopBox = pygame.Rect(self.pos, self.size)

    def BlueDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlueBishop, (self.pos.x + 10, self.pos.y))
    
    def BlueMove(self, mxpos, mypos, MousePos,  enemies):
        pass

    def BlackDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackBishop, (self.pos.x + 10, self.pos.y))
