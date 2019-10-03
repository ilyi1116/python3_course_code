from PIL import Image
import pytesseract

image = Image.open('./a.png')
image = image.point(lambda x: 0 if x < 140 else 255)
image.save('./a_processed.png')
print(pytesseract.image_to_string(image))
