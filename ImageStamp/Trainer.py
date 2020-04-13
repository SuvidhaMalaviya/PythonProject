import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path="dataSet"


def getImgWithId(path):
    imagepaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    Ids=[]

    for imagepath in imagepaths:
        faceImg=Image.open(imagepath).convert('L')
        face=np.array(faceImg,'uint8')
        Id=int(os.path.split(imagepath)[-1].split('.')[1])
        faces.append(face)
        Ids.append(Id)
        cv2.imshow("training",face)
        cv2.waitKey(10)
    return np.array(Ids),faces


def exe():
    Ids,faces=getImgWithId(path)
    recognizer.train(faces,Ids)
    recognizer.save('recognizer/trainningData.yml')
    cv2.destroyAllWindows()