import cv2
from skimage import data, draw
from skimage import transform, util
import numpy as np
from skimage import filters, color
from PIL import ImageFont, ImageDraw, Image


# hl_color = np.array([0, 1, 0])
# imgnm = input('Enter the image name! >> ')
# img = cv2.imread('./img/'+imgnm)
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

        if h > w:
            rew = w
            reh = int(w*1.414)
            if reh > h:
                rew = h//1.414
                reh = h
        else:
            reh = h
            rew = h//1.414
            if rew > w:
                reh = int(w*1.414)
                rew = w
        print('height, width = ', h, w, '=>', reh, rew)
        # out = seam_carving.resize(
        #     img, (rew, reh),
        #     energy_mode='backward',   # Choose from {backward, forward}
        #     order='width-first',  # Choose from {width-first, height-first}
        #     keep_mask=None
        # )
        out = self.kuwahara(img)
        out = self.puttext(out, texts, point, font_path, font_size, color)
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


    def puttext(self, cv_image, texts, point=(30, 30), font_path='/IPAexfont00401/ipaexm.ttf', font_size=100, color=(255,0,0)):
        h, w, _ = img.shape
        font_path = './font'+font_path
        font = ImageFont.truetype(font_path, font_size)

        cv_rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_rgb_image)

        draw = ImageDraw.Draw(pil_image)
        dx = 0
        dy = (h//3)//len(texts)
        for i, text in enumerate(texts):
            repoint = (point[0]+dx, point[1]+i*dy)
            draw.text(repoint, text, fill=color, font=font)

        cv_rgb_result_image = np.asarray(pil_image)
        cv_bgr_result_image = cv2.cvtColor(cv_rgb_result_image, cv2.COLOR_RGB2BGR)

        return cv_bgr_result_image


    def kuwahara(self, img, r=30, resize=False, rate=0.5): #元画像、正方形領域の一辺、リサイズするか、リサイズする場合の比率
        h, w, _ = img.shape
        if resize:img=cv2.resize(img,(int(w*rate),int(h*rate)));h,w,_=img.shape
        img=np.pad(img,((r,r),(r,r),(0,0)),"edge")
        ave,var=cv2.integral2(img)
        ave=(ave[:-r-1,:-r-1]+ave[r+1:,r+1:]-ave[r+1:,:-r-1]-ave[:-r-1,r+1:])/(r+1)**2 #平均値の一括計算
        var=((var[:-r-1,:-r-1]+var[r+1:,r+1:]-var[r+1:,:-r-1]-var[:-r-1,r+1:])/(r+1)**2-ave**2).sum(axis=2) #分散の一括計算

        def filt(i,j):
            return np.array([ave[i,j],ave[i+r,j],ave[i,j+r],ave[i+r,j+r]])[(np.array([var[i,j],var[i+r,j],var[i,j+r],var[i+r,j+r]]).argmin(axis=0).flatten(),j.flatten(),i.flatten())].reshape(w,h,_).transpose(1,0,2)
        filtered_pic = filt(*np.meshgrid(np.arange(h),np.arange(w))).astype(img.dtype) #色の決定
        return filtered_pic



if __name__ == '__main__':
    imgnm = input('Enter the relative path of the image under ./img! (ex. nittc.jpg)>> ')
    texts = input('Enter a catchphrase! >> ').split()
    font_size = int(input('Enter a font size as integer type! (rec = 100) >> '))
    font_path = input('Enter the relative path of the font under ./font (ex. /IPAexfont00401/ipaexm.ttf)>> ')
    point = tuple(map(int, input('Enter the coordinates for your catchphrase! (rec = (30, 30)) >> ').split()))
    color = tuple(map(int, input('Enter a color for the text! (r, g, b) >> ').split()))
    img = cv2.imread('./img/'+imgnm)
    out = SeamCarving()
    out.processing()


# out = transform.seam_carve(img, eimg, 'vertical', 200)
