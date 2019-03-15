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
import DatabaseSession
import Constants
from DatabaseModels import Videos,Knows,Unknows
import Blocker

class RecognizeFaces(Bolt):
    # "filepath", "type", "size"

    def process(self, tup):
        mylogger = loger.getLoger("RecognizeFaces",Constants.boltpath + "logs")
        dataset = loger.getLoger("dataset",Constants.boltpath + "dataset", format='%(message)s')
        names=[]
        colors = []
        try:

            filepath = tup.values[0]
            output_image = tup.values[1]
            encoding_array = tup.values[2]
            encoding = np.array(encoding_array)
            boxes = tup.values[3]
            r = tup.values[4]
            mylogger.info("Loading tuple output_image: " + output_image +
                          " boxes:"  + str(boxes) + " r: " + str(r))
            mylogger.info("Load model file")
            models = Constants.know_people_pickle
            data = pickle.loads(open(models, "rb").read())
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding,
                                                     tolerance=Constants.TOLERANCE)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
                colors.append((0, 0, 255))
            else:
                colors.append((0, 255, 0))

            # update the list of names
            names.append(name)

            frame = cv2.imread(output_image)
            # loop over the recognized faces
            for ((top, right, bottom, left), name, color) in zip(boxes, names, colors):
                # rescale the face coordinates
                top = int(top )
                right = int(right )
                bottom = int(bottom )
                left = int(left )

                # draw the predicted face name on the image
                cv2.rectangle(frame, (left, top), (right, bottom),
                              color, 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, color , 2)
                x = uuid.uuid4()

                if not os.path.exists(Constants.boltpath + "faces/"+ str(name) + "/"):
                    os.makedirs(Constants.boltpath + "faces/"+ str(name) + "/")

                output_image_faces = Constants.boltpath + "faces/"+ str(name) + "/" + str(x) + "_faces.png"
                dataset.info('"' + filepath + '"' +
                             ', "' + output_image_faces + '"' +
                             ', "' + name + '"' +
                             ', ' + str(top) +
                             ', ' + str(right) +
                             ', ' + str(bottom) +
                             ', ' + str(left) +
                             ', "Encoding" ' +
                             ', ' + str(encoding_array).replace("[","").replace("]","")
                             )

            cv2.imwrite(output_image_faces,frame)
            video = DatabaseSession.session.query(Videos).filter(Videos.video_path == filepath).first()

            if name == "Unknown":
                alias = str(uuid.uuid4());
                mylogger.info("UNKNOWN FOUND!!!!!!!")
                mylogger.info(output_image_faces)
                unknow = Unknows(alias=alias,
                                 video=video,
                                 path=output_image_faces)
                DatabaseSession.session.add(unknow)
                DatabaseSession.session.commit()

                self.emit([output_image_faces, alias,filepath])
            else:
                know = Knows(name=name,
                             video=video,
                             path=output_image_faces)
                DatabaseSession.session.add(know)
                DatabaseSession.session.commit()
            Blocker.actualtime = Blocker.current_milli_time()

        except Exception as inst:
            mylogger.error("Python error.")
            mylogger.error(type(inst))
            mylogger.error(inst)

RecognizeFaces().run()
