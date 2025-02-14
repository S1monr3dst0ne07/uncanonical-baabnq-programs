import cv2, sys, time

TARGETFPS = 20
TARGETSIZE = (19, 14)
CHAR = '#'

xCap = cv2.VideoCapture(sys.argv[1])

xHeight     = xCap.get(cv2.CAP_PROP_FRAME_HEIGHT)
xWidth      = xCap.get(cv2.CAP_PROP_FRAME_WIDTH)
xFps        = xCap.get(cv2.CAP_PROP_FPS)
xFrameCount = xCap.get(cv2.CAP_PROP_FRAME_COUNT)

#correct frame rate
print(f"Original frame rate: {xFps}\nCorrected frame rate {TARGETFPS}\nFrame count: {xFrameCount}".format())
input("Press enter to continue")


xIndexIn = 0
xIndexOut = -1

xStrBuffer = []


while True:    
    xSuc = xCap.grab()
    if not xSuc: break
    print(f"Frames: {xIndexIn}/{xFrameCount}".format())

    xOutDue = int(xIndexIn / xFps * TARGETFPS)    
    if xOutDue > xIndexOut:
        xSuc, xFrame = xCap.retrieve()
        if not xSuc: break
        
        xComFrame = cv2.resize(xFrame, TARGETSIZE)
        xBoolFrame = [[list(y) == [255, 255, 255] for y in x] for x in xComFrame]
        
        xFrame = "\n".join(["".join([(CHAR if y else "_") for y in x]) for x in xBoolFrame])
        xStrBuffer.append(xFrame.replace("\n", ""))
        
        print(xFrame)
        #time.sleep((1/TARGETFPS))

        

        xIndexOut += 1
    xIndexIn += 1


xCap.release()
cv2.destroyAllWindows()

xOutput = f"data modify storage minecraft:video data set value {str(xStrBuffer)}".format()


with open("loadvid.mcfunction", "w") as xFile:
    xFile.write(xOutput)