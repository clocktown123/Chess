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

#-----------------------------------Rooks-----------------------------------#
BlueRook = pygame.image.load(resource_path("ChessImages/BlueRook.png"))
BlueRook.set_colorkey((255, 0, 255))

BlackRook = pygame.image.load(resource_path("ChessImages/BlackRook.png"))
BlackRook.set_colorkey((255, 0, 255))

#-----------------------------------Kings-----------------------------------#
BlueKing = pygame.image.load(resource_path("ChessImages/BlueKing.png"))
BlueKing.set_colorkey((255, 0, 255))

BlackKing = pygame.image.load(resource_path("ChessImages/BlackKing.png"))
BlackKing.set_colorkey((255, 0, 255))



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

########################################### PAWNS ##################################################

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
    def BlueMove(self, mxpos, mypos, mouseDown, enemies):
        self.update_rect()
        if self.isAlive:

            if self.PawnBox.collidepoint(mxpos, mypos) and mouseDown:
                self.selected = True
                return False
            
            for i in enemies:
                for j in i:
                    if j.isAlive and self.BlueEnemyCheck.colliderect(j.pos.x, j.pos.y, j.size.x, j.size.y):
                        self.MF = False
                        break  # No need to keep checking
            
            if self.selected and mouseDown:
                # Move one step forward
                self.one_step = pygame.Rect(self.pos.x, self.pos.y - 100, self.size.x, self.size.y)
                self.two_step = pygame.Rect(self.pos.x, self.pos.y - 200, self.size.x, self.size.y)
                self.TopLeft = pygame.Rect(self.pos.x-100, self.pos.y-100, 100, 100)
                self.TopRight = pygame.Rect(self.pos.x+100, self.pos.y-100, 100, 100)

                for i in enemies:
                    for j in i:
                        if self.TopLeft.colliderect(j.pos.x, j.pos.y, j.size.x, j.size.y):
                            if self.TopLeft.collidepoint(mxpos, mypos) and mouseDown:
                                self.pos.y -= 100
                                self.pos.x -= 100
                                self.selected = False
                                j.isAlive = False
                                return True

                        elif self.TopRight.colliderect(j.pos.x, j.pos.y, j.size.x, j.size.y):
                            if self.TopRight.collidepoint(mxpos, mypos) and mouseDown:
                                self.pos.y -= 100
                                self.pos.x += 100
                                self.selected = False
                                j.isAlive = False
                                return True

                if self.MF and self.FirstMove and self.two_step.collidepoint(mxpos, mypos):
                    self.pos.y -= 200
                    self.FirstMove = False
                    self.selected = False
                    return True
                elif self.MF and self.one_step.collidepoint(mxpos, mypos):
                    self.pos.y -= 100
                    self.FirstMove = False
                    self.selected = False
                    return True

            return False

    def BlueDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BluePawnPiece, self.pos)

    # ---------------- black pawn ----------------------------------------------
    def BlackMove(self, mxpos, mypos, mouseDown, enemies):
        self.update_rect()
        if self.isAlive:

            if self.PawnBox.collidepoint(mxpos, mypos) and mouseDown:
                self.selected = True
                return False
            
            for i in enemies:
                for j in i:
                    if j.isAlive and self.BlackEnemyCheck.colliderect(j.pos.x, j.pos.y, j.size.x, j.size.y):
                        self.MF = False
                        break  # No need to keep checking
            
            if self.selected and mouseDown:
                self.one_step = pygame.Rect(self.pos.x, self.pos.y + 100, self.size.x, self.size.y)
                self.two_step = pygame.Rect(self.pos.x, self.pos.y + 200, self.size.x, self.size.y)
                self.BottomLeft = pygame.Rect(self.pos.x-100, self.pos.y+100, 100, 100)
                self.BottomRight = pygame.Rect(self.pos.x+100, self.pos.y+100, 100, 100)

                for i in enemies:
                    for j in i:
                        if self.BottomLeft.colliderect(j.pos.x, j.pos.y, j.size.x, j.size.y):
                            if self.BottomLeft.collidepoint(mxpos, mypos) and mouseDown:
                                self.pos.y += 100
                                self.pos.x -= 100
                                self.selected = False
                                j.isAlive = False
                                return True

                        elif self.BottomRight.colliderect(j.pos.x, j.pos.y, j.size.x, j.size.y):
                            if self.BottomRight.collidepoint(mxpos, mypos) and mouseDown:
                                self.pos.y += 100
                                self.pos.x += 100
                                self.selected = False
                                j.isAlive = False
                                return True

                if self.MF and self.FirstMove and self.two_step.collidepoint(mxpos, mypos):
                    self.pos.y += 200
                    self.FirstMove = False
                    self.selected = False
                    return True
                elif self.MF and self.one_step.collidepoint(mxpos, mypos):
                    self.pos.y += 100
                    self.FirstMove = False
                    self.selected = False
                    return True

            return False

    def Blackdraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackPawnPiece, self.pos)

