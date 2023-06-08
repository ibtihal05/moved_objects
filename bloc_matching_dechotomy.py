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


moves_img2=[]
moves_img1=[]
def dicho(img1,bloc,centre):
    step=32  
    init_pos=centre
    while(step>=1) :
        r=[0,-step,step]
        mses=[]
        poses={}
        pos=centre

        for i in r :
            for j in r :
                pos=(centre[0]+i,centre[1]+j)
                if(pos[0]>=8 and pos[0]<=1072 and pos[1]>=8 and pos[1]<=1912):
                    voi=img1[pos[0]-8:pos[0]+8, pos[1]-8:pos[1]+8]
                    mse=MSE(bloc,voi)
                    mses.append(mse)
                    poses[mse]=pos
        centre=poses[min(mses,default=0)]
        step=int(step/2)
    
    if min(mses,default=0)>50 :
        moves_img2.append(init_pos)
        moves_img1.append(poses[min(mses,default=0)])


img1 = cv2.imread('image072.png')
img1_grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread('image092.png')
img2_grey = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

height, width = img2_grey.shape 
box_size = 16
for i in range(0, height-box_size, box_size):
    for j in range(0, width-box_size, box_size):
        bloc = img2_grey[i:i + box_size, j:j + box_size]
        dicho(img1_grey,bloc,(i+8,j+8))
        
moved_objects=np.zeros(img1_grey.shape)
for pos, sim_pos in zip(moves_img2, moves_img1):
    moved_objects[pos[0]-8:pos[0]+8,pos[1]-8:pos[1]+8]=img1_grey[sim_pos[0]-8:sim_pos[0]+8,sim_pos[1]-8:sim_pos[1]+8]-img2_grey[pos[0]-8:pos[0]+8,pos[1]-8:pos[1]+8]
cv2.imwrite('moved_objects.png', moved_objects)

