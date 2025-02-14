import cv2, sys, time, nbt, itertools

STARTINDEX = 100
TARGETFPS = 20
TARGETSIZE = (32, 32)

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

xOutputBuffer = [[] for i in range(TARGETSIZE[0] * TARGETSIZE[1])]

while True:    
    xSuc = xCap.grab()
    if not xSuc: break
    print(f"Frames: {xIndexIn}/{xFrameCount}".format())

    xOutDue = int(xIndexIn / xFps * TARGETFPS)    
    if xOutDue > xIndexOut:
        xSuc, xFrame = xCap.retrieve()
        if not xSuc: break
        
        xComFrame = cv2.resize(xFrame, TARGETSIZE)
                
        for y in range(TARGETSIZE[1]):
            for x in range(TARGETSIZE[0]):
                xIsWhite = sum(xComFrame[y][x]) > 128 * 3
                xOutputBuffer[x + y * TARGETSIZE[0]].append(int(xIsWhite))
                                

        xIndexOut += 1
    xIndexIn += 1

xCap.release()
cv2.destroyAllWindows()


with open("loadvid.mcfunction", "w") as xFile:
    xFile.write(f'data modify storage minecraft:video binary set value {xOutputBuffer}')

