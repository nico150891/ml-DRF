from django.urls import path
from .views import WeightPrediction, HeightPrediction

urlpatterns = [
    path('weight/', WeightPrediction.as_view(), name = 'weight_prediction'),
    path('height/', HeightPrediction.as_view(), name = 'weight_prediction'),
]