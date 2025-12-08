import os
import shutil
import time
from PIL import Image, ImageFilter
import multiprocessing as mp

images_folder = "images"
out_folder = "out"

if os.path.isdir(out_folder):
  shutil.rmtree(out_folder)
os.mkdir(out_folder)

def apply_filters(image):
  out = image.filter(ImageFilter.BoxBlur(50))
  # out = out.filter(ImageFilter.BoxBlur(50))

  return out

def process_image(file):
  with Image.open(f"{images_folder}/{file}") as image:
    out = apply_filters(image)
    out.save(f"{out_folder}/{file}")

os.path

file_count = len(os.listdir(images_folder))
print(f"\033[33mProcessing {file_count} file(s)...")

start_time = time.time()
files = os.listdir(images_folder)
for i, file in enumerate(files):
  process_image(file)
  print(f"\033[33mProcessed {i+1}/{file_count} file(s)...")

end_time = time.time()
duration = end_time - start_time

print(f"\033[32mDone! Processed {file_count} file(s) in {round(duration, 2)} seconds. Avg. {round((file_count / duration), 2)} files/s.\033[0m")
