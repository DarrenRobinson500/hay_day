import cv2
import numpy as np
import pyautogui
import cv2
from time import *
from items import *

PRODUCTION_ZONE_A = (665, 651, 350, 200)

def find_image_in_region(image, region=PRODUCTION_ZONE_A):
    # Get the screen
    # Capture a screenshot
    screenshot = pyautogui.screenshot()
    screen = np.array(screenshot)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    image = np.array(image)
    image_a = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # Extract the specified region from the screen
    x, y, w, h = region
    screen_region = screen[y:y + h, x:x + w]  # Cropping the region

    # Restrict scaling to 50% to 80% of the original size
    best_match = None
    best_scale = None
    best_loc = None
    best_val = 0.7

    for scale in np.linspace(0.5, 1, 51):  # Test different scales
        resized_a = cv2.resize(image_a, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        if resized_a.shape[0] > screen_region.shape[0] or resized_a.shape[1] > screen_region.shape[1]:
            continue  # Skip sizes larger than the region

        result = cv2.matchTemplate(screen_region, resized_a, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val:  # Store the best match
            best_match = resized_a
            best_scale = scale
            best_loc = (max_loc[0] + x, max_loc[1] + y)  # Adjust to global coordinates
            best_val = max_val

    if best_match is not None:
        h, w = best_match.shape
        top_left = best_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        return {"scale": best_scale, "position": best_loc, "match_value": best_val, "box": (top_left, bottom_right)}

    return None  # No good match found


# Example usage:
pyautogui.hotkey('alt', 'tab')
sleep(0.5)

image = cheese.image_menu.image
result = find_image_in_region(image)
if result:
    print(f"Image found at {result['position']} with scale {result['scale']} and match value {result['match_value']}")
else:
    print("Image not found in the specified region")


# print(cheese.image_menu_mini_1.find(region=PRODUCTION_ZONE))


sleep(0.5)
pyautogui.hotkey('alt', 'tab')
