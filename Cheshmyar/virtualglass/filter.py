import os

import numpy as np
import cv2
import matplotlib.pyplot as plt

from Cheshmyar.settings import STATICFILES_DIRS


class ColorFilter:
    def __init__(self, barcode, im_dir):
        self.barcode = barcode
        self.im_dire = im_dir

    def fetch_images(self):
        path = os.path.join(STATICFILES_DIRS[0], "Services\\glassesfilters\\" + self.barcode + ".jpg")
        cv_img = plt.imread(path)
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        cv_img = cv_img.copy()
        cv_img = cv_img.astype("uint8")

        path = os.path.join(STATICFILES_DIRS[0], self.im_dire)
        # print(path)
        customer_img = plt.imread(path)
        customer_img = customer_img.copy()
        customer_img = customer_img.astype("int")
        contrast = 40
        img_con = customer_img * (contrast / 127 + 1) - contrast
        img_con = np.clip(img_con, 0, 255)
        img_con = img_con.astype("uint8")
        # img_con_shp1 = img_con.shape[0]
        # img_con_shp2 = img_con.shape[1]
        #
        # if cv_img.shape != img_con.shape:
        #     cv_img = cv2.resize(cv_img, (img_con_shp1, img_con_shp2))
        # else:
        #     pass

        img_blend = cv_img * 0.4 + img_con * 0.6
        img_blend = np.clip(img_blend, 0, 255)
        img_blend = img_blend.astype("uint8")
        self.img_blendd = img_blend

