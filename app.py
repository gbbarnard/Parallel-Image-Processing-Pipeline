from PIL import Image
import multiprocessing as mp

nprocs = mp.cpu_count()
print(f"Number of CPU cores: {nprocs}")
