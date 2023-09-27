from django.urls import path
from .views import WeightPrediction, HeightPrediction, YoloInference

urlpatterns = [
    path('weight/', WeightPrediction.as_view(), name = 'weight_prediction'),
    path('height/', HeightPrediction.as_view(), name = 'height_prediction'),
    path('yolo/', YoloInference.as_view(), name = 'yolo_inference'),
]