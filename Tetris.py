### SAMS Senior CS-Track Hw5
### Due Date: Monday 08/05 8:30pm
### Name: aghernan
### andrewID: Angello Hernandez

# Use the guidelines at the following website to implement the game Tetris.
# http://krivers.net/15112-s19/notes/notes-tetris/index.html

# If you finish before the deadline, consider adding bonus features for
# additional points! If you choose to do this, please submit the core Tetris
# implementation on Autolab under hw5, then submit the bonus implementation
# under hw5-bonus.

# BONUS FEATURES SO FAR! :
# Hard Drop
# Music Note: Autolab doesn't like sounds and it requires PyGame so I commented out the music :(
# Better Rotation (Can rotate at edges)
# Different Scoring System (like the real Tetris!)
# Piece Holding
# Better Random System (Like the real Tetris 7 block system!) (Described here: https://tetris.fandom.com/wiki/Random_Generator)
# Outline Now you can see where your piece will fall!
# Much easier system for UI instead of margins. This doesn't affect gameplay but made it much easier to show piece holding and the next piece. I had to redesign the run() function, though.
# Levels: You can now progress through levels, and the pieces will come faster as you progress
# Visible NEXT and HOLD pieces! Much easier due to the UI update
# High Scores List: Doesn't have names yet but it shows any high scores!



### Problem 1: Tetris ###

"""
Follow the instructions here:
http://krivers.net/15112-s19/notes/notes-tetris/index.html

Note that we already set up the starter code and wrote gameDimensions() for you.
"""

from tkinter import *
import random
import copy
import winsound
import pygame
def playTetris():
    width = gameDimensions()[3]*2 + (gameDimensions()[1]*gameDimensions()[2])
    height = gameDimensions()[3]*2 + (gameDimensions()[0]*gameDimensions()[2])
    run(40,40,100,40,width,height)
    pass
    
def gameDimensions():
    # rows, cols, cellSize, margin
    return [20, 10,20,1]

def init(data):
    data.pieceBagCount = 0
    data.bgColor = "DodgerBlue4"
    data.timerDelay = 400
    pygame.init()
    pygame.mixer.unpause()
    data.pieceBagCount = 0
    data.gameOver = False
    data.alreadyHeld = False
    data.paused = False
    data.highScoresList = False
    data.timerDelayLevel = 20
    data.clearedLines = 0
    data.level = 1
    data.scoring = {0 : 0,
    1 : 40,
    2 : 100,
    3 : 300,
    4 : 1200
    }
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("tetris.wav"),-1)
    #Get columns, rows, cellsize, margin
    data.cols = gameDimensions()[1]
    data.rows = gameDimensions()[0]
    data.cellSize = gameDimensions()[2]
    data.margin = gameDimensions()[3] #remove to undo the "damage"
    data.isRotated = False
    #data.removedRow = False
    data.score = 0
    data.heldPiece = []
    #Make the board
    data.emptyColor = "gray45"
    data.board = [[data.emptyColor] * data.cols for i in range(data.rows)]
    
    ##Make the tetrominos
    data.iPiece = [
    [ True, True, True, True]
    ]
    data.jPiece = [
    [True, False, False],
    [True, True, True]
    ]
    data.lPiece = [
    [ False, False, True],
    [True, True, True]
    ]
    data.oPiece = [
    [True, True],
    [True, True]
    ]
    data.sPiece = [
    [False,True,True],
    [True,True,False]
    ]
    data.tPiece = [
    [False,True,False],
    [True,True,True]
    ]
    data.zPiece = [
    [True,True,False],
    [False,True,True]
    ]
    
    #Final Holders
    data.tetrisPieces = [data.iPiece,data.jPiece,data.lPiece,data.oPiece,data.sPiece,data.tPiece,data.zPiece]
    data.pieceColors = ["cyan","blue","orange","yellow","green2","purple","red"]
    ##End Tetrominos
    shufflePieces(data)
    getNewFallingPiece(data)

    
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if(not data.paused):
        if(event.keysym == "Down" and  data.fallingPieceRow < data.rows-1):
            if(moveFallingPiece(data,1,0)):
                data.score += 1
        elif(event.keysym == "Left"):
            moveFallingPiece(data,0,-1)
        elif(event.keysym == "Right"):
            moveFallingPiece(data,0,1)
        elif(event.keysym == "Up"):
            rotateFallingPiece(data)
        elif(event.keysym == "c"):
            holdPiece(data)
        elif(event.keysym == "space"):
            if(not data.gameOver):
                dScore = hardDropPiece(data)
                data.score += dScore
                placeFallingPiece(data)
                removeFullRows(data)
                getNewFallingPiece(data)
        elif(event.keysym == "p"):
            data.paused = True
            pygame.mixer.Channel(0).pause()
        elif(event.keysym == "r" and data.gameOver):
            init(data)
        elif(event.keysym == "h" and data.gameOver):
            if(data.highScoresList):
                data.highScoresList = False
            else:
                data.highScoresList = True
    elif(event.keysym == "p"):
        data.paused = False
        pygame.mixer.Channel(0).unpause()
    
