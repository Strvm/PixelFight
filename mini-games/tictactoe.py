import os
import math
from colorama import Fore, Style

grid = [['1 |', ' 2 |', ' 3'],
        ['4 |', ' 5 |', ' 6'],
        ['7 |', ' 8 |', ' 9']]

playerTurn = True
numberOfPlays = 0
def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")



def start():
    printBoard()
    choose()



def choose():
    number = input(getPlayer() + " please choose a spot: ")
    if str(number).isdigit() and int(number) >= 1 and int(number) <= 9:
        place(int(number))
    else:
        clearTerminal()
        printBoard()
        choose()


def place(number):
    row = math.ceil(number / 3) - 1
    placement = number % 3
    if placement == 1:
        placement = 0
    elif placement == 2:
        placement = 1
    else:
        placement = 2
    if grid[row][placement].__contains__('X') or grid[row][placement].__contains__('●'):
        clearTerminal()
        printBoard()
        choose()
    else:
        grid[row][placement] = replaceNumber(grid[row][placement])
        clearTerminal()
        printBoard()
        checkIfWon(getPlayerSymbol())
        global playerTurn
        playerTurn = not playerTurn
        choose()




def checkIfWon(symbol):
    #horizontal
    for x in grid:
        counter = 0
        for b in x:
            if b.__contains__(symbol):
                counter += 1
            else:
                counter = 0
            if counter == 3:
                input(getPlayer() + " has Won!")



    # vertical
    index = 0
    for b in range(3):
        for x in range(len(grid)):
            if grid[x][index].__contains__(symbol):
                counter = counter + 1
            else:
                counter = 0;
            if counter == 3:
                input(getPlayer() + " has Won!")
                return
        counter = 0
        index += 1


    # diagonal left
    counter = 0
    for x in range(4):
        if grid[x][x].__contains__(symbol):
            counter += 1
        else:
            break
        if counter == 3:
            input(getPlayer() + " has Won!")
            return

    # diagonal right
    index = 0
    counter = 0
    for x in reversed(range(3)):
        if grid[index][x].__contains__(symbol):
            counter += 1
        else:
            break
        if counter == 3:
            input(getPlayer() + " has Won!")
            return
        index += 1


def replaceNumber(choice):
    string = ('' + choice);
    for x in range(10):
        if string.__contains__(str(x)):
            string = string.replace(str(x), getPlayerSymbol())
    print("VAL " + string.replace(str(x), getPlayerSymbol()))
    return string




def printBoard():
    i = 0
    for x in grid:
        print(''.join(x))
        if i < 2:
            print("─────────")
        i += 1


def getPlayer():
    if playerTurn:
        return f'{Style.RESET_ALL}{Fore.YELLOW}Player 1{Style.RESET_ALL}'
    else:
        return f'{Style.RESET_ALL}{Fore.RED}Player 2{Style.RESET_ALL}'


def getPlayerSymbol():
    if getPlayer().__contains__("Player 1"):
        return f'{Style.RESET_ALL}{Fore.YELLOW}X{Style.RESET_ALL}'
    else:
        return f'{Style.RESET_ALL}{Fore.RED}●{Style.RESET_ALL}'


start()