import concurrent.futures
import threading
import tkinter as tk
import cv2
from kafka import KafkaProducer, KafkaConsumer
import time
import numpy as np
import os
import requests
import json

def get_jwt_token():
    user_name = 'x'
    password = 'x'

    url = 'http://127.0.0.1:8001/login/login'

    data = {"username": user_name, "password": password}

    json_data = json.dumps(data)

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 404:
        print("Endpoint not found.")
    else:
        print(response.json())

    return response.json()['access_token']

def send_image_to_kafka_and_save(image):
    try:
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: v.tobytes(),  # Serialize image as bytes
            key_serializer= lambda v: v.encode('utf-8')  # Serialize string as bytes
        )

        topic_name = 'test'

        image_bytes = cv2.imencode('.jpg', image)[1]
        producer.send(topic_name, value=image_bytes, key=get_jwt_token())
        producer.flush()
        producer.close()

        desktop_path = os.path.expanduser("~/Desktop")
        image_filename = f"captured_image_{int(time.time())}.jpg"
        image_path = os.path.join(desktop_path, image_filename)
        cv2.imwrite(image_path, image)

        return True
    except Exception as e:
        print(f'Error sending image to Kafka and saving: {str(e)}')
        return False

def capture_and_send_six_images(image_count=0):
    if image_count < 6:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            response_label.config(text="Error: Camera not found.")
            return

        ret, frame = cap.read()

        if ret:
            for _ in range(3):
                if send_image_to_kafka_and_save(frame):
                    response_label.config(text=f"Image {image_count + 1} sent to Kafka.")
                    break
                else:
                    time.sleep(1)
            else:
                response_label.config(text=f"Failed to send image {image_count + 1} to Kafka after multiple retries.")
        else:
            response_label.config(text="Error capturing image.")

        cap.release()

        window.after(125, capture_and_send_six_images, image_count + 1)
    else:
        response_label.config(text="All 6 images sent to Kafka.")


def listen_for_response():
    # Listening is done in a separate thread. Otherwise, the GUI will freeze.
    try:
        consumer = KafkaConsumer(
            'face_auth_response',
            bootstrap_servers='localhost:9092',
            enable_auto_commit=False,
        )

        for message in consumer:
            print(f"Key: {message.key}")
            print(f"Value: {message.value}")
            print(f"Timestamp: {message.timestamp}")

            response_label.config(text="Face recognized")
            print("Face recognized")

    except KeyboardInterrupt:
        print("Consumer stopped manually")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        consumer.close()


def start_listener_thread():
    listener_thread = threading.Thread(target=listen_for_response)
    listener_thread.daemon = True
    listener_thread.start()

window = tk.Tk()
window.title("Image Sender App")
window.geometry("500x500")

send_button = tk.Button(window, text="Start Sending 6 Images", command=capture_and_send_six_images)
send_button.pack(pady=20)

response_label = tk.Label(window, text="")
response_label.pack()


start_listener_thread()

window.mainloop()

