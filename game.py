import Entity,Player,Room,pygame,Inventory,Items,Fonts,time,random,Save,os,Text,webbrowser

pygame.mixer.init()
pygame.init()

background_music = pygame.mixer.Sound('Sounds/background.wav')
damage_tags_delay = 67
damage_event = pygame.USEREVENT + 1
pygame.time.set_timer(damage_event, damage_tags_delay)

death_delay = 67
death_event = pygame.USEREVENT + 1
pygame.time.set_timer(death_event, death_delay)
window = None




isInMenu = True
isInSecondaryMenu = False
x = 450
y = 500
width = 100
height = 100
velocity = 20
inventorySlots = []
run = True
playerWalking = False
rects = []

map = None
player = None
playerInventory = None
currentRoom = None
debug = False
achievements = None
timeBeforeEnd = None





def start(name):

    global run, isInMenu, isInSecondaryMenu, window, timeBeforeEnd
    window = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Pixel Fight")
    pygame.display.set_icon(pygame.image.load("Entities/Player/Player_Idle_1.png"))
    while isInMenu:
        printMenu()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkMenuClick(name)
        pygame.time.delay(1)
        pygame.display.update()

    Text.printAchievement("talkedToKing")
    background_music.set_volume(0.02)
    background_music.play(-1)
    while run and not isInMenu:
        if Text.isDone("foundPrincess") or Text.isDone("hasDied"):
            if timeBeforeEnd == None:
                timeBeforeEnd = time.time()
            else:
                if time.time() - 5 > timeBeforeEnd:
                    isInMenu = True
                    run = False
                    timeBeforeEnd = None
                    start(name)
        window.fill((0, 0, 0))
        if not isInSecondaryMenu:
            window.blit(currentRoom.background, (0, 0))
            for entity in currentRoom.entities:
                entity.moveTowardsPlayer()
                entity.updateHealthBar()
                window.blit(entity.image, (entity.posX, entity.posY))
            window.blit(player.image, (player.posX, player.posY))
            player.updateHealthBar()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE] and not isInSecondaryMenu and not Inventory.inventoryOpen:
                    isInSecondaryMenu = True
                elif pygame.key.get_pressed()[pygame.K_ESCAPE] and isInSecondaryMenu:
                    window.blit(currentRoom.background, (0, 0))
                    isInSecondaryMenu = False
            if event.type == pygame.MOUSEBUTTONDOWN and isInSecondaryMenu:
                if checkSecondaryMenuClick():
                    return
            if not isInSecondaryMenu:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Inventory.inventoryClickItem(window, inventorySlots, playerInventory, player)
                if event.type == damage_event:
                    displayDamageTags()
                if event.type == death_event:
                    displayDeathEffect()
                    displayDropLoot()
                #To detect single KEYDOWN's
                if event.type == pygame.KEYDOWN:
                    pressed_key = pygame.key.get_pressed()
                    if pressed_key[pygame.K_i] and not Inventory.inventoryOpen:
                        Inventory.inventoryOpen = True
                    elif pressed_key[pygame.K_i] or pressed_key[pygame.K_ESCAPE] and Inventory.inventoryOpen:
                        Inventory.inventoryOpen = False
                    elif pressed_key[pygame.K_f]:
                        player.attack(currentRoom)

        if isInSecondaryMenu:
            window.fill((0, 0, 0))
            printSecondaryMenu()
            pygame.display.update()
            pygame.time.delay(60)
            continue
        keys = pygame.key.get_pressed()
        solid = currentRoom.solidSurfaces
        playerRect = pygame.Rect((player.posX + 70, player.posY + 90, 60, 90))
        checkIfShouldChangeRoom()




        Text.printTextTask(window)
        #KEYS MANAGEMENT (Can be used for continuous KEYDOWN)

        #Prevent player from moving if inventory is open.
        if not Inventory.inventoryOpen:
            if keys[pygame.K_LEFT]:
                if debug or not pygame.Rect((player.posX + 70 - velocity, player.posY + 90, 60, 90)).collidelist(rects) >= 0 and not isCollidingWithEntity(-velocity, 0) and player.posX > -90:
                    player.posX -= velocity
                player.lastDirection = "LEFT"
                player.setWalkFrame()
            if keys[pygame.K_RIGHT]:
                if debug or not pygame.Rect((player.posX + 70 + velocity, player.posY + 90, 60, 90)).collidelist(rects) >= 0 and not isCollidingWithEntity(velocity, 0) and player.posX < 880:
                    player.posX += velocity
                player.lastDirection = "RIGHT"
                player.setWalkFrame()
            if keys[pygame.K_UP]:
                if debug or not pygame.Rect((player.posX + 70, player.posY + 90 - velocity, 60, 90)).collidelist(rects) >= 0 and not isCollidingWithEntity(0, -velocity) and player.posY > -100:
                    if not player.lastDirection.__contains__("UP"):
                        player.lastDirection = player.lastDirection.replace("DOWN", "")  + "UP"
                    player.posY -= velocity
                player.setWalkFrame()
            if keys[pygame.K_DOWN]:
                if debug or not pygame.Rect((player.posX + 70, player.posY + 90 + velocity, 60, 90)).collidelist(rects) >= 0 and not isCollidingWithEntity(0, velocity * 2 + 10) and player.posY < 860:
                    if not player.lastDirection.__contains__("DOWN"):
                        player.lastDirection = player.lastDirection.replace("UP", "") + "DOWN"
                    player.posY += velocity
                player.setWalkFrame()
            if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
                player.setIdle()
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                player.setIdle()


        if Inventory.inventoryOpen:
            Inventory.printInventory(playerInventory, window, inventorySlots)
            Inventory.hoverInventoryItem(window, inventorySlots, playerInventory)
        pygame.time.delay(60)
        pygame.display.update()






