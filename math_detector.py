import subprocess

# pip install cnstd
def analyze_image_with_cnstd(input_image_path, output_image_path):
    try:
        command = [
            'cnstd',
            'analyze',
            '-m', 'mfd',
            '--conf-thresh', '0.25',
            '--resized-shape', '800',
            '-i', input_image_path,
            '-o', output_image_path
        ]
        
        subprocess.run(command, check=True)
        print(f"Analysis completed: {output_image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during analysis: {e}")
