from PIL import Image
import pytesseract
from docx.api import Document
import io
from django.core.files.base import ContentFile
def recognize(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image, lang='rus')
    scan = Document()
    file_stream = io.BytesIO()
    p = scan.add_paragraph(text)
    scan.save(file_stream)
    file_stream.seek(0)
    file_name = image_file.name + '.docx'
    file = ContentFile(file_stream.getvalue(), name=file_name)
    return file, text, file_name