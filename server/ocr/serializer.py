from rest_framework import serializers
from . models import *


        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRDocument
        fields = '__all__'