import cv2
import numpy as np

#########################################################
# Ross Browning
# Instructions:
# Click and drag to create rectangle for the ROI
# press "C" to copy the ROI
#
# press "H" to apply histogram equalization
#   - equalizes the RGB channels separately
#   - converts to YCrCb
#   - equalizes the Y channel
#   - converts to RGB
#   - Final img displayed in the RGBtoYCrCb Window
#
# press "Y" to apply RGB histogram equalization
#   - converts to YCrCb
#   - equalizes the Y channel
#   - converts to RGB
#   - Final img displayed in the RGBtoYCrCb Window
#########################################################



x1, y1 = -1, -1
x2, y2 = -1, -1

# mouse callback function
# For more mouse event types, check https://docs.opencv.org/3.1.0/d7/dfc/group__highgui.html#ga927593befdddc7e7013602bca9b079b0
# For more drawing functions, check https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html

def region(event, x, y, flags, param):
    global x1, y1, x2, y2
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        cv2.rectangle(param, (x1, y1), (x2, y2), (0, 0, 255), 1)

#img = cv2.imread('TestImages/bord.jpg')
#img = cv2.imread('TestImages/NikonContest2016Winner.png')
#img = cv2.imread('TestImages/apple.png')
#img = cv2.imread('TestImages/Castle_badexposure.jpg')
#img = cv2.imread('TestImages/dog.jpg')
img = cv2.imread('TestImages/010img.png')
img = cv2.resize(img, (1000, 1000))


# It is a good idea to first clone this image,
# so that your drawing will not contaminate the original image
cloneImg = img.copy()
hsvclone = img.copy()
mask = img.copy()
text = img.copy()
mask[:, :, :] = (0, 0, 0)  # ~ Black

cv2.namedWindow('image')
cv2.setMouseCallback('image', region, cloneImg)
#good num = 50
threshold = 50

bTHRESHOLD = 18

def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])


def is_similar(pixel_a, pixel_b, threshold):
    return abs(luminance(pixel_a) - luminance(pixel_b)) > threshold

width = cloneImg.shape[1]
height = cloneImg.shape[0]


while (1):
    #cv2.imshow('s', img)
    cv2.imshow('image', cloneImg)

    cv2.imshow('mask', mask)
    cv2.imshow('hsvmethod', hsvclone)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
    elif k == ord('c'):
        yval = y1
        print(x1, x2, y1, y2)
        while yval < y2:
            xval = x1
            while xval < x2:
                i = 0
                #print("current: ", xval, yval, cloneImg[yval, xval], " left corner: ",cloneImg[y1, x1])
                #print("hsv here: ", hsv[yval,xval, 0], "corners: ", hsv[y1,x1, 0], hsv[y2,x1, 0], hsv[y1,x2, 0], hsv[y2,x2, 0])
                #hsvmethod
                #print("hsv val: ", hsv[yval,xval, 0])
                hsv1 = abs(int(hsv[yval, xval, 0]) - int(hsv[y1, x1, 0]))
                hsv2 = abs(int(hsv[yval, xval, 0]) - int(hsv[y2, x1, 0]))
                hsv3 = abs(int(hsv[yval, xval, 0]) - int(hsv[y1, x2, 0]))
                hsv4 = abs(int(hsv[yval, xval, 0]) - int(hsv[y2, x2, 0]))
                print("black values: ", cloneImg[yval, xval], cloneImg[y1, x1])
                #print("hsv values: ", hsv1,hsv2,hsv3,hsv4)
                if hsv1 > threshold and hsv1 > threshold and hsv1 > threshold and hsv4 > threshold:
                    #print("inside white hsv: ", hsvclone[yval, xval])
                    hsvclone[yval, xval] = (255, 255, 255)
                    mask[yval, xval] = (255, 255, 255)
                xval = xval + 1
            yval = yval + 1
    elif k == ord('p'):
        pixels = img.copy()
        pixels = cv2.bitwise_not(pixels)
        yval = y1
        while yval < y2:
            xval = x1
            while xval < x2:
                print("running")
                if is_similar(pixels[yval, xval], (0, 0, 0), bTHRESHOLD):
                    hsvclone[yval, xval] = (255, 255, 255)
                    mask[yval, xval] = (255, 255, 255)
                xval = xval + 1
            yval = yval + 1

cv2.imwrite('010.png', hsvclone)
cv2.imwrite('010mask.png', mask)
cv2.imwrite('010ori.png', cloneImg)
cv2.destroyAllWindows()