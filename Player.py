import pygame
import Fonts
import math
import Text
pygame.mixer.init()
sword_swing = pygame.mixer.Sound('Sounds/sword_swing.wav')  # Load a sound.
sword_swing.set_volume(0.5)
entity_hit = pygame.mixer.Sound('Sounds/flesh_hit.wav')  # Load a sound.
player_walk = pygame.mixer.Sound('Sounds/player_walk.wav')  # Load a sound.
player_walk.set_volume(0.1)


#All player settings
class Player:
  def __init__(self, name, level, xp, health, attackDamage, posX, posY, velocity, image, walkStep, lastDirection, achievements, window):
    img = pygame.image.load(image)
    img = pygame.transform.scale(img, (200,200))
    self.name = name
    self.posX = posX
    self.achievements = achievements
    self.lastDirection = lastDirection
    self.posY = posY
    self.walkStep = walkStep
    self.velocity = velocity
    self.image = img
    self.attackDamage = attackDamage
    self.health = health
    self.level = level
    self.xp = xp
    self.window = window
    self.hitbox = pygame.Rect((self.posX + 70, self.posY + 90, 60, 90))

  def setWalkFrame(self):
      self.hitbox = pygame.Rect((self.posX + 70, self.posY + 90, 60, 90))
      if self.walkStep == 5:
          self.walkStep = 1
      img = pygame.image.load("Entities/Player/Player_Walk_" + str(self.walkStep) + ".png")
      if self.lastDirection.__contains__("LEFT"):
        img = pygame.transform.flip(img, True, False)
      self.image = pygame.transform.scale(img, (200, 200))
      if self.walkStep == 1:
        player_walk.play()
      self.walkStep += 1


  def setIdle(self):
      img = pygame.image.load("Entities/Player/Player_Idle_1.png")
      if  self.lastDirection.__contains__("LEFT"):
        img = pygame.transform.flip(img, True, False)
      self.image = pygame.transform.scale(img, (200, 200))

  def attack(self, room):
      img = pygame.image.load("Items/Weapons/ezgif-5-912d390ed9a9-gif-im/frame_0_delay-0.1s.gif").convert_alpha()
      img = pygame.transform.scale(img, (70, 70))
      hitDirection = self.hitDirection(room.entities)
      #print(hitDirection)
      if hitDirection == "RIGHT":
          for entity in reversed(room.entities):
              if pygame.Rect((self.posX + 70 + 80, self.posY + 90, 60, 90)).colliderect(entity.hitbox):
                  entity.damage(self.attackDamage)
                  break
          self.window.blit(img, (self.posX + 125, self.posY + 85))
          sword_swing.play()
      elif hitDirection == "LEFT":
          img = pygame.transform.flip(img, True, False)
          for entity in room.entities:
              if pygame.Rect((self.posX + 70 - 80, self.posY + 90, 60, 90)).colliderect(entity.hitbox):
                  entity.damage(self.attackDamage)
                  break
          self.window.blit(img, (self.posX + 5 , self.posY + 85))
          sword_swing.play()
      elif hitDirection == "UP":
          img = pygame.transform.flip(img, True, False)
          img = pygame.transform.rotate(img, -90)
          for entity in room.entities:
              if pygame.Rect((self.posX + 85, self.posY + 25 - 15, 60, 90)).colliderect(entity.hitbox):
                  entity.damage(self.attackDamage)
                  break
          self.window.blit(img, (self.posX + 85, self.posY + 25))
          sword_swing.play()
      elif hitDirection == "DOWN":
          img = pygame.transform.flip(img, True, False)
          img = pygame.transform.rotate(img, 90)
          for entity in room.entities:
              if pygame.Rect((self.posX + 45, self.posY + 175 + 5, 60, 90)).colliderect(entity.hitbox):
                  entity.damage(self.attackDamage)
                  break
          self.window.blit(img, (self.posX + 45, self.posY + 175))
          sword_swing.play()

  def updateHealthBar(self):
    currentHealth = self.health
    size = 2
    if currentHealth <= 0:
        currentHealth = 0
        Text.printAchievement("hasDied")
    pygame.draw.rect(self.window, (173,255,47), (10, 920, currentHealth * size, 30 * size))
    pygame.draw.rect(self.window, (255, 0, 0), (110 - (100 - currentHealth * 2), 920, (100 - currentHealth) * size, 30 * size))


  #Used to hit towards the nearest entity
  def hitDirection(self, entities):
    entity = self.getNearestEntity(entities)
    if entity != "NOT FOUND":
        rel_x, rel_y = self.posX - entity.posX, self.posY - entity.posY
        angle = math.atan2(rel_y, rel_x)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        print(angle)

        if angle > 129 or angle == -180:
            return "RIGHT"
            print("RIGHT")
        elif angle >= 90:
            return "DOWN"
            print("DOWN")
        elif angle < 100 and angle > -40:
            return "LEFT"
            print("LEFT")
        else:
            return "UP"
            print("UP")

    return "NONE"


  def getNearestEntity(self, entities):
    entityLoc = []
    for entity in entities:
        distance = pygame.math.Vector2(entity.posX, entity.posY).distance_to(pygame.math.Vector2(self.posX, self.posY))
        entityLoc.append(distance)

    closest = "NOT FOUND"
    for entity in entityLoc:
        if len(entityLoc) == 1:
            return entities[entityLoc.index(entity)]
        if closest == "NOT FOUND":
            closest = entity
        elif closest > entity:
            closest = entity

    if closest == "NOT FOUND":return "NOT FOUND"
    return entities[entityLoc.index(closest)]








def turnPos(number):
    if number < 0:
        return number * -1
    else:
        return number
