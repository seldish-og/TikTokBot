import cv2 as cv


class CaptchaSolver:

    def __init__(self, captcha, captcha_key):
        self.captcha = captcha
        self.captcha_key = captcha_key

    def find_coordinates(self):
        captcha_img = cv.imread(self.captcha, 0)
        key_img = cv.imread(self.captcha_key, 0)
        w, h = key_img.shape[::-1]
        # choose method
        method = eval('cv.TM_CCOEFF')  # 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF_NORMED'

        # apply template matching
        match = cv.matchTemplate(captcha_img, key_img, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(match)
        # result is a x-coordinate + measurement uncertainty
        return int(max_loc[0]) + 4


captcha = CaptchaSolver('captcha.jpg', 'captcha_puzzle.png')
print(captcha.find_coordinates())

''' Tested only with 'cv.TM_CCOEFF' method.
    But you can try other methods'''

# # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
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
