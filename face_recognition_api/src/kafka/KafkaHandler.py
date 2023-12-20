import json
import threading
import cv2
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import time
import os
import asyncio
import base64


class KafkaHandler():
    def __init__(self, sending_topic, receiving_topic):
        self.receiving_topic = receiving_topic
        self.sending_topic = sending_topic
        self.recognized = asyncio.Event()
        self.producer = AIOKafkaProducer(
            bootstrap_servers='localhost:9092',
            key_serializer=lambda v: v.encode('utf-8')
        )
        self.consumer = AIOKafkaConsumer(
            self.receiving_topic,
            bootstrap_servers='localhost:9092',
            enable_auto_commit=False,
            loop=asyncio.get_event_loop()
        )

    async def send_images_to_kafka(self, images, user_id):
        try:
            await self.producer.start()

            image_list = []
            for image in images:
                image_bytes = image.file.read()

                # Encode image as base64
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                image_list.append(base64_image)

            user_data = {
                "user_id": user_id,
                "images": image_list
            }

            serialized_data = json.dumps(user_data)

            await self.producer.send_and_wait(
                self.sending_topic,
                key=str(user_id),
                value=serialized_data.encode('utf-8')
            )

            return True
        except Exception as e:
            print(f'Error sending images to Kafka: {str(e)}')
            return False
        finally:
            await self.producer.stop()

    async def listen_for_response(self):

        try:

            async for message in self.consumer:
                print(f"Key: {message.key}")
                print(f"Value: {message.value}")
                print(f"Timestamp: {message.timestamp}")

                if message.value == b'1':
                    self.recognized.set()
                print("Face recognized")

        except KeyboardInterrupt:
            print("Consumer stopped manually")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await self.consumer.stop()

    async def start_listener_thread(self):
        listener_task = asyncio.create_task(self.listen_for_response())
        await listener_task

    async def wait_for_recognition(self):
        try:
            await self.start_listener_thread()

            await asyncio.wait_for(self.recognized.wait(), timeout=10)

            return self.recognized.is_set()

        except asyncio.TimeoutError:
            print("Recognition timeout")
            return False
        except Exception as e:
            print(f'Error waiting for recognition: {str(e)}')
            return False