################################################ BISHOPS ########################################################

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
                if dest_piece in AllPieces[0] or dest_piece in AllPieces[2] or dest_piece in AllPieces[4] or dest_piece in AllPieces[6]:  # blue pieces list is first
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
                if dest_piece in AllPieces[1] or dest_piece in AllPieces[3] or dest_piece in AllPieces[5] or dest_piece in AllPieces[7]:  # black pieces list is second
                    return False
                dest_piece.isAlive = False

            self.pos.x = tx * 100
            self.pos.y = ty * 100
            self.selecting = False
            return True

        return False
    
######################################################## KNIGHTS ####################################################################
    
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
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.TopFLeft.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.TopMRight.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.TopFRight.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.BottomMLeft.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.BottomFLeft.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.BottomMRight.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.BottomFRight.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            else:
                self.selecting = False
                return False

            if square_occupied(x, y, Friends):
                self.selecting = False
                return False
                
            dest_piece = square_occupied(x, y, Enemies)
            if dest_piece:
                if dest_piece in Friends[2]:  # black pieces list is second
                    return False
                dest_piece.isAlive = False

            self.pos.x = x * 100
            self.pos.y = y * 100
            self.selecting = False
            return True
        return False
    ######################## Black Knight ############################

    def BlackDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackKnight, (self.pos.x+10, self.pos.y))

    def BlackMove(self, mxpos, mypos, mouseDown, Enemies, Friends):
        self.update_rect()

        if self.KnightBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selecting = True
            return False
        
        if self.selecting and mouseDown:
            #print("hit")
            
            
            if self.TopMLeft.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.TopFLeft.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.TopMRight.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.TopFRight.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.BottomMLeft.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.BottomFLeft.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.BottomMRight.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            elif self.BottomFRight.collidepoint(mxpos, mypos) and mouseDown:
                x, y = int(mxpos // 100), int(mypos // 100)
            else:
                self.selecting = False
                return False

            if square_occupied(x, y, Friends):
                self.selecting = False
                return False
                
            dest_piece = square_occupied(x, y, Enemies)
            if dest_piece:
                if dest_piece in Friends[2]:  # black pieces list is second
                    return False
                dest_piece.isAlive = False

            self.pos.x = x * 100
            self.pos.y = y * 100
            self.selecting = False
            return True
        return False
    
####################################################### ROOKS ################################################################

class Rook(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
        self.RookBox = pygame.Rect(self.pos, self.size)
        self.RookBoxX = pygame.Rect(self.pos.x-8000, self.pos.y, 20000, 100)
        self.RookBoxY = pygame.Rect(self.pos.x, self.pos.y - 8000, 100, 20000)

    def update_rect(self):
        self.RookBox = pygame.Rect(self.pos, self.size)
        self.RookBoxX = pygame.Rect(self.pos.x-8000, self.pos.y, 20000, 100)
        self.RookBoxY = pygame.Rect(self.pos.x, self.pos.y - 8000, 100, 20000)
    #------------------------ Blue Rooks ---------------------------#

    def BlueDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlueRook, (self.pos.x + 10, self.pos.y, self.size.x, self.size.y))

    def BlueMove(self, mxpos, mypos, mouseDown, AllPieces):
        self.update_rect()

        if self.RookBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selecting = True
            return False

        if self.selecting and mouseDown:
            sx, sy = int(self.pos.x // 100), int(self.pos.y // 100)
            tx, ty = int(mxpos // 100), int(mypos // 100)

            dx, dy = tx - sx, ty - sy

            # Must move in a straight line (no diagonals)
            if dx != 0 and dy != 0:
                self.selecting = False
                return False

            #ai did the steps section
            step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

            # Check for pieces in the way
            x, y = sx + step_x, sy + step_y
            while (x, y) != (tx, ty):
                if square_occupied(x, y, AllPieces):
                    return False
                x += step_x
                y += step_y

            dest_piece = square_occupied(tx, ty, AllPieces)
            if dest_piece:
                # blue pieces are assumed to be AllPieces[0]
                if dest_piece in AllPieces[0] or dest_piece in AllPieces[2] or dest_piece in AllPieces[4] or dest_piece in AllPieces[6]:
                    return False
                dest_piece.isAlive = False  # capture

            self.pos.x = tx * 100
            self.pos.y = ty * 100
            self.selecting = False
            return True

        return False


    #------------------------ Black Rooks ---------------------------#

    def BlackDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackRook, (self.pos.x + 10, self.pos.y, self.size.x, self.size.y))
    
    def BlackMove(self, mxpos, mypos, mouseDown, AllPieces):
        self.update_rect()

        if self.RookBox.collidepoint(mxpos, mypos) and mouseDown:
            self.selecting = True
            return False

        if self.selecting and mouseDown:
            sx, sy = int(self.pos.x // 100), int(self.pos.y // 100)
            tx, ty = int(mxpos // 100), int(mypos // 100)

            dx, dy = tx - sx, ty - sy

            # Must move in a straight line (no diagonals)
            if dx != 0 and dy != 0:
                self.selecting = False
                return False

            #ai did the steps section
            step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

            # Check for pieces in the way
            x, y = sx + step_x, sy + step_y
            while (x, y) != (tx, ty):
                if square_occupied(x, y, AllPieces):
                    return False
                x += step_x
                y += step_y

            dest_piece = square_occupied(tx, ty, AllPieces)
            if dest_piece:
                # blue pieces are assumed to be AllPieces[0]
                if dest_piece in AllPieces[1] or dest_piece in AllPieces[3] or dest_piece in AllPieces[5] or dest_piece in AllPieces[7]:
                    return False
                dest_piece.isAlive = False  # capture

            self.pos.x = tx * 100
            self.pos.y = ty * 100
            self.selecting = False
            return True

        return False


class king(piece):
    def __init__(self, position, Size):
        super().__init__(position, Size)
        self.KingBox = pygame.Rect(self.pos, self.size)
        self.KingMBox = pygame.Rect(self.pos.x - 100, self.pos.y - 100, 300, 300)
        

    def update_rect(self):
        self.KingBox = pygame.Rect(self.pos, self.size)
        self.KingMBox = pygame.Rect(self.pos.x - 100, self.pos.y - 100, 300, 300)
    #--------------------------------Blue King-------------------------------#
    def BlueDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlueKing, (self.pos.x +10, self.pos.y, self.size.x, self.size.y))

    def BlueMove(self, mxpos, mypos, mouseDown, AllPieces, friends):
        self.update_rect()

        if self.KingBox.collidepoint(mxpos, mypos):
            self.selecting = True
            return False
    
        if self.selecting and mouseDown:
            sx, sy = int(self.pos.x // 100), int(self.pos.y // 100)
            tx, ty = int(mxpos // 100), int(mypos // 100)

            self.TopCheck = pygame.Rect((tx*100), (ty*100)-100, 100, 100)
            self.BottomCheck = pygame.Rect((tx*100), (ty*100)+100, 100, 100)
            self.LeftCheck = pygame.Rect((tx*100)-100, (ty*100), 100, 100)
            self.RightCheck = pygame.Rect((tx*100)+100, (ty*100), 100, 100)

            self.TopRight = pygame.Rect((tx*100)+100, (ty*100)-100, 100, 100)
            self.TopLeft = pygame.Rect((tx*100)-100, (ty*100)-100, 100, 100)
            self.BottomRight = pygame.Rect((tx*100)+100, (ty*100)+100, 100, 100)
            self.BottomLeft = pygame.Rect((tx*100)-100, (ty*100)+100, 100, 100)

            
            if square_occupied(tx, ty, friends):
                print("test")
                self.selecting = False
                return False

            if self.KingMBox.collidepoint(mxpos, mypos):
                #print(self.TopRight)
                # print(self.TopLeft)
                # print(self.BottomRight)
                # print(self.BottomLeft)
                if self.TopRight.collidepoint(mxpos, mypos):
                    print("right")
                    for j in AllPieces:
                        for i in j:
                            if self.TopCheck.colliderect(i.pos.x, i.pos.y, i.size.x, i.size.y) and self.RightCheck.colliderect(i.pos.x, i.pos.y, i.size.x, i.size.y):
                                print("print")
                                self.selecting = False
                                return False

                    self.pos.x = tx*100
                    self.pos.y = ty*100
                    return True
        return False
            


    #---------------------------------Black King-------------------------------#
    def BlackDraw(self, screen):
        self.update_rect()
        if self.isAlive:
            screen.blit(BlackKing, (self.pos.x +10, self.pos.y, self.size.x, self.size.y))

    

