import cv2
from PIL import Image
import pytesseract

class ImageProcessing:
    def __init__(self):
        pass

    def extract_text_from_image(self, image_path):
        """Extract text from an image using OCR and check for XAUUSD-related terms."""
        # Load the image
        image = cv2.imread(image_path)
        
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Perform OCR to extract text
        text = pytesseract.image_to_string(gray).strip()
        
        # Keywords to check
        keywords = ["Gold", "XAUUSD", "XAUUSDm", "XAUUSD.m"]
        
        # Check for keywords in the extracted text (case-insensitive)
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return f"Relevant terms detected in the image: {', '.join(keywords)}"
        else:
            # Custom message when no keywords are found
            return "🚫 This is not an image of the XAUUSD pair or Gold. I only trade XAUUSD/Gold for now! 💰"

