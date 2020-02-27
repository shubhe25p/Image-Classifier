import tensorflow as tf
import sys
import os
import cv2
import math
import serial
import time
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
ser = serial.Serial('COM8', baudrate = 9600)
import tensorflow as tf
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("retrained_labels.txt")]
with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())	
    _ = tf.import_graph_def(graph_def, name='')	
with tf.Session() as sess:
    video_capture = cv2.VideoCapture(0)
    i = 0
    while True:
        try:
            _,frame = video_capture.read()
            #frame=frame[50:460,50:620]
            label1=[]
            cv2.imshow("image", frame)
            ar = ser.readline().strip()
            while ser.in_waiting:
                ar = ser.readline().strip()
            a=int((ser.readline()).decode())
            send=-1
            if(a==1):
                i=i+1
                print(a)
                cv2.imwrite("screens/"+str(i)+"image.jpg", img=frame)
                image_data = tf.gfile.FastGFile("screens/"+str(i)+"image.jpg", 'rb').read()
                softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                predictions = sess.run(softmax_tensor, \
                                 {'DecodeJpeg/contents:0': image_data})		
                top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
                for node_id in top_k:
                    human_string = label_lines[node_id]
                    score = predictions[0][node_id]
                    print('%s (score = %.5f)' % (human_string, score))
                    label1.append(human_string)
                if(label1[0]=='plastics'):
                    send=3
                    ser.write(str(send).encode())
                elif(label1[0]=='metals'):
                    send=4
                    ser.write(str(send).encode())
                else:
                    send=5
                    ser.write(str(send).encode())
                print(send)   
                print ("\n\n")
        except:
            pass
        cv2.imshow("image", frame)
        if cv2.waitKey(1)==27:
            break
video_capture.release()
cv2.destroyAllWindows()
