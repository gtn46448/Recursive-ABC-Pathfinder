#Solves ABCPath puzzles (example puzzle can be found on BrainBashers)

import time
from tkinter import *

displayChars = []

#buttonfunctions
def edit():
    #toggle editing side stuff
    if displayChars[0]["state"] == "disabled":
        for item in displayChars:
            item["state"] = "normal"
        for i in range(5):
            for j in range(5):
                displayGrid[i][j]["bg"] = "#ffffff"
        editButton["text"] = "Confirm Board"
        checkButton["text"] = "Clear Board"
        checkButton["command"] = boardClear
        solveButton["text"] = "Reset to Preset"
        solveButton["command"] = preset
    else:
        for item in displayChars:
            item["state"] = "disabled"
        editButton["text"] = "Set up Board"
        checkButton["text"] = "Check Solution"
        checkButton["command"] = check
        solveButton["text"] = "Solve Board"
        solveButton["command"] = solve
    toggleBoardEdit()
    editButton["state"] = "normal"
    checkButton["state"] = "normal"
    solveButton["state"] = "normal"

def boardClear():
    for i in range(5):
        for j in range(5):
            displayContents[i][j].set("")
    for i in displayChars:
        i.delete(0, END)

def preset():
    boardClear()
    message["text"] = "Fill the board with letters 'a' through 'y'. Use the outer letters as a guide. Consecutive letters must be adjacent(linear or diagonal)"
    displayContents[2][4].set('a')
    toAdd = "ujoxdqpfcbwmnthyrsgivekl"
    for i in displayChars:
        i.insert(0, toAdd[displayChars.index(i)])

