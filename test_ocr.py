import fitz  
import pytesseract
import cv2
import numpy as np
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load each page
        raw_text = page.get_text("text")
        # print(raw_text)
        images = page.get_images(full=True)  # Extract images
        image_text = ""
        # Iterate through the images in each page
        for img_index, img in enumerate(images):
            xref = img[0]  # Extract image reference number (XREF)
            base_image = pdf_document.extract_image(xref)  # Extract image
            image_bytes = base_image["image"]  # Get the raw image bytes
            image_ext = base_image["ext"]  # Get the image extension (like jpg, png)
            
            # Convert the raw image bytes into an OpenCV image
            np_array = np.frombuffer(image_bytes, np.uint8)  # Convert bytes to numpy array
            image_cv = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # Decode the image as OpenCV format
            

            # Convert the OpenCV image to grayscale for better OCR results
            gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            
            # Perform OCR using pytesseract
            image_text += pytesseract.image_to_string(gray_image,lang='vie')
        full_text = raw_text + image_text
        print(full_text)
            
# Example usage:
pdf_path = r"D:\pypy\Crawl_data\test.pdf"  # Replace with your PDF path
extract_images_from_pdf(pdf_path)



import requests
from pathlib import Path
import os
def get_pdf(url,out_name):
    out_dir = "Save_pdf"
    Path(out_dir).mkdir(parents=False,exist_ok=True)
    res = requests.get(url)
    with open(os.path.join(out_dir,out_name),'wb') as file:
        file.write(res.content)

# get_pdf("https://tayho.hanoi.gov.vn/Medias/1//33//2024//7//8/754ccda3-5ece-40fc-808e-7c0314da37df.pdf","tayho.pdf")

import PyPDF2

def pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# pdf_to_text("")