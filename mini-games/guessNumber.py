import random
import os

toGuess = random.randint(1, 1024)
def start():
    print(toGuess)
    chooseNumber()

def guess(number):
    check = toGuess - number
    found = False
    if check == 0:
        print("You've found the correct number!")
        found = True
    elif check > -5 and check < 5:
        print("Extremely Warm")
    elif check > -10 and check < 10:
        print("Very Warm")
    elif check > -50 and check < 50:
        print("Warm")
    elif check > -100 and check < 100:
        print("Warmish")
    else:
        print("Cold")

    if found:
        input("Would you like to play again? (y/n)")
    else:
        chooseNumber()


def chooseNumber():
    num = input("Please guess a number between 1 and 1024: ")
    print(num.isdigit())
    if num.isdigit() and int(num) >= 1 and int(num) <= 1024:
        clearTerminal()
        guess(int(num))
    else:
        chooseNumber()

def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")

start()
