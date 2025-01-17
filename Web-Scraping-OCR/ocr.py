import cv2
import easyocr
import os

class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    def perform_ocr(self,image):
        self.results = self.reader.readtext(image=image,paragraph=True,detail=0)
        return self.results
    
    def write_to_file(self,filename):
        with open(filename,"w") as file:
            for result in self.results:
                file.write(f"{result}\n")
    
    def ocr_product(self,product_name):
        for root, _, files in os.walk(product_name):
            for file in files:
                if file.lower().endswith(self.image_extensions):
                    original_path = os.path.join(root, file)
                    
                    image = cv2.imread(original_path)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    _, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    cv2.imwrite('processed_image.png', binary_img)

                    # Perform OCR on the image
                    self.perform_ocr('processed_image.png')

                    name, _ = os.path.splitext(file)
                    text_file_path = os.path.join(root, f"{name}_ocr.txt")
                    
                    self.write_to_file(text_file_path)
                        
                    print(f"Text extracted and saved to: {text_file_path}")



