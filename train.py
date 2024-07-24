## pip install opencv-python
import os
import numpy as np
from PIL import Image
import cv2



# get latest image stored in the directory 
#source: https://stackoverflow.com/questions/30882796/how-to-read-the-latest-image-in-a-folder-using-python
def get_latest_image(dirpath, valid_extensions=('jpg')):
    """
    Get the latest image file in the given directory
    """

    # get filepaths of all files and dirs in the given dir
    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
    # filter out directories, no-extension, and wrong extension files
    valid_files = [f for f in valid_files if '.' in f and \
        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

    if not valid_files:
        raise ValueError("No valid images in %s" % dirpath)

    return max(valid_files, key=os.path.getmtime) 

#train the classifier 
def train_class(dir):
    path = [os.path.join(dir,i) for i in os.listdir(dir)] # get path for each image in given directory
    faces = []
    ids = []
    for image in path:
        gray_img = Image.open(image).convert('L') # convert img to grayscale 
        imageNp = np.array(gray_img,'uint8')
        id = (int)(os.path.split(image)[1].split(".")[1]) # get image id ex. /user.1.2 ->split to get 'user.1.1', then split by '.' to get 'user,'1','1', and then get '1'
        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids) # convert ids to correct format 

    #Train classifier and save
    clf = cv2.face.LBPHFaceRecognizer_create() # use LBPHF Face Recognizer to train the classifier
    clf.train(faces,ids)
    clf.write("classifier.xml")#update classifier file