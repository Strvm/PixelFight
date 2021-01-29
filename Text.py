import pygame, time, Fonts

img = pygame.image.load("Images/textbox.png")
img = pygame.transform.scale(img, (350, 125))
textToBePrinted = []

achievements = {"travelledMiddle": [False, "Be careful of the monsters around here. Some might drop items upon death!"],
                "travelledSouth": [False, "Bandits! Be careful of with your belongings and of their daggers!"],
                "travelledEast": [False, ""],
                "travelledWest": [False, "Oh no a huge bear! Try and defeat it!"],
                "talkedToKing": [False, "Here you are ! My daughter has been kidnapped by an evil prince. Please help me get her back!"],
                "killedBear": [False, ""],
                "killedTroll": [False, "What a horrible monster! Good job on killing it!"],
                "killedMushroom": [False, ""],
                "foundOneNecklace": [False, "You've found a necklace! I wonder what we can do with it.."],
                "foundTwoNecklace": [False, "Another necklace! There must be a meaning behind it.."],
                "foundThreeNecklace": [False, "A third one! We must be able to use them somewhere.."],
                "drankHealthPotion": [False, "You seem to have replenished some health!"],
                "drankStrengthPotion": [False, "You seem to be able to hit harder!"],
                "hasDied": [False, "Oh no you have died.."],
                "foundPrincess": [False, "You have found my daughter! Thank you so much!"]}
#Used to display text when narrator (King) talks to you
class Text:
    def __init__(self, image, text, speed):
        self.imagePath = image
        self.image = pygame.image.load(image)
        self.text = text
        self.speed = speed
        self.printedLetters = ""
        self.timeSincePrint = time.time()
        self.timeAfterEnd = 0
        self.done = False

    def printText(self, window):
       # rec = pygame.draw.rect(window, (255, 0, 0), pygame.Rect((610, 850, 350, 125)))
        if time.time() - self.speed > self.timeSincePrint:
            self.timeSincePrint = time.time()
            if len(self.text) != 0 or (self.timeAfterEnd != 0 and self.timeAfterEnd + 3 > time.time()):
                img2 = pygame.image.load("Images/king.png")
                img2 = pygame.transform.scale(img2, (125, 125))
                window.blit(img2, (500, 850))
                window.blit(img, (610, 850))
                self.printedLetters = self.printedLetters + (self.text[:1])
                self.text = self.text[1:]
                blit_text(window, self.printedLetters, (640, 870), Fonts.textFont)
                if len(self.text) == 0 and self.timeAfterEnd == 0:
                    print("END")
                    self.timeAfterEnd = time.time()
            else:
                self.done = True





def printTextTask(window):
    for text in textToBePrinted:
        if text.done:
            textToBePrinted.remove(text)
        text.printText(window)


def printAchievement(achievement):
    if not achievements.get(achievement)[0]:
        textToBePrinted.append(Text("Images/map_middle.png", achievements.get(achievement)[1], 0.01))
        achievements.get(achievement)[0] = True

def isDone(achievement):
    return achievements.get(achievement)[0]

def reset():
    for achievement in achievements:
        achievements.get(achievement)[0] = False

SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 30
clock = pygame.time.Clock()

#CREDIT TO THIS POST FOR THIS METHOD https://stackoverflow.com/a/42015712/10546042
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    max_width = 940
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.