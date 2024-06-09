import random
import os

def get_random_meme(category):
    files = os.listdir(f"assets/{category}")
    random_file = random.choice(files)
    random_file_path = f"assets/{category}/{random_file}"
    return random_file_path