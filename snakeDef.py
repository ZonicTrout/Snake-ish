import random
import pygame
import json
#   Defines Game and Member variables
#   Used for Game-wide Variables like points

class Game:
    """Contains Game-Related member variables and functions like points, and setting the json file"""
    Borders = (0, 0)
    points = 0
    highScore = 0 # Fill this with a read file for High Score saves
    frameNum = 0
    windowName = ""
    playerName = ""

    def __init__(self) -> None:
        """Initializing Reads config.json file and Distributes values into member variables"""
        with open("config.json", "r") as configJsonFile:
            configJsonText = configJsonFile.read()
            configText = json.loads(configJsonText)
            self.Borders = (configText["X Border"], configText["Y Border"])
            self.highScore = configText["High Score"]
            self.windowName = configText["Window Name"]
            self.playerName = configText["Player Name"]
            
    def setJson(self) -> None:
        """Writes to json file using open()"""
        with open("config.json", "w") as configJsonFile:
            infoDictionary = {
                "High Score": self.points if self.points > self.highScore else self.highScore, 
                "Player Name": "Anonymous", "Window Name": "Snake", 
                "X Border": self.Borders[0], "Y Border": self.Borders[1]
            }
            infoJson = json.dumps(infoDictionary, sort_keys=True)
            configJsonFile.write(infoJson)
    

#   Defines Walls and Member variables
#   Used for random generation of Obstacles

class Walls:
    """Contains Wall-related meber variables and functions"""
    wallCoordsList = []
    """List of Wall Coordinates [x, y]"""
    def __init__(self, gameself: Game, RGB: tuple[int, int, int] = (255, 0, 255)) -> None:
        self.color = RGB
        self.gameself = gameself

    def newWall(self) -> tuple[int, int]:
        """Creates values for new Walls and returns them in a tuple(x, y)"""
        DivideByTenL = int(self.gameself.Borders[0]/10)
        DivideByTenW = int(self.gameself.Borders[1]/10)
        return (random.randint(0, DivideByTenL * 10), random.randint(0, DivideByTenW * 10))


#   Defines Snake and Member variables
#   Used for Snake-related variables like size and color

class Snake:
    def __init__(self, h: int, w: int, RGB: tuple[int, int, int], gameself: Game, vel: int = 5) -> None:
        """Assigns member variables to heights, width, color (RGB)"""
        self.height = h
        self.width = w
        self.color = RGB
        self.coords: list[float, float] = [(gameself.Borders[0] + w) / 2, (gameself.Borders[1] + h) / 2]
        self.veclocity = vel
        self.dir = "None"
        self.gameself:Game = gameself
        self.recordedCoords = []
        self.usingFrames:dict = {}

    #   The Die function resets points and coords

    def Die(self) -> None:
        """Resets Snake-Related Items"""
        self.dir = None
        self.coords = [self.gameself.Borders[0] / 2, self.gameself.Borders[1] / 2]
        self.gameself.setJson()
        self.gameself.points = 0


    def Direction(self, keys) -> None:
        """If-else Chain deciding what direction the snake should go"""
        if (keys[pygame.K_LEFT] or keys[pygame.K_a])and self.dir != "Right":
            self.dir = "Left"

        if (keys[pygame.K_RIGHT]or keys[pygame.K_d]) and self.dir != "Left":
            self.dir = "Right"

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.dir != "Down":
            self.dir = "Up"

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.dir != "Up":
            self.dir = "Down"
        

    def Move(self) -> None:
        """Moves the Snake in the direction set by Snake.Direction()"""
        if self.dir == "Right":
            self.coords[0] += self.veclocity

        if self.dir == "Left":
            self.coords[0] -= self.veclocity
        
        if self.dir == "Up":
            self.coords[1] -= self.veclocity
        
        if self.dir == "Down":
            self.coords[1] += self.veclocity

    def changeVelocity(self, keys) -> None:
        if keys[pygame.K_PERIOD]:
            if self.veclocity > 1 and self.veclocity <= 20:
                self.veclocity += 1

        if keys[pygame.K_COMMA]:
            if self.veclocity > 1 and self.veclocity <= 20:
                self.veclocity -= 1

            
#   Defines Apple and Member variables
#   Used for Apple-related variables like size, color, and location

class Apple:
    def __init__(self, h, w, RGB: tuple[int, int, int], gameself: Game) -> None:
        """Create Apple instance and assign dimensions"""
        self.height = h
        self.width = w
        self.color:tuple[int, int, int] = RGB
        self.gameself:Game = gameself
        self.randCoords = (random.randint(20, gameself.Borders[0]-20), random.randint(20, gameself.Borders[1]-20))

    #   The Eaten function adds to points and re-rolls coordinates

    def Eaten(self, gameself: Game) -> None:
        """Adds 1 to Game.points and resets Apple coordinates to random intergers"""
        gameself.points += 1
        self.randCoords = (random.randint(20, gameself.Borders[0]-20), random.randint(20, gameself.Borders[1]-20))

class Server:
    """Deals with flask Server"""

    test = None
    def runServer() -> None:
        """Using the import keyword, imports and runs the server.py file"""
        import server

# Checks if within range

class Misc: # Miscellanous Funtions
    """These are functions that either have no clear Catergory to fit into or are not yet Catergorized"""

    def withinRange(inp: list[int, int], benchmark: list[int, int], closeness: int = 10) -> bool:
        """Checks whether two lists with two items each are within range of closeness (default is 10)\n
        Returns a boolean value"""
        firstCheck: bool = (inp[0] <= benchmark[0] + closeness and inp[0] >= benchmark[0] - closeness)
        secondCheck: bool = (inp[1] <= benchmark[1] + closeness and inp[1] >= benchmark[1] - closeness)
        return firstCheck and secondCheck

    def fullDeath(font:pygame.font.Font, gameself: Game, screen: pygame.Surface, Snak: Snake, Walls: Walls) -> None:
        """Causes inputed Snake instance to use the Die() method and set dir to None, resets Game.points displays LoseText for 
        3000 milliseconds"""

        LoseText = font.render(f'You Lose\n Points {gameself.points}', False, (255, 255, 255))
        screen.blit(LoseText, (250, 0))
        Walls.wallCoordsList = []
        pygame.display.update()
        pygame.time.delay(3000)
        Snak.dir = None
        Snak.Die()