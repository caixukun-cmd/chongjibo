import json
import os
import dlib

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('C:/Users/86130/Desktop/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('C:/Users/86130/Desktop/dlib_face_recognition_resnet_model_v1.dat')

def load_registered_faces():
    registered_faces_file = 'registered_faces.json'
    if os.path.exists(registered_faces_file):
        with open(registered_faces_file, 'r') as file:
            return json.load(file)
    return {}

registered_faces = load_registered_faces()
