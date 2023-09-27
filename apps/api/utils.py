import io
import sys
from .apps import ApiConfig

import numpy as np
import cv2
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def from_image_to_cv2(image) -> np.array:
    # This is necessary in order for OpenCV to accept our image
    return np.array(Image.open(image).convert('RGB'))


def from_cv2_to_image(image: np.array) -> Image:
    # Intermediate step before returning for the next function
    return Image.fromarray(image)


def from_image_to_InMemoryUploadedFile(image: Image) -> InMemoryUploadedFile:
    """
        This function is a necessity because we are using FileResponse in our view, which works with
        InMemoryUploadedFile objects as long as we read them in binary form.
    """
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=75)
    return InMemoryUploadedFile(
        file=buffer,
        field_name='image',
        name='image.jpg',
        content_type='image/jpg',
        size=sys.getsizeof(buffer),
        charset=None
    )

def object_detection(image):
    
    # Coco names for taging the images processed by yolo
    LABELS = ApiConfig.yolo_names

    # Random colors for each coco class (For bounding boxes)
    colors = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

    # Process images to feed the NN
    image = from_image_to_cv2(image)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image_rgb.shape

    # Create a blob
    blob = cv2.dnn.blobFromImage(image_rgb, 1 / 255.0, (416, 416),
                              swapRB=True, crop=False)
    
    # Load NN
    net = ApiConfig.net
    
    # NN processing the image (blob)
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    net.setInput(blob)
    outputs = net.forward(ln)
    
    # Filter detections based on the threshold (confidence)
    boxes = []
    confidences = []
    classIDs = []
    for output in outputs:
     for detection in output:
          scores = detection[5:]
          classID = np.argmax(scores)
          confidence = scores[classID]
          if confidence > 0.8:
               # Build the bounding boxes
               box = detection[:4] * np.array([width, height, width, height])
               (x_center, y_center, w, h) = box.astype("int")
               x = int(x_center - (w / 2))
               y = int(y_center - (h / 2))
               boxes.append([x, y, w, h])
               confidences.append(float(confidence))
               classIDs.append(classID)
    # Select the best detections (Avoid boxes overlaping)
    idx = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.8,nms_threshold=0.5)

    # Image postprocessing with boinding boxes
    for i in idx:
        x, y, w, h = boxes[i]
        color = colors[classIDs[i]].tolist()
        text = "{}: {:.3f}".format(LABELS[classIDs[i]], confidences[i])
        cv2.rectangle(image_rgb, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image_rgb, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Image postprocessing to answer the API request in memory
    image = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)
    image = from_cv2_to_image(image)
    image = from_image_to_InMemoryUploadedFile(image)

    return image