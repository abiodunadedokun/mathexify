import os
import cv2

def process_images(input_folder, output_folder, without_cropped_folder):
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(without_cropped_folder, exist_ok=True)

    mf_counter = 1  # counter for cropped images

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg','.jpeg','.png')):  
            input_image_path = os.path.join(input_folder, filename)
            mf_counter = crop_and_save(input_image_path, output_folder, without_cropped_folder, mf_counter)

def crop_and_save(input_image_path, output_folder, without_cropped_folder, mf_counter):
    image = cv2.imread(input_image_path)
    if image is None:
        print(f"Failed to load image: {input_image_path}")
        return mf_counter  

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 10, 250)
    cnts, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cropped_coordinates = []

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w * h > image.shape[0] * image.shape[1] * 0.0005 and w > image.shape[1] * 0.001 and h > image.shape[0] * 0.001: # these can be adjusted
            cropped_coordinates.append((x, y, x + w, y + h))
            cropped_img = image[y:y + h, x:x + w]
            output_filename = f"MF{mf_counter}.png"
            cv2.imwrite(os.path.join(output_folder, output_filename), cropped_img)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)  
            mf_counter += 1

    cv2.imwrite(os.path.join(without_cropped_folder, os.path.basename(input_image_path)), image)

    coords_filename = os.path.splitext(os.path.basename(input_image_path))[0] + "_cropped_coordinates.txt"
    with open(os.path.join(output_folder, coords_filename), "w") as f:
        for idx, (x1, y1, x2, y2) in enumerate(cropped_coordinates, start=1):
            f.write(f"cropped_{idx}: ({x1}, {y1}, {x2}, {y2})\n")

    print(f'Objects Cropped Successfully for: {input_image_path}')
    return mf_counter 
