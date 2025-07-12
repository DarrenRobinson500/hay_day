# import time
import pyautogui
import cv2
import math
import numpy as np
import os
from time import *
from datetime import *
from datetime import datetime
import pyautogui
import ast
# from shapely.geometry import LineString, box

print("Utilities")

screen_width, screen_height = 1920, 1080


def string_to_tuple(s):
    if not s:
        # print("String to tuple - no input")
        return
    try:
        result = ast.literal_eval(s)
        if isinstance(result, tuple) and all(isinstance(i, int) for i in result):
            return result
        else:
            raise ValueError("Input is not a valid tuple of integers.")
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing tuple: {e}")
        return None

gap_x, gap_y = 53, -26.8

def spiral(num_turns=24, step_size=35):
    center_x, center_y = pyautogui.position()
    """Moves the mouse in an outward spiral."""
    angle = 0  # Initial angle
    radius = 25  # Initial radius

    for _ in range(num_turns * 360 // step_size):  # Loop through degrees in steps
        x = center_x + int(radius * math.cos(math.radians(angle)))
        y = center_y + int(radius * math.sin(math.radians(angle)))

        pyautogui.moveTo(x, y)
        # time.sleep(0.01)  # Small delay for smooth movement

        angle += step_size  # Increase angle to move circularly
        radius += .5  # Gradually increase radius for outward motion


# Example usage
# spiral()

def add(a, b):
    if a and b:
        result = b[0] + a[0], b[1] + a[1]
        return result

def distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def difference(a, b):
    result = b[0] - a[0], b[1] - a[1]
    return result

def zoom_old():
    # pyautogui.hotkey('shift', 'z')
    pyautogui.keyDown('shift')
    pyautogui.keyDown('z')

    # Wait for 2 seconds
    sleep(2)

    # Release the keys
    pyautogui.keyUp('z')
    pyautogui.keyUp('shift')


def zoom():
    for x in range(5):
        pyautogui.press('f5')
    for x in range(5):
        pyautogui.press('f5')


def is_point_on_screen(a):
    if not a: return
    x, y = a
    return 0 <= x < screen_width and 0 <= y < screen_height

def drag(a, b, speed=1, add_spiral=False):
    b = clamp_point_to_screen(a, b)
    # print("Clamped b:", b)
    if not is_point_on_screen(a) or not is_point_on_screen(b): return
    dist_a_b = distance(a, b)
    if dist_a_b < 40: return
    duration = dist_a_b / 500 / speed
    pyautogui.moveTo(a)
    pyautogui.mouseDown()
    pyautogui.moveTo(b[0], b[1], duration=duration)
    if add_spiral: spiral()
    pyautogui.mouseUp()

def drag_many(positions, speed):
    for position in positions:
        if not(is_point_on_screen(position)):
            print(f"Drag many. Point: {position} is not valid")
            return
    # Set-up
    pyautogui.moveTo(positions[0])
    previous_pos = positions[0]
    pyautogui.mouseDown()
    # Loop
    for pos in positions[1:]:
        if pos:
            dist_a_b = distance(previous_pos, pos)
            duration = dist_a_b / 500 / speed
            pyautogui.moveTo(pos[0], pos[1], duration=duration)
            previous_pos = pos
    # Close
    pyautogui.mouseUp()

def find_image_and_check_color(imageB, sensitivity=20):
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
    print(f"Check color: Blue green {diff_b_g} Blue red {diff_b_r} Green red {diff_g_r}")

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
    result = int(result_x), int(result_y)
    # print("Coords:", base, x, y, result)
    return result


def haze(pos_0, pos_left, width, height):
    rows_per_square = 4
    pos_right = coords(pos_left, width, 0)
    positions = [pos_0, pos_left, pos_right]
    print("Haze positions:", positions)
    for x in range(height * rows_per_square):
        pos_left = coords(pos_left, 0, 1 / rows_per_square)
        pos_right = coords(pos_right, 0, 1 / rows_per_square)
        positions.append(pos_left)
        positions.append(pos_right)
    drag_many(positions, speed=4)


def find_files_with_word(directory, word):
    matching_files = []

    for filename in os.listdir(directory):
        if word.lower() in filename.lower():  # Case-insensitive search
            matching_files.append(directory + filename)

    return matching_files


def wait_for_image(image, time):
    interval = 0.5
    found, count = False, 0
    while not found and count < time / interval:
        found = image.find()
        sleep(interval)
        print("Wait for image:", count, image)
        count += 1
        if count == 40: zoom()
    return found

def wait_for_images(images_to_click, destination_image, time_seconds):
    interval = 0.5
    found, count = False, 0
    while not found and count < time_seconds / interval:
        for image in images_to_click:
            if image.find(): image.click()
        found = destination_image.find()
        sleep(interval)
        print("Wait for image:", count * interval, destination_image)
        count += 1
    return found

def clamp_point_to_screen(a, b, min_x=1, min_y=1, max_x=screen_width-1, max_y=screen_height-1):
    x, y = b
    clamped_x = max(min_x, min(x, max_x))
    clamped_y = max(min_y, min(y, max_y))
    return clamped_x, clamped_y


# def clamp_point_to_screen(a, b):
#
#     # Define the screen box and the line segment
#     screen = box(0, 0, screen_width, screen_height)
#     line = LineString([a, b])
#
#     # If b is inside the screen, just return b
#     if screen.contains(line):
#         return b
#
#     # Intersect the line with the screen bounds
#     intersection = screen.boundary.intersection(line)
#
#     # Handle different intersection types
#     if intersection.is_empty:
#         return a  # No intersection found — default to a
#     elif intersection.geom_type == 'Point':
#         c = (intersection.x, intersection.y)
#         print(f"Clamped {b} to {c}")
#         return c
#     elif intersection.geom_type == 'MultiPoint':
#         # Pick the closest point to a
#         points = list(intersection)
#         points.sort(key=lambda p: ((p.x - a[0])**2 + (p.y - a[1])**2))
#         return (points[0].x, points[0].y)
#     else:
#         return a  # Fallback

# Example usage:
a = (400, 300)
b = (2000, 900)  # Outside a 1024x768 screen

result = clamp_point_to_screen(a, b)
print("Clamped point on screen edge:", result)


print("Utilities End")