def check():
    #disable editing board
    toggleBoardEdit()
    #check solution
    grid = [["","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
    #function fillGrid will return -1, -1 if character 'a' is not found.
    startRow, startCol = fillGrid(grid)
    if startRow == -1:
        message["text"] = "Start point 'A' not found."
    else:
        message["text"] = "Verifying answer..."
        if pathFinderCheck("abcdefghijklmnopqrstuvwxy", startRow, startCol, grid):
            message["text"] = "Correct!"
        else:
            message["text"] = "Incorrect"

    #renable board
    toggleBoardEdit()

def pathFinderCheck(charsLeft, row, col, grid):
    if len(charsLeft) == 0:
        # return "Solved!"
        displayGrid[row][col]["bg"] = '#93ff7a'
        return True
    if row < 0 or row >= 5 or col < 0 or col >= 5:
        # return ""
        return False
    contents = displayGrid[row][col].get()
    if len(contents) != 1:
        displayGrid[row][col]["bg"] = '#ff7a7a'
        # return "(" + str(row) + ", " + str(col) + ") must have exactly 1 letter.\n"
        return False
    elif not contents.lower() in grid[row][col]:
        displayGrid[row][col]["bg"] = '#ff7a7a'
        # return "(" + str(row) + ", " + str(col) + ") must follow border letter rules.\n"
        return False
    elif contents != charsLeft[0]:
        return ""
        return False
    else:
        update = charsLeft[1:]
        if (pathFinderCheck(update, row - 1, col - 1, grid) or
            pathFinderCheck(update, row - 1, col, grid) or
            pathFinderCheck(update, row - 1, col + 1, grid) or
            pathFinderCheck(update, row, col - 1, grid) or
            pathFinderCheck(update, row, col + 1, grid) or
            pathFinderCheck(update, row + 1, col - 1, grid) or
            pathFinderCheck(update, row + 1, col, grid) or
            pathFinderCheck(update, row + 1, col + 1, grid)):
            displayGrid[row][col]["bg"] = '#93ff7a'
            return True
        else:
            return False

def solve():
    #disable editing board
    toggleBoardEdit()
    #yikes
    grid = [["","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
    #function fillGrid will return -1, -1 if character 'a' is not found.
    startRow, startCol = fillGrid(grid)
    if startRow == -1:
        message["text"] = "Start point 'A' not found."
    else:
        message["text"] = "Finding Solution..."
        if pathFinderSolve("abcdefghijklmnopqrstuvwxy", startRow, startCol, grid):
            message["text"] = "Board solved!"
        else:
            message["text"] = "No possible solution found."

    #reenable board
    toggleBoardEdit()

def pathFinderSolve(charsLeft, row, col, grid):
    if len(charsLeft) == 0:
        return True
    elif row < 0 or row >= 5 or col < 0 or col >= 5 or not charsLeft[0] in grid[row][col]:
        return False
    else:
        backup = grid[row][col]
        grid[row][col] = charsLeft[0]
        displayContents[row][col].set(charsLeft[0])
        root.update()
        #pause for dramatic effect
        time.sleep(.05)
        update = charsLeft [1:]
        result = (pathFinderSolve(update, row - 1, col - 1, grid) or
            pathFinderSolve(update, row - 1, col, grid) or
            pathFinderSolve(update, row - 1, col + 1, grid) or
            pathFinderSolve(update, row, col - 1, grid) or
            pathFinderSolve(update, row, col + 1, grid) or
            pathFinderSolve(update, row + 1, col - 1, grid) or
            pathFinderSolve(update, row + 1, col, grid) or
            pathFinderSolve(update, row + 1, col + 1, grid))
        if not result and grid[row][col] !='a':
            displayContents[row][col].set("")
        grid[row][col] = backup
        return result

#helper function to disable/enable main board
def toggleBoardEdit():
    if displayGrid[0][0]["state"] == "normal":
        for i in displayGrid:
            for j in range(5):
                i[j]["state"] = "disabled"
        editButton["state"] = "disabled"
        checkButton["state"] = "disabled"
        solveButton["state"] = "disabled"
    else:
        for i in displayGrid:
            for j in range(5):
                i[j]["state"] = "normal"
        editButton["state"] = "normal"
        checkButton["state"] = "normal"
        solveButton["state"] = "normal"

#helper function to fill out grid for solving/verifying
#returns row and column of character if found, -1 , -1 (impossible value) if not found
def fillGrid(grid):
    for i in range(5):
        for j in range(5):
            displayGrid[i][j]["bg"] = "#ffffff"
            grid[j][i] += displayChars[i].get().lower() + displayChars[i + 5].get().lower()
    for i in range(5):
        for j in range(5):
            grid[i][j] += displayChars[i + 10].get().lower() + displayChars[i + 15].get().lower()
    for i in range(5):
        grid[i][i] += displayChars[20].get().lower() + displayChars[21].get().lower()
        grid[4-i][i] += displayChars[22].get().lower() + displayChars[23].get().lower()
    count = 0
    while (count < 26):
        if count > 24:
            return -1, -1
        if displayContents[int(count/5)][int(count%5)].get().lower() == "a":
            grid[int(count/5)][int(count%5)] = 'a'
            return int(count/5), int(count%5)
        count+=1

root = Tk()
root.title("ABC Path")
titleFrame = Frame(root)
boardFrame = Frame(root)
messageFrame = Frame(root)
buttonFrame = Frame(root)

title = Label(titleFrame, text="ABC Path", font = ('Calibri', 32)).grid(row = 0, column = 0, columnspan = 9, pady = (0, 10))

verticalChars = ['','','','','']
horizontalChars = ['','','','','']
downDiagChars = ['','',]
upDiagChars = ['','']

#display grid
displayGrid = [
    [],
    [],
    [],
    [],
    []
]
displayContents = [
    [],
    [],
    [],
    [],
    []
]

for i in displayGrid:
    for j in range(5):
        v = StringVar()
        e = Entry(boardFrame, textvariable=v, justify = 'center', font = ('Calibri', 40), width = 2)
        e.grid(row = (displayGrid.index(i) + 3), column = (j + 2))
        i.append(e)
        displayContents[displayGrid.index(i)].append(v)

#adds outer characters to displayChars on top from left to right.
for i in range(5):
    e = Entry(boardFrame, justify = 'center', state = 'disabled', width = 2, font = ('Calibri', 16))
    e.grid(row = 1, column = i + 2)
    displayChars.append(e)
    dirArrow = Label(boardFrame, justify = 'center', width = 2, text = '↓', font = ('Calibri', 16)).grid(row = 2, column = i + 2)
#adds outer characters to displayChars on bot from left to right.
for i in range(5):    
    e = Entry(boardFrame, justify = 'center', state = 'disabled', width = 2, font = ('Calibri', 16))
    e.grid(row = 9, column = i + 2)
    displayChars.append(e)
    dirArrow = Label(boardFrame, justify = 'center', width = 2, text = '↑', font = ('Calibri', 16)).grid(row = 8, column = i + 2)
#adds outer characters to displayChars on left from top to bot.
for i in range(5): 
    e = Entry(boardFrame, justify = 'center', state = 'disabled', width = 2, font = ('Calibri', 16))
    e.grid(row = i + 3, column = 0)
    displayChars.append(e)
    dirArrow = Label(boardFrame, justify = 'center', width = 2, text = '→', font = ('Calibri', 16)).grid(row = i + 3, column = 1)
#adds outer characters to displayChars on right from top to bot.
for i in range(5):  
    e = Entry(boardFrame, justify = 'center', state = 'disabled', width = 2, font = ('Calibri', 16))
    e.grid(row = i + 3, column = 8)
    displayChars.append(e)
    dirArrow = Label(boardFrame, justify = 'center', width = 2, text = '←', font = ('Calibri', 16)).grid(row = i + 3, column = 7)


#adds downward diagonal characters then upward diagonal characters to displayChars. chars added left to right
e = Entry(boardFrame, justify = 'center', state = 'disabled', width = 2, font = ('Calibri', 16))
e.grid(row = 1, column = 0)
displayChars.append(e)
dirArrow = Label(boardFrame, justify = 'center', width = 2, text = '↘', font = ('Calibri', 16)).grid(row = 2, column = 1)
e = Entry(boardFrame, justify = 'center', state = 'disabled', width = 2, font = ('Calibri', 16))
e.grid(row = 9, column = 8)
displayChars.append(e)
dirArrow = Label(boardFrame, justify = 'center', width = 2, text = '↖', font = ('Calibri', 16)).grid(row = 8, column = 7)
e = Entry(boardFrame, justify = 'center', state = 'disabled', width = 2, font = ('Calibri', 16))
e.grid(row = 9, column = 0)
displayChars.append(e)
dirArrow = Label(boardFrame, justify = 'center', width = 2, text = '↗', font = ('Calibri', 16)).grid(row = 8, column = 1)
e = Entry(boardFrame, justify = 'center', state = 'disabled', width = 2, font = ('Calibri', 16))
e.grid(row = 1, column = 8)
displayChars.append(e)
dirArrow = Label(boardFrame, justify = 'center', width = 2, text = '↙', font = ('Calibri', 16)).grid(row = 2, column = 7)

#multipurpose message
message = Label(messageFrame, width=100)
message.grid(row = 0, column = 0, pady = (5))



#buttons
editButton = Button(buttonFrame, text="Set up Board", width = 12, command = edit)
editButton.grid(row = 0, column = 0, pady = (5))
spacer = Label(buttonFrame, text="").grid(row = 1, column = 1, padx = (1))
checkButton = Button(buttonFrame, text="Check Solution", width = 13, command = check)
checkButton.grid(row = 0, column = 2, pady = (5))
spacer = Label(buttonFrame, text="").grid(row = 1, column = 3, padx = (1))
solveButton = Button(buttonFrame, text="Solve Board", width = 12, command = solve)
solveButton.grid(row = 0, column = 4, pady = (5))


titleFrame.grid(row = 0)
boardFrame.grid(row = 1)
messageFrame.grid(row = 2)
buttonFrame.grid(row = 3)
edit()
preset()
edit()
root.mainloop()