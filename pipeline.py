import cv2
import numpy as np
import math
import os
import time
import winsound
import scipy.misc
cv2.ocl.setUseOpenCL(False)
print("cv2_version = ", cv2.__version__)
if str(cv2.__version__)[0] != "3":
    raise "please install opencv version 3.?"

from keras.models import load_model
convnet = load_model("binary_model_6")
#print(cv2.__version__)
import pyautogui # for keyboard stimulation

save_thresh = None
# parameters
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 40  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50

# variables
isBgCaptured = 0   # bool, whether the background captured
hand_controller = True  # if true, keyborad simulator works
#buttons_down = []
#prev_b = current_b = None

def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


def removeBG(bgModel,frame):
    fgmask = bgModel.apply(frame,learningRate=0)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res  # return eroded binary image




# Camera
camera = cv2.VideoCapture(0)
#camera.set(10,200)   #setting resulotion
cv2.namedWindow('least noiseless thr')
cv2.createTrackbar('trh', 'least noiseless thr', threshold, 100, printThreshold)

bgModel = None

while camera.isOpened():

    ret, frame = camera.read()
    threshold = cv2.getTrackbarPos('trh', 'least noiseless thr')
    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                 (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)  # BGR --> Blue rectangle
    cv2.imshow('original', frame)

    #  Main operation
    if isBgCaptured == 1:  # this part wont run until background captured
        #print("type :", type(bgModel))
        img = removeBG(bgModel,frame)
        img = img[0:int(cap_region_y_end * frame.shape[0]),
                    int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the blue rectangle
        #cv2.imshow('mask', img)

        # convert the image into binary image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gaussian_filtered = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        #cv2.imshow('blur', blur)
        ret, thresh = cv2.threshold(gaussian_filtered, threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('extracted', thresh)

        thresh_save = scipy.misc.imresize(thresh, (64, 64))
        thresh_pred = np.expand_dims(thresh_save, axis=0)
        thresh_pred = np.expand_dims(thresh_pred, axis=-1)

        # prediction = call the model
        prob = convnet.predict(thresh_pred)
        pred = np.argmax(prob)

        #print(pred)

        #prev_b = current_b
        #current_b = pred
        if hand_controller is True : #and prev_b == current_b
            #for button in buttons_down:
                #pyautogui.keyUp(button)
            #buttons_down = []
            if pred == 0:
                print("None")
            elif pred == 1:
                pyautogui.press('up')
                print("up")
                #pyautogui.press("z")
                #pyautogui.keyDown("right")
                #buttons_down = ["right"]
            elif pred == 2:
                print("victory")
                #pyautogui.keyDown('left')
                pyautogui.press('down')
                #buttons_down = ["left"]

            elif pred == 3:
                print("swing")
                pyautogui.press('left')
                #pyautogui.keyDown('left')
                #buttons_down=["left"]
            elif pred == 4:
                print("fist")
                pyautogui.press('right')
                #pyautogui.keyDown('right')
                #buttons_down=["right"]
            elif pred == 5:
                print("stop")


        if save_thresh is not None:
            scipy.misc.imsave("binary_images\\" + save_thresh + "\\" + str(time.time()) + ".jpg", thresh_save)

    # Keyboard OP
    k = cv2.waitKey(10) & 0xFF
    if k == 27:  # press ESC to exit
        break

    elif k == ord('b'):  # press 'b' to capture the background
        bgModel = cv2.createBackgroundSubtractorMOG2(history=0, varThreshold=bgSubThreshold)
        for i in range(16):
            fgmask = bgModel.apply(frame, learningRate=0.5)
        print("bgModel instantiated", type(bgModel))
        isBgCaptured = 1
        print ('!!!Background Captured!!!')

    elif k == ord('r'):  # press 'r' to reset the background
        isBgCaptured = 0
        print ('!!!Reset BackGround!!!')


    elif k == ord('c'):
        hand_controller = True
        print ('!!!Trigger On!!!')

    elif k == ord('0') or k == ord('1') or k == ord('2') or k == ord('3') or k == ord('4') or k == ord('5'):
        winsound.Beep(300, 600)
        print("start writing images to class:" , chr(k))

        save_thresh = chr(k)
camera.release()
cv2.destroyAllWindows()