import random
import os
import re
import shutil
animals = 'steer lemur puppy cat pig llama deer rooster yak fox alpaca warthog polar bear gnu rat mink gila monster ' \
          'civet crow orangutan turtle springbok guinea pig frog puma wildcat hartebeest snowy owl lizard cow mynah ' \
          'bird walrus buffalo wombat weasel toad leopard dugong basilisk thorny devil giraffe impala chamois silver ' \
          'fox highland cow tapir parrot bull reindeer jackal snake skunk moose coati shrew cougar bear fish mustang ' \
          'mandrill doe mole panda gopher camel grizzly bear sloth badger ewe seal chicken armadillo rhinoceros ' \
          'canary marmoset lynx hyena mongoose vicuna oryx crocodile hamster mouse hare aoudad bald eagle antelope ' \
          'raccoon guanaco squirrel zebra duckbill platypus burro ibex otter pronghorn kangaroo mule lovebird rabbit ' \
          'goat dung beetle ground hog eagle owl wolf coyote wolverine dormouse dog jerboa anteater tiger starfish ' \
          'boar jaguar dingo musk-ox lion chimpanzee chinchilla musk deer ermine hedgehog budgerigar sheep waterbuck ' \
          'salamander chameleon bat beaver elephant argali ox bison woodchuck colt blue crab monkey iguana ape ' \
          'bighorn chipmunk capybara donkey gazelle dromedary aardvark porcupine baboon mare gemsbok finch lamb ' \
          'bumble bee ram mountain goat ferret quagga peccary bunny hippopotamus newt okapi prairie dog panther ' \
          'stallion kitten addax opossum octopus pony ocelot meerkat horse gorilla alligator elk muskrat koala ' \
          'parakeet fawn whale hog zebu cheetah porpoise marten eland '
animalsList = animals.split()

hangman = ['''

                +---+
                |   |
                    |
                    |
                    |
                    |
              =========''', '''

                +---+
                |   |
                O   |
                    |
                    |
                    |
              =========''', '''

                +---+
                |   |
                O   |
                |   |
                    |
                    |
              =========''', '''

                +---+
                |   |
                O   |
               /|   |
                    |
                    |
              =========''', '''

                +---+
                |   |
                O   |
               /|\  |
                    |
                    |
              =========''', '''

                +---+
                |   |
                O   |
               /|\  |
               /    |
                    |
              =========''', '''
                +---+
                |   |
                O   |
               /|\  |
               / \  |
                    |
              =========''']

hanged_man = '''
                +---+
                |   |
               _O_  |
                |   |
               / \  |
                    |
              ========='''

free_man = ['''
                +---+
                    |
                    |
               _O_  |
                |   |
               | |  |
              =========''', '''
                +---+
                    |
                    |
               \O/  |
                |   |
               | |  |
              =========''']



def game():
    print('Hello player! A random Animal has been generated, try and guess it!')
    guessLetter()


amountOfGuesses = 0
usedChars = []
word = random.choice(animalsList)
wordSize = len(word)
wordArray = []
correctGuesses = 0
for x in range(wordSize):
    wordArray.append("_ ")
def guessLetter():
    if amountOfGuesses > 0:
        clearTerminal()
    if len(word) == correctGuesses and correctGuesses != 0:
        print(free_man[1])
        print(''.join(wordArray))
        print('Cheat: ', word)
        input("You've found the word!")
    else:
        print(hangman[amountOfGuesses])
        print(''.join(wordArray))
        print('Cheat: ',word)
        if len(usedChars) > 0:
            print("Used letters: [", ', '.join(usedChars) , "]")
        guessedLetter = input("Please choose a letter!")
        if not guessedLetter.isalpha():
            clearTerminal()
            print('Please choose a letter!')
            guessLetter()
        else:
            if usedChars.__contains__(guessedLetter):
                clearTerminal()
                print("You've already used " , guessedLetter , "!")
                guessLetter()
            else:
                usedChars.append(guessedLetter)
                if word.__contains__(guessedLetter):
                    print('CONTAINS')
                    addLetter(guessedLetter)
                    clearTerminal()
                else:
                    incrGuesses()
                    if amountOfGuesses == 6:
                        input(f"You've have no more guesses! The word was {word}!")
                    else:
                        clearTerminal()
                guessLetter()




def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")

def incrGuesses():
    global amountOfGuesses
    amountOfGuesses = amountOfGuesses + 1

def incrCorrectGuesses():
    global correctGuesses
    correctGuesses = correctGuesses + 1

def addLetter(letter):
    indexOfLetters = [i.start() for i in re.finditer(letter, word)]
    for x in indexOfLetters:
        incrCorrectGuesses()
        wordArray[x] = f"{letter} "

game()