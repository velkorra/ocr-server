from django.db import models

# Create your models here.
class OCRDocument(models.Model):
    name = models.CharField(max_length=50)
    text = models.CharField()
    file = models.FileField()
    image = models.ImageField()
    
    
