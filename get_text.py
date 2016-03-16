import pytesseract
from PIL import Image


filename = "test_image.png"
test_image = Image.open(filename)
result = pytesseract.image_to_string(test_image)
print(result)