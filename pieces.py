import pygame
import sys
import os

# ---------- utility -----------------------------------------------------------
def resource_path(relative_path):
    """Return absolute path to resource (works for dev & PyInstaller)."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


def square_occupied(board_x, board_y, piece_groups):
    """
    Return the first *live* piece on board square (board_x, board_y) or None.

    Squares are 0‑indexed (0‑7).  piece_groups is the list you already pass
    around called AllPieces ‑‑ a list of lists [bluePieces, blackPieces].
    """
    for group in piece_groups:
        for p in group:
            if p.isAlive \
               and int(p.pos.x // 100) == board_x \
               and int(p.pos.y // 100) == board_y:
                return p
    return None


###################################IMAGES#########################################

#-----------------------------------Pawns-----------------------------------#
BluePawnPiece = pygame.image.load(resource_path("ChessImages/BluePawn.png"))
BluePawnPiece.set_colorkey((255, 0, 255))

BlackPawnPiece = pygame.image.load(resource_path("ChessImages/BlackPawn.png"))
BlackPawnPiece.set_colorkey((255, 0, 255))

#-----------------------------------Bishops-----------------------------------#

BlueBishop = pygame.image.load(resource_path("ChessImages/BlueBishop.png"))
BlueBishop.set_colorkey((255, 0, 255))

BlackBishop = pygame.image.load(resource_path("ChessImages/BlackBishop.png"))
BlackBishop.set_colorkey((255, 0, 255))

#-----------------------------------Knights-----------------------------------#
BlueKnight = pygame.image.load(resource_path("ChessImages/BlueKnight.png"))
BlueKnight.set_colorkey((255, 0, 255))

BlackKnight = pygame.image.load(resource_path("ChessImages/BlackKnight.png"))
BlackKnight.set_colorkey((255, 0, 255))



################################## Parent class ####################################
class piece:
    def __init__(self, position, Size):
        self.pos = pygame.Vector2(position)
        self.size = pygame.Vector2(Size)
        self.isAlive = True
        self.PawnBox = pygame.Rect(self.pos, self.size)  # reused by all pieces
        self.selecting = False

    def draw(self, screen):
        raise NotImplementedError("must be overridden by subclass")


# ---------- pawn --------------------------------------------------------------
class Pawn(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
        self.FirstMove = True
        self.selected = False
        self.MF = True  # “Move Forward” flag (path blocked)

    def update_rect(self):
        self.PawnBox = pygame.Rect(self.pos, self.size)
        self.BlueEnemyCheck = pygame.Rect(self.pos.x, self.pos.y - 100, 100, 100)
        self.BlackEnemyCheck = pygame.Rect(self.pos.x, self.pos.y + 100, 100, 100)

    # ---------------- blue pawn ------------------------------------------------
    def BlueMove(self, mxpos, mypos, mouseDown, enemies, BluePawns):
        self.update_rect()
        if not self.isAlive:
            return False

        if self.PawnBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selected = True
            return False

        # test square directly in front
        self.MF = all(
            not (e.isAlive and e.PawnBox.colliderect(self.BlueEnemyCheck))
            for e in enemies
        )

        if self.selected and mouseDown:
            self.one_step = pygame.Rect(self.pos.x, self.pos.y - 100, self.size.x, self.size.y)
            self.two_step = pygame.Rect(self.pos.x, self.pos.y - 200, self.size.x, self.size.y)
            self.TopLeft  = pygame.Rect(self.pos.x - 100, self.pos.y - 100, 100, 100)
            self.TopRight = pygame.Rect(self.pos.x + 100, self.pos.y - 100, 100, 100)

            # captures
            for e in enemies:
                if e.isAlive and (e.PawnBox.colliderect(self.TopLeft) or e.PawnBox.colliderect(self.TopRight)):
                    if (self.TopLeft if e.PawnBox.colliderect(self.TopLeft) else self.TopRight).collidepoint(mxpos, mypos):
                        self.pos += pygame.Vector2(-100 if e.PawnBox.colliderect(self.TopLeft) else 100, -100)
                        self.selected = False
                        e.isAlive = False
                        return True

            # forward moves
            if self.MF:
                if self.FirstMove and self.two_step.collidepoint(mxpos, mypos):
                    self.pos.y -= 200
                elif self.one_step.collidepoint(mxpos, mypos):
                    self.pos.y -= 100
                else:
                    return False
                self.FirstMove = False
                self.selected  = False
                return True
        return False

    def BlueDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BluePawnPiece, self.pos)

    # ---------------- black pawn ----------------------------------------------
    def BlackMove(self, mxpos, mypos, mouseDown, enemies, BlackPawns):
        self.update_rect()
        if not self.isAlive:
            return False

        if self.PawnBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selected = True
            return False

        self.MF = all(
            not (e.isAlive and e.PawnBox.colliderect(self.BlackEnemyCheck))
            for e in enemies
        )

        if self.selected and mouseDown:
            self.one_step = pygame.Rect(self.pos.x, self.pos.y + 100, self.size.x, self.size.y)
            self.two_step = pygame.Rect(self.pos.x, self.pos.y + 200, self.size.x, self.size.y)
            self.BottomLeft  = pygame.Rect(self.pos.x - 100, self.pos.y + 100, 100, 100)
            self.BottomRight = pygame.Rect(self.pos.x + 100, self.pos.y + 100, 100, 100)

            for e in enemies:
                if e.isAlive and (e.PawnBox.colliderect(self.BottomLeft) or e.PawnBox.colliderect(self.BottomRight)):
                    if (self.BottomLeft if e.PawnBox.colliderect(self.BottomLeft) else self.BottomRight).collidepoint(mxpos, mypos):
                        self.pos += pygame.Vector2(-100 if e.PawnBox.colliderect(self.BottomLeft) else 100, 100)
                        self.selected = False
                        e.isAlive = False
                        return True

            if self.MF:
                if self.FirstMove and self.two_step.collidepoint(mxpos, mypos):
                    self.pos.y += 200
                elif self.one_step.collidepoint(mxpos, mypos):
                    self.pos.y += 100
                else:
                    return False
                self.FirstMove = False
                self.selected  = False
                return True
        return False

    def Blackdraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackPawnPiece, self.pos)


# ---------- bishop ------------------------------------------------------------
class Bishop(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
        self.BishopBox = pygame.Rect(self.pos, self.size)

    def update_rect(self):
        self.BishopBox = pygame.Rect(self.pos, self.size)

    # ---------------- blue bishop ---------------------------------------------
    def BlueDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlueBishop, (self.pos.x + 10, self.pos.y))

    def BlueMove(self, mxpos, mypos, mouseDown, AllPieces):
        self.update_rect()

        # 1st click = select
        if self.BishopBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selecting = True
            return False

        # 2nd click = attempt move
        if self.selecting and mouseDown:
            sx, sy = int(self.pos.x // 100), int(self.pos.y // 100)  # start square
            tx, ty = int(mxpos // 100), int(mypos // 100)            # target square
            dx, dy = tx - sx, ty - sy

            # must be diagonal
            if abs(dx) != abs(dy) or dx == 0:
                self.selecting = False
                return False

            step_x = 1 if dx > 0 else -1
            step_y = 1 if dy > 0 else -1

            # scan squares between start and destination
            x, y = sx + step_x, sy + step_y
            while (x, y) != (tx, ty):
                if square_occupied(x, y, AllPieces):
                    return False  # piece blocks path
                x += step_x
                y += step_y

            dest_piece = square_occupied(tx, ty, AllPieces)
            if dest_piece:
                # friendly piece blocks move
                if dest_piece in AllPieces[0]:  # blue pieces list is first
                    return False
                dest_piece.isAlive = False      # capture enemy

            # perform move
            self.pos.x = tx * 100
            self.pos.y = ty * 100
            self.selecting = False
            return True

        return False

    # ---------------- black bishop -------------------------------------------
    def BlackDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackBishop, (self.pos.x + 10, self.pos.y))

    def BlackMove(self, mxpos, mypos, mouseDown, AllPieces):
        self.update_rect()

        if self.BishopBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selecting = True
            return False

        if self.selecting and mouseDown:
            sx, sy = int(self.pos.x // 100), int(self.pos.y // 100)
            tx, ty = int(mxpos // 100), int(mypos // 100)
            dx, dy = tx - sx, ty - sy

            if abs(dx) != abs(dy) or dx == 0:
                self.selecting = False
                return False

            step_x = 1 if dx > 0 else -1
            step_y = 1 if dy > 0 else -1

            x, y = sx + step_x, sy + step_y
            while (x, y) != (tx, ty):
                if square_occupied(x, y, AllPieces):
                    return False
                x += step_x
                y += step_y

            dest_piece = square_occupied(tx, ty, AllPieces)
            if dest_piece:
                if dest_piece in AllPieces[1]:  # black pieces list is second
                    return False
                dest_piece.isAlive = False

            self.pos.x = tx * 100
            self.pos.y = ty * 100
            self.selecting = False
            return True

        return False
    
class Knight(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
        self.KnightBox = pygame.Rect(self.pos, self.size)
        #------------------------- Upper squares -------------------------
        self.TopMLeft = pygame.Rect(self.pos.x - 100, self.pos.y - 200, 100, 100)
        self.TopFLeft = pygame.Rect(self.pos.x - 200, self.pos.y - 100, 100, 100)
        self.TopMRight = pygame.Rect(self.pos.x + 100, self.pos.y - 200, 100, 100)
        self.TopFRight = pygame.Rect(self.pos.x + 200, self.pos.y - 100, 100, 100)
        #--------------------------Lower Squares ---------------------------
        self.BottomMLeft = pygame.Rect(self.pos.x - 100, self.pos.y + 200, 100, 100)
        self.BottomFLeft = pygame.Rect(self.pos.x - 200, self.pos.y + 100, 100, 100)
        self.BottomMRight = pygame.Rect(self.pos.x + 100, self.pos.y + 200, 100, 100)
        self.BottomFRight = pygame.Rect(self.pos.x + 200, self.pos.y + 100, 100, 100)

    def update_rect(self):
        self.KnightBox = pygame.Rect(self.pos, self.size)

        #------------------------- Upper squares -------------------------
        self.TopMLeft = pygame.Rect(self.pos.x - 100, self.pos.y - 200, 100, 100)
        self.TopFLeft = pygame.Rect(self.pos.x - 200, self.pos.y - 100, 100, 100)
        self.TopMRight = pygame.Rect(self.pos.x + 100, self.pos.y - 200, 100, 100)
        self.TopFRight = pygame.Rect(self.pos.x + 200, self.pos.y - 100, 100, 100)
        #--------------------------Lower Squares ---------------------------
        self.BottomMLeft = pygame.Rect(self.pos.x - 100, self.pos.y + 200, 100, 100)
        self.BottomFLeft = pygame.Rect(self.pos.x - 200, self.pos.y + 100, 100, 100)
        self.BottomMRight = pygame.Rect(self.pos.x + 100, self.pos.y + 200, 100, 100)
        self.BottomFRight = pygame.Rect(self.pos.x + 200, self.pos.y + 100, 100, 100)

    ####################### Blue Knight ############################
    def BlueDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlueKnight, (self.pos.x + 10, self.pos.y))

    def BlueMove(self, mxpos, mypos, mouseDown, Enemies, Friends):
        self.update_rect()

        if self.KnightBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selecting = True
            return False
        
        if self.selecting and mouseDown:
            #print("hit")
            
            if self.TopMLeft.collidepoint(mxpos, mypos) and mouseDown:
                print("hit")
                for i in Enemies:
                    for j in i:
                        if self.KnightBox.colliderect(j.pos.x, j.pos.y, 100, 100):
                            print("yep")
                            self.pos.x = self.TopMLeft.x
                            self.pos.y = self.TopMLeft.y
                            self.selecting = False
                            j.isAlive = False
                            return True
                        else:
                            self.pos.x = self.TopMLeft.x
                            self.pos.y = self.TopMLeft.y
                            self.selecting = False
                            return True
        return False
                # for i in Friends:
                #     for j in i:
                #         if square_occupied(j.pos.x, j.pos.y, Friends):
                #             print("true")

    ######################## Black Knight ############################

    def BlackDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackKnight, (self.pos.x+10, self.pos.y))
    
