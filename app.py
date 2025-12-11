import os
import shutil
import time
from PIL import Image, ImageFilter
import multiprocessing as mp


# Config
IMAGES_FOLDER = "images"
OUT_SEQ = "out_seq"
OUT_PAR = "out_par"


# Image pipeline
def apply_filters(image):
    out = image.filter(ImageFilter.BoxBlur(50))
    return out

def process_image_to(args):
    """
    args: (filename, output_folder)
    Must be top-level for multiprocessing pickling.
    """
    file, output_folder = args
    in_path = os.path.join(IMAGES_FOLDER, file)
    out_path = os.path.join(output_folder, file)

    with Image.open(in_path) as image:
        out = apply_filters(image)
        out.save(out_path)

    return file

# Helpers
def reset_folder(folder):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

def run_sequential(files):
    reset_folder(OUT_SEQ)

    start = time.perf_counter()

    for i, file in enumerate(files, start=1):
        process_image_to((file, OUT_SEQ))
        print(f"\033[33m[SEQ] Processed {i}/{len(files)} file(s)...\033[0m")

    end = time.perf_counter()
    return end - start

def run_parallel(files, workers=None):
    reset_folder(OUT_PAR)

    workers = workers or mp.cpu_count()
    tasks = [(f, OUT_PAR) for f in files]

    start = time.perf_counter()

    with mp.Pool(processes=workers) as pool:
        for i, _ in enumerate(pool.imap_unordered(process_image_to, tasks), start=1):
            print(f"\033[36m[PAR] Processed {i}/{len(files)} file(s)...\033[0m")

    end = time.perf_counter()
    return end - start, workers

def main():
    if not os.path.isdir(IMAGES_FOLDER):
        print(f"\033[31mMissing '{IMAGES_FOLDER}' folder.\033[0m")
        return

    files = [f for f in os.listdir(IMAGES_FOLDER)
             if os.path.isfile(os.path.join(IMAGES_FOLDER, f))]

    file_count = len(files)
    if file_count == 0:
        print(f"\033[31mNo files found in '{IMAGES_FOLDER}'.\033[0m")
        return

    print(f"\033[33mFound {file_count} file(s).\033[0m\n")

    # 1) Sequential baseline
    print("\033[33mRunning SEQUENTIAL baseline...\033[0m")
    t_seq = run_sequential(files)

    print(
        f"\n\033[32m[SEQ] Time: {t_seq:.4f}s | "
        f"Rate: {(file_count / t_seq):.2f} files/s\033[0m\n"
    )

    # 2) Parallel test
    print("\033[36mRunning MULTIPROCESSING version...\033[0m")
    t_par, workers = run_parallel(files)

    print(
        f"\n\033[32m[PAR] Time: {t_par:.4f}s | "
        f"Rate: {(file_count / t_par):.2f} files/s | "
        f"Workers: {workers}\033[0m\n"
    )

    # 3) Metrics
    speedup = t_seq / t_par if t_par > 0 else 0
    efficiency = speedup / workers if workers > 0 else 0

    print("\033[35m--- Performance Summary ---\033[0m")
    print(f"\033[35mSequential time      : {t_seq:.4f}s\033[0m")
    print(f"\033[35mParallel time        : {t_par:.4f}s\033[0m")
    print(f"\033[35mSpeedup (T1/Tp)      : {speedup:.3f}x\033[0m")
    print(f"\033[35mEfficiency (S/p)     : {efficiency:.3f}\033[0m")
    print(f"\033[35mOutput folders       : {OUT_SEQ}/ , {OUT_PAR}/\033[0m")

if __name__ == "__main__":
    mp.freeze_support()  # good practice for Windows
    main()
