import pygame



def Map(screen):
    map1 = [[0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]]
    for i in range(8):
        for j in range(8):
            if map1[i][j] == 1:
                pygame.draw.rect(screen,(30,144,255), (i*100, j*100, 100, 100))
            elif map1[i][j] == 0:
                pygame.draw.rect(screen,(64,64,64), (i*100, j*100, 100, 100))