def hardDropPiece(data):
    dScore = 0
    while (not data.gameOver):
        data.fallingPieceRow += 1
        dScore += 1
        if(not isValidMove(data)):
            data.fallingPieceRow -=1
            dScore -=1
            return dScore
            break
    return 0
            
def moveFallingPiece(data, dRow, dCol):
    data.fallingPieceCol += dCol
    data.fallingPieceRow += dRow
    if(not isValidMove(data)):
        data.fallingPieceCol -= dCol
        data.fallingPieceRow -= dRow
        return False
    return True
    
def isValidMove(data):
    y = 0
    for block in data.fallingPiece:
        for i in range(len(block)):
            if(block[i] == True):
                try:
                    if data.fallingPieceRow < 0 or data.fallingPieceCol < 0:
                        return False
                    if not data.board[data.fallingPieceRow+y][data.fallingPieceCol+i] == data.emptyColor:
                        return False
                except:
                    return False
        y += 1
    return True
    pass


def removeFullRows(data):
    nuBoard = []
    #data.removedRow = False
    linesRemoved = 0
    for row in (range(len(data.board))):
        c = data.board[row].count(data.emptyColor)
        if(c >= 1 and c < len(data.board[0])):
            nuBoard += [data.board[row]]
        elif(c == 0):
            linesRemoved += 1
            data.clearedLines += 1
            #data.removedRow = True
    for row in (range(len(nuBoard),len(data.board))):
        nuBoard.insert(0,[data.emptyColor] * data.cols)
    if(linesRemoved > 0):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("clearSound.wav"))
        data.score += data.scoring[linesRemoved] * data.level
        data.level = data.clearedLines//10 + 1
        if(not (data.level-1)*20 > data.timerDelay-20):
            data.timerDelayLevel = ((data.level-1) * 20)
        else:
            data.timerDelayLevel = 20
    data.board = nuBoard
    
def timerFired(data,canvas):
    isMoved = moveFallingPiece(data,1,0)
    if(not isMoved):
        placeFallingPiece(data)
        removeFullRows(data)
        getNewFallingPiece(data)
        if(not isValidMove(data)):
            data.gameOver = True
            getHighScores(data)
            pygame.mixer.pause()
        pass

def getHighScores(data):
    f = open("highScores.txt","a+")
    f.write((str(data.score) + "\n"))
    f.close()
    s = open("highScores.txt","r")
    data.highScores = s.readlines()
    s.close()
    data.highScores = '\n'.join(data.highScores)
    data.highScores = data.highScores.split()
    for i in range(len(data.highScores)):
        data.highScores[i] = int(data.highScores[i])
    data.highScores.sort(reverse=True)
    print(data.highScores) 
    

def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if(data.fallingPiece[row][col] == True):
                data.board[data.fallingPieceRow+row][data.fallingPieceCol+col] = data.fallingPieceColor
    data.alreadyHeld = False
    
def holdPiece(data):
    if(data.heldPiece == []):
        data.heldColor = data.fallingPieceColor
        data.heldPiece = copy.deepcopy(data.origFallingPiece)
        getNewFallingPiece(data)
        data.alreadyHeld = True
    elif(not data.alreadyHeld):
        holder = copy.deepcopy(data.heldPiece)
        data.heldPiece = copy.deepcopy(data.origFallingPiece)
        data.fallingPiece = copy.deepcopy(holder)
        data.fallingPieceRow = 0
        data.fallingPieceCol = len(data.board[0])//2 - data.numFallingPieceCols//2
        colorHolder = data.fallingPieceColor
        data.fallingPieceColor = data.heldColor
        data.heldColor = colorHolder
        data.alreadyHeld = True
    
    
    
    

