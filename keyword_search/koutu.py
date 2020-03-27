import numpy as np
import cv2
from matplotlib import pyplot as plt
import os


#针对单一区域

def watershed(img):
    
    #img = cv2.imread('../picture/psp0.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)#膨胀
    # Finding sure foreground area
    
    dist_transform = cv2.distanceTransform(opening,2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.05*dist_transform.max(),255,0)#参数改小了，出现不确定区域
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)#减去前景
    
    return sure_fg

def fenge(img_path):
    #这里img1必须传入分水岭分割后的图
    path = './result'
    if not os.path.exists(path):
        os.mkdir(path)
    picture_name = img_path.split('/')[-1].split('.')[0]
    img = cv2.imread(img_path)
    img1 = watershed(img)
    height = img1.shape[0]
    width = img1.shape[1]
    thresh_value = 50
    h_number = int(height/thresh_value)
    #print(h_number)
    w_number = int(width/thresh_value)
    detect_point_array = np.zeros((h_number,w_number))
    r = 20 #检测半径
    for i in range(h_number):
        for j in range(w_number):
            #这是监测点的实际坐标
            point_pos_h = i*thresh_value
            point_pos_w = j*thresh_value
            detect_region = img1[point_pos_h:point_pos_h+r,
                                 point_pos_w:point_pos_w+r]
            white_pixel = np.where(detect_region==255)[0].shape[0]
            if white_pixel <30:
                detect_point_array[i][j] = 0
            else:
                detect_point_array[i][j] = 1
    y_list = []
    for i in range(len(detect_point_array)):
        if detect_point_array[i].max() == 0:
            y_list.append(i)

    region_max = np.where(img1==255)[0].max()
    region_min = np.where(img1==255)[0].min()

    #print(y_list)
    

    
    delete_list = []
    #print(delete_list)
    for i in range(len(y_list)):
        if y_list[i]*thresh_value  < region_min:
            delete_list.append(y_list[i])
        elif y_list[i]*thresh_value+r > region_max:
            delete_list.append(y_list[i])
        else:
            continue
    for i in delete_list:
        y_list.remove(i)

    #print(y_list)
    if not os.path.exists(path):
        os.mkdir(path)

    if y_list != []:
        first_bottom = y_list[0]*thresh_value
        second_top = y_list[-1]*thresh_value
        #print(second_top)
        #print(region_max)
        picture1 = img[region_min:first_bottom,:]
        picture2 = img[second_top:region_max,:]
        cv2.imwrite(path+'/%s_up.png'%(picture_name),picture1)
        cv2.imwrite(path + '/%s_down.png'%(picture_name),picture2)
        img[region_min:first_bottom,:] =255
        img[second_top:region_max,:] = 255

        return img
        

    else:
        xmin = np.min(np.where(img1==255)[1])
        xmax = np.max(np.where(img1==255)[1])
        ymin = np.min(np.where(img1==255)[0])
        ymax = np.max(np.where(img1==255)[0])

        bias = 10
        picture = img[ymin-bias:ymax+bias,xmin-bias:xmax+bias]
        cv2.imwrite(path+'/%s.png'%(picture_name),picture)

        img[ymin-bias:ymax+bias,xmin-bias:xmax+bias] = 255

        return img
    
    

def main():
    img_path = './test_duotu.jpg'
    img = fenge(img_path)
    #print(os.getcwd())


if __name__ == "__main__":
    main()