import time
import pyautogui
import cv2
import math
import numpy as np
import os
from time import *
from datetime import *
from datetime import datetime


# from pynput.keyboard import Controller, Key
# keyboard = Controller()

gap_x, gap_y = 52, -26.5

def add(a, b):
    result = b[0] + a[0], b[1] + a[1]
    return result

def distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def difference(a, b):
    result = b[0] - a[0], b[1] - a[1]
    return result

def zoom():
    # pyautogui.hotkey('shift', 'z')
    pyautogui.keyDown('shift')
    pyautogui.keyDown('z')

    # Wait for 2 seconds
    sleep(2)

    # Release the keys
    pyautogui.keyUp('z')
    pyautogui.keyUp('shift')


def drag(a, b, speed=1):
    if not a or not b: return
    dist_a_b = distance(a, b)
    if dist_a_b < 40: return
    duration = dist_a_b / 500 / speed
    pyautogui.moveTo(a)
    pyautogui.mouseDown()
    pyautogui.moveTo(b[0], b[1], duration=duration)
    pyautogui.mouseUp()

def drag_many(positions, duration):
    # print("Drag many:", positions)
    pyautogui.moveTo(positions[0])
    pyautogui.mouseDown()
    for pos in positions[1:]:
        if pos:
            pyautogui.moveTo(pos[0], pos[1], duration=duration)
    pyautogui.mouseUp()

def find_image_and_check_color(imageB, sensitivity=10):
    """Finds ImageB in ImageA and determines if the matched region is color or grayscale."""
    # Load images

    screenshot = pyautogui.screenshot()
    imageA = np.array(screenshot)

    if imageA is None or imageB is None:
        print("Error: One or both image files not found.")
        return None

    # Match template to find ImageB in ImageA
    result = cv2.matchTemplate(cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY), cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get the matched region in ImageA
    h, w = imageB.shape[:2]
    matched_region = imageA[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w]

    if matched_region.size == 0:
        print("Error: No matching region found.")
        return None

    # Split channels
    b, g, r = cv2.split(matched_region)

    # Compute color channel differences
    diff_b_g = np.abs(b - g).mean()
    diff_b_r = np.abs(b - r).mean()
    diff_g_r = np.abs(g - r).mean()

    # Determine if the matched region is grayscale or color
    is_grayscale = (diff_b_g < sensitivity) and (diff_b_r < sensitivity) and (diff_g_r < sensitivity)

    return False if is_grayscale else True

def load_and_show_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image file not found.")
        return

    cv2.imshow("Image", img)
    cv2.waitKey(0)  # Waits until a key is pressed
    cv2.destroyAllWindows()  # Closes the window

def show(image, file="Image", dur=500):
    cv2.imshow(file, image)
    cv2.waitKey(dur)  # Waits until a key is pressed
    cv2.destroyAllWindows()  # Closes the window

def match_number(image_path, numbers_dir):
    # Load the input image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding to enhance recognition
    _, image_thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

    best_match = None
    best_match_score = -float('inf')

    # Loop through digit images for direct matching
    for i in range(10):
        digit_image = cv2.imread(os.path.join(numbers_dir, f"{i}.jpg"), cv2.IMREAD_GRAYSCALE)
        _, digit_image_thresh = cv2.threshold(digit_image, 150, 255, cv2.THRESH_BINARY)

        # Match the entire input image with each digit template
        res = cv2.matchTemplate(image_thresh, digit_image_thresh, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        if max_val > best_match_score:
            best_match_score = max_val
            best_match = str(i)

    return int(best_match) if best_match else None

def coords(base, x, y):
    result_x = base[0] + x * gap_x + y * gap_x
    result_y = base[1] + x * gap_y - y * gap_y
    result = result_x, result_y
    # print("Coords:", base, x, y, result)
    return result


def haze(pos_0, pos_left, width, height):
    rows_per_square = 3
    pos_right = coords(pos_left, width, 0)
    positions = [pos_0, pos_left, pos_right]
    print("Haze positions:", positions)
    for x in range(height * rows_per_square):
        pos_left = coords(pos_left, 0, 1 / rows_per_square)
        pos_right = coords(pos_right, 0, 1 / rows_per_square)
        positions.append(pos_left)
        positions.append(pos_right)
    drag_many(positions, duration=0.5)


def find_files_with_word(directory, word):
    matching_files = []

    for filename in os.listdir(directory):
        if word.lower() in filename.lower():  # Case-insensitive search
            matching_files.append(directory + filename)

    return matching_files
# Example usage:
# directory_path = "/path/to/your/directory"
# print(find_files_with_word(directory_path))