def rotateFallingPiece(data):
    data.isRotated = True
    #Save old Piece
    data.prevPieceRow = len(data.fallingPiece)
    data.prevPieceCol = len(data.fallingPiece[0])
    data.prevFallingPiece = [[]]
    data.prevFallingPiece = [data.fallingPiece[i][:] for i in range(len(data.fallingPiece))]
       
    #New piece
    data.nuFallingPiece = [[None] * len(data.fallingPiece) for i in range(len(data.fallingPiece[0]))]
    nuCols = len(data.fallingPiece)
    nuRows = len(data.fallingPiece[0])
    #centers
    prevRow = data.fallingPieceRow
    prevCol = data.fallingPieceCol
    newRow = data.fallingPieceRow + data.prevPieceRow/2 - nuRows/2
    newCol = data.fallingPieceCol + data.prevPieceCol/2 - nuCols/2
    
    #Initiate new piece
    for i in range(len(data.fallingPiece)): #rows
        for l in range(len(data.fallingPiece[0])): #cols
            data.nuFallingPiece[data.prevPieceCol-1-l][i] = data.fallingPiece[i][l] #row, col
    
    data.fallingPiece = copy.deepcopy(data.nuFallingPiece)
    data.fallingPieceRow = round(newRow)
    data.fallingPieceCol = round(newCol)
    if(not isValidMove(data)):
        data.fallingPieceCol -= 1
        if(not isValidMove(data)):
            data.fallingPiece = copy.deepcopy(data.prevFallingPiece)
            data.fallingPieceRow = prevRow
            data.fallingPieceCol = prevCol
            data.isRotated = False



def getNewFallingPiece(data):
    data.fallingPiece = data.tetrisPieces[data.pieceBagCount-1]
    data.origFallingPiece = copy.deepcopy(data.fallingPiece)
    data.fallingPieceColor = data.pieceColors[data.pieceBagCount-1]
    data.numFallingPieceCols = len(data.fallingPiece[0])
    data.fallingPieceRow = 0
    data.fallingPieceCol = len(data.board[0])//2 - data.numFallingPieceCols//2
    if(not data.pieceBagCount == 6):
        data.nextFallingPiece = data.tetrisPieces[data.pieceBagCount]
        data.nextFallingPieceColor = data.pieceColors[data.pieceBagCount]
    data.pieceBagCount += 1
    if(data.pieceBagCount == 7):
        shufflePieces(data)
        data.nextFallingPiece = data.tetrisPieces[data.pieceBagCount-1]
        data.nextFallingPieceColor = data.pieceColors[data.pieceBagCount-1]

def shufflePieces(data):
    pieces = list(zip(data.tetrisPieces,data.pieceColors))
    data.pieceBagCount = 0
    random.shuffle(pieces)
    data.tetrisPieces,data.pieceColors = zip(*pieces)

def getOutlinePieceRow(data):
    data.outlinePiece = data.fallingPiece
    tempRow = data.fallingPieceRow
    hardDropPiece(data)
    data.outlinePieceRow = data.fallingPieceRow
    data.fallingPieceRow = tempRow

def drawOutlinePiece(data,canvas):
    getOutlinePieceRow(data)
    y = 0
    for block in data.outlinePiece:
        for i in range(len(block)):
            if(block[i] == True):
                canvas.create_rectangle((data.fallingPieceCol+i)*data.width/(data.cols),(data.outlinePieceRow+y)*(data.height)/(data.rows),((data.fallingPieceCol+i+1)*(data.width)/(data.cols)),(data.outlinePieceRow+1+y)*(data.height)/(data.rows),outline=data.fallingPieceColor,width=2)
        y += 1
    pass

def drawFallingPiece(data,canvas):
    drawOutlinePiece(data,canvas)
    y = 0
    for block in data.fallingPiece:
        for i in range(len(block)):
            if(block[i] == True):
                canvas.create_rectangle((data.fallingPieceCol+i)*(data.width)/(data.cols),(data.fallingPieceRow+y)*(data.height)/(data.rows),((data.fallingPieceCol+i+1)*(data.width)/(data.cols)),(data.fallingPieceRow+1+y)*(data.height)/(data.rows),fill=data.fallingPieceColor,width=3)
        y += 1
    
    pass

