import cv2
import mouse
import keyboard
import numpy as np
import pytesseract
from PIL import ImageGrab
from PIL import Image
import time
import ctypes


positionsToClickNPC = [[919, 902], [1121, 925], [1365, 948], [1607, 958], [1878, 968]]
questNumberPositions = [[1220, 523],[1550, 523],[1885, 523]]
questTimeEff = []
questTimes = []
lastMousePos = [0, 0]
#waitBetweenQuests = True
goldWeight = 25
user32 = ctypes.windll.user32
screenSize = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
arenaTimeCounter = 0
doOnlyArenas = False

testMode = False
if(not testMode):    
    flatTimeReduction = int(input("Flat quest time reduction: "))
    beersToDrink = int(input("Number of beers to drink: "))
    tempWaitForArena = input("Do arenas inbetween quests (True/False): ")
    if(tempWaitForArena == "True"): 
        waitForArena = True
        arenaPositionToStartFrom = int(input("Position to start from: "))
        arenaStartDelay = int(input("Arena start delay: "))
        arenaTimeCounter = 600 - arenaStartDelay
    else: waitForArena = False

    tempDoArenasInsteadOfWatch = input("Do arenas instead of watch (True/False): ")
    if(tempDoArenasInsteadOfWatch == "True"): 
        doArenasInsteadOfWatch = True
    else: doArenasInsteadOfWatch = False
#percentualTimeReduction = int(input("Percentual quest time reduction: ")) not needed, its already accounted for in the scanned number


def AntiBanMoveRandomness(originalInt):
    return np.random.randint(originalInt-5, originalInt+5)

def FormatImageString(originalStr):
    print(originalStr)
    originalStr = originalStr.replace("\n", "")
    originalStr = originalStr.replace("N", "4")
    originalStr = originalStr.replace("y", "4")
    originalStr = originalStr.replace("q", "4")
    originalStr = originalStr.replace(" ", "")
    originalStr = originalStr.replace(",", ".")
    originalStr = originalStr.replace(":¥:Yo)", "880") #ok lol tak jo
    originalStr = originalStr.replace("o", "0")
    originalStr = originalStr.replace("O", "0")
    try:
        float(originalStr.replace(":", ""))
    except:
        originalStr = "1"
    
    if(originalStr == ""):
        originalStr = "1"
    return originalStr

def AdjustCoordinatesForScreen(originalSize1, originalSize2, useRandomness = True):
    global screenSize
    if(useRandomness):
        newSizes = [AntiBanMoveRandomness(round(originalSize1/2560*screenSize[0])), AntiBanMoveRandomness(round(originalSize2/1440*screenSize[1]))]
    else:
        newSizes = [round(originalSize1/2560*screenSize[0]), round(originalSize2/1440*screenSize[1])]
    #print(originalSize1, originalSize2, newSizes)
    return [newSizes[0], newSizes[1]]

def CheckIfGotLoggedOut():
    temp = AdjustCoordinatesForScreen(1367, 482)
    if(ImageGrab.grab().load()[temp[0], temp[1]] == (57, 178, 214)):
        print("Got logged out, logging back in")
        temp = AdjustCoordinatesForScreen(1523, 689)
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
        time.sleep(3)
        return True
    return False


