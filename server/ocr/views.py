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
    
    