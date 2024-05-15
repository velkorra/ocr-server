from PIL import Image
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

image = cv2.imread('tests/test2.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Удаление шума
kernel = np.ones((1, 1), np.uint8)
processed_image = cv2.dilate(binary, kernel, iterations=1)
processed_image = cv2.erode(processed_image, kernel, iterations=1)

final_image = Image.fromarray(processed_image)

text = pytesseract.image_to_string(final_image, lang='rus_handwriting')
print(text)