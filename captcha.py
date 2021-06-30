import urllib
from urllib.request import urlopen
import requests
import cv2
import numpy as np
from PIL import Image as im

class CaptchaSolver:

    def __init__(self, captcha, captcha_key):
        self.captcha = captcha
        self.captcha_key = captcha_key

    def url_to_image(self):
        # get images
        # captcha = urllib.request.urlopen(self.captcha)
        # captcha_key = urllib.request.urlopen(self.captcha_key)
        #
        # # convert it to a NumPy array
        # img1 = np.array(bytearray(captcha.read()), dtype="uint8")
        # img2 = np.array(bytearray(captcha_key.read()), dtype="uint8")
        #
        # # then read it into OpenCV format
        # img1 = cv2.imdecode(img1, 1)
        # img2 = cv2.imdecode(img2, 1)
        #
        # # using PIL save images as .png
        # image1 = im.fromarray(img1)
        # image2 = im.fromarray(img2)
        # image1.save('test1.png')
        # image2.save('test2.png')
        
        # easier way to save iamges
        captcha = requests.get(self.captcha)
        captcha_key = requests.get(self.captcha_key)

        with open("test1.png", "wb") as captcha_image:
            captcha_image.write(captcha.content)

        with open("test2.png", "wb") as captcha_key_image:
            captcha_key_image.write(captcha_key.content)

    def find_coordinates(self):
        # run func and gen 2 images
        self.url_to_image()

        captcha = cv2.imread('test1.png', 0)
        key = cv2.imread('test2.png', 0)

        # choose method
        method = eval('cv2.TM_CCOEFF')  # 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF_NORMED'

        # apply template matching
        match = cv2.matchTemplate(captcha, key, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        # result is a x-coordinate + measurement uncertainty
        return int(max_loc[0]) + 24


''' Tested only with 'cv.TM_CCOEFF' method.
    But you can try other methods'''

# # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
# w, h = key_img.shape[::-1]
# if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
#     top_left = min_loc
# else:
#     top_left = max_loc
'''code below make a graphic interface of matching'''
# bottom_right = (top_left[0] + w, top_left[1] + h)
#     cv.rectangle(img,top_left, bottom_right, 255, 2)
#     plt.subplot(121),plt.imshow(res,cmap = 'gray')
#     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#     plt.subplot(122),plt.imshow(img,cmap = 'gray')
#     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#     plt.suptitle(meth)
#     plt.show()
