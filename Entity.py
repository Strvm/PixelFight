import pygame
import time
import random
import Text
import Items
import Inventory

pygame.mixer.init()
entity_hit = pygame.mixer.Sound('Sounds/flesh_hit.wav')
ogre_growl = pygame.mixer.Sound('Sounds/ogre_growl.wav')
bear_attack = pygame.mixer.Sound('Sounds/bear_attack.wav')
bandit_dagger = pygame.mixer.Sound('Sounds/bandit_dagger.wav')
golem_hit = pygame.mixer.Sound('Sounds/golem_hit.wav')

necklaceCount = 0
dmgTags = []
deathBlood = []
droppedItems = []
availableEntities = ["Troll", "Bandit", "Bear", "LargeMushroom"]

#Used to create monsters/entities
class Entity:
    def __init__(self, name, image,  health, maxHealth, speed, attackDamage, attackSpeed, shield, isAgressive, posX, posY, lastDirection, player, walkStep, width, height, plusX, plusY,plusHeight, plusWidth, itemDrop, playerInventory, window):
        img = pygame.image.load("Entities/" + image + "/" + image  + "_Idle_1.png")
        img = pygame.transform.scale(img, (width, height))
        self.plusWidth = plusWidth
        self.name = name
        self.imagePath = image
        self.health = health
        self.maxHealth = maxHealth
        self.attackDamage = attackDamage
        self.shield = shield
        self.isAgressive = isAgressive
        self.image = img
        self.posX = posX
        self.playerInventory = playerInventory
        self.posY = posY
        self.plusX = plusX
        self.itemDrop = itemDrop
        self.plusY = plusY
        self.lastDirection = lastDirection
        self.player = player
        self.walkStep = walkStep
        self.attackSpeed = attackSpeed
        self.width = width
        self.height = height
        self.plusHeight = plusHeight
        self.window = window
        self.speed = speed
        self.lastAttack = 0
        self.randomX = self.posX + 100
        self.randomY = self.posY - 100
        self.lastMove = time.time()
        self.room = "Room"
        self.hitbox = pygame.Rect((self.posX, self.posY, self.width + self.plusX, self.height + self.plusY))


    def drawHitbox(self):
        pygame.draw.rect(self.window, (255, 0, 0), self.hitbox, 3)

    #Used to set their walking sprite
    def setWalkFrame(self):
        if self.walkStep == 5:
            self.walkStep = 1
        img = pygame.image.load("Entities/" + self.name + "/" + self.name + "_Walk_" + str(self.walkStep) + ".png")
        if self.lastDirection == "LEFT":
            img = pygame.transform.flip(img, True, False)
        self.image = pygame.transform.scale(img, (self.width, self.height))
        self.walkStep += 1

    # Used to set their idle sprite
    def setIdle(self):
        img = pygame.image.load("Entities/" + self.name + "/" + self.name + "_Idle_1" + ".png")
        if self.lastDirection == "LEFT":
            img = pygame.transform.flip(img, True, False)
        self.image = pygame.transform.scale(img, (self.width, self.height))

    #Used to update the health bar of entities
    def updateHealthBar(self):
        currentHealth = self.health
        size = 2
        if currentHealth < 0: currentHealth = 0
        percentUsed = (self.maxHealth - currentHealth) / self.maxHealth
        usedWidth = self.width - (percentUsed * self.width)
        pygame.draw.rect(self.window, (255, 0, 0), (self.posX, self.posY + self.height, self.width, 5 * size))
        pygame.draw.rect(self.window, (173, 255, 47),(self.posX, self.posY + self.height, usedWidth, 5 * size))

    #Used to attack Player
    def attack(self):
        if not self.isAgressive: return
        self.player.health = self.player.health - self.attackDamage
        self.lastAttack = time.time()
        playerRect = pygame.Rect((self.player.posX + 70, self.player.posY + 90, 60, 90))
        deathBlood.append([self.attackDamage, playerRect.x - 35, playerRect.y - 0, time.time(), (138, 3, 3)])
        # if self.name == "Troll":
        #     ogre_growl.play()
        if self.name == "Bear":
            bear_attack.play()
        elif self.name == "Bandit":
            bandit_dagger.play()
        elif self.name == "Golem":
            golem_hit.play()

    # Used for non-aggressive entities to move around randomly to make them more 'alive'
    def randomMove(self):
        if not time.time() - 2 > self.lastMove:return
        if time.time() - 4 > self.lastMove:
            self.randomX = random.randint(-100, 100)
            self.randomY = random.randint(-100, 100)
            self.setIdle()
            self.lastMove = time.time()
            return
        if (self.posX + self.randomX < - 30 or self.posX + self.randomX > 850):return
        if (self.posY + self.randomX < - 20 or self.posY + self.randomY > 800): return
        playerRect = pygame.Rect((self.player.posX + 70, self.player.posY + 90, 60, 90))
        if playerRect.colliderect((self.posX + self.plusX, self.posY + self.plusY + 10, self.width, self.height)):
            self.setIdle()
            return
        x = self.randomX
        y = self.randomY

        rects = []
        for solid in self.room.solidSurfaces:
            rect = pygame.Rect((solid), (10, 101))
            rects.append(rect)
        self.setWalkFrame()
        #LEFT
        if x < 0:
            if pygame.Rect(self.posX - 5, self.posY + 50, self.width, self.height).collidelist(rects) == -1:
                self.lastDirection = "LEFT"
                self.posX -= self.speed
        #RIGHT
        elif x > 1:
            if pygame.Rect(self.posX + 5, self.posY + 50, self.width, self.height).collidelist(rects) == -1:
                self.lastDirection = "RIGHT"
                self.posX += self.speed
        #UP
        if y < 0:
            if pygame.Rect(self.posX, self.posY + 50 - 55, self.width, self.height).collidelist(rects) == -1:
                self.posY -= self.speed
        #DOWN
        elif y > 1:
            if pygame.Rect(self.posX, self.posY + 50 + 40, self.width, self.height).collidelist(rects) == -1:
                self.posY += self.speed

    #Path finding towards player
    def moveTowardsPlayer(self):
        self.hitbox = pygame.Rect((self.posX + self.plusX, self.posY + self.plusY, self.width + self.plusWidth, self.height + self.plusHeight))
        if not self.isAgressive:
            self.randomMove()
            return
        rects = []
        for solid in self.room.solidSurfaces:
            rect = pygame.Rect((solid), (10, 101))
            rects.append(rect)
        playerRect = pygame.Rect((self.player.posX + 70, self.player.posY + 90, 60, 90))
        #pygame.draw.rect(self.window, (0, 0, 255), pygame.Rect((self.posX + self.plusX - 10, self.posY + self.plusY - 10, self.width + self.plusWidth + 20, self.height + self.plusHeight + 20)))
        if playerRect.colliderect((self.posX + self.plusX - 10, self.posY + self.plusY - 10, self.width + self.plusWidth + 20, self.height + self.plusHeight + 20)):
            if time.time() - self.attackSpeed > self.lastAttack:
                self.attack()
            self.setIdle()
            return

        self.setWalkFrame()
        x = self.player.posX - self.posX
        y = self.player.posY - self.posY
        #LEFT
        if x < 0:

            if pygame.Rect((self.posX + self.plusX - 10 - 5, self.posY + self.plusY - 10, self.width + self.plusWidth + 20, self.height + self.plusHeight + 20)).collidelist(rects) == -1:
                self.lastDirection = "LEFT"
                self.posX -= self.speed

        #RIGHT
        elif x > 1:
            if pygame.Rect((self.posX + self.plusX - 10 + 5, self.posY + self.plusY - 10, self.width + self.plusWidth + 20, self.height + self.plusHeight + 20)).collidelist(rects) == -1:
                self.lastDirection = "RIGHT"
                self.posX += self.speed

        #UP
        if y < 0:
            if pygame.Rect((self.posX + self.plusX - 10, self.posY + self.plusY - 10 - 5, self.width + self.plusWidth + 20, self.height + self.plusHeight + 20)).collidelist(rects) == -1:
                self.posY -= self.speed

        #DOWN
        elif y > 1:
            if pygame.Rect((self.posX + self.plusX - 10, self.posY + self.plusY - 10 + 5, self.width + self.plusWidth + 20, self.height + self.plusHeight + 20)).collidelist(rects) == -1:
                self.posY += self.speed

    #Used to damage entities
    def damage(self, amount):
        entity_hit.play()
        damage = amount
        color = (138, 3, 3)
        isCrit = random.randint(1, 100)
        if isCrit >= 75:
            color = (255, 165, 0)
            damage = damage + 2

        self.health = self.health - damage
        #DEATH OF ENTITY
        if self.health < 0:
            if len(self.playerInventory.contents) < 12:
                for item in self.itemDrop:
                    test = random.randint(0, 100)
                    if self.itemDrop.get(item) > test :
                        if item.__contains__("Necklace"):
                            if Text.achievements.get("foundThreeNecklace")[0]: continue
                            global necklaceCount
                            necklaceCount += 1
                            if not Text.achievements.get("foundOneNecklace")[0]:
                                Text.printAchievement("foundOneNecklace")
                            elif not Text.achievements.get("foundTwoNecklace")[0]:
                                Text.printAchievement("foundTwoNecklace")
                            elif not Text.achievements.get("foundThreeNecklace")[0]:
                                Text.printAchievement("foundThreeNecklace")
                            self.playerInventory.contents.append(
                                Items.Item(item, "Items/Inventory/" + str(item) + ".png", 0, 0, False, True))
                        else:
                            self.playerInventory.contents.append(
                                Items.getPotionByName(item))
                        img = pygame.image.load("Items/Inventory/" + str(item) + ".png")
                        img = pygame.transform.scale(img, (50, 50))
                        if self.name == "Golem":
                            Text.printAchievement("foundPrincess")
                            img = pygame.transform.scale(img, (200, 200))
                            droppedItems.append([img, (self.hitbox.x + self.hitbox.x) / 2 , (self.hitbox.y + self.hitbox.y) / 2, time.time() + 6])
                        else:
                            droppedItems.append([img, (self.hitbox.x + self.hitbox.x) / 2 + test,(self.hitbox.y + self.hitbox.y) / 2 + test, time.time()])

            if self.name == "Troll":
                Text.printAchievement("killedTroll")
            self.room.entities.remove(self)
            deathBlood.append([damage, (self.hitbox.x + self.hitbox.x) / 2, (self.hitbox.y + self.hitbox.y) / 2, time.time(), color])
        dmgTags.append([damage, self.hitbox.x + (self.hitbox.x / 7), self.hitbox.y - 40, time.time(), color])




