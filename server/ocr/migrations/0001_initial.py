# Generated by Django 5.0.6 on 2024-05-16 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OCRDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('text', models.CharField()),
                ('file', models.FileField(upload_to='')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]