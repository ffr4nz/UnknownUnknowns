model_path= '/opt/face-recognition/'

SQLLite_file = model_path + "knows_unknows.db"
SQLLite_Base_URL = 'sqlite:///' + SQLLite_file

model_type = "hog"
videoWidth= 640
numberOfFrames = 30
TOLERANCE = 0.45
TOLERANCE_WHISPER = 0.4
know_people_pickle = model_path + "models/encodings.pickle"
predictor_path = model_path + 'models/shape_predictor_5_face_landmarks.dat'
face_rec_model_path = model_path + 'models/dlib_face_recognition_resnet_model_v1.dat'

boltpath = model_path + "videos/"
faces_folder_path = boltpath + 'faces/Unknown/'
output_folder_path = boltpath + 'faces/Unknown_Whispered/'
