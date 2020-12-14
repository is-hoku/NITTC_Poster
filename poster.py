# import cv2
# import numpy as np
#
#
# def make_pyramid(gray):
#     pyramid = [gray]
#     H, W = gray.shape
#
#     for i in range(1, 6):
#         a = 2. ** i
#
#         p = cv2.resize(gray, (int(W/a), int(H/a)), interpolation=cv2.INTER_LINEAR)
#         p = cv2.resize(p, (W, H), interpolation=cv2.INTER_LINEAR)
#
#         pyramid.append(p.astype(np.float32))
#
#     return pyramid
#
#
# def saliency_map(pyramid):
#     H, W = pyramid[0].shape
#     out = np.zeros((H, W), dtype=np.float32)
#
#     out += np.abs(pyramid[0] - pyramid[1])
#     out += np.abs(pyramid[0] - pyramid[3])
#     out += np.abs(pyramid[0] - pyramid[5])
#     out += np.abs(pyramid[1] - pyramid[4])
#     out += np.abs(pyramid[2] - pyramid[3])
#     out += np.abs(pyramid[3] - pyramid[5])
#
#     out = out / out.max() * 255
#
#     return out
#
#
# def seam_carving(img, gray, reh, rew):
#     H, W = gray.shape
#     reh = H-reh
#     x, y = 0, 0
#     # seam = gray
#     row = 255 * H + 1
#     line = 255 * W + 1
#     for h in range(reh):
#         for i in range(W):
#             cnt = 0
#             for y in range(H):
#                 min_idx = np.argmin([gray[y, max(x-1, 0)], gray[y, x], gray[y, min(x+1, W)]])
#                 min_idx -= 1
#                 x = min_idx
#                 cnt += gray[y, x]
#             if cnt < row:
#                 row = cnt
#                 row_y = y
#         img = np.delete(img, row_y, 1)
#         gray = np.delete(gray, row_y, 1)
#         print('1 row deleted')
#
#     H, W = gray.shape
#     print('H, W', H, W)
#     rew = W-rew
#     x, y = 0, 0
#     for w in range(rew):
#         for i in range(H):
#             cnt = 0
#             for x in range(W):
#                 min_idx = np.argmin([gray[max(y-1, 0), x], gray[y, x], gray[min(y+1, H), x]])
#                 min_idx -= 1
#                 y = min_idx
#                 cnt += gray[y, x]
#             if cnt < line:
#                 line = cnt
#                 line_x = x
#         img = np.delete(img, line_x, 1)
#         gray = np.delete(gray, line_x, 1)
#         print('1 line deleted')
#
#     seam, seam_gray = img, gray
#     return seam, seam_gray
#
# imgnm = input('Enter the image name!')
# reh, rew = map(int,input('Enter the modified image size!(height, width)').split())
#
# # Create SaliencyMap
# img = cv2.imread('./img/'+imgnm)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# pyramid = make_pyramid(gray)
# out = saliency_map(pyramid)
# out = out.astype(np.uint8)
# cv2.imwrite("./img/map.png", out)
#
# # Seam Carving
# gray = cv2.imread("./img/map.png", 0)
# # img = cv2.imread("./img/glider.jpeg")
# # gray = cv2.imread("./SaliencyMap/seam_gray.png", 0)
# # img = cv2.imread("./SaliencyMap/seam.png")
#
# seam, seam_gray = seam_carving(img, gray, reh, rew)
#
# cv2.imwrite("./img/seam.png", seam)
# cv2.imwrite("./img/seam_gray.png", seam_gray)


import cv2
from skimage import data, draw
from skimage import transform, util
import numpy as np
from skimage import filters, color
from matplotlib import pyplot as plt


# hl_color = np.array([0, 1, 0])
imgnm = input('Enter the image name! >> ')
img = cv2.imread('./img/'+imgnm)
# img = util.img_as_float(img)
# print(img)
# eimg = filters.sobel(color.rgb2gray(img))
# print(eimg)

# resized = transform.resize(img, (img.shape[0], img.shape[1] - 200),
#                            mode='reflect')



import seam_carving, sys, time, threading

class SeamCarving:
    def __init__(self):
        self.work_ended = False


    def spinner(self):
        while not self.work_ended:
            print('|' + '\033[1D', end='', file=sys.stderr)
            # time.sleep(0.01)
            print('/' + '\033[1D', end='', file=sys.stderr)
            # time.sleep(0.01)
            print('-' + '\033[1D', end='', file=sys.stderr)
            # time.sleep(0.01)
            print('\\' + '\033[1D', end='', file=sys.stderr)
            # time.sleep(0.01)
        print(' ' + '\033[1D')


    def work(self):
        h, w, _ = img.shape
        out = seam_carving.resize(
            img, (w - 2, h),
            energy_mode='backward',   # Choose from {backward, forward}
            order='width-first',  # Choose from {width-first, height-first}
            keep_mask=None
        )
        self.work_ended = True
        cv2.imwrite("./img/seam.png", out)


    def processing(self):
        thread1 = threading.Thread(target=self.spinner)
        thread2 = threading.Thread(target=self.work)
        thread1.start()
        thread2.start()
        thread2.join()
        thread1.join()
        print("done!" + '\033[1D')


if __name__ == '__main__':
    seam = SeamCarving()
    seam.processing()



# out = transform.seam_carve(img, eimg, 'vertical', 200)
