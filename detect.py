import cv2
import numpy as np
from PIL import Image
import os
from db import *

def draw_facebox(img, classifier, scaleFactor, minNeighbors, color, clf):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    for (x,y,w,h) in features:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2 ) #draw a rectangle around the face 
         
        # returns id, and pred 
        #id represents the label that program predicts the face to most likely be
        # pred is used to get our confidence level
        id, pred = clf.predict(gray_img[y:y+h,x:x+w]) 
        confidence_lvl = int(100*(1-pred/300))
        
        #look for entrys in the database that have the matching id to what the classifier is predicting
        #there will always be an id that is predicted
        mycursor.execute("select name from people WHERE id="+str(id))
        myresult = mycursor.fetchone()
        name = myresult[0]

        if confidence_lvl>55:
            cv2.putText(img, name, (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        else:
            cv2.putText(img, "UNKNOWN", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)
     
    return img
 
def run_camera():
    # loading classifier
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")
    video_capture = cv2.VideoCapture(1)
    #draw boxes around any face detected in the camera frame     
    while True:
        ret, img = video_capture.read()
        if len(os.listdir("data"))!=0:
            img = draw_facebox(img, faceCascade, 1.3, 6, (0,255,0), clf)
        else:
            cv2.putText(img, "BEWARE: YOU HAVEN'T ADDED ANYONE YET", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(img, "press 'q' to close camera", (200,450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 1, cv2.LINE_AA)
        cv2.imshow("SecurityCam", img)
        if (cv2.waitKey(25) & 0xFF) == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

