import face_recognition
import os, sys
import cv2
import numpy as np
import math
from src.database.models.schema import User, Image
from src.cloud_bucket.bucket_actions import BucketActions
from src.utils import delete_temp_files


class FaceConfidence:
    def __init__(self, face_distance, face_match_threshold=0.6):
        self.face_distance = face_distance
        self.face_match_threshold = face_match_threshold
        self.confidence_range = 1.0 - face_match_threshold

    def calculate_confidence_linear(self):
        linear_val = (1.0 - self.face_distance) / (self.confidence_range * 2.0)
        return linear_val

    def calculate_confidence_nonlinear(self, linear_val):
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

    def calculate_confidence(self):
        if self.face_distance > self.face_match_threshold:
            linear_val = self.calculate_confidence_linear()
            result = linear_val * 100
        else:
            linear_val = self.calculate_confidence_linear()
            value = self.calculate_confidence_nonlinear(linear_val)
            result = value * 100

        return f'{result:.2f}%'


class FaceRecognition:
    known_face_encodings = []
    known_face_names = []

    @staticmethod
    def format_result(face_locations, face_details):
        return [
            {
                "location": {
                    "top": face_loc[0],
                    "right": face_loc[1],
                    "bottom": face_loc[2],
                    "left": face_loc[3]
                },
                "details": face_name
            }
            for face_loc, face_name in zip(face_locations, face_details)
        ]

    def encode_faces(self, user: User, face_name: str):
        self.known_face_encodings = []
        self.known_face_names = []
        temp_image_filenames, temp_image_folder = BucketActions.get_images_from_folder(user_id=user.id,
                                                                                       face_name=face_name)
        for image_filename in temp_image_filenames:
            image_path = os.path.join(temp_image_folder, image_filename)

            face_image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(face_image)

            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(face_name)
                print(f"Face encoding added for {face_name} from {image_filename}")
            else:
                print(f"No face found in {image_filename}")

        delete_temp_files(temp_image_folder)

    def recognize(self, image_bytes: bytes):

        face_image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        face_locations = face_recognition.face_locations(face_image)
        face_encodings = face_recognition.face_encodings(face_image, face_locations)
        face_details = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            if not self.known_face_encodings:
                face_details.append({'name': 'unknown', 'confidence_level': ''})
            else:
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                if face_distances.size > 0:
                    best_match_index = np.argmin(face_distances)
                    name = self.known_face_names[best_match_index] if matches[best_match_index] else "Unknown"
                    confidence = FaceConfidence(face_distances[best_match_index]).calculate_confidence()
                    face_details.append({'name': name, 'confidence_level': confidence})
                else:
                    face_details.append({'name': 'unknown', 'confidence_level': ''})

        return self.format_result(face_locations, face_details)
