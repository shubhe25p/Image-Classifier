import tensorflow as tf
import sys
import os
import cv2
import math
import serial
import time
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
ser = serial.Serial('COM7', baudrate = 9600,)
import tensorflow as tf
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("retrained_labels.txt")]
with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())	
    _ = tf.import_graph_def(graph_def, name='')	
with tf.Session() as sess:
    video_capture = cv2.VideoCapture(1)
    i = 0
    while True:
        try:
            _,frame = video_capture.read()
    ##        frame = video_capture.read()[1]
    ##        frameId = video_capture.get(1)
            
            
            label1=[]
            cv2.imshow("image", frame)
            #ar = ser.readline().strip()
            while ser.in_waiting:
                ar = ser.readline().strip()
            
       ## q=int(ar)
        ##print(q)
        #print(ar)
            
            i = i + 1
            if cv2.waitKey(1) & 0xff==ord('q'):
                print('TRUE')
                string =[]
                
                
                cv2.imwrite(filename="screens/"+str(i)+"image.jpg", img=frame)
                image_data = tf.gfile.FastGFile("screens/"+str(i)+"image.jpg", 'rb').read()
                softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                predictions = sess.run(softmax_tensor, \
                                 {'DecodeJpeg/contents:0': image_data})		
                top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
                for node_id in top_k:
                    human_string = label_lines[node_id]
                    score = predictions[0][node_id]
                    print('%s (score = %.5f)' % (human_string, score))
                    score = str(score)
                    string.append(score)
                    label1.append(human_string)
    ##                    print(label1[0],"   ",string[0])
                print ("\n\n")       
                if(label1[0]=='plastic'):
                    send=1
                    ser.write(str(send).encode())
                elif(label1[0]=='metals'):
                    send=2
                    ser.write(str(send).encode())
                else:
                    send=3
                    ser.write(str(send).encode())
                   

        except:
            pass
        cv2.imshow("image", frame)
        cv2.waitKey(1)
video_capture.release()
cv2.destroyAllWindows()
