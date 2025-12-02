import easyocr
print("Downloading OCR models... this may take a few minutes...")
reader = easyocr.Reader(['en'], gpu=False)
print("OCR models downloaded successfully!")