quitRec = pygame.Rect((362, 520, 300, 70))
saveRec = pygame.Rect((362, 626, 300, 70))
def printSecondaryMenu():
    menu = pygame.image.load('Images/secondarymenu.png')
    menu = pygame.transform.scale(menu, (1010, 1010))

    window.blit(menu, (0,0))
    if quitRec.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, (255, 0 , 0), quitRec, 10)
    if saveRec.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, (255, 0, 0), saveRec, 10)

def checkSecondaryMenuClick():
    global isInSecondaryMenu
    if quitRec.collidepoint(pygame.mouse.get_pos()):
        pygame.quit()
        return True
    if saveRec.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, (255, 255, 0), saveRec)
        Save.Save(player, map, playerInventory, map.index(currentRoom))
        isInSecondaryMenu = False



newGameRec = pygame.Rect((355, 520, 300, 70))
loadGameRec = pygame.Rect((355, 626, 300, 70))
aboutRec = pygame.Rect((365, 737, 134, 52))
exitRec = pygame.Rect((510, 737, 134, 52))
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def printMenu():
    window.fill((0,0,255))
    menu = pygame.image.load('Images/menu.png')
    menu = pygame.transform.scale(menu, (1010, 1010))
    window.blit(menu, (0,0))
    if newGameRec.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, (255, 0 , 0), (355, 520, 300, 70), 10)
    if not os.path.isfile("Saves/playerData"):
        draw_rect_alpha(window, (0, 119,136,153), loadGameRec)
    elif loadGameRec.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, (255, 0, 0), loadGameRec, 10)
    if aboutRec.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, (255, 0, 0), aboutRec, 10)
    if exitRec.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, (255, 0, 0), exitRec, 10)


#Used to check if user is clicking on buttons in the Main game menu.
def checkMenuClick(name):
    global isInMenu, run
    if newGameRec.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, (255, 255, 0), newGameRec)
        loadData(True, name)
        isInMenu = False
        run = True

    if loadGameRec.collidepoint(pygame.mouse.get_pos()) and os.path.isfile("Saves/playerData"):
        pygame.draw.rect(window, (255, 255, 0), loadGameRec)
        loadData(False, "")
        isInMenu = False
    if aboutRec.collidepoint(pygame.mouse.get_pos()):
        #Open browser to go to Github repo.
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        url = 'https://github.com/Strvm/Pixel-Fight'
        webbrowser.get(chrome_path).open(url)
    if exitRec.collidepoint(pygame.mouse.get_pos()):
        pygame.quit()




