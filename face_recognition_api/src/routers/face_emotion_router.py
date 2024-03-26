from fastapi import FastAPI, UploadFile, File
from keras.models import load_model
import cv2
import numpy as np

model = load_model('best_emotion_model.h5')

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

face_emotion_router = APIRouter(prefix='/face_emotion_recognition', tags=['face_emotion_recognition'])

def preprocess_image(image):
    resized_image = cv2.resize(image, (48, 48))
    normalized_image = resized_image / 255.0
    input_image = np.expand_dims(normalized_image, axis=0)
    return input_image


@face_emotion_router.post("/predict-emotion/")
async def predict_emotion(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    input_image = preprocess_image(image)

    predictions = model.predict(input_image)

    predicted_emotion_index = np.argmax(predictions[0])

    predicted_emotion = emotion_labels[predicted_emotion_index]

    return {"predicted_emotion": predicted_emotion}