def ClickNPC():
    global beersToDrink 
    temp = AdjustCoordinatesForScreen(1040, 1238, False)
    #print(ImageGrab.grab().load()[temp[0], temp[1]])
    if(ImageGrab.grab().load()[temp[0], temp[1]] == (97, 43, 16)):
        if(beersToDrink == 0):
            if(not doArenasInsteadOfWatch):
                print("Not enough Quest motivation and no more beers to drink! Going to city watch")
                time.sleep(5)
                GoToCityWatch()
                return
            else:
                print("Not enough Quest motivation and no more beers to drink! Going to arena")
                global doOnlyArenas 
                doOnlyArenas = True
                temp = AdjustCoordinatesForScreen(343, 1162) #sin slavy
                mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
                mouse.click("left")
                time.sleep(0.5)
                try:
                    time.sleep(arenaStartDelay)
                except:
                    time.sleep(5)
                GoToArena()
                return
        print("Drinking beer")
        beersToDrink = beersToDrink - 1
        temp = AdjustCoordinatesForScreen(2268, 722)
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
        time.sleep(np.random.randint(1, 10)/10)
        temp = AdjustCoordinatesForScreen(1536, 1062)
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
        time.sleep(np.random.randint(1, 10)/10)
        temp = AdjustCoordinatesForScreen(2048, 371)
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
        time.sleep(np.random.randint(1, 10)/10)

    print("Opening quest NPC dialogue")
    for i in positionsToClickNPC:
        temp = AdjustCoordinatesForScreen(i[0], i[1])
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
        time.sleep(np.random.randint(1, 10)/10)
        temp = AdjustCoordinatesForScreen(1229, 525, False)
        print(ImageGrab.grab().load()[temp[0], temp[1]], ImageGrab.grab().load()[1229, 525])
        if(ImageGrab.grab().load()[temp[0], temp[1]] == (223, 184, 67)):
            print("NPC Quest offers opened")
            SelectQuest()
            break

def SelectQuest():
    pytesseract.pytesseract.tesseract_cmd =(r"c:\Program Files\Tesseract-OCR\tesseract")
    for x in questNumberPositions:
        temp = AdjustCoordinatesForScreen(x[0], x[1])
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
        time.sleep(np.random.randint(1, 10)/10)
        
        temp1 = AdjustCoordinatesForScreen(1450, 881, False); temp2 = AdjustCoordinatesForScreen(1600, 918, False)
        expAmountImage = ImageGrab.grab(bbox=(temp1[0], temp1[1], temp2[0], temp2[1]))
        temp1 = AdjustCoordinatesForScreen(1705, 881, False); temp2 = AdjustCoordinatesForScreen(1825, 918, False)
        timeAmountImage = ImageGrab.grab(bbox=(temp1[0], temp1[1], temp2[0], temp2[1]))
        temp1 = AdjustCoordinatesForScreen(1180, 881, False); temp2 = AdjustCoordinatesForScreen(1323, 918, False)
        goldAmountImage = ImageGrab.grab(bbox=(temp1[0], temp1[1], temp2[0], temp2[1]))

        time.sleep(np.random.randint(1, 10)/10)
        tesstrExp = pytesseract.image_to_string(expAmountImage, config='--psm 6')
        expNum = int(FormatImageString(tesstrExp))
        time.sleep(np.random.randint(1, 10)/10)

        tesstrTime = pytesseract.image_to_string(timeAmountImage, config='--psm 6')
        tempSplit = FormatImageString(tesstrTime).split(":")
        timeNum = int(tempSplit[0])*60 + int(tempSplit[1])
        time.sleep(np.random.randint(1, 10)/10)
        
        tesstrGold = pytesseract.image_to_string(goldAmountImage, config='--psm 6')
        goldNum = float(FormatImageString(tesstrGold))
        global goldWeight
        print("Gold:", goldNum, ", Exp:", expNum, ", Time:", timeNum, ", Time eff:", (expNum+goldWeight*goldNum)/timeNum)
        
        questTimes.append(timeNum)
        questTimeEff.append((expNum+goldWeight*goldNum)/timeNum)


    print("Quest exp efficiency:", questTimeEff, ", selected quest: ", questTimeEff.index(np.max(questTimeEff)))
    temp = AdjustCoordinatesForScreen(questNumberPositions[questTimeEff.index(np.max(questTimeEff))][0], questNumberPositions[questTimeEff.index(np.max(questTimeEff))][1])
    mouse.move(temp[0] ,temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    temp = AdjustCoordinatesForScreen(1550, 1020)
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    
    CompleteQuest(questTimes[questTimeEff.index(np.max(questTimeEff))])
    
def CompleteQuest(timeNum):
    global arenaTimeCounter
    arenaTimeCounter = arenaTimeCounter + timeNum
    print("Quest selected, sleeping for", (timeNum-flatTimeReduction+3), " seconds")
    time.sleep(timeNum-flatTimeReduction+3)

    if(CheckIfGotLoggedOut()):
        temp = AdjustCoordinatesForScreen(350, 365) #zpet do hospody
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
    
    temp = AdjustCoordinatesForScreen(1678, 1278)
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    time.sleep(3)
    print("Claiming the rewards")
    mouse.click("left")
    time.sleep(5)
    questTimeEff.clear()
    questTimes.clear()
    temp = AdjustCoordinatesForScreen(1292, 268, False)
    if(ImageGrab.grab().load()[temp[0], temp[1]] == (231, 206, 79)):
        temp = AdjustCoordinatesForScreen(1651, 1218)
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 3)/10) 
        mouse.click("left")
        time.sleep(1)
    
    if(arenaTimeCounter > 600 and waitForArena):
        arenaTimeCounter = 0
        
        GoToArena()
        print("came back from arena, going back to the tavern")

        temp = AdjustCoordinatesForScreen(350, 365) #zpet do hospody
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
        # temp = AdjustCoordinatesForScreen(350, 455) #do areny
        # mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        # mouse.click("left")
        # time.sleep(60)
        # CheckIfGotLoggedOut()
        # temp = AdjustCoordinatesForScreen(350, 365) #zpet do hospody
        # mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 3)/10)
        # mouse.click("left")
        # time.sleep(0.3)
    ClickNPC()
    print("End of script, repeating \n")


