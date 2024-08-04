import os
import argparse
from pdf2image import pdf_to_images
from math_detector import analyze_image_with_cnstd
from segment import process_images 
from math_latex import convert_images_to_latex
from latex import generate_text_flow

def main(input_folder, output_folder):
    math_detected_folder = os.path.join(output_folder, "math_detected")
    os.makedirs(math_detected_folder, exist_ok=True)

    """ PDF to image conversion """
    pdf_images_folder = os.path.join(output_folder, "pdf_images")
    os.makedirs(pdf_images_folder, exist_ok=True)  
    pdf_to_images(input_folder, pdf_images_folder)

    """ Detect math regions in images """
    for image_file in os.listdir(pdf_images_folder):
        input_image_path = os.path.join(pdf_images_folder, image_file)
        output_image_path = os.path.join(math_detected_folder, image_file)
        analyze_image_with_cnstd(input_image_path, output_image_path)
    
    segmented_folder = os.path.join(output_folder, "segmented")
    os.makedirs(segmented_folder, exist_ok=True) 

    without_cropped_folder = os.path.join(output_folder, "without_cropped")
    os.makedirs(without_cropped_folder, exist_ok=True)  
    
    """ Image segmentation """
    process_images(math_detected_folder, segmented_folder, without_cropped_folder)
    
    """ Image to Latex conversion """
    latex_folder = os.path.join(output_folder, "math_latex")
    os.makedirs(latex_folder, exist_ok=True)  
    convert_images_to_latex(segmented_folder, latex_folder)
    
    """ Generate and save LaTeX """
    for image_file in os.listdir(without_cropped_folder):
        image_path = os.path.join(without_cropped_folder, image_file)
        generate_text_flow(image_path, latex_folder, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF documents to LaTeX.")
    parser.add_argument("--input_folder", type=str, help="Path to the folder containing PDF files.")
    parser.add_argument("--output_folder", type=str, help="Path to the folder where the LaTeX files will be saved.")
    args = parser.parse_args()

    main(args.input_folder, args.output_folder)
