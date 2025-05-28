import pygame
import sys
from map import Map
from pieces import Pawn, Bishop, Knight, Rook, king




pygame.init()
pygame.display.set_caption("Chess")
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()


def main():


    #pieces

    #---------------------------------------------------Pawns---------------------------------------------------#
    BluePawns = [Pawn((10,600), (80, 80)), Pawn((110,600), (80, 80)), Pawn((210,600), (80, 80)), Pawn((310,600), (80, 80)), Pawn((410,600), (80, 80)), Pawn((510,600), (80, 80)), Pawn((610,600), (80, 80)), Pawn((710,600), (80, 80))]
    BlackPawns = [Pawn((10,100), (80, 80)), Pawn((110,100), (80, 80)), Pawn((210,100), (80, 80)), Pawn((310,100), (80, 80)), Pawn((410,100), (80, 80)), Pawn((510,100), (80, 80)), Pawn((610,100), (80, 80)), Pawn((710,100), (80, 80))]
    #-------------------------------Bishops-------------------------------------------#
    BlueBishops = [Bishop((200, 700), (80, 96)), Bishop((500, 700), (80, 96))]
    BlackBishops = [Bishop((200, 0), (80, 96)), Bishop((500, 0), (80, 96))]
    #-----------------------------------Knights------------------------------------------#
    BlueKnights = [Knight((100, 700), (80, 96)), Knight ((600, 700), (80, 96))]
    BlackKnights = [Knight((100, 0), (80,96)), Knight((600, 0), (80, 96))]
    #-----------------------------------Rooks------------------------------------------#
    BlueRooks = [Rook((0, 700), (80, 96)), Rook ((700, 700), (80, 96))]
    BlackRooks = [Rook((0, 0), (80,96)), Rook((700, 0), (80, 96))]
    #-----------------------------------Rooks------------------------------------------#
    BlueKing = [king((400, 700), (80, 96))]
    BlackKing = [king((400, 0), (80,96))]

    AllPieces = [BluePawns, BlackPawns, BlueBishops, BlackBishops, BlueKnights, BlackKnights, BlueRooks, BlackRooks]
    BluePieces = [BluePawns, BlueBishops, BlueKnights, BlueRooks]
    BlackPieces = [BlackPawns, BlackBishops, BlackKnights, BlackRooks]
    #Mouse variables
    mxpos = 0
    mypos = 0
    mousePos = (mxpos, mypos)
    mouseDown = False


    #Turn
    turn = "Blue"


    running = True
    clock.tick(60)
    while running: #GAME LOOP####################################
        #event section------------------------------------
        for event in pygame.event.get():
            mouseX, mouseY = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
           


       


        if event.type == pygame.MOUSEMOTION:
            mousePos = event.pos


        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False


        keys = pygame.key.get_pressed()




        #print(BluePawns[0].PawnBox)
        #physics---------------------------------------------------

        #BluePieceMovement ##############################################################################
        if turn == "Blue":
            for i in BlackPawns:
                i.selected = False
            for i in BlackBishops:
                i.selected = False


            #pawns------------------------------------------------------------------------
            for i in BluePawns:
                #i.BlueCaptures(mouseX, mouseY, mouseDown, BlackPawns)
                if i.BlueMove(mouseX, mouseY, mouseDown, BlackPieces):
                    turn = "Black"
                    break

            #Bishops----------------------------------------------------------------------
            for i in BlueBishops:
                if i.BlueMove(mouseX, mouseY, mouseDown, AllPieces):
                    turn = "Black"
                    break

            #Knights-----------------------------------------------------------------------
            for i in BlueKnights:
                if i.BlueMove(mouseX, mouseY, mouseDown, BlackPieces, BluePieces):
                    turn = "Black"
                    break

            #Rooks-----------------------------------------------------------------------
            for i in BlueRooks:
                if i.BlueMove(mouseX, mouseY, mouseDown, AllPieces):
                    turn = "Black"
                    break
            #King-----------------------------------------------------------------------
            for i in BlueKing:
                if i.BlueMove(mouseX, mouseY, mouseDown, AllPieces, BluePieces):
                    turn = "Black"
                    break

        #BlackPiceMovement ####################################################################################
        if turn == "Black":
            for i in BluePawns:
                i.selected = False
            for i in BlueBishops:
                i.selecting = False
            #pawns-------------------------------------------------------------------------
            for i in BlackPawns:
                if i.BlackMove(mouseX, mouseY, mouseDown, BluePieces):
                    turn = "Blue"
                    break

            #Bishops -------------------------------------------------------------------------
            for i in BlackBishops:
                if i.BlackMove(mouseX, mouseY, mouseDown, AllPieces):
                    turn = "Blue"
                    break

            #Knights-----------------------------------------------------------------------
            for i in BlackKnights:
                if i.BlackMove(mouseX, mouseY, mouseDown, BluePieces, BlackPieces):
                    turn = "Blue"
                    break

            #Rooks-----------------------------------------------------------------------
            for i in BlackRooks:
                if i.BlackMove(mouseX, mouseY, mouseDown, AllPieces):
                    turn = "Blue"
                    break
        #Render section
       
        screen.fill((0, 0, 0))


        Map(screen)
       
       #Pawns
        for i in BluePawns:
            i.BlueDraw(screen)
        for i in BlackPawns:
            i.Blackdraw(screen)

        #Bishops
        for j in BlueBishops:
            j.BlueDraw(screen)
        for j in BlackBishops:
            j.BlackDraw(screen)

        #Knights
        for k in BlueKnights:
            k.BlueDraw(screen)
        for k in BlackKnights:
            k.BlackDraw(screen)

        #Rooks
        for g in BlueRooks:
            g.BlueDraw(screen)
        for g in BlackRooks:
            g.BlackDraw(screen)

        #Kings
        for t in BlueKing:
            t.BlueDraw(screen)
        for t in BlackKing:
            t.BlackDraw(screen)


        pygame.display.flip()


    #end of GAME LOOP##############################################
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
