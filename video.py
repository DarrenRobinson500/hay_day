from image import *
from utilities import *
import cv2
import os
import re

def save_image(image, save_dir):
    # Ensure the directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Pattern to match existing files like img_1.jpg, img_2.jpg, etc.
    pattern = re.compile(r"img_(\d+)\.jpg")

    # Get existing filenames
    existing_files = os.listdir(save_dir)
    numbers = [int(match.group(1)) for f in existing_files if (match := pattern.match(f))]

    # Determine next number
    next_number = max(numbers, default=0) + 1
    filename = f"img_{next_number}.jpg"
    filepath = os.path.join(save_dir, filename)

    # Save the image
    success = cv2.imwrite(filepath, image)
    if not success:
        raise IOError(f"Failed to save image to {filepath}")

    return filepath

pyautogui.hotkey('alt', 'tab')
sleep(0.5)

height, width = i_field_marker.image.shape[:2]

print(f"Size: {height}x{width}")

marker_x, marker_y = i_field_marker.find()
print(marker_x, marker_y)

img1 = capture_screen_region_cv2(marker_x, marker_y, width, height)
count = 0
while count < 300:
    img2 = capture_screen_region_cv2(marker_x, marker_y, width, height)
    similarity = compare_images(img1, img2)
    print("Compare", similarity)
    if similarity < 0.8:
        print("Saving")
        save_image(img2, "video")
    count += 1
    sleep(1)

sleep(0.5)
pyautogui.hotkey('alt', 'tab')

