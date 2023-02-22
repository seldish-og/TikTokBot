import requests
import cv2


class CaptchaSolver:

    def __init__(self, captcha_image_src, captcha_key_src):
        self.captcha = captcha_image_src
        self.captcha_key = captcha_key_src

    def download_captcha_images(self):
        # easy way to save images
        captcha = requests.get(self.captcha)
        captcha_key = requests.get(self.captcha_key)

        with open("test1.png", "wb") as captcha_image:
            captcha_image.write(captcha.content)

        with open("test2.png", "wb") as captcha_key_image:
            captcha_key_image.write(captcha_key.content)

    def find_coordinates(self):
        self.download_captcha_images()

        captcha = cv2.imread('test1.png', 0)
        key = cv2.imread('test2.png', 0)

        # other methods: 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF_NORMED'
        method = eval('cv2.TM_CCOEFF_NORMED')

        # apply template matching
        match = cv2.matchTemplate(captcha, key, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        # result is a x-coordinate + measurement uncertainty
        return int(max_loc[0]) + 26


''' Tested only with 'cv.TM_CCOEFF' method.
    But you can try other methods after #'''


'''If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum'''
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
