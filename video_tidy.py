import cv2
import os
import numpy as np
from utilities import *

def load_images_from_directory(directory):
    images = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img = cv2.imread(filepath)
            if img is not None:
                images[filename] = img
    return images

def are_images_identical(img1, img2):
    return img1.shape == img2.shape and np.array_equal(img1, img2)

def find_and_delete_duplicates(directory):
    images = load_images_from_directory(directory)
    filenames = list(images.keys())
    deleted = set()

    for i in range(len(filenames)):
        if filenames[i] in deleted:
            continue
        for j in range(i + 1, len(filenames)):
            if filenames[j] in deleted:
                continue
            img1 = images[filenames[i]]
            img2 = images[filenames[j]]
            compare = compare_images(img1, img2)
            print(f"Compare: {filenames[j]} vs {filenames[i]}: {compare}")
            if compare > 0.15:
                duplicate_path = os.path.join(directory, filenames[j])
                try:
                    os.remove(duplicate_path)
                    deleted.add(filenames[j])
                    print(f"Deleted duplicate: {filenames[j]} (same as {filenames[i]})")
                except FileNotFoundError:
                    print(f"File already deleted: {filenames[j]}")

    return list(deleted)


directory_path = 'video'
deleted_files = find_and_delete_duplicates(directory_path)
print(deleted_files)