def spawnRandomEntities(r, player, inventory, window, bypassRand):
    #50% chance to spawn a new entity
    if not bypassRand and random.randint(1, 2) != 1:return
    solids = []
    entityName = random.choice(availableEntities)
    randX = random.randint(130, 790)
    randY = random.randint(140, 660)
    entity = getEntityByName(entityName, randX, randY, player, inventory, window)
    entity.room = r
    for solid in r.solidSurfaces:
        s = pygame.Rect((solid), (10, 101))
        solids.append(s)
    if pygame.Rect(entity.posX, entity.posY + 50, entity.width, entity.height).collidelist(solids) == -1:
        r.entities.append(entity)
    else:
        spawnRandomEntities(r, player, inventory, window, True)



def getEntityByName(name, posX, posY, player, playerInventory, window):
    if str(name).lower() == "troll":
        return Entity("Troll", "Troll", 120, 120,5, 4, 2, 0, True, posX, posY, "LEFT", player, 1, 135, 160, 0, 10, -10, 0, {"Health": 80, "Strength": 30, "Necklace": 25}, playerInventory, window)
    elif str(name).lower() == "bear":
        return Entity("Bear", "Bear", 30, 30, 5, 4, 2, 0, True, posX, posY, "LEFT", player, 1, 200, 170, 0, 50, -50, 0, {"Health": 80, "Strength": 30, "Necklace": 25}, playerInventory, window)
    elif str(name).lower() == "largemushroom":
        return Entity("LargeMushroom", "LargeMushroom", 30, 30, 5, 4, 2, 0, False, posX, posY, "LEFT", player, 1, 100, 70, 0, 10, -10, 0, {"Health": 80}, playerInventory, window)
    elif str(name).lower() == "bandit":
        return Entity("Bandit", "Bandit", 30, 30, 8, 4, 1, 0, True, posX, posY, "LEFT", player, 1, 100, 150, 30, 80, -80, -60, {"Strength": 20, "Necklace": 25} ,playerInventory, window)
    elif str(name).lower() == "golem":
        return Entity("Golem", "Golem", 450, 450, 5, 4, 2, 0, True, posX, posY, "LEFT", player, 1, 275, 305, 25, 130, -140, -60, {"Princess": 100}, playerInventory, window)