def redrawPads(pad3,pad4,data):
    pad3.create_rectangle(0,0,data.wPad1,data.height,fill=data.bgColor,width=0)
    pad4.create_rectangle(0,0,data.wPad2,data.height,fill=data.bgColor,width=0)
    ##BASE UI
    pad3.create_text(data.wPad1/2,data.height/10,text="HOLD",font="Arial 13 bold")
    pad3.create_rectangle(data.wPad1/10,3*data.height/20,9*data.wPad1/10,6*data.height/20,width=5,fill=data.emptyColor)
    pad4.create_text(data.wPad2/2,data.height/10,text="NEXT",font="Arial 13 bold")
    
    pad4.create_rectangle(data.wPad1/10,3*data.height/20,9*data.wPad1/10,6*data.height/20,width=5,fill=data.emptyColor)
    
    
    pad4.create_text(data.wPad2/2,4*data.height/10,text="SCORE",font="Arial 13 bold")
    pad4.create_text(data.wPad2/2,4*data.height/10,text="\n\n" + str(data.score),font="Arial 13 bold")
    pad4.create_text(data.wPad2/2,6*data.height/10,text="LEVEL",font="Arial 13 bold")
    pad4.create_text(data.wPad2/2,6*data.height/10,text="\n\n" + str(data.level),font="Arial 13 bold")
    pad4.create_text(data.wPad2/2,8*data.height/10,text="LINES",font="Arial 13 bold")
    pad4.create_text(data.wPad2/2,8*data.height/10,text="\n\n" + str(data.clearedLines),font="Arial 13 bold")
    ##END BASE UI
    """for row in range(len(data.nextFallingPiece)):
        for col in range(len(data.nextFallingPiece[0])):
            if(data.nextFallingPiece[row][col]):
                pad4.create_rectangle(((col+2)*data.wPad1/10)+data.wPad1/10,(row+1+3)*data.height/20,(col+3)*data.wPad1/10+data.wPad1/10,(row+2+3)*data.height/20,width=3,fill=data.nextFallingPieceColor)
    
    if(not data.heldPiece == []):
        for row in range(len(data.heldPiece)):
            for col in range(len(data.heldPiece[0])):
                if(data.heldPiece[row][col]):
                    pad3.create_rectangle(((col+2)*data.wPad1/10)+data.wPad1/10,(row+4)*data.height/20,(col+3)*data.wPad1/10+data.wPad1/10,(row+5)*data.height/20,width=3,fill=data.heldColor)
    """
    y = 3
    add = 0
    for block in data.nextFallingPiece:
        for i in range(len(block)):
            if(block[i] == True):
                if(len(block)) == 4:
                    add = -.5
                elif(len(block)) == 2:
                    add = .5
                pad4.create_rectangle((i+1+add)*(data.width)/(data.cols),(y+1)*(data.height)/(data.rows),((i+2+add)*(data.width)/(data.cols)),(2+y)*(data.height)/(data.rows),fill=data.nextFallingPieceColor,width=3)
                add = 0
        y += 1
    if(not data.heldPiece == []):
        y = 3
        add = 0
        for block in data.heldPiece:
            for i in range(len(block)):
                if(block[i] == True):
                    if(len(block)) == 4:
                        add = -.5
                    elif(len(block)) == 2:
                        add = .5
                    pad3.create_rectangle((i+1+add)*(data.width)/(data.cols),(y+1)*(data.height)/(data.rows),((i+2+add)*(data.width)/(data.cols)),(2+y)*(data.height)/(data.rows),fill=data.heldColor,width=3)
                    add = 0
            y += 1
        
    
    
def redrawAll(canvas, data):
    for y in range(0,data.rows):
        for x in range(0,data.cols):
            canvas.create_rectangle((x*(data.width)/(data.cols)),(y*(data.height)/(data.rows)),(x+1)*(data.width)/(data.cols),(y+1)*(data.height)/(data.rows),width=3,fill=data.board[y][x])
    drawFallingPiece(data,canvas)
    if(data.gameOver):
        canvas.create_rectangle(0,data.height/3,data.width,2*data.height/3,fill="white")
        canvas.create_text((data.width/3+2*data.width/3)/2,(data.height/3+3*data.height/6)/2,font="Arial",fill="black",text="Game Over!")
        canvas.create_text((data.width/3+2*data.width/3)/2,(data.height/3+2*data.height/3)/2,font="Arial",fill="black",text="Score: " + str(data.score))
        canvas.create_text((2*data.width/3+2*data.width/6)/2,(data.height/3+5*data.height/6)/2,font="Arial",fill="black",text="R: Retry, H: High Scores")
        if(data.highScoresList):
            canvas.create_rectangle(0,0,data.width,data.height,fill=data.emptyColor, width = 0)
            canvas.create_text(data.width/2,data.height/10,font="Arial 15 bold",fill="black",text="High Scores")
            try:
                for i in range(0,5):
                        canvas.create_text(data.width/10,i*data.height/6 +data.height/5,font="Arial",fill="black",text=str(i+1)+ ": ")
                        canvas.create_text(7*data.width/10,i*data.height/6 +data.height/5,font="Arial",fill="black",text=str(data.highScores[i]))
            except:
                pass


    elif(data.paused):
        canvas.create_rectangle(0,data.height/3,data.width,2*data.height/3,fill="white")
        canvas.create_text((data.width/3+2*data.width/3)/2,(data.height/3+2*data.height/3)/2,font="Arial",fill="black",text="Paused")
        
    pass
    


