from PIL import ImageGrab, Image
import cv2 as cv
import imutils
import pytesseract
import numpy as np

import binput
import bmath
import bfile
import time

def crop_image(image, top_left, size):
    image = image[top_left[1]: top_left[1] + size[1], top_left[0]: top_left[0] + size[0]]

    return image
def show_image(image):
    cv.imshow('Result', image)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    cv.waitKey()

def search_object(dir='', name='', method=cv.TM_SQDIFF_NORMED, hl=0, threshold=0, top_left=None, size=None):
    image = binput.take_screenshot()
    image = crop_image(image, top_left, size)
    img = cv.imread(dir, cv.TM_CCOEFF)
    # image = np.float32(image)
    # samples = np.float32(samples)
    val = None
    loc = (0, 0)

    # Match for each sample.
    result = cv.matchTemplate(image, img, method)
    t_min_val, t_max_val, t_min_loc, t_max_loc = cv.minMaxLoc(result)
    print(str(t_min_val)+' '+ str(t_max_val)+ ' '+str(t_min_loc)+ str(t_max_loc))

    # Find best value.
    if hl == 0:
        if val == None or t_min_val < val:
            val = t_min_val
            loc = t_min_loc

            print(loc)

            needle_h = img.shape[0]
            needle_w = img.shape[1]
    else:
        if val == None or t_max_val > val:
            val = t_max_val
            loc = t_max_loc
            
            needle_h = img.shape[0]
            needle_w = img.shape[1]

    needle = (needle_w, needle_h)

    # show_best_match(image, loc, needle)
    # print('Total best match top left position:', loc)
    # print('Total best match confidence:', val)

    loc = bmath.find_centre(loc, needle)

    # Threshold.
    if not threshold == None:
        if hl == 0:
            if val > threshold:
                return None
        else:
            if val <= threshold:
                return None

    return loc
while True:
    print(search_object(dir='Capture.png',top_left=(1130, 50),size=(150, 150)))
    time.sleep(0.1)