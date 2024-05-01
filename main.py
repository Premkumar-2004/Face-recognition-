import os
import cv2
import pickle
import numpy as np
import cvzone
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime


cred = credentials.Certificate("C:\\Users\\91765\\PycharmProjects\\toyota contest\\serviceaccountkey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendencerealtime-6838c-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendencerealtime-6838c.appspot.com"
})

bucket=storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgbackground = cv2.imread("C:\\Users\\91765\\PycharmProjects\\toyota contest\\venv\\resources\\background.jpg")
foldermodepath = "C:\\Users\\91765\\PycharmProjects\\toyota contest\\venv\\resources\\modes"
modepathlist = os.listdir(foldermodepath)
imgmodelist = []
for path in modepathlist:
    imgmodelist.append(cv2.imread(os.path.join(foldermodepath, path)))

x, y, width, height = 25, 125, 505, 376
x1, y1, w1, h1 = 607, 43, 311, 479

print('LOADING ENCODE FILE')
file = open("C:\\Users\\91765\\PycharmProjects\\toyota contest\\venv\\encodefile.p", "rb")
encodelistwithknownwithids = pickle.load(file)
file.close()
encodelistknown, studentids = encodelistwithknownwithids
print("ENCODE FILE LOADED")
modetype = 0
counter = 0
id = -1
imgstudent=[]

while True:
    success, img = cap.read()

    # Check if the frame is empty
    if not success or img is None:
        continue

    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
    facecurframe = face_recognition.face_locations(imgs)
    encodecurframe = face_recognition.face_encodings(imgs, facecurframe)

    img_resized = cv2.resize(img, (width, height))
    imgbackground[y:y + height, x:x + width] = img_resized

    mode_resized = cv2.resize(imgmodelist[modetype], (w1, h1))
    imgbackground[y1:y1 + h1, x1:x1 + w1] = mode_resized



    for encodeface, faceloc in zip(encodecurframe, facecurframe):
        matches = face_recognition.compare_faces(encodelistknown, encodeface)
        facedis = face_recognition.face_distance(encodelistknown, encodeface)

        matchindex = np.argmin(facedis)

        if matches[matchindex]:
            y2, x3, y3, x2 = faceloc
            y2, x3, y3, x2 = y2 * 4, x3 * 4, y3 * 4, x2 * 4
            bbox = x2, y2, x3 - x2, y3 - y2
            imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0)
            id = studentids[matchindex]
            print("FACE DETECTED")
            print(studentids[matchindex])

            if counter == 0:
                cvzone.putTextRect(imgbackground,"Loading",(260,290))
                cv2.imshow("Face attendence",imgbackground)
                cv2.waitKey(1)
                counter = 1
                modetype = 1

    if counter != 0:

        if counter == 1:

            studentinfo = db.reference(f'students/{id}').get()
            print(studentinfo)
            blob=bucket.get_blob(f"C:\\Users\\91765\\PycharmProjects\\toyota contest\\venv\\images/{id}.png")
            array=np.frombuffer(blob.download_as_string(),np.uint8)
            imgstudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
            #update attendence

            # for attendence
            datetimeobject = datetime.strptime(studentinfo['last_attendence_time'], "%Y-%m-%d %H:%M:%S")
            secondelapsed = (datetime.now() - datetimeobject).total_seconds()

            if secondelapsed>20:

                ref=db.reference(f'students/{id}')
                studentinfo['total_attendence']+=1
                ref.child('total_attendence').set(studentinfo['total_attendence'])
                ref.child('last_attendence_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if 10<counter<20:
            modetype=2

        mode_resized = cv2.resize(imgmodelist[modetype], (w1, h1))
        imgbackground[y1:y1 + h1, x1:x1 + w1] = mode_resized



        if counter<10:

            cv2.putText(imgbackground, str(studentinfo['total_attendence']), (655, 115),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

            cv2.putText(imgbackground, str(id), (765, 385),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(imgbackground, str(studentinfo['major']), (750, 430),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(imgbackground, str(studentinfo['standing']), (650, 730),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 100, 0), 1)
            cv2.putText(imgbackground, str(studentinfo['year']), (850, 730),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            (w,h),_=cv2.getTextSize(studentinfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
            offset=(252-w)//2
            cv2.putText(imgbackground, str(studentinfo['name']), (670+offset, 350),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

        counter += 1
        if counter>20:
            counter=0
            modetype=0
            studentinfo=[]
            imgstudent=[]

            mode_resized = cv2.resize(imgmodelist[modetype], (w1, h1))
            imgbackground[y1:y1 + h1, x1:x1 + w1] = mode_resized


    cv2.imshow("Web Cam", imgs)
    cv2.imshow("Face Recognition", imgbackground)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
