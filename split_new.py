import cv2
import numpy as np
cap= cv2.VideoCapture(0)
#cap.set(5,60)
while(1):
    ret, image = cap.read(0)
    height , width = image.shape[:2]
    n= int(width)
    x=0
    d = 0
    while(x<=0.75):
        start_row , start_col = int(0), int(n*(x))
        end_row , end_col = int(height) , int(n*(x+0.25))
        cropped_top = image[start_row:end_row , start_col :end_col]
        filename = "screens\cropped_top_%d.jpg"%d
        cv2.imwrite(filename,cropped_top)
        d+=1
        x=x+0.25
        cv2.imshow('image',image)
cap.release(0)
cv2.waitKey(0)
cv2.destroyAllWindows()
