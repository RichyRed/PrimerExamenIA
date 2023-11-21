from typing import List
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from ultralytics import YOLO

CAR_PATH = "ssd_mobilenet_v2.tflite"

class CarsPredictor:
    def __init__(self, model_path: str = CAR_PATH, object_detector: vision.ObjectDetector = None):
        print("Creando predictor...")
        self.model_path = model_path
        self.object_detector = object_detector

    def initialize_object_detector(self):
        if not self.object_detector:
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            options = vision.ObjectDetectorOptions(
                base_options=base_options,
                score_threshold=0.5
            )
            self.object_detector = vision.ObjectDetector.create_from_options(options)

    def predict_image(self, image_array: np.ndarray):
        self.initialize_object_detector()

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_array)


        object_detection_result = self.object_detector.detect(mp_image)

        return {
            "object_detection_result": object_detection_result
        }

    def predict_file(self, file_path: str):

        self.initialize_object_detector()

        image = mp.Image.create_from_file(file_path)
        object_detection_result = self.object_detector.detect(image)

        return object_detection_result

cars_predictor = CarsPredictor()
