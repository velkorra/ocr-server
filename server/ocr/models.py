from django.db import models

# Create your models here.
class OCRDocument(models.Model):
    name = models.CharField(max_length=255)
    text = models.CharField()
    file = models.FileField(upload_to='documents/')
    image = models.ImageField(upload_to='images/')
    def __str__(self) -> str:
        return self.file.name
    
    
