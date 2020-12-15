import cv2
from skimage import data, draw
from skimage import transform, util
import numpy as np
from skimage import filters, color


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
        out = self.draw_texts(out, texts)
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


    def draw_texts(self, img, texts, x=10, y=0, r=0, g=0, b=0, font_scale=0.7, thickness=2):
        h, w, _ = img.shape
        offset_x = x  # 左下の座標
        initial_y = y
        dy = int(img.shape[1] / 15)
        color = (g, b, r)  # black

        texts = [texts] if type(texts) == str else texts

        for i, text in enumerate(texts):
            offset_y = initial_y + (i+1)*dy
            cv2.putText(img, text, (offset_x, offset_y), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, color, thickness, cv2.LINE_AA)
        return img


    def kuwahara(self, img, r=30, resize=False, rate=0.5): #元画像、正方形領域の一辺、リサイズするか、リサイズする場合の比率
        h, w, _ = img.shape
        if resize:img=cv2.resize(img,(int(w*rate),int(h*rate)));h,w,_=img.shape
        img=np.pad(img,((r,r),(r,r),(0,0)),"edge")
        ave,var=cv2.integral2(img)
        ave=(ave[:-r-1,:-r-1]+ave[r+1:,r+1:]-ave[r+1:,:-r-1]-ave[:-r-1,r+1:])/(r+1)**2 #平均値の一括計算
        var=((var[:-r-1,:-r-1]+var[r+1:,r+1:]-var[r+1:,:-r-1]-var[:-r-1,r+1:])/(r+1)**2-ave**2).sum(axis=2) #分散の一括計算

    #--以下修正部分--
        def filt(i,j):
            return np.array([ave[i,j],ave[i+r,j],ave[i,j+r],ave[i+r,j+r]])[(np.array([var[i,j],var[i+r,j],var[i,j+r],var[i+r,j+r]]).argmin(axis=0).flatten(),j.flatten(),i.flatten())].reshape(w,h,_).transpose(1,0,2)
        filtered_pic = filt(*np.meshgrid(np.arange(h),np.arange(w))).astype(img.dtype) #色の決定
        return filtered_pic



if __name__ == '__main__':
    imgnm = input('Enter the image name! >> ')
    texts = input('Enter a catchphrase! >> ').split()
    print(type(texts), texts)
    img = cv2.imread('./img/'+imgnm)
    out = SeamCarving()
    out.processing()


# out = transform.seam_carve(img, eimg, 'vertical', 200)