#Used to load data to either start a new game or load a previous game session.
def loadData(newGame, name):
    global map, player, playerInventory, currentRoom, debug, achievements ,timeBeforeEnd
    map = None
    player = None
    playerInventory = None
    currentRoom = None
    debug = False
    achievements = None
    timeBeforeEnd = None
    pygame.init()
    # global map, player, playerInventory, currentRoom
    if newGame:
        Text.reset()
        player = Player.Player(name,1, 0, 100, 4, x, y, velocity, "Entities/Player/Player_Idle_1.png", 1, "RIGHT", Text.achievements, window)
        playerInventory = Inventory.Inventory(player.name + "'s Inventory", 12, [], player)
        playerInventory.contents = []

        map = [Room.Room("Middle Room", "Images/map_middle.png", [Entity.getEntityByName("largemushroom", 550, 150, player, playerInventory, window), Entity.getEntityByName("Troll", 650, 150, player, playerInventory, window)], 0, "MIDDLE",["WEST", "EAST", "SOUTH", "NORTH"], [(260, 15), (280, 15), (300, 15), (320, 15), (340, 15), (360, 15), (380, 15), (400, 15), (420, 15), (440, 15), (660, 15), (700, 15), (740, 15), (780, 15), (820, 15), (860, 15), (460, 15), (480, 15), (880, 15), (240, 235), (240, 255), (260, 255), (280, 255), (800, 275), (840, 275), (880, 275), (800, 235), (860, 235), (440, 610), (460, 610), (720, 775), (740, 695), (760, 775), (760, 675), (820, 675), (780, 755), (820, 755), (860, 755), (860, 675), (800, 635), (880, 715), (140, 635), (100, 635), (60, 635), (20, 635), (140, 315), (160, 315), (80, 275), (60, 275), (40, 275), (100, 295)]),
        Room.Room("First West Point", "Images/map-west.png", [Entity.getEntityByName("Bear", 350, 200, player, playerInventory, window)], 1,"WEST",["EAST"], [(800, 535), (820, 535), (760, 595), (740, 675), (660, 695), (640, 695), (620, 695), (580, 715), (560, 715), (460, 735), (440, 735), (380, 715), (340, 715), (260, 735), (240, 735), (160, 715), (140, 655), (100, 655), (100, 575), (100, 495), (80, 415), (80, 335), (80, 275), (100, 195), (120, 75), (120, 95), (140, 95), (140, 55), (240, 55), (240, 75), (260, 75), (340, 75), (380, 75), (340, 15), (380, 15), (260, 15), (220, 15), (460, 55), (500, 55), (560, 55), (580, 55), (580, 75), (560, 75), (540, 75), (680, 35), (680, 55), (700, 55), (760, 135), (780, 135), (800, 195), (800, 215), (840, 215), (840, 175), (800, 115), (720, 15), (800, 595), (780, 695), (40, 255), (60, 195), (100, 55), (40, 415), (60, 535)]),
                 Room.Room("First East Point", "Images/map-est.png", [], 2, "EAST",["WEST"], [(30, 235), (50, 215), (50, 235), (70, 235), (90, 235), (110, 175), (90, 95), (50, 95), (150, 195), (150, 215), (170, 195), (190, 175), (210, 135), (210, -5), (210, 35), (230, 55), (250, -25), (250, 15), (270, 15), (70, 715), (90, 715), (110, 655), (90, 675), (110, 715), (130, 715), (130, 695), (150, 715), (150, 775), (190, 775), (170, 775), (210, 795), (170, 835), (910, 815), (890, 855), (930, 855), (530, 395), (550, 395), (570, 395), (590, 395), (510, 455), (490, 475), (630, 475), (650, 475), (590, 335), (570, 335), (550, 335), (510, 335), (530, 335), (490, 335), (610, 335), (630, 335), (650, 335), (570, 415)]),
                 Room.Room("First South Point", "Images/map-south.png", [Entity.getEntityByName("bandit", 670, 190, player, playerInventory, window)], 3, "SOUTH",["MIDDLE"], [(360, 715), (380, 715), (400, 715), (340, 715), (300, 715), (260, 715), (320, 715), (240, 715), (200, 715), (200, 595), (200, 455), (200, 495), (200, 355), (200, 255), (200, 195), (220, 95), (220, 115), (240, 115), (260, 115), (280, 115), (300, 115), (340, 115), (360, 115), (380, 115), (400, 115), (420, 115), (440, 115), (460, 115), (500, 115), (480, 115), (520, 115), (560, 115), (580, 115), (620, 115), (660, 115), (700, 115), (740, 115), (780, 115), (800, 115), (800, 215), (800, 315), (800, 395), (800, 495), (800, 595), (800, 695), (780, 735), (780, 715), (760, 715), (720, 715), (680, 715), (640, 715), (620, 715), (600, 715), (500, 435), (500, 455), (520, 455), (560, 455), (480, 455), (460, 455), (580, 455), (540, 435), (380, 315), (400, 315), (420, 315), (440, 315), (460, 315), (520, 315), (540, 315), (560, 315), (580, 315), (600, 315)]),
               Room.Room("Starting Map", "Images/map-north (1).png", [Entity.getEntityByName("largemushroom", 750, 50, player, playerInventory, window), Entity.getEntityByName("largemushroom", 770,770, player, playerInventory, window), Entity.getEntityByName("largemushroom", 700, 740, player, playerInventory, window)], 3, "NORTH",["SOUTH"], [(300, 695), (380, 715), (320, 655), (240, 675), (260, 695), (180, 655), (220, 695), (140, 695), (120, 655), (80, 675), (60, 755), (40, 795), (80, 815), (120, 815), (160, 815), (220, 815), (260, 835), (320, 795), (300, 835), (380, 495), (400, 495), (400, 375), (400, 235), (580, 235), (580, 355), (580, 475), (580, 495), (620, 495), (660, 495), (700, 495), (740, 495), (800, 495), (780, 495), (860, 495), (820, 495), (900, 495), (940, 495), (980, 495), (620, 235), (660, 235), (700, 235), (760, 235), (800, 235), (840, 235), (880, 235), (920, 235), (960, 235), (980, 235), (320, 235), (360, 235), (260, 235), (180, 235), (220, 235), (280, 235), (140, 235), (100, 235), (40, 235), (60, 235), (40, 355), (40, 455), (40, 495), (60, 495), (100, 495), (140, 495), (180, 495), (220, 495), (260, 495), (300, 495), (340, 495), (220, 35), (180, 35), (200, 35)])]
        currentRoom = map[4]

    else:
        player = Save.loadPlayer(window)
        achievements = Text.achievements
        playerInventory = Save.loadInventory(player)
        map = Save.loadRooms(player, playerInventory, window)
        currentRoom = map[Save.loadCurrentRoom()]
    setSolid()


