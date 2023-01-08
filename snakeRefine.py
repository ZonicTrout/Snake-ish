# import pygame module in this program
import pygame
import random
import snakeDef
pygame.init()

run = True
# Run Setup Once
#   Initializing Fonts, Sprites, and Objects

game1 = snakeDef.Game(500, 500)
snek = snakeDef.Snake(20, 20, (255, 20, 147), game1)
app = snakeDef.Apple(10, 10, (0, 0, 0), game1)
screen = pygame.display.set_mode(game1.Borders)
pygame.display.set_caption("Snake")
timesRoman = pygame.font.SysFont("times new roman.ttf",  30)

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

    #   Checks whether apple is within range
    #   If so adds a game point and rerolls coordinates

    if snakeDef.withinRange((snek.coords[0], snek.coords[1]), (app.randCoords[0], app.randCoords[1]), 30):
        app.Eaten(game1)

    #   Direction Logic

    keys = pygame.key.get_pressed()

    if (snek.coords[0] < 0 or snek.coords[0] > game1.Borders[0] - snek.width):
        snakeDef.fullDeath(timesRoman, game1, screen, snek)
        continue

    if (snek.coords[1] < 0 or snek.coords[1] > game1.Borders[1] - snek.height):
        snakeDef.fullDeath(timesRoman, game1, screen, snek)
        continue

    for i in snek.usingFrames:
        if (snek.coords[0] <= (snek.usingFrames[i][0])+10 and snek.coords[0] >= (snek.usingFrames[i][0])-10):
            if (snek.coords[1] <= (snek.usingFrames[i][1])+10 and snek.coords[1] >= (snek.usingFrames[i][1])-10):
                snakeDef.fullDeath(timesRoman, game1, screen, snek)
                continue

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
        i+=1
        pygame.draw.rect(screen, (0, 0, 0), (snek.recordedCoords[game1.frameNum - (i*snek.veclocity)][0], snek.recordedCoords[game1.frameNum - (i*snek.veclocity)][1], snek.height, snek.width))
        snek.usingFrames.update({i: snek.recordedCoords[game1.frameNum - (i*snek.veclocity)]})

    pygame.draw.circle(screen, (255, 0, 0), app.randCoords, app.height)
    screen.blit(writeCoordsText, (0, 0))
    screen.blit(frameText, (0, 480))

    #   End of Loop Code

    pygame.display.update()

#   Clean Up

print("Goodbye!")