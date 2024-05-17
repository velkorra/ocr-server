from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import *
from . serializer import *
from django.contrib.auth.models import User
from django.db.models import Q
import os
from PIL import Image
import pytesseract

class DocumentView(APIView):
    def get(self, request):
        return Response({'aaa': True})
    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Начальный обработчик изображения без сохранения файла на диск
        image = Image.open(file_obj)
        text = pytesseract.image_to_string(image, lang='rus')

        # Создание и сохранение нового документа в базу данных
        document = OCRDocument.objects.create(
            name = file_obj.name,
            text = text,
            # Здесь мы сохраняем изображение напрямую без создания временного файла.
            # file_obj - это InMemoryUploadedFile, который можно непосредственно сохранить в ImageField
            image = file_obj
        )

        return Response({'message': text, 'document_id': document.pk}, status=status.HTTP_201_CREATED)
    
    