#Used to check if room should be changed depending on the player's position.
def checkIfShouldChangeRoom():
    global currentRoom
    if currentRoom.name.__contains__("Starting"):
        if (player.posX >= 330 and player.posX <= 450) and player.posY <= -95 and "SOUTH" in currentRoom.allowedDirections:
            player.posY = 820
            player.posX = 490
            currentRoom = getMapByDirection("MIDDLE")
            Entity.spawnRandomEntities(currentRoom, player, playerInventory, window, False)
            Text.printAchievement("travelledMiddle")
    elif currentRoom.name.__contains__("Middle"):
        if player.posX <= -70 and (player.posY >= 320 and player.posY <= 420) and "WEST" in currentRoom.allowedDirections:
            Text.printAchievement("travelledWest")
            currentRoom = getMapByDirection("WEST")
            player.posX = 870
            Entity.spawnRandomEntities(currentRoom, player, playerInventory, window, False)
            player.posY = player.posY - 45
        elif player.posX >= 880 and (player.posY >= 320 and player.posY <= 420) and "EAST" in currentRoom.allowedDirections:
            currentRoom = getMapByDirection("EAST")
            player.posX = -60
            Entity.spawnRandomEntities(currentRoom, player, playerInventory, window, False)
            if Text.isDone("foundThreeNecklace"):
                boss = Entity.getEntityByName("Golem", 750, 300, player, playerInventory, window)
                boss.room = currentRoom
                currentRoom.entities.append(boss)
        elif (player.posX >= 430 and player.posX <= 530) and player.posY <= -40 and "SOUTH" in currentRoom.allowedDirections:
            player.posY = 500
            player.posX = 430
            Text.printAchievement("travelledSouth")
            currentRoom = getMapByDirection("SOUTH")
            Entity.spawnRandomEntities(currentRoom, player, playerInventory, window, False)
        elif (player.posX >= 410 and player.posX <= 550) and player.posY >= 840 and "NORTH" in currentRoom.allowedDirections:
            player.posY = -80
            player.posX = 390
            currentRoom = getMapByDirection("NORTH")
            Entity.spawnRandomEntities(currentRoom, player, playerInventory, window, False)
    else:
        if player.posX <= -70 and (player.posY >= 320 and player.posY <= 420) and "WEST" in currentRoom.allowedDirections:
            currentRoom = getMapByDirection("MIDDLE")
            player.posX = 870
        elif player.posX >= 860 and (player.posY >= 200 and player.posY <= 335) and "EAST" in currentRoom.allowedDirections:
            currentRoom = getMapByDirection("MIDDLE")
            player.posX = -30
            player.posY = player.posY + 45
            Entity.spawnRandomEntities(currentRoom, player, playerInventory, window, False)
        elif (player.posX >= 430 and player.posX <= 530) and player.posY <= -40 and "SOUTH" in currentRoom.allowedDirections:
            player.posY = 480
            currentRoom = getMapByDirection("MIDDLE")
            Entity.spawnRandomEntities(currentRoom, player, playerInventory, window, False)
        elif player.posY >= 810 and (player.posX >= 350 and player.posX <= 470) and "MIDDLE" in currentRoom.allowedDirections:
            player.posY = -50
            player.posX = 480
            currentRoom = getMapByDirection("MIDDLE")
            Entity.spawnRandomEntities(currentRoom, player, playerInventory, window, False)
    setSolid()