def GoToCityWatch():
    temp = AdjustCoordinatesForScreen(1436, 217) #npc click
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    
    temp = AdjustCoordinatesForScreen(1538, 917) #potvrzeni
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    time.sleep(3605)
    print("hlidka dodelana")
    
    CheckIfGotLoggedOut()
    temp = AdjustCoordinatesForScreen(1540, 1289) #claimnuti
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")

    temp = AdjustCoordinatesForScreen(350, 365) #zpet do hospody
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    
    time.sleep(60)
    GoToCityWatch()

def GoToArena():
    global doOnlyArenas
    if(CheckIfGotLoggedOut() or not doOnlyArenas):
        temp = AdjustCoordinatesForScreen(343, 1162) #sin slavy
        mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
        mouse.click("left")
        time.sleep(0.5)

    global arenaPositionToStartFrom

    temp = AdjustCoordinatesForScreen(965, 1327) #search bar
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    time.sleep(0.5)

    
    keyboard.write(str(arenaPositionToStartFrom)) #napsani pozice
    arenaPositionToStartFrom = arenaPositionToStartFrom + 1
    time.sleep(0.5)

    temp = AdjustCoordinatesForScreen(1386, 1327) #searchnuti
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    time.sleep(0.5)

    temp = AdjustCoordinatesForScreen(2140, 207) #zautoceni
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    time.sleep(0.5)

    temp = AdjustCoordinatesForScreen(1543, 906) #potvrzeni zautoceni
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    time.sleep(0.5)

    
    temp = AdjustCoordinatesForScreen(1531, 1273) #claimnuti
    mouse.move(temp[0], temp[1], absolute=True, duration=np.random.randint(1, 10)/10)
    mouse.click("left")
    time.sleep(1)
    mouse.click("left")
    print("Fight over, sleeping for 10 mins")
    
    if(doOnlyArenas): 
        time.sleep(600)
        GoToArena()
    time.sleep(1)


def TestImage(size1, size2):
    x = ImageGrab.grab(bbox=(size1[0], size1[1], size2[0], size2[1]))
    x.show()

