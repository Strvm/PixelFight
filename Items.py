import pygame

#Used to create items to put inside inventory
class Item:
    def __init__(self, name, image, healthRegen, strengthBoost, isPotion, isSpecial):
        self.imagePath = image
        img = pygame.image.load(self.imagePath)
        img = pygame.transform.scale(img, (80, 80))
        self.name = name
        self.image = img
        self.isPotion = isPotion
        self.isSpecial = isSpecial
        self.healthRegen = healthRegen
        self.strengthBoost = strengthBoost



def getPotionByName(name):
    if str(name).lower().__contains__("health"):
        return Item("Health Potion", "Items/Inventory/Health.png", 10, 0, True, False)
    elif str(name).lower().__contains__("strength"):
        return Item("Strength Potion", "Items/Inventory/Strength.png", 0, 2, True, False)