def getMapByDirection(direction):
    for room in map:
        if room.direction == direction:
            return room


#Used to check if two entities are colliding.
def isCollidingWithEntity(x, y):
    playerRect = pygame.Rect((player.posX + 85 + x, player.posY + 120 + y, 30, 40))
    for entity in currentRoom.entities:
        if playerRect.colliderect(entity.hitbox):
            return True
    return False


#Used to display damage tags when hitting an entity.
def displayDamageTags():
    for tag in Entity.dmgTags:
        textsurface = Fonts.bigFont.render(str(tag[0]), False, tag[4])
        window.blit(textsurface, (tag[1], tag[2]))
        if time.time() - 1 > tag[3]:
            Entity.dmgTags.remove(tag)

#Used to death "blood" when entity dies.
def displayDeathEffect():
    for tag in Entity.deathBlood:
        for x in range(15):
            #pygame.draw.rect(window, (138, 3, 3), (tag[1] + random.randint(10, 110), tag[2] + (tag[2] / 4) + random.randint(10, 70), 5, 5))
            pygame.draw.rect(window, (138, 3, 3), (tag[1] + random.randint(10, 110), tag[2] + random.randint(10, 70), 5, 5))

        if time.time() - 0.5 > tag[3] - 0.25:
            Entity.deathBlood.remove(tag)

#Used to display entity drop loot.
def displayDropLoot():
    for item in Entity.droppedItems:
        window.blit(item[0], (item[1], item[2]))
        if time.time() - 1.5 > item[3] - 0.25:
            Entity.droppedItems.remove(item)

#Sets the current room solid object, to create collisions after.
def setSolid():
    rects.clear()
    for solid in currentRoom.solidSurfaces:
        rect = pygame.Rect((solid), (10, 101))
        rects.append(rect)



#Fake RPG joke.
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format
import random
import string
def startFakeRpg():
    print("MAIN MENU:")
    print("1. Create New Game")
    print("2. Load Saved Game")
    print("3. About")
    print("4. Exit")
    name = input("> What is your name: ")
    input("> King: Hello " + name + ". I am seeking you help, are you willing to help me?")
    input("> King: Great! Ok l网络isten carefullקוםy")
    input("> Kந்ng: Caந்n you heந்ar me??l网ந்?!")
    os.system('color a')
    os.system('dir/s')
    cprint(figlet_format('PIXEL FIGHT', font='starwars'),
           'yellow', 'on_red', attrs=['bold'])

    start(name)

#startFakeRpg()

start("name")

