import os
from wand.image import Image       #pip install wand

def pdf_to_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, pdf_file)
            base_name = pdf_file[:-4]
            with Image(filename=pdf_path, resolution=300) as img:
                for i, page in enumerate(img.sequence):
                    with Image(page) as page_image:
                        page_image.format = 'png'
                        output_file_name = f"{base_name}_{i+1}.png"
                        page_image.save(filename=os.path.join(output_folder, output_file_name))
