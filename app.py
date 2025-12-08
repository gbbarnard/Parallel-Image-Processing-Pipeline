import os
import shutil
import time
from PIL import Image, ImageFilter
import multiprocessing as mp

# Set constants.
IMAGES_FOLDER = "images"
OUTPUT_FOLDER = "out"

# Remove old output folder and its contents if it exists already.
if os.path.isdir(OUTPUT_FOLDER):
  shutil.rmtree(OUTPUT_FOLDER)
os.mkdir(OUTPUT_FOLDER)

# Apply filters to provided Pillow image.
def apply_filters(image):
  out = image.filter(ImageFilter.BoxBlur(50))
  # out = out.filter(ImageFilter.BoxBlur(50))

  return out

# Fully process a file in the images folder.
def process_image(file):
  with Image.open(f"{IMAGES_FOLDER}/{file}") as image:
    out = apply_filters(image)
    out.save(f"{OUTPUT_FOLDER}/{file}")

file_count = len(os.listdir(IMAGES_FOLDER))
print(f"\033[33mProcessing {file_count} file(s)...")

start_time = time.time()
files = os.listdir(IMAGES_FOLDER)
# The actual sequential execution.
for i, file in enumerate(files):
  process_image(file)
  print(f"\033[33mProcessed {i+1}/{file_count} file(s)...")

# Calculate runtime and rate.
end_time = time.time()
duration = end_time - start_time
print(f"\033[32mDone! Processed {file_count} file(s) in {round(duration, 2)} seconds. Avg. {round((file_count / duration), 2)} files/s.\033[0m")
