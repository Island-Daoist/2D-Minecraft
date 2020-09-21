import pygame, sys, random
from pygame.locals import *



#constants representing colours
BLACK = (0, 0, 0)
BROWN = (153, 76, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (125, 125, 125)
WHITE = (255, 255, 255)

#constants representing the different resouces
DIRT = 0
GRASS = 1
WATER = 2
COAL = 3
CLOUD = 4
WOOD = 5
FIRE = 6
SAND = 7
GLASS = 8
ROCK = 9
STONE = 10
BRICK = 11
DIAMOND = 12

#a dictionary linking resources to colours
textures = {
    DIRT: pygame.image.load('graphics/dirt.png'),
    GRASS: pygame.image.load('graphics/grass.png'),
    WATER: pygame.image.load('graphics/water.png'),
    COAL: pygame.image.load('graphics/coal.png'),
    CLOUD: pygame.image.load('graphics/cloud.png'),
    WOOD: pygame.image.load('graphics/wood.png'),
    FIRE: pygame.image.load('graphics/fire.png'),
    SAND: pygame.image.load('graphics/sand.png'),
    GLASS: pygame.image.load('graphics/glass.png'),
    ROCK: pygame.image.load('graphics/rock.png'),
    STONE: pygame.image.load('graphics/stone.png'),
    BRICK: pygame.image.load('graphics/brick.png'),
    DIAMOND: pygame.image.load('graphics/diamond.png')
}

#a dictionary containing the player's inventory
inventory = {
    DIRT: 0,
    GRASS: 0,
    WATER: 0,
    COAL: 0,
    WOOD: 0,
    FIRE: 0,
    SAND: 0,
    GLASS: 0,
    ROCK: 0,
    STONE: 0,
    BRICK: 0,
    DIAMOND: 0
}

#maps each resource to the EVENT key used to place/craft it
controls = {
    DIRT: 49,
    GRASS: 50,
    WATER: 51,
    COAL: 52,
    WOOD: 53,
    FIRE: 54,
    SAND: 55,
    GLASS: 56,
    ROCK: 57,
    STONE: 48,
    BRICK: 45,
    DIAMOND: 61
}

craft = {
    FIRE: {WOOD: 2, ROCK: 2},
    STONE: {ROCK: 2},
    GLASS: {FIRE: 1, SAND: 2},
    DIAMOND: {WOOD: 2, COAL: 3},
    BRICK: {ROCK: 2, FIRE: 1},
    SAND: {ROCK: 2}
}

#useful game dimensions
TILESIZE = 40
MAPWIDTH = 25
MAPHEIGHT = 15

#list of resources
resources = [DIRT, WATER, GRASS, COAL, WOOD, FIRE, SAND, GLASS, ROCK, STONE, BRICK, DIAMOND]
#use list comprehension to create our tilemap
tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ]

#setup the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + 50))

INVFONT = pygame.font.Font('fonts/freesansbold.ttf', 18)

#the player image
player = pygame.image.load('graphics/player.png').convert_alpha()
#the position of player's x, y coordinates
playerPos = [0, 0]

#cloud position
cloudx = -200
cloudy = 0

#loop through each row
for rw in range(MAPHEIGHT):
    #loop through each column
    for cl in range(MAPWIDTH):
        #pick a random number between 0 and 15
        randomNumber = random.randint(0, 15)
        #if a zero, then the tile is coal
        if randomNumber == 0:
            tile = COAL
        #water if the random number of 1 or 2
        elif randomNumber == 1 or randomNumber == 2:
            tile = WATER
        elif randomNumber >= 3 and randomNumber <= 7:
            tile = GRASS
        else:
            tile = DIRT
        #set the position in the tilemap to the random tile
        tilemap[rw][cl] = tile

pygame.display.set_caption('M I N E C R A F T -- 2D')
pygame.display.set_icon(pygame.image.load('grahpics/player.png'))
fpsClock = pygame.time.Clock()

while True:

    #get all the user events
    for event in pygame.event.get():
        #if user wants to quit
        if event.type == QUIT:
            #end the game and window
            pygame.quit()
            sys.exit()

        #if a key is pressed
        elif event.type == KEYDOWN:
            #if the right arrow is pressed
            if event.key == K_RIGHT and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                playerPos[0] += 1
            #if the left arrow is pressed
            elif event.key == K_LEFT and playerPos[0] > 0:
                #change the player's x position
                playerPos[0] -= 1
            #if the up arrow is pressed
            elif event.key == K_UP and playerPos[1] > 0:
                #change the player's y position
                playerPos[1] -= 1
            #if the down arrow is pressed
            elif event.key == K_DOWN and playerPos[1] < MAPHEIGHT - 1:
                #change player's y position
                playerPos[1] += 1

            #if the space key is pressed
            elif event.key == K_SPACE:
                #find what resource the player is standing on
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                #add that resource to player inventory
                inventory[currentTile] += 1
                #change tile player is standing on to dirt
                tilemap[playerPos[1]][playerPos[0]] = DIRT

            #controls for interacting with game
            for key in controls:
                #if this key was pressed
                if event.key == controls[key]:

                    #craft if the mouse button is also pressed
                    if pygame.mouse.get_pressed()[0]:
                        #if the item can be crafted
                        if key in craft:
                            #keep track of whether we have the resources to craft this item
                            canBeMade = True
                            #for each item needed to craft ...
                            for i in craft[key]:
                                # ... if we don't have enough materials
                                if craft[key][i] > inventory[i]:
                                    canBeMade = False
                                    break
                            #if we can craft it (we have all the needed resources
                            if canBeMade == True:
                                #take each item from the inventory
                                for i in craft[key]:
                                    inventory[i] -= craft[key][i]
                                #add crafted item to inventory
                                inventory[key] += 1

                    else:
                        #get the tile the player is standing on
                        currentTile = tilemap[playerPos[1]][playerPos[0]]
                        #if we have the item in our inventory
                        if inventory[key] > 0:
                            #take it from the inventory
                            inventory[key] -= 1
                            #swap it with the tile we are standing on
                            inventory[currentTile] += 1
                            #place the tile down
                            tilemap[playerPos[1]][playerPos[0]] = key

    #clear screen by blacking it out
    DISPLAYSURF.fill(BLACK)

    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))

    #display the cloud
    DISPLAYSURF.blit(textures[CLOUD].convert_alpha(), (cloudx, cloudy))
    #move the cloud to the left slightly
    cloudx += 1
    #if the cloud has moved past the map
    if cloudx > MAPWIDTH*TILESIZE:
        #pick a new position to place the cloud
        cloudy = random.randint(0, MAPHEIGHT*TILESIZE)
        cloudx = -200

    #display the inventory, starting 10 pixels in
    placePosition = 10
    for item in resources:
        #add the image
        DISPLAYSURF.blit(textures[item], (placePosition, MAPHEIGHT*TILESIZE+15))
        placePosition += 30
        #add the text showing the amount in the inventory
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+15))
        placePosition += 50

    #draw the player on the screen
    DISPLAYSURF.blit(player, (playerPos[0]*TILESIZE+5, playerPos[1]*TILESIZE+5))

    #update the display
    pygame.display.update()
    fpsClock.tick(24)
