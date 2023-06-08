import cv2 
import numpy as np
import math
def MSE(bloc1,bloc2):
    n=bloc1.shape[0]
    m=bloc1.shape[1]
    diff=(bloc1-bloc2)**2
    s=np.sum(diff)
    err=s/(n*m)
    return err

img1 = cv2.imread('image072.png')
img1_grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread('image092.png')
img2_grey = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

height, width = img1_grey.shape 
box_size = 16
d=7
mses=[]
valable_mse=[]
bloc_rouge=[]
for i in range(0, height-box_size, box_size):
    for j in range(0, width-box_size, box_size):
        bloc_img1 = img1_grey[i:i + box_size, j:j + box_size]
        
        min_mse = math.inf
        
        for k in range(max(0, i - d), min(i + d, height - box_size)):
            for l in range(max(0, j - d), min(j + d, width - box_size)):
                bloc_img2 = img2_grey[k:k + box_size, l:l + box_size]
                err=MSE(bloc_img1,bloc_img2)
                if err < min_mse:
                    min_mse=err
                    pos=(l,k)
        
        if min_mse > 50 :
            valable_mse.append((min_mse,pos))
            bloc_rouge.append((j,i))


moved_objects_part1=np.zeros(img1.shape)

for i in range(len(valable_mse)):
    pos_img2=valable_mse[i][1]
    pos_img1=bloc_rouge[i]
    moved_objects_part1[pos_img2[1]:pos_img2[1]+box_size,pos_img2[0]:pos_img2[0]+box_size]= np.subtract(img2[pos_img2[1]:pos_img2[1]+box_size,pos_img2[0]:pos_img2[0]+box_size] ,img1[pos_img1[1]:pos_img1[1]+box_size,pos_img1[0]:pos_img1[0]+box_size])
    
cv2.imwrite('moved_objects.png', moved_objects_part1)
cv2.waitKey(0)
