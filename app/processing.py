import os
import subprocess

def process_video(input_path):
    output_path = input_path.rsplit('.', 1)[0] + '_processed.mp4'
    subprocess.run(['ffmpeg', '-i', input_path, '-vf', 'scale=640:480', output_path])
    return output_path

def process_audio(input_path):
    output_path = input_path.rsplit('.', 1)[0] + '_processed.mp3'
    subprocess.run(['ffmpeg', '-i', input_path, '-acodec', 'libmp3lame', '-b:a', '128k', output_path])
    return output_path

def process_image(input_path):
    from PIL import Image
    output_path = input_path.rsplit('.', 1)[0] + '_processed.jpg'
    with Image.open(input_path) as img:
        img.thumbnail((800, 800))
        img.save(output_path, 'JPEG')
    return output_path

def process_text(input_path):
    output_path = input_path.rsplit('.', 1)[0] + '_processed.txt'
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        text = infile.read()
        # Example processing: convert to uppercase
        processed_text = text.upper()
        outfile.write(processed_text)
    return output_path