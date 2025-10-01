from PIL import Image
import pytesseract

def text2img(path_img):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image = Image.open(path_img)
    
    options = "--psm 6 --oem 3"

    text = pytesseract.image_to_string(image, lang="eng", config=options)

    return text

def confirm_tests(path_img,count=10):
    results = []

    for i in range(count):
        results.append(text2img(path_img))

    for i in range(len(results)-1):
        if results[i] != results[i+1]:
            return None
        
    return results[1]
