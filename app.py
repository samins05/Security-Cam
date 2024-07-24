import tkinter as tk
from tkinter import messagebox
from train import *
from detect import *
from db import *
from pathlib import Path


def clear():
    if len(os.listdir("data"))==0:
        messagebox.showerror('Clear Error', 'Error: The dataset is already empty. You cannot clear it.')
    else:
        #delete each path in the data directory/folder
        for path in Path('data').glob("*"):
            path.unlink()
        #clear the 'people' table in local sql database
        mycursor.execute("TRUNCATE TABLE people")
        mydb.commit()

#adds images of given person to the data folder, where images of given person will be trained to the face classifier
def add_person():
    # if invalid name then give user an error
    if name_entry.get()=="":
        messagebox.showerror('Name Error', 'Error: Please type a valid name with at least 1 character')
    else: 
        #set face classifier to haarcascade file 
        face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")# set cascade classifier
        def cropped_face(image):
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # convert image to grayscale
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)#set scaling factor to 1.3 and min neighbours to 5, with gray scaled image
            
            if faces is ():
                return None
            for (x,y,w,h) in faces:
                gray_face = image[y:y+h,x:x+w] # get cropped image from each dimension in the face
            return gray_face
    
        #id is default by one, and it won't change if there is nothing in the data folder
        user_id =1
        # get latest image path and set a new id if there already exists a dataset in the data folder
        if len(os.listdir("data"))!=0:
            image_path = get_latest_image("data") 
            user_id = (int)(os.path.split(image_path)[1].split(".")[1])+1 #create a different user id from the latest picture

        
        img_id = 0
        cap = cv2.VideoCapture(1) # capture external camera
        #create picture of each frame in video capture where a face is detected and add it to data folder
        while True:
            ret, frame = cap.read()
            if cropped_face(frame) is not None: #if we detect a face, then take a picture of the face
                display_text = "Image #:" +str(img_id)
                face = cv2.resize(cropped_face(frame), (300,300)) 
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) #turn face to gray_scale
                file_name_path = "data/user."+str(user_id)+"."+str(img_id)+".jpg" 
                cv2.imwrite(file_name_path, face) # create a jpg image file and add it to data folder 
                cv2.putText(face, display_text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2) #display count of image 
                cv2.putText(face, "press 'q' to close", (50,200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 1, cv2.LINE_AA)
                cv2.imshow("Cropped face", face)
                img_id+=1
            if (cv2.waitKey(25) & 0xFF) == ord('q') or int(img_id)==301: #Press enter to break, loop automatically stops after x images
                break
        add(user_id,name_entry.get())
        cap.release()
        cv2.destroyAllWindows()
        train_class("data") # train the classifier after putting images in the data folder

#make data directory if it doesnt already exist
if not os.path.isdir("./data"):
    os.mkdir("./data")

interface = tk.Tk()
#field for entering person's name to be added to database
name_label = tk.Label(interface,text="Name", font=("Bell Gothic Std Black",20))
name_label.grid(column=0,row=0)
name_entry = tk.Entry(interface, width=30,bd=5)
name_entry.grid(column=1,row=0)

#button for adding person to database
add_btn= tk.Button(interface, text='Add Person to Database', command=add_person) # intend to run the video capture
add_btn.grid(column=1,row=1)

camera_btn= tk.Button(interface, text='Open Security Camera', command=run_camera) # intend to run the video capture
camera_btn.grid(column=1,row=2)

clear_btn= tk.Button(interface, text='CLEAR DATABASE', command=clear) # intend to run the video capture
clear_btn.grid(column=1,row=3)

interface.mainloop()