####################################
# use the run function as-is
####################################

def run(widthPad1,heightPad1,widthPad2,heightPad2,width=500, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    
    def redrawPadWrapper(pad3,pad4,data):
        try:
            pad3.delete(ALL)
            pad3.create_rectangle(0,0,data.wPad1,data.height,fill="white",width=0)
            pad4.delete(ALL)
            pad3.create_rectangle(0,0,data.wPad2,data.height,fill='white',width=0)
            redrawPads(pad3,pad4,data)
            pad3.update()
            pad4.update()
        except:
            pass
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
        redrawPadWrapper(pad3,pad4,data)

    def timerFiredWrapper(canvas,pad3,pad4,data):
        if(not data.gameOver and not data.paused):
            timerFired(data,canvas)
            
            redrawAllWrapper(canvas, data)
            redrawPadWrapper(pad3,pad4,data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay - data.timerDelayLevel, timerFiredWrapper, canvas, pad3,pad4,data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height # milliseconds
    data.wPad1 = widthPad1
    data.hPad1 = heightPad1
    data.wPad2 = widthPad2
    data.hPad2 = heightPad2
    if(data.wPad2 > data.wPad1):
        data.wPad1 = data.wPad2
    else:
        data.wPad1 = data.wPad2
    root = Tk()
    root.title("Tetris")
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    
    
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.grid(column=1,row=1)
    pad1 = Canvas(root,width=data.wPad1,height=data.hPad1)
    pad1.configure(bd=0, highlightthickness=0)
    pad1.grid(column=0,row=0)
    pad1.create_rectangle(0,0,data.wPad1,data.hPad1, fill = data.bgColor, width = 0)
    
    pad2 = Canvas(root,width=data.wPad2,height=data.hPad2)
    pad2.configure(bd=0, highlightthickness=0)
    pad2.grid(column=2,row=2)
    pad2.create_rectangle(0,0,data.wPad2,data.hPad2, fill = data.bgColor, width = 0)
    
    pad3 = Canvas(root,width = data.wPad1, height = data.height)
    pad3.configure(bd = 0, highlightthickness=0)
    pad3.grid(column=0,row=1)
    
    pad4 = Canvas(root,width = data.wPad2, height = data.height)
    pad4.configure(bd = 0, highlightthickness=0)
    pad4.grid(column=2,row=1)
    
    pad5 = Canvas(root,width=data.width,height=data.hPad1)
    pad5.configure(bd = 0, highlightthickness=0)
    pad5.grid(column=1,row=0)
    pad5.create_rectangle(0,0,data.width,data.hPad1,fill=data.bgColor,width=0)
    
    pad6 = Canvas(root,width=data.width,height=data.hPad2)
    pad6.configure(bd = 0, highlightthickness=0)
    pad6.grid(column=1,row=2)
    pad6.create_rectangle(0,0,data.width,data.hPad2,fill=data.bgColor,width=0)
    
    pad7 = Canvas(root,width=data.wPad1,height=data.hPad1)
    pad7.configure(bd = 0, highlightthickness = 0)
    pad7.grid(column=2,row=0)
    pad7.create_rectangle(0,0,data.wPad1,data.hPad1,fill=data.bgColor,width=0)
    
    pad8 = Canvas(root,width=data.wPad2,height=data.hPad2)
    pad8.configure(bd = 0, highlightthickness = 0)
    pad8.grid(column=0,row=2)
    pad8.create_rectangle(0,0,data.wPad2,data.hPad2,fill=data.bgColor,width=0)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas,pad3,pad4,data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    pygame.quit()
    print("bye!")

playTetris()
