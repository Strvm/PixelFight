import pickle
import pygame
import Player
import os
import Room
import Items
import Entity
import Inventory
import Text

playerData = 'Saves/playerData'
roomData = 'Saves/roomData'
inventoryData = "Saves/inventoryData"

#Used to serialize/save data
class Save:
    def __init__(self, player, rooms, inventory, currentRoom):
        global  playerData, roomData, inventoryData

        playerOutfile = open(playerData, 'wb')
        roomOutfile = open(roomData, 'wb')
        playerD = []
        playerD.extend((player.name, player.level, player.xp, player.health, player.attackDamage, player.posX, player.posY, player.velocity, "Entities/Player/Player_Idle_1.png", player.walkStep, player.lastDirection, currentRoom, Text.achievements))
        pickle.dump(playerD, playerOutfile)
        playerOutfile.close()

        roomD = []

        for room in rooms:
            entitiesData = []
            r = []
            for entity in room.entities:
                entityData = []
                entityData.extend((entity.name, entity.imagePath, entity.health, entity.maxHealth, entity.speed, entity.attackDamage, entity.attackSpeed, entity.shield, entity.isAgressive, entity.posX, entity.posY, entity.lastDirection, entity.walkStep, entity.width, entity.height, entity.plusX, entity.plusY, entity.plusHeight, entity.plusWidth, entity.itemDrop))
                entitiesData.append(entityData)
            r.extend((room.name, room.backgroundPath, entitiesData, room.index, room.direction, room.allowedDirections, room.solidSurfaces))
            roomD.append(r)
        pickle.dump(roomD, roomOutfile)
        roomOutfile.close()

        inventoryOutfile = open(inventoryData, 'wb')
        inventoryD = []

        items = []
        itemsList = []
        for item in inventory.contents:
            items = []
            items.extend((item.name, item.imagePath, item.healthRegen, item.strengthBoost, item.isPotion, item.isSpecial))
            itemsList.append(items)

        inventoryD.extend((inventory.name, inventory.size, itemsList))
        pickle.dump(inventoryD, inventoryOutfile)
        inventoryOutfile.close()


def loadCurrentRoom():
    playerInfile = open(playerData, 'rb')
    playerSave = pickle.load(playerInfile)
    playerInfile.close()
    return playerSave[11]


def loadPlayer(window):
    playerInfile = open(playerData,'rb')
    playerSave = pickle.load(playerInfile)
    playerInfile.close()
    Text.achievements = playerSave[12]
    return Player.Player(playerSave[0], playerSave[1], playerSave[2], playerSave[3], playerSave[4], playerSave[5], playerSave[6], playerSave[7], playerSave[8], playerSave[9], playerSave[10], playerSave[12], window)


def loadRooms(player, window, playerInventory):
    roomInfile = open(roomData, 'rb')
    roomSave = pickle.load(roomInfile)
    rooms = []
    for room in roomSave:
        entities = []
        for entity in room[2]:
            entities.append(Entity.Entity(entity[0], entity[1], entity[2], entity[3], entity[4], entity[5], entity[6], entity[7], entity[8], entity[9], entity[10], entity[11], player, entity[12], entity[13], entity[14], entity[15], entity[16], entity[17], entity[18], entity[19], window, playerInventory))
        rooms.append(Room.Room(room[0], room[1], entities, room[3], room[4], room[5], room[6]))
    roomInfile.close()
    return rooms

def loadInventory(player):
    inventoryInfile = open(inventoryData, 'rb')
    inventorySave = pickle.load(inventoryInfile)
    items = []
    for item in inventorySave[2]:
        items.append(Items.Item(item[0], item[1], item[2], item[3], item[4], item[5]))
    return Inventory.Inventory(inventorySave[0], inventorySave[1], items, player)



