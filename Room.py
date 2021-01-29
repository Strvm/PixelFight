import pygame, Text, Entity

#Used to create rooms and what contains them
class Room:
    def __init__(self, name, background, entities, index, direction, allowedDirections, solidSurfaces):
        img = pygame.image.load(background)
        self.name = name
        self.backgroundPath = background
        self.background = img
        self.entities = entities
        self.index = index
        self.direction = direction
        self.solidSurfaces = solidSurfaces
        self.allowedDirections = allowedDirections
        for entity in self.entities:
            entity.room = self




def getRoom(roomId):
    for room in map:
        if room.index == roomId:
            return room
def loadRoom(roomId):
    for room in map:
        if room.index == roomId:
            return room.background


