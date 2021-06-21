import cv2 as cv
from matplotlib import pyplot as plt


class CaptchaSolver:

    def __init__(self, captcha, captcha_key):
        self.captcha = captcha
        self.captcha_key = captcha_key

    def find_coordinates(self):
        img = cv.imread(self.captcha, 0)
        img2 = img.copy()
        template = cv.imread(self.captcha_key, 0)
        w, h = template.shape[::-1]
        # choose method
        method = 'cv.TM_CCOEFF'  # 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED'

        method = eval(method)

        # apply template matching
        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img, top_left, bottom_right, 255, 2)
        plt.subplot(121), plt.imshow(res, cmap='gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img, cmap='gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(method)
        plt.show()


captcha = CaptchaSolver('captcha.jpg', 'captcha_puzzle.png')
captcha.find_coordinates()
