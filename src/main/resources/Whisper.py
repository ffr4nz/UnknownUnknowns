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
import numpy as np
import sys
import os
import dlib
import glob
import Constants
import DatabaseSession
import Blocker
from DatabaseModels import Videos, Wishper

class Whisper(Bolt):
    # "filepath", "type", "size"

    def process(self, tup):
        mylogger = loger.getLoger("Whisper",Constants.boltpath + "logs")
        try:
            timenow = Blocker.current_milli_time()
            # We only use the last value of tuple, the other two are fixed in
            # WhisperCache.java. Change this to make other things
            original_image = tup.values[0]
            alias = tup.values[1]
            filepath = tup.values[2]
            # Generic models
            video = DatabaseSession.session.query(Videos).filter(Videos.video_path == filepath).first()

            # Some paths

            detector = dlib.get_frontal_face_detector()
            sp = dlib.shape_predictor(Constants.predictor_path) # 128D face descriptor predictor
            facerec = dlib.face_recognition_model_v1(Constants.face_rec_model_path)
            descriptors = []
            images = []

            # Now find all the faces and compute 128D face descriptors for each face.
            for f in glob.glob(os.path.join(Constants.faces_folder_path, "*.png")):
                mylogger.info("Processing file: {}".format(f))
                img = dlib.load_rgb_image(f)

                # Ask the detector to find the bounding boxes of each face. The 1 in the
                # second argument indicates that we should upsample the image 1 time. This
                # will make everything bigger and allow us to detect more faces.
                dets = detector(img, 1)
                mylogger.info("Number of faces detected: {}".format(len(dets)))

                # Now process each face we found.
                for k, d in enumerate(dets):
                    # Get the landmarks/parts for the face in box d.
                    shape = sp(img, d)

                    # Compute the 128D vector that describes the face in img identified by
                    # shape.
                    face_descriptor = facerec.compute_face_descriptor(img, shape)
                    descriptors.append(face_descriptor)
                    images.append((img, shape))

            # Now let's cluster the faces.
            labels = dlib.chinese_whispers_clustering(descriptors, Constants.TOLERANCE_WHISPER)
            num_classes = len(set(labels))
            mylogger.info("Number of clusters: {}".format(num_classes))
            if num_classes > 0 :
                counts = 0
                DatabaseSession.session.query(Wishper).filter(
                    Wishper.video==video
                ).delete()
                DatabaseSession.session.commit()
                for i, label in enumerate(labels):
                    # Ensure output directory exists
                    output_folder_path_real= Constants.output_folder_path + str(label)
                    if not os.path.isdir(output_folder_path_real):
                        os.makedirs(output_folder_path_real)

                    # Save the extracted faces
                    mylogger.info("Saving faces cluster to output folder...")
                    img, shape = images[i]
                    file_path = os.path.join(output_folder_path_real, "face_" + str(counts))
                    # The size and padding arguments are optional size=300x300 and padding=0.25
                    dlib.save_face_chip(img, shape, file_path, size=300, padding=0.25)
                    counts = counts +1
                    whisper = Wishper(alias=file_path,
                                      original_image=file_path,
                                      video=video,
                                      group=str(label),
                                      path=file_path + ".jpg")

                    DatabaseSession.session.add(whisper)
                    DatabaseSession.session.commit()

        except Exception as inst:
            mylogger.error("Python error.")
            mylogger.error(type(inst))
            mylogger.error(inst)

Whisper().run()

