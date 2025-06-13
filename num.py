import cv2
import numpy as np
import os

class Numbers:
    def __init__(self, numbers_dir):
        self.digits = {}
        for i in range(10):
            digit_path = os.path.join(numbers_dir, f"{i}.jpg")
            self.digits[i] = cv2.imread(digit_path, cv2.IMREAD_GRAYSCALE)

    def read(self, image, threshold=0.7, min_distance=10):
        """Reads a number (1 to 3 digits) from an input image, removing duplicate detections."""
        # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        detected_digits = []

        try:
            for digit, template in self.digits.items():
                result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
                locations = np.where(result >= threshold)

                for pt in zip(*locations[::-1]):
                    detected_digits.append((digit, pt[0]))  # Store (digit, x-coordinate)

            # Sort detections by x-coordinate (left to right)
            detected_digits.sort(key=lambda x: x[1])

            # Remove detections that are too close to each other
            filtered_digits = []
            for digit, x in detected_digits:
                if all(abs(x - existing_x) > min_distance for _, existing_x in filtered_digits):
                    filtered_digits.append((digit, x))

            # Convert filtered digits into a number
            number_string = "".join(str(d[0]) for d in filtered_digits)

            return int(number_string) if number_string else None  # Return None if no digits found
        except:
            return 0


def extract_region(template, image, x_offset, y_offset, w, h, threshold=0.8):
    # Load images
    # image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # template = cv2.imread(template_path, cv2.IMREAD_COLOR)

    # Get template dimensions
    tw, th = template.shape[1], template.shape[0]

    # Perform template matching
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        print("Template not found with sufficient confidence.")
        return None

    # Determine center coordinates of the best match
    center_x = max_loc[0] + tw // 2
    center_y = max_loc[1] + th // 2

    # Compute the region coordinates based on offsets
    x_start = max(0, center_x + x_offset)
    y_start = max(0, center_y + y_offset)
    x_end = min(image.shape[1], x_start + w)
    y_end = min(image.shape[0], y_start + h)

    # Extract the region
    extracted_region = image[y_start:y_end, x_start:x_end]
    extracted_region_gray = cv2.cvtColor(extracted_region, cv2.COLOR_BGR2GRAY)

    return extracted_region_gray

menu_numbers = Numbers("images/numbers/menu")
market_numbers = Numbers("images/numbers/market")
