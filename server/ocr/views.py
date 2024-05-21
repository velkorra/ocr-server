from django.shortcuts import render
import docx.api
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
import docx
from docx.api import Document 
from django.http import HttpResponse
from django.core.files.base import ContentFile
import io
from unidecode import unidecode
from .recognition.recognition import recognize

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
morgan = """
Моргана родилась как настоящая, признанная дочь короля Утера. Хотя она была старшей сестрой и имела такой же статус, в глазах Морганы Артурия получила любовь и надежды их отца, заставив её в конечном счете стать королевой-ведьмой, жаждущей мести всю оставшуюся часть её дней. Во время обучения Артурии Моргана устроила ловушку, и из-за распутства Мерлина, Артурия попалась в неё и потеряла Калибурн. Как только Камелот был построен, она отправилась в уединение. Она посла туда Агравейна в качестве убийцы. Она была феей озера и полной злой противоположностью Вивиан, Владычицы Озера."""
@csrf_exempt  # Отключаем CSRF для демонстрации, в продакшене используйте токены CSRF
def upload_image(request):
    if request.method == "POST":
        image_file = request.FILES.get('image')
        if image_file:
            with open('media/images/' + image_file.name, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            return JsonResponse({'status': 'success', 'image_id': morgan}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'No image provided'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

class DownloadWordDocumentView(APIView):
    def get(self, request, *args, **kwargs):
        filename = 'media/' + str(OCRDocument.objects.latest('id').file)
        with open(filename, 'rb') as doc:
            response = HttpResponse(doc.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{unidecode(filename.split('/')[-1])}"'
            return response

class DocumentView(APIView):
    def get(self, request):
        return Response({'aaa': True})
    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        
        file, text, file_name = recognize(file_obj)
        
        document = OCRDocument.objects.create(
            name = file_obj.name,
            text = text,
            file=file,
            image = file_obj
        )
        return Response({'message': text, 'document_name': file_name}, status=status.HTTP_201_CREATED)
    
    