while testMode:

    if(mouse.is_pressed("right") and mouse.get_position() != lastMousePos and testMode):
        # pytesseract.pytesseract.tesseract_cmd =(r"c:\Program Files\Tesseract-OCR\tesseract")
        # #expAmountImage = ImageGrab.grab(bbox=(1450, 881, 1600, 918))
        # timeAmountImage = ImageGrab.grab(bbox=(1705, 881, 1825, 918))
        # #tesstr = pytesseract.image_to_string(expAmountImage, config='--psm 6')
        # tesstr = pytesseract.image_to_string(timeAmountImage, config='--psm 6')
        # if(tesstr == ""):
        #     print("Unable to read")
        # else:
        #     tesstr = tesstr.replace("N", "4")
        #     print(tesstr)
        #ClickNPC()
        #mouse.move(1229, 525, absolute=True)
        # o = ImageGrab.grab(bbox=(1570, 685, 1685, 790))
        # o.show()
        # s = ImageGrab.grab(bbox=(1570, 502, 1685, 607))
        # s.show()
        # q = ImageGrab.grab(bbox=(1570, 685, 1685, 790))
        # q.show()
        
        # x = ImageGrab.grab(bbox=(1590, 700, 1690, 800))
        # x.show()
        # # o.save("G:/Test/testFile.jpg")
        print(mouse.get_position())
        #print(ImageGrab.grab().load()[mouse.get_position()])
        TestImage((1568, 125), (1679, 240))
        TestImage((1568, 309), (1679, 422))
        TestImage((1568, 495), (1679, 607))
        TestImage((1569, 679), (1678, 793))

        TestImage((1820, 679), (1935, 789))
        TestImage((2008, 679), (2168, 837))

        TestImage((2261, 127), (2373, 238))
        TestImage((2261, 311), (2373, 423))
        TestImage((2261, 495), (2373, 607))
        TestImage((2261, 679), (2373, 790))

        lastMousePos = mouse.get_position()

if(not testMode):
    print("Starting!")
    time.sleep(15)
    ClickNPC()


#1570, 685, 1685, 790 box na boty (115x 105y) - ke kraji nahore levo: x = -3px, y = -9px; ke kraji dole pravo: x = +46px, y = +50;
(1567, 676) #levy horni
(1731, 840) #pravy spodni

#vynechat y =9+20+114= 143px, velka doprava x =3+88+46= 137px

#zbran
(1830, 690)
(1930, 790)
#boty
(1590, 700)
(1690, 800)

(1679, 793) #boty new

(1567, 840) #levy spodni 
(1731, 676) #pravy horni 


(1729, 656) #mezera horni - 20 px
(1819, 676) #mezera prava - 88 px
#ctverec 164x164


#(1229, 525)
# (1450, 881)
#(1599, 918)
# (1705, 883)
#(1825, 920)
#(1556, 1019)
#(1678, 1278)
#(1179, 885)
#(1323, 921)
#(1040, 1238)
#(97, 43, 16)
#(2268, 722)
#(1536, 1062)
#(2048, 371)
#(350, 455)
#(350, 365)
#(1292, 268)
#(231, 206, 79)
#(1651, 1218)
#(1436, 217)
#(1538, 917)
#(1540, 1289)
#(1367, 482)
#(57, 178, 214)
#(1523, 689)
#(343, 1162) sin slavy
#(965, 1327) search bar
#(1386, 1327) search tlacitko
#(2140, 207) attack tlacitko
#(1543, 906) potvrzeni
#(1531, 1273) claimnuti

#left
(1568, 125) #capka
(1679, 240)

(1568, 309) #armor
(1679, 422)

(1568, 495) #rukavice
(1679, 607)

(1569, 679) #boty
(1678, 793)

#mid
(1820, 679) #zbran
(1935, 789)

(2008, 679) #shield
(2168, 837)

#right
(2261, 127) #nahrdelnik
(2373, 238)

(2261, 311) #opasek
(2373, 423)

(2261, 495) #prsten
(2373, 607)

(2261, 679) #charm
(2373, 790)