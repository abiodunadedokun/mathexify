import os
from PIL import Image
from pix2tex.cli import LatexOCR
from tqdm import tqdm

def convert_images_to_latex(input_folder, output_folder):
    image_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
                         key=lambda x: int(x.replace('MF', '').split('.')[0]))
    
    total_images = len(image_files)
    
    model = LatexOCR()
    pbar = tqdm(total=total_images, desc="Processing images", unit="image")

    for filename in image_files:
        img_path = os.path.join(input_folder, filename)
        try:
            img = Image.open(img_path)
            latex_output = model(img)

            output_filename = f"{os.path.splitext(filename)[0]}.tex"
            output_path = os.path.join(output_folder, output_filename)
            
            with open(output_path, "w") as f:
                f.write(latex_output)
            
            pbar.update(1)
            pbar.set_postfix({"Current file": filename})

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    pbar.close()

