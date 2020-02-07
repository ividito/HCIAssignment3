BUTTONSIZE = 25
BUTTONGAP = 15
BUTTONCOUNT = 25

uid = ""
roundCounter = 0
condition = ""
buttons = []
userState = 0


def generateButtons():
    global buttons
    for _ in range(BUTTONCOUNT):
        seeking = True
        x = 0
        y = 0
        while seeking:
            seeking = False
            x = random(BUTTONGAP+BUTTONSIZE, width - (BUTTONGAP + BUTTONSIZE))
            y = random(BUTTONGAP+BUTTONSIZE, height - (BUTTONGAP + BUTTONSIZE))
            for b in buttons:
                if dist(x, y, b[0], b[1]) < 2 * BUTTONSIZE + BUTTONGAP:
                    seeking = True
        buttons.append([x, y])
    
def initialState():
    global uid
    background(50)
    textSize(32)
    prompt = "1. Enter User Id: " + uid
    text(prompt, 10, 32)
    
def keyPressed():
    global userState, uid
    if key == ESC:
        exit()
    if userState == 0:
        if key == ENTER:
            userState += 1
        else:
            uid += key
    
def conditionSelection():
    background(50)
    fill(220)
    textSize(32)
    text("2. Select Condition", 10, 74)
    fill(220)
    rect(10, 120, 150, 50)
    rect(180, 120, 150, 50)
    fill(0)
    text("1", 75, 160)
    text("2", 245, 160)
    
def mousePressed():
    global userState, condition
    if userState == 1:  # condition selection
        global condition
        if 10 < mouseX < 160 and 120 < mouseY < 170:
            condition = 'normal'
            userState+=1
        elif 180 < mouseX < 330 and 120 < mouseY < 170:
            condition = 'area'
            userState+=1
    elif userState == 2: #starting the trial
        # if initial button pressed, move userState to trial
        pass
    elif userState == 3:
        pass
        # check if any button is pressed, move trial along

def initialTargetState():
    global condition
    background(50)
    fill(220)
    text(condition, 10, 116)
    fill(250, 0, 20)
    if len(buttons) == 0:
        generateButtons()
    for b in buttons:
        x = b[0]
        y = b[1]
        circle(x, y, BUTTONSIZE)
    # Pick a button as start
    
def trial():
    pass
    
drawState = { 0: initialState,
              1: conditionSelection,
              2: initialTargetState,
              3: trial}

def setup():
    size(720, 720)
    
def draw():
    drawState[userState]()
