import os
import cv2
from PIL import Image
import pytesseract
from pytesseract import Output
from datetime import datetime

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def detect_black_boxes(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 15, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [cv2.boundingRect(cnt) for cnt in contours if cv2.contourArea(cnt) > 100]

def get_ocr_data_with_position(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_data(img, output_type=Output.DICT)

def load_latex_formulas(latex_folder_path):
    latex_formulas = {}
    for filename in os.listdir(latex_folder_path):
        if filename.endswith('.tex'):
            placeholder = filename.split('.')[0]
            with open(os.path.join(latex_folder_path, filename), 'r') as file:
                latex_formulas[placeholder] = file.read().strip()
    return latex_formulas

def generate_text_flow(image_path, latex_folder_path, output_folder):
    black_boxes = detect_black_boxes(image_path)
    ocr_data = get_ocr_data_with_position(image_path)
    latex_formulas = load_latex_formulas(latex_folder_path)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    elements = []
    for i, text in enumerate(ocr_data['text']):
        if int(ocr_data['conf'][i]) > 60:
            elements.append(('text', text, ocr_data['top'][i], ocr_data['left'][i]))
    
    for i, box in enumerate(black_boxes):
        placeholder = f"MF{i+1}"
        latex_content = latex_formulas.get(placeholder, None)
        if latex_content:
            elements.append(('latex', latex_content, box[1], box[0]))

    elements.sort(key=lambda e: (e[2], e[3]))

    output_text = ' '.join([content for _, content, _, _ in elements])

    base_filename = os.path.splitext(os.path.basename(image_path))[0] + ".tex"
    output_file_path = os.path.join(output_folder, base_filename)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(output_text)  # Now 'output_text' is defined and contains the combined text
    
    print(f"Output written to: {output_file_path}")

    elements = []
    for i, text in enumerate(ocr_data['text']):
        if int(ocr_data['conf'][i]) > 60:
            elements.append(('text', text, ocr_data['top'][i], ocr_data['left'][i]))
    for i, box in enumerate(black_boxes):
        latex_content = latex_formulas.get(f"MF{i+1}", f"[MF{i+1} not found]")
        elements.append(('latex', latex_content, box[1], box[0]))
    
    elements.sort(key=lambda e: (e[2], e[3]))
    text_flow = ' '.join([content for _, content, _, _ in elements])
    
    return text_flow

def save_text_flow_to_file(text_flow, output_folder, base_filename='text_flow'):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{base_filename}_{timestamp}.tex"  # Changed to .tex
    filepath = os.path.join(output_folder, filename)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write("\\documentclass{article}\n\\usepackage{amsmath}\n\\begin{document}\n")
        file.write(text_flow)
        file.write("\n\\end{document}")
    
    print(f"LaTeX document saved to: {filepath}")



