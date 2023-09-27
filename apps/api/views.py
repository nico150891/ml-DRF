from django.http import HttpResponse, FileResponse
import numpy as np
import pandas as pd
from .apps import ApiConfig
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import object_detection
from .serializers import YoloSerializer


class WeightPrediction(APIView):
    def post(self, request):
        data = request.data
        height = data['Height']
        gender = data['Gender']
        if gender == 'Male':
            gender = 0
        elif gender == 'Female':
            gender = 1
        else:
            return Response("Gender field is invalid", status=400)
        lin_reg_model = ApiConfig.model
        weight_predicted = lin_reg_model.predict([[gender, height]])[0][0]
        weight_predicted = np.round(weight_predicted, 1)
        response_dict = {"Predicted Weight (kg)": weight_predicted}
        return Response(response_dict, status=200)

class HeightPrediction(APIView):
    def post(self, request):
        data = request.data
        height = data['Height']
        gender = data['Gender']
        if gender == 'Male':
            gender = 0
        elif gender == 'Female':
            gender = 1
        else:
            return Response("Gender field is invalid", status=400)
        lin_reg_model = ApiConfig.model
        weight_predicted = lin_reg_model.predict([[gender, height]])[0][0]
        weight_predicted = np.round(weight_predicted, 1)
        response_dict = {"Predicted Height (kg)": weight_predicted}
        return Response(response_dict, status=200)

class YoloInference(APIView):
    
      def post(self, request):

        serializer = YoloSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = object_detection(serializer.validated_data['image'])

        return FileResponse(
            # Return InMemoryUploadedFile in binary
            image.open('rb')
        )