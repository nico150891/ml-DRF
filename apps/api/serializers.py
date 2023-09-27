import magic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class YoloSerializer(serializers.Serializer):
    image = serializers.ImageField(allow_empty_file=False, allow_null=False)

    def validate(self, attrs):
        # Validate image
        VALID_MIME_TYPES = ["image/jpeg", "image/png"]
        MAX_RESOLUTION = (1080, 1920)

        detected_mime = magic.from_buffer(attrs['image'].open('rb').read(2048), mime=True)

        if detected_mime not in VALID_MIME_TYPES:
            raise ValidationError({'image': 'Invalid image format.'})

        if attrs['image'].image.size > MAX_RESOLUTION:
            raise ValidationError({'image': f'Max resolution allowed is {MAX_RESOLUTION}'})

        return super(YoloSerializer, self).validate(attrs)