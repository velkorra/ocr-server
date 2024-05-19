from PIL import Image
import pytesseract
from docx.api import Document
import io
from django.core.files.base import ContentFile
import cv2
import numpy as np
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    denoised = cv2.medianBlur(binary, 5)
    
    return denoised

def enhance_contrast(image_path):

    img = cv2.imread(image_path, 0) 


    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(img)
    
    return cl1


def edge_detection(image):
    edges = cv2.Canny(image, 100, 200)
    return edges


def morphological_transformation(image):
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    
    return closing

image_path ='tests/image.png'


def preprocess(someFilename, psmValue=3, processABit=True):
    if processABit:
        img = np.array(Image.open(someFilename))
        norm_img = np.zeros((img.shape[0], img.shape[1]))
        img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
        img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
        img = cv2.GaussianBlur(img, (1, 1), 0)
        Image.fromarray(img).save('qq.png')
    try:
        someText = pytesseract.image_to_string(someFilename, config='--psm {}'.format(psmValue), lang='rus_handwriting')
        return someText
    except:
        return None
    
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