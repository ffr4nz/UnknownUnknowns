# import storm
# from storm import reportError
from pystorm.bolt import Bolt

import face_recognition
import imutils
import pickle
import time
import cv2
import os
import loger
import uuid
import DatabaseSession
import Constants
from DatabaseModels import Videos
# this import create default database
import CreateDatabaseSQLite


class IdentifyFaces(Bolt):
    # "filepath", "output_image", "type"

    def process(self, tup):
        mylogger = loger.getLoger("IdentifyFaces",Constants.boltpath + "logs")
        try:

            filepath = tup.values[0]
            type = tup.values[1]
            size = tup.values[2]

            mylogger.info("Loading video " + str(filepath) +
                   " Size: " + str(size) +
                   " Type: " + str(type))
            stream = cv2.VideoCapture(filepath)

            mylogger.info("Video loaded")
            (haveMoreFrames, frame) = stream.read()
            if haveMoreFrames:
                new_Videos = Videos(video_path=str(filepath))
                DatabaseSession.session.add(new_Videos)
                DatabaseSession.session.commit()
                # session.query(Videos).all()
            frame_number = 0
            while True:
                # grab the next frame

                frame_number = frame_number +1
                # end of the stream
                # only 1 of Constants.numberOfFrames
                if frame_number % Constants.numberOfFrames != 0:
                    continue
                if not haveMoreFrames:
                    break
                x = uuid.uuid4()
                if not os.path.exists(Constants.boltpath + "frames/"):
                  os.mkdir(Constants.boltpath + "frames/")
                  print("Directory " , Constants.boltpath + "frames/" +
                    " Created ")
                output_image = Constants.boltpath + "frames/" + str(x) + ".png"
                cv2.imwrite(output_image,frame)
                self.emit([filepath, output_image, "PNG"])
                (haveMoreFrames, frame) = stream.read()
            stream.release()
        except Exception as inst:
            mylogger.error("Python error.")
            mylogger.error(type(inst))
            mylogger.error.error(inst)

CreateDatabaseSQLite.createDatabase()
IdentifyFaces().run()
