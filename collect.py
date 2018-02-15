"""
captures and save data to : sys.argv[1]/sys.argv[2]

"""

import cv2
import numpy as np
import math
import os
import time
import scipy.misc
import sys
cv2.ocl.setUseOpenCL(False)
if str(cv2.__version__)[0] != "3":
    raise "please install opencv version 3.?"

try:
    import winsound
except ImportError:
    def playsound(frequency,duration):
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, frequency))
import sys
A = False
if len(sys.argv)>1:
    #print(sys.argv[1])
    k_arg = os.path.join(sys.argv[1],sys.argv[1])
    A = True

save_thresh = None
# parameters
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 35  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
isBgCaptured = 0   # bool, whether the background captured

# Camera
camera = cv2.VideoCapture(0)

bgModel = None

def removeBG(bgModel,frame):
    fgmask = bgModel.apply(frame,learningRate=0)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res  # return eroded binary image

if A == False:
    while camera.isOpened():
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)  # flip the frame horizontally
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                      (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)  # BGR --> Blue rectangle
        cv2.imshow('original', frame)


        #  Main operation
        if isBgCaptured == 1:  # this part wont run until background captured
            img = removeBG(bgModel, frame)
            img = removeBG(bgModel, frame)
            img = img[0:int(cap_region_y_end * frame.shape[0]),
                  int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the blue rectangle

            # convert the image into binary image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gaussian_filtered = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
            ret, thresh = cv2.threshold(gaussian_filtered, threshold, 255, cv2.THRESH_BINARY)
            cv2.imshow('extracted', thresh)
            thresh_save = scipy.misc.imresize(thresh, (64, 64))
            scipy.misc.imsave("binary_images/" + save_thresh + "/" + str(time.time()) + ".jpg", thresh_save)
            print("frame captured")

        # Keyboard OP
        k = cv2.waitKey(10) & 0xFF
        if k == 27:  # Esc key to stop
            break

        if k == ord('0') or k == ord('1') or k == ord('2') or k == ord('3') or k == ord('4') or k == ord('5'):
            save_thresh = chr(k)
            print("save :", save_thresh)
            playsound(440, 0.5)
            print("start writing images to class:", chr(k))
            if not os.path.exists("binary_images/" + chr(k)):
                os.makedirs("binary_images/" + chr(k))
            bgModel = cv2.createBackgroundSubtractorMOG2(history=0, varThreshold=bgSubThreshold)
            isBgCaptured = 1

else:
    save_thresh = k_arg
    print("save :", save_thresh)
    #playsound(440, 1)
    print("start writing images to class:", k_arg)
    if not os.path.exists(k_arg):
        os.makedirs(k_arg)
    bgModel = cv2.createBackgroundSubtractorMOG2(history=0, varThreshold=bgSubThreshold)
    isBgCaptured = 1

    s = -100

    while camera.isOpened():
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)  # flip the frame horizontally
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                      (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0),
                      2)  # BGR --> Blue rectangle
        cv2.imshow('original', frame)

        if s == 0:
            playsound(440, 1)
            s = s+1
        elif s<0:
            s = s+1
        #  Main operation
        if isBgCaptured == 1 and s == 1:  # this part wont run until background captured
            img = removeBG(bgModel, frame)
            img = removeBG(bgModel, frame)
            img = img[0:int(cap_region_y_end * frame.shape[0]),
                  int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the blue rectangle

            # convert the image into binary image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gaussian_filtered = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
            ret, thresh = cv2.threshold(gaussian_filtered, threshold, 255, cv2.THRESH_BINARY)
            cv2.imshow('extracted', thresh)
            thresh_save = scipy.misc.imresize(thresh, (64, 64))
            scipy.misc.imsave(save_thresh + "/" + str(time.time()) + ".jpg", thresh_save)
            print("frame captured")

        # Keyboard OP
        k = cv2.waitKey(10) & 0xFF
        if k == 27:  # Esc key to stop
            break




camera.release()
cv2.destroyAllWindows()
