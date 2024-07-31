import os
import re
import pandas as pd
from transformers import pipeline
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

class Scanner:
    def __init__(self):
        # Load a pre-trained language model from Hugging Face (optional, not used in this version)
        self.nlp = pipeline("zero-shot-classification")

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def extract_text_from_image(self, image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def extract_text(self, file_path):
        if file_path.endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        elif file_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            return self.extract_text_from_image(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            return None

    def extract_information(self, text):
        # Define regular expressions for each field based on the provided text
        patterns = {
            "Customer Name": r"Customer Name\s*:\s*(.*)",
            "Phone number": r"Jio Number\s*:\s*(\d+)",
            "Invoice Number": r"Invoice No\s*:\s*(\S+)",
            "Address": r"Customer Address\s*:\s*(.*)",
            "Date": r"Invoice/Payment Date & Time\s*:\s*(.*? \d{2}:\d{2}:\d{2})",
            "GST No": r"GST No\s*:\s*(\S+)",
            "PAN No": r"PAN No\s*:\s*(\S+)",
            "Total Amount": r"Total Amount[\s(₹)]*\s*:\s*(\d+\.\d{2})"
        }

        extracted_info = {}
        for label, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                extracted_info[label] = match.group(1).strip()  # Extract the relevant value

        return extracted_info

    def process_documents(self, path):
        data = []
        if os.path.isdir(path):
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                file_data = self.process_single_file(file_path)
                if file_data:
                    data.append(file_data)
        elif os.path.isfile(path):
            file_data = self.process_single_file(path)
            if file_data:
                data.append(file_data)
        else:
            print(f"Invalid path: {path}")

        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data)
        df.to_csv("results/"+"extracted"+".csv")
        return df

    def process_single_file(self, file_path):
        print(f"Processing: {file_path}")
        text = self.extract_text(file_path)
        
        if not text:
            print("No text extracted.")
            return None

        # Print the extracted text for debugging
        print("Extracted Text:")
        print(text[:1000])  # Print the first 1000 characters for brevity
        
        extracted_data = self.extract_information(text)
        
        if not extracted_data:
            print("No information extracted.")
            return None

        return extracted_data





