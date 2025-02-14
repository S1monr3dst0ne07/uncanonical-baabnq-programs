import cv2, sys, time, nbt, itertools

STARTINDEX = 100
TARGETFPS = 20
TARGETSIZE = (128, 128)
BLACKVAL = 29 * 4
WHITEVAL = 8  * 4


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

xFrameIndex = 0
while True:    
    xSuc = xCap.grab()
    if not xSuc: break
    print(f"Frames: {xIndexIn}/{xFrameCount}".format())

    xOutDue = int(xIndexIn / xFps * TARGETFPS)    
    if xOutDue > xIndexOut:
        xSuc, xFrame = xCap.retrieve()
        if not xSuc: break
        
        xComFrame = cv2.resize(xFrame, TARGETSIZE)
                
        #cv2.imshow('frame', xComFrame)
        #cv2.waitKey(1)
        
        xIntFrame   = [[(1 if sum(y) > 127 * 3 else 0) for y in x] for x in xComFrame]
        xRenderFrame = [[WHITEVAL, BLACKVAL][x] for x in itertools.chain.from_iterable(xIntFrame)]
                        
        xNbtFile = nbt.nbt.NBTFile("map.dat")        
        xNbtFile['data']['colors'].value = xRenderFrame

        with open(f"maps\\map_{xFrameIndex + STARTINDEX}.dat", "wb") as xFile:        
            xNbtFile.write_file(fileobj = xFile)
        
        #print("\n".join(["".join([["_", "#"][y] for y in x]) for x in xIntFrame]))
        #time.sleep((1/TARGETFPS))
        xFrameIndex += 1
        

        xIndexOut += 1
    xIndexIn += 1


xCap.release()
cv2.destroyAllWindows()
