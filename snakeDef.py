import random
import pygame
#   Defines Game and Member variables
#   Used for Game-wide Variables like points

class Game:
    def __init__(self, x = 500, y = 500) -> None:
        self.Borders = (x, y)
        self.points = 0
        self.highScore = 0 # Fill this with a read file for High Score saves
        self.frameNum = 0
    def Restart(self):
        pass
#   Defines Walls and Member variables
#   Used for random generation of Obstacles

class Walls:
    def __init__(self, x, y, RGB) -> None:
        self.coords = (x, y)
        self.color = RGB

#   Defines Snake and Member variables
#   Used for Snake-related variables like size and color

class Snake:
    def __init__(self, h, w, RGB, gameself, vel = 5, rows = 5) -> None:
        self.height = h
        self.width = w
        self.color = RGB
        self.coords = [(gameself.Borders[0] + w) / 2, (gameself.Borders[1] + h) / 2]
        self.veclocity = vel
        self.dir = "None"
        self.rows = rows
        self.gameself = gameself
        self.recordedCoords = []
        self.usingFrames = {}

    #   The Die function resets points and coords

    def Die(self):
        self.gameself.points = 0
        self.dir = "None"
        self.coords = [self.gameself.Borders[0] / 2, self.gameself.Borders[1] / 2]
    
    def Lose(self):
        pass

    def Direction(self, keys):
        if keys[pygame.K_LEFT] and self.dir != "Right" and (self.coords[0] % self.rows == 0):
            self.dir = "Left"

        if keys[pygame.K_RIGHT] and self.dir != "Left" and (self.coords[0] % self.rows == 0):
            self.dir = "Right"

        if keys[pygame.K_UP] and self.dir != "Down" and (self.coords[1] % self.rows == 0):
            self.dir = "Up"

        if keys[pygame.K_DOWN] and self.dir != "Up" and (self.coords[1] % self.rows == 0):
            self.dir = "Down"
        

    def Move(self):
        if self.dir == "Right": #and (self.coords[0] < self.gameself.Borders[0] - self.width):
            self.coords[0] += self.veclocity

        if self.dir == "Left": # and (self.coords[0] > 0):
            self.coords[0] -= self.veclocity
        
        if self.dir == "Up": # and (self.coords[1] > 0):
            self.coords[1] -= self.veclocity
        
        if self.dir == "Down": # and (self.coords[1] < self.gameself.Borders[1] - self.height):
            self.coords[1] += self.veclocity

            
#   Defines Apple and Member variables
#   Used for Apple-related variables like size, color, and location

class Apple:
    def __init__(self, h, w, RGB, gameself) -> None:
        self.height = h
        self.width = w
        self.color = RGB
        self.randCoords = (random.randint(20, gameself.Borders[0]-20), random.randint(20, gameself.Borders[1]-20))
    def createApple(h, w, RGB, gameself):
        height = h
        width = w
        color = RGB
        randCoords = (random.randint(0, gameself.Borders[0]), random.randint(0, gameself.Borders[1]))

    #   The Eaten function adds to points and re-rolls coordinates

    def Eaten(self, gameself):
        gameself.points += 1
        self.randCoords = (random.randint(0, gameself.Borders[0]), random.randint(0, gameself.Borders[1]))

def withinRange(inp, benchmark, closeness = 10):
    if (inp[0] <= benchmark[0] + closeness and inp[0] >= benchmark[0] - closeness):
        if (inp[1] <= benchmark[1] + closeness and inp[1] >= benchmark[1] - closeness):
            return True
    return False

def fullDeath(font, gameself, screen, Snak):
    LoseText = font.render(f'You Lose\n Points {gameself.points}', False, (255, 255, 255))
    screen.blit(LoseText, (250, 0))
    pygame.display.update()
    pygame.time.delay(3000)
    Snak.Die()