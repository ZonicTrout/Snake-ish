# import pygame module in this program
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
from snakeDef import *
pygame.init()



# Run Setup Once
#   Initializing Fonts, Sprites, and Objects

game1 = Game()
"""Game Object"""
wallData = Walls(game1, RGB=(255, 0, 255))
"""Wall Object"""
snek = Snake(20, 20, (255, 20, 147), game1, vel=5)
"""Snake Object"""
app = Apple(10, 10, (0, 0, 0), game1)
"""Apple Object"""
screen = pygame.display.set_mode(game1.Borders, pygame.RESIZABLE)
"""Screen Surface"""
pygame.display.set_caption(game1.windowName)
timesRoman = pygame.font.SysFont("times new roman.ttf",  30)
"""This Games Standard Font"""
run = True
"""Whether the main loop is running"""

# Run Game Loop

while run == True:

    #   Time delay in Milliseconds for anti-lag

    pygame.time.delay(10)
    game1.frameNum += 1
    tempCoords = snek.coords
    snek.recordedCoords.append(snek.coords.copy())

    #   Checks if player closes the window, and if so closes the application

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            game1.Borders = (event.w, event.h)

    #   Checks whether apple is within range
    #   If so adds a game point and rerolls coordinates

    if Misc.withinRange((snek.coords[0], snek.coords[1]), (app.randCoords[0], app.randCoords[1]), 30):
        app.Eaten(game1)

    #   Direction Logic


    if (snek.coords[0] < 0 or snek.coords[0] > game1.Borders[0] - snek.width):
        Misc.fullDeath(timesRoman, game1, screen, snek, wallData)
        continue

    if (snek.coords[1] < 0 or snek.coords[1] > game1.Borders[1] - snek.height):
        Misc.fullDeath(timesRoman, game1, screen, snek, wallData)
        continue


#       check Why withinRange Function does not work with it
    for i in snek.usingFrames:
        if (snek.coords[0] <= (snek.usingFrames[i][0])+9 and snek.coords[0] >= (snek.usingFrames[i][0])-9):
            if (snek.coords[1] <= (snek.usingFrames[i][1])+9 and snek.coords[1] >= (snek.usingFrames[i][1])-9):
                Misc.fullDeath(timesRoman, game1, screen, snek, wallData)
                continue
    
    keys = pygame.key.get_pressed()

    snek.Direction(keys)
    snek.Move()


    #   Rendering

    screen.fill((0, 165, 0))
    writeCoordsText = timesRoman.render(f'{snek.coords}\n{game1.points}', False, (255, 255, 255))
    frameText = timesRoman.render(f'{game1.frameNum}', False, (255, 255, 255))
    pygame.draw.rect(screen, snek.color, (snek.coords[0], snek.coords[1], snek.width, snek.height))


    if (game1.points == 0):
        snek.usingFrames = {}

    for i in range(game1.points):
    #   Data for Snake Body
        i+=1
        framesBack = int (i * ( ((snek.width + snek.height) / 2) /snek.veclocity ))

        pygame.draw.rect(screen, (0, 0, 0), (snek.recordedCoords[game1.frameNum - framesBack][0], snek.recordedCoords[game1.frameNum - framesBack][1], snek.height, snek.width))
        snek.usingFrames.update({i: snek.recordedCoords[game1.frameNum - framesBack]})

    if ( game1.points > len(wallData.wallCoordsList) ):
        wallData.wallCoordsList.append(wallData.newWall())

    for wallCoordinate in wallData.wallCoordsList:
        pygame.draw.rect(screen, wallData.color, (wallCoordinate[0], wallCoordinate[1], snek.height, snek.width))
        if Misc.withinRange(snek.coords, wallCoordinate, 20):
            Misc.fullDeath(timesRoman, game1, screen, snek, wallData)
            continue

    pygame.draw.circle(screen, (255, 0, 0), app.randCoords, app.height)
    screen.blit(writeCoordsText, (0, 0))
    screen.blit(frameText, (0, 480))

    #   End of Loop Code

    pygame.display.update()

#   Clean Up
print("Goodbye!")