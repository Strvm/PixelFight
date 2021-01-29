import os
from colorama import Fore, Style
grid = [['| 0 |',' 0 |',' 0 |',' 0 |',' 0 |',' 0 |', ' 0 |'],

        ['| 0 |',' 0 |',' 0 |',' 0 |',' 0 |',' 0 |', ' 0 |'],

        ['| 0 |',' 0 |',' 0 |',' 0 |',' 0 |',' 0 |', ' 0 |'],

        ['| 0 |',' 0 |',' 0 |',' 0 |',' 0 |',' 0 |', ' 0 |'],

        ['| 0 |',' 0 |',' 0 |',' 0 |',' 0 |',' 0 |', ' 0 |'],

        ['| 0 |',' 0 |',' 0 |',' 0 |',' 0 |',' 0 |', ' 0 |']]

playerTurn = True

def start():
    print("📦")
    printBoard()
    choose()


def printBoard():
    for x in range(len(grid)):
        if str(grid[x]).__contains__("-"):
            print(grid[x])
        else:
            print(''.join(grid[x]))
        print('-----------------------------')
    print("─────────────────────────────")
    print('| 1 |','2 |','3 |','4 |','5 |','6 |','7 |')



def choose():
    number = input(getPlayer() + " please choose a spot: ")
    if str(number).isdigit() and int(number) >= 1 and int(number) <= 7:
        place(int(number))
    else:
        clearTerminal()
        printBoard()
        choose()

def place(pos):
    pos = pos - 1
    level = -1
    for x in reversed(grid):
        if not x[pos].__contains__("●"):
            x[pos] = x[pos].replace("0", getPlayerSymbol())
            global playerTurn
            level += 1
            break
    clearTerminal()
    printBoard()
    if level > -1:
        checkIfWon(getPlayerSymbol())
        playerTurn = not playerTurn
    choose()

def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")

def getPlayer():
    if playerTurn == True:
        return f'{Style.RESET_ALL}{Fore.YELLOW}Player 1{Style.RESET_ALL}'
    else:
        return f'{Style.RESET_ALL}{Fore.RED}Player 2{Style.RESET_ALL}'

def getPlayerSymbol():
    if getPlayer().__contains__("Player 1"):
        return f'{Style.RESET_ALL}{Fore.YELLOW}●{Style.RESET_ALL}'
    else:
        return f'{Style.RESET_ALL}{Fore.RED}●{Style.RESET_ALL}'



def checkIfWon(symbol):
    counter = 0
    winningComb = []
    #horizontal
    for x in reversed(grid):
        for b in x:
            if counter == 4:
                input(getPlayer() + " has Won!")
                return
            elif b.__contains__(symbol):
                counter += 1
            else:
                counter = 0;
        counter = 0
    counter = 0


    # vertical
    index = 0
    for b in range(6):
        for x in range(len(grid)):
            if grid[x][index].__contains__(symbol):
                counter = counter + 1
            else:
                counter = 0;
            if counter >= 4:
                input(getPlayer() + " has Won!")
                return
        counter = 0
        index += 1

    # diagonal left
    counter = 0
    index = 0
    gridIndex = 0
    decrease = False
    for b in range(7 * 2):
        if not decrease:
            index += 1
        else:
            index -= 1
        if index == 6:
            decrease = True
        gridIndex = index - 1
        for x in range(index):
            if grid[x][gridIndex].__contains__(symbol):
                counter += 1
            else: counter = 0
            if counter == 4:
                input(getPlayer() + " has Won!")
            gridIndex -= 1

    # diagonal right
    counter = 0
    index = 5
    gridIndex = 0
    decrease = False
    for b in range(7 * 2):
        if not decrease:
            index += 1
        else:
            index -= 1
        if index == 6:
            decrease = True
        gridIndex = index
        for x in reversed(range(index)):
            if grid[x][gridIndex].__contains__(symbol):
                counter += 1
            else:
                counter = 0
            if counter == 4:
                input(getPlayer() + " has Won!")
            gridIndex -= 1



start()