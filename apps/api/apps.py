import os
import joblib
from django.apps import AppConfig
from django.conf import settings
import cv2


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api'
    MODEL_FILE = os.path.join(settings.MODELS, "WeightPredictionLinRegModel.joblib")
    model = joblib.load(MODEL_FILE)
    
    yolo_config = os.path.join(settings.MODELS, "yolov3/yolov3.cfg")
    yolo_weights = os.path.join(settings.MODELS, "yolov3/yolov3.weights")
    yolo_names_path = os.path.join(settings.MODELS, "yolov3/coco.names")
    yolo_names = open(yolo_names_path).read().split("\n")
    net = cv2.dnn.readNetFromDarknet(yolo_config, yolo_weights)
