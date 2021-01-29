import Player
import Items
import pygame
import pygame.gfxdraw
import Fonts
import Items
import Text


drink_potion = pygame.mixer.Sound('Sounds/potion_drink.wav')
drink_potion.set_volume(drink_potion.get_volume() / 2)

#Inventory of Player
class Inventory:
    def __init__(self, name, size, contents, player):
        self.name = name
        self.contents = contents
        self.size = size
        self.player = player

    def openInventory(self):
        global inventoryOpen
        inventoryOpen = True

    def closeInventory(self):
        global inventoryOpen
        inventoryOpen = False


def printInventory(inventory, window, slots):

    mainRec = pygame.draw.rect(window, (198, 198, 198), (250, 250, 550, 500))

    posX = mainRec.x + (mainRec.x / 4.75)
    posY = mainRec.y + (mainRec.y/ 4.75)
    pygame.draw.rect(window, (139, 139, 139), (posX, posY, 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + (posX / 2.5), posY, 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + ((posX / 2.5) * 2), posY, 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + ((posX / 2.5) * 3), posY, 550 / 6, 500 / 6))

    pygame.draw.rect(window, (139, 139, 139), (posX, posY + (posY / 2), 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + (posX / 2.5), posY + (posY / 2), 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + ((posX / 2.5) * 2), posY + (posY / 2), 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + ((posX / 2.5) * 3), posY + (posY / 2), 550 / 6, 500 / 6))

    pygame.draw.rect(window, (139, 139, 139), (posX, posY * 2, 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + (posX / 2.5), posY * 2, 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + ((posX / 2.5) * 2), posY * 2, 550 / 6, 500 / 6))
    pygame.draw.rect(window, (139, 139, 139), (posX + ((posX / 2.5) * 3), posY * 2, 550 / 6, 500 / 6))


    itemX = posX + (posX / 45)
    itemY = posY + (posY / 50)



    indexY = 1
    indeX = 0
    i = 1
    for item in inventory.contents:
        if i == 5:
            indexY += 1
            indeX = 0
            i = 1
        if indexY == 1:
            if indeX >= 1:
                if not slots.__contains__(window.blit(item.image, pygame.Rect((itemX + (itemX / 2.55) * indeX, itemY, 550 / 7, 500 / 7)))):
                    slots.append(window.blit(item.image, pygame.Rect((itemX + (itemX / 2.55) * indeX, itemY, 550 / 7, 500 / 7))))
            else:
                if not slots.__contains__(window.blit(item.image, pygame.Rect((itemX, itemY, 550 / 7, 500 / 7)))):
                    slots.append(window.blit(item.image, pygame.Rect((itemX, itemY, 550 / 7, 500 / 7))))

        elif indexY == 2:
            if indeX >= 1:
                if not slots.__contains__(window.blit(item.image, pygame.Rect((itemX + (itemX / 2.55) * indeX, itemY + (itemY / 2.05), 550 / 7, 500 / 7)))):
                    slots.append(window.blit(item.image, pygame.Rect((itemX + (itemX / 2.55) * indeX, itemY + (itemY / 2.05), 550 / 7, 500 / 7))))
            else:
                if not slots.__contains__(window.blit(item.image, pygame.Rect(
                        (itemX + (itemX / 2.55) * indeX, itemY + (itemY / 2.05), 550 / 7, 500 / 7)))):
                    slots.append(window.blit(item.image, pygame.Rect(
                        (itemX + (itemX / 2.55) * indeX, itemY + (itemY / 2.05), 550 / 7, 500 / 7))))
        else:
            if indeX >= 1:
                if not slots.__contains__(window.blit(item.image, pygame.Rect(
                        (itemX + (itemX / 2.55) * indeX, itemY * 1.98, 550 / 7, 500 / 7)))):
                    slots.append(window.blit(item.image, pygame.Rect(
                        (itemX + (itemX / 2.55) * indeX, itemY * 1.98, 550 / 7, 500 / 7))))
            else:
                if not slots.__contains__(window.blit(item.image, pygame.Rect(
                        (itemX + (itemX / 2.55) * indeX, itemY * 1.98, 550 / 7, 500 / 7)))):
                    slots.append(window.blit(item.image, pygame.Rect(
                        (itemX + (itemX / 2.55) * indeX, itemY * 1.98, 550 / 7, 500 / 7))))
        i += 1
        indeX += 1




def hoverInventoryItem(window, slots, inventory):

    for slot in slots:
        if slot.collidepoint(pygame.mouse.get_pos()):
            index = slots.index(slot)
            try:
                pygame.draw.rect(window, (150, 100, 100), slot, 3)
                textsurface = Fonts.bigFont.render(inventory.contents[index].name, False, (0, 0, 0))
                window.blit(textsurface, (slot.x - (8 + len(inventory.contents[index].name)), slot.y + 85))
            except IndexError:
                slots.remove(slot)

def inventoryClickItem(window, slots, inventory, player):
    i = 0
    for slot in reversed(slots):
        if slot.collidepoint(pygame.mouse.get_pos()):
            index = slots.index(slot)
            if inventory.contents[index].isSpecial: return
            slots = []
            if inventory.contents[index].healthRegen > 0 and player.health == 100:
                continue
            useItem(player, inventory.contents[index], window)
            inventory.contents.remove(inventory.contents[index])
            printInventory(inventory, window, slots)
            break
        i += 1
inventoryOpen = False


def useItem(player, item, window):
    if item.strengthBoost > 0:
        Text.printAchievement("drankStrengthPotion")
    elif item.healthRegen > 0:
        Text.printAchievement("drankHealthPotion")
    player.attackDamage = player.attackDamage + item.strengthBoost
    if player.health + item.healthRegen >= 100:
        player.health = 100
    else:player.health = player.health + item.healthRegen
    if item.isPotion:
        drink_potion.play()
