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
import Constants
videoWidth= 640
numberOfFrames = 60

class ExtractImages(Bolt):
    # "filepath", "type", "size"

    def process(self, tup):
        mylogger = loger.getLoger("ExtractImages",Constants.boltpath + "logs")
        try:

            filepath = tup.values[0]
            input_image = tup.values[1]
            type = tup.values[2]

            mylogger.info("Loading image from video " + str(filepath) +
                          " input_image: " + str(input_image) +
                          " Type: " + str(type))
            frame = cv2.imread(input_image)
            mylogger.info("Image loaded")


            # convert the input frame from BGR to RGB then resize it to have
            # a width of 500px (to speedup processing)
            mylogger.info("Converting color")
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mylogger.info("Resizing")
            rgb = imutils.resize(rgb, width=videoWidth)
            r = frame.shape[1] / float(rgb.shape[1])

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb,
                                                    model=Constants.model_type)
            mylogger.info("Locating faces")
            encodings = face_recognition.face_encodings(rgb, boxes)
            mylogger.info("Encoding faces")
            encoding_number = 0
            x = uuid.uuid4()
            for encoding in encodings:
                video_file_name = os.path.basename(filepath)
                encoding_number = encoding_number + 1
                mylogger.info("saving faces files")
                if not os.path.exists(Constants.boltpath + "results/"):
                  os.makedirs(Constants.boltpath + "results/")

                output_image = Constants.boltpath + "results/" \
                               + video_file_name \
                               + "_frame_" \
                               + str(x) \
                               + "_encoding_" \
                               + str(encoding_number) \
                               + "_result.png"
                mylogger.info("Saving file "+ output_image)
                cv2.imwrite(output_image,rgb)
                # mylogger.info(encoding)
                self.emit([filepath, output_image, encoding.tolist(), boxes, r])

        except Exception as inst:
            mylogger.error("Python error.")
            mylogger.error(type(inst))
            mylogger.error.error(inst)

ExtractImages().run()
