import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

import mysql.connector
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import Trainer

class WindowManager(ScreenManager):
    pass


class CreateAccountWindow(Screen):
    id = ObjectProperty(None)
    namee = ObjectProperty(None)
    age = ObjectProperty(None)
    gen = ObjectProperty(None)
    cr = ObjectProperty(None)
    pid = ""
    page = ""
    pnamee = ""
    pgen = ""
    pcr = ""

    def back(self):
        sm.current = "main"

    def submit(self):
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", charset='utf8',
                                       database="python_test")

        facecascade = cv2.CascadeClassifier(
            r"C:\Users\LAPCARE\Anaconda3\envs\ImageStamp\Library\etc\haarcascades\haarcascade_frontalface_default.xml")

        sampleNum = 0
        # namee=self.root.get_screen('create').ids.namee.text
        person = self.ids
        self.pid = person['id'].text
        self.page = person['age'].text
        self.pnamee = person['namee'].text
        self.pgen = person['gen'].text
        self.pcr = person['cr'].text
        # print(pid)
        if self.pid != "" and self.pnamee != "" and self.page != "" and self.pgen != "" and self.pcr != "":
            # print(self.pid, self.pnamee, self.page, self.pgen, self.pcr)
            self.insertOrUpdate(self.pid, self.pnamee, self.page, self.pgen, self.pcr, mydb)

            while True:
                # Capture frame-by-frame
                ret, frame = video_capture.read()
                # frame = np.array(frame, dtype=np.uint8)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = facecascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

                # Draw a rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    sampleNum = sampleNum + 1
                    # img_name = "dataSet/User." + str(Id) + "." + str(sampleNum) + ".jpg".format(img_counter)
                    # cv2.imwrite(img_name, save_img)
                    cv2.imwrite("dataSet/User." + str(self.pid) + "." + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.waitKey(100)

                # Display the resulting frame
                cv2.imshow('Video', frame)
                cv2.waitKey(1)
                if (sampleNum > 20):
                    video_capture.release()
                    cv2.destroyAllWindows()
                    break
            # When everything is done, release the capture

            pop = Popup(title='Submit Success',
                        content=Label(text='Your Data Saved Succesfully'),
                        size_hint=(None, None), size=(400, 200))

            pop.open()
            sm.current = "main"
        else:
            self.invalidForm()

    def invalidForm(self):
        pop = Popup(title='Invalid Form',
                    content=Label(text='Please fill in all inputs with valid information.'),
                    size_hint=(None, None), size=(400, 200))

        pop.open()

    def reset(self):
        self.age.text = ""
        self.gen.text = ""
        self.cr.text = ""
        self.Id.text = ""
        self.namee.text = ""

    def insertOrUpdate(self, Id, Name, Age, Gen, CR, mydb):
        cmd = "select * from people where Id=" + str(Id)
        cursor = mydb.cursor()
        cursor.execute(cmd)
        isRecordExist = 0
        myResponse = cursor.fetchall()

        for row in myResponse:
            isRecordExist = 1
            # print(("exist"))
        print("Record", isRecordExist)

        if isRecordExist == 1:
            cmd1 = "update people set Name= %s where Id= %s"
            val1 = (str(Name), str(Id))
            cmd2 = "update people set Age= %s where Id= %s"
            val2 = (str(Age), str(Id))
            cmd3 = "update people set Gender= %s where Id= %s"
            val3 = (str(Gen), str(Id))
            cmd4 = "update people set CR= %s where Id= %s"
            val4 = (str(CR), str(Id))
        else:
            cmd1 = "insert into people(Id,Name,Age,Gender,CR) values(%s,%s,%s,%s,%s)"
            val1 = (str(Id), str(Name), str(Age), str(Gen), str(CR))
            cmd2 = ""
            val2 = ""
            cmd3 = ""
            val3 = ""
            cmd4 = ""
            val4 = ""
        cursor.execute(cmd1, val1)
        if val2 != "":
            cursor.execute(cmd2, val2)
        if val3 != "":
            cursor.execute(cmd3, val3)
        if val4 != "":
            cursor.execute(cmd4, val4)
        mydb.commit()
        mydb.close()


class MainScreen(Screen):
    def addFace(self):
        sm.current = "create"
        pass

    def detectFace(self):
        exec()
        pass

    def processFace(self):
        Trainer.exe()
        pass


def getProfile(id, mydb):
    # conn=mysql.connect("FaceBase.db")
    cmd = "select * from people where Id=" + str(id)
    cursor = mydb.cursor()
    cursor.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    # mydb.close()
    return profile


def exec():
    facecascade =cv2.CascadeClassifier(
            r"C:\Users\LAPCARE\Anaconda3\envs\ImageStamp\Library\etc\haarcascades\haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)
    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read("recognizer/trainningData.yml")
    # font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX,0.4,1,0,1)
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 1
    fontcolor = (255, 255, 255)
    # cv2.putText(im, str(Id), (x,y+h), fontface, fontscale, fontcolor)
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="", charset='utf8',
                                   database="python_test")
    while (True):
        ret, img = video_capture.read()

        #        img = np.array(img, dtype=np.uint8)
        #       print(img)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = facecascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, conf = rec.predict(gray[y:y + h, x:x + w])
            profile = getProfile(id, mydb)
            if (profile != None):
                cv2.putText(img, "Name : " + str(profile[1]), (x, y + h + 20), fontface, fontscale, fontcolor)
                cv2.putText(img, "Age : " + str(profile[2]), (x, y + h + 45), fontface, fontscale, fontcolor)
                cv2.putText(img, "Gender : " + str(profile[3]), (x, y + h + 70), fontface, fontscale, fontcolor)
                cv2.putText(img, "Criminal Records : " + str(profile[4]), (x, y + h + 95), fontface, fontscale,
                            fontcolor)
                # cv2.cv.PutText(cv2.cv.fromarray(img), "Name : " + str(profile[1]), (x, y + h + 20), font, (0, 255, 0));
                # cv2.cv.PutText(cv2.cv.fromarray(img), "Age : " + str(profile[2]), (x, y + h + 45), font, (0, 255, 0));
                # cv2.cv.PutText(cv2.cv.fromarray(img), "Gender : " + str(profile[3]), (x, y + h + 70), font, (0, 255, 0));
                # cv2.cv.PutText(cv2.cv.fromarray(img), "Criminal Records : " + str(profile[4]), (x, y + h + 95), font,
                #                (0, 0, 255));
        cv2.imshow("Face", img)
        if cv2.waitKey(1) == ord('q'):
            mydb.close()
            video_capture.release()
            cv2.destroyAllWindows()
            break


# exec()

kv = Builder.load_file("main.kv")
video_capture = cv2.VideoCapture(0)
sm = WindowManager()

screens = [MainScreen(name="main"), CreateAccountWindow(name="create")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"


class MyApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyApp().run()
