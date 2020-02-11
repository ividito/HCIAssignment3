BUTTONSIZE = 25*2
BUTTONGAP = 15
BUTTONCOUNT = 25
TARGETLIMIT = 21

uid = ""
roundCounter = 0
condition = ""
buttons = []
userState = 0
target = [0,0]
targetCounter = 0

roundPrompts = { 0 : "This is a practice round. Select the highlighted dots as quickly and accurately as possible.",
                 1 : "This is round 1/3. Select the highlighted dots as quickly and accurately as possible.",
                 2 : "This is round 2/3. Select the highlighted dots as quickly and accurately as possible.",
                 3 : "This is round 3/3. Select the highlighted dots as quickly and accurately as possible."
                 }


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
    global userState, condition, targetCounter, roundCounter, target
    if userState == 1:  # condition selection
        global condition
        if 10 < mouseX < 160 and 120 < mouseY < 170:
            condition = 'normal'
            userState+=1
        elif 180 < mouseX < 330 and 120 < mouseY < 170:
            condition = 'area'
            userState+=1
    elif userState == 2: #starting the trial
        check, radius = isValid(mouseX, mouseY)
        fill(0, 0, 220, 30)
        circle(mouseX, mouseY, radius)
        if (check):            
            targetCounter += 1
            userState += 1
    elif userState == 3:
        check, radius = isValid(mouseX, mouseY)
        if (check):
            if targetCounter > TARGETLIMIT:
                roundCounter += 1
                userState -= 1
            else:
                targetCounter += 1
                # TODO We also need to add logging
            

def initialTargetState():
    global condition, target, targetCounter, roundCounter, roundPrompts
    background(50)
    fill(250, 0, 20)
    if len(buttons) == 0 or targetCounter > 0:
        generateButtons()
        targetCounter = 0
    for b in buttons:
        x = b[0]
        y = b[1]
        circle(x, y, BUTTONSIZE)
    target = buttons[targetCounter]
    fill(0, 250, 20)
    circle(target[0], target[1], BUTTONSIZE)
    check, radius = isValid(mouseX, mouseY)
    fill(0, 0, 220, 30)
    circle(mouseX, mouseY, radius)
    fill(250)
    prompt = roundPrompts[roundCounter]
    text(prompt, 10, 30)
    
def trial():
    global condition, target, targetCounter
    background(50)
    fill(250, 0, 20)
    for b in buttons:
        x = b[0]
        y = b[1]
        circle(x, y, BUTTONSIZE)
    target = buttons[targetCounter % len(buttons)]
    fill(0, 250, 20)
    circle(target[0], target[1], BUTTONSIZE)
    radius = getRadius()
    fill(0, 0, 220, 30)
    circle(mouseX, mouseY, radius)
    
drawState = { 0: initialState,
              1: conditionSelection,
              2: initialTargetState,
              3: trial}

def isValid(x, y):
    global condition, targetCounter, buttons
    if condition == "normal":
        if dist(x, y, target[0], target[1]) < BUTTONSIZE/2:
            return True, 0
        else:
            return False, 0
    elif condition == "area": # BubbleCursor Functionality
        minPointer = 0
        minDist = 9999  # arbitrary high value
        for i, b in enumerate(buttons):
            if dist(x, y, b[0], b[1]) < minDist:
                minPointer = i
                minDist = dist(x, y, b[0], b[1])
        if minPointer == targetCounter:
            return True, minDist
        else:
            return False, minDist

def getRadius():
    global condition, buttons
    if condition == "normal":
        return 0
    else:
        minPointer = 0
        minDist = 9999  # arbitrary high value
        for i, b in enumerate(buttons):
            if dist(mouseX, mouseY, b[0], b[1]) < minDist:
                minPointer = i
                minDist = dist(mouseX, mouseY, b[0], b[1])
        return minDist
        

def setup():
    frameRate(30)
    size(720, 720)
    
def draw():
    drawState[userState]()
    text(userState, 10, 30)
