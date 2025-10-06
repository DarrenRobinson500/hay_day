import os
import cv2
import numpy as np
import pyautogui
from time import sleep

def find_building_offsets(farm_image_path, house_path, building_names, production_dir="images/production"):
    def locate_center(image, template, threshold=0.8):
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray_img, gray_template, cv2.TM_CCOEFF_NORMED)
        loc = cv2.minMaxLoc(result)
        max_val = loc[1]
        if max_val < threshold:
            raise ValueError("Template not found with sufficient confidence.")
        x, y = loc[3]
        w, h = gray_template.shape[::-1]
        return (x + w // 2, y + h // 2)

    farm_img = cv2.imread(farm_image_path)
    house_template = cv2.imread(house_path)
    house_pos = locate_center(farm_img, house_template)

    offsets = {"house": house_pos}
    for name in building_names:
        template_path = os.path.join(production_dir, f"{name}.jpg")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Missing template: {template_path}")
        template = cv2.imread(template_path)
        building_pos = locate_center(farm_img, template)
        offsets[name] = (building_pos[0] - house_pos[0], building_pos[1] - house_pos[1])

    return offsets


def drag_from_center(dx, dy, duration=2):
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    safe_x = max(1, min(screen_width - 2, center_x))
    safe_y = max(1, min(screen_height - 2, center_y))
    pyautogui.moveTo(safe_x, safe_y, duration=0.2)
    pyautogui.dragRel(dx, dy, duration=duration)
    sleep(0.5)

def capture_screen():
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def find_house_position(image, house_template, threshold=0.8):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_img, house_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    if loc[0].size == 0:
        raise ValueError("House not found in image.")
    x, y = loc[1][0], loc[0][0]
    return (x, y)

def center_house_on_screen(house_image_path):
    screen_width, screen_height = pyautogui.size()
    screen = capture_screen()
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    house_template = cv2.imread(house_image_path)
    house_gray = cv2.cvtColor(house_template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen_gray, house_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.8)
    if loc[0].size == 0:
        raise ValueError("House not found on screen.")

    house_x, house_y = loc[1][0], loc[0][0]
    house_w, house_h = house_gray.shape[::-1]
    house_center_x = house_x + house_w // 2
    house_center_y = house_y + house_h // 2

    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2

    dx = screen_center_x - house_center_x
    dy = screen_center_y - house_center_y

    drag_from_center(dx, dy)
    sleep(0.5)

def capture_farm_grid(house_image_path, step_size=400, overlap=100, side_crop=200):
    screen_width, screen_height = pyautogui.size()
    center_house_on_screen(house_image_path)

    grid_images = []
    current_row = 0
    current_col = 0

    for target_row in [-1, 0, 1]:
        row_images = []
        for target_col in [-1, 0, 1]:
            dx = (target_col - current_col) * step_size
            dy = (target_row - current_row) * step_size

            if dx != 0 or dy != 0:
                drag_from_center(dx, dy)

            img = capture_screen()
            cropped = img[
                overlap if target_row > -1 else 0 : screen_height - (overlap if target_row < 1 else 0),
                side_crop + (overlap if target_col > -1 else 0) : screen_width - side_crop - (overlap if target_col < 1 else 0)
            ]
            row_images.append(cropped)

            current_row = target_row
            current_col = target_col

        grid_images.append(row_images)

    # Flip grid to correct orientation
    corrected_grid = [list(reversed(row)) for row in reversed(grid_images)]
    return corrected_grid

def stitch_by_house_alignment(grid_images, house_template_path):
    house_template = cv2.imread(house_template_path, cv2.IMREAD_GRAYSCALE)
    flat_images = [img for row in grid_images for img in row]
    house_positions = [find_house_position(img, house_template) for img in flat_images]
    ref_x, ref_y = house_positions[4]  # center tile

    # Calculate relative offsets
    offsets = [(ref_x - hx, ref_y - hy) for (hx, hy) in house_positions]

    # Determine placement bounds
    positions = []
    for img, (dx, dy) in zip(flat_images, offsets):
        h, w = img.shape[:2]
        x = dx
        y = dy
        positions.append((x, y, w, h))

    # Compute bounding box
    min_x = min(x for x, _, w, _ in positions)
    min_y = min(y for _, y, _, h in positions)
    max_x = max(x + w for x, _, w, _ in positions)
    max_y = max(y + h for _, y, _, h in positions)

    canvas_w = max_x - min_x
    canvas_h = max_y - min_y
    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    for img, (x, y, w, h) in zip(flat_images, positions):
        canvas_x = x - min_x
        canvas_y = y - min_y
        canvas[canvas_y:canvas_y+h, canvas_x:canvas_x+w] = img

    return canvas

def save_grid_images(grid, output_dir="farm_tiles"):
    # Create or clean the output directory
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(output_dir)

    # Save each tile
    for row_idx, row in enumerate(grid):
        for col_idx, img in enumerate(row):
            filename = f"tile_r{row_idx}_c{col_idx}.png"
            path = os.path.join(output_dir, filename)
            cv2.imwrite(path, img)

    print(f"✅ Saved {len(grid) * len(grid[0])} tiles to '{output_dir}/'")


def load_grid_images(input_dir="farm_tiles", grid_shape=(3, 3)):
    grid = []
    for row_idx in range(grid_shape[0]):
        row = []
        for col_idx in range(grid_shape[1]):
            filename = f"tile_r{row_idx}_c{col_idx}.png"
            path = os.path.join(input_dir, filename)
            if not os.path.exists(path):
                raise FileNotFoundError(f"Missing tile: {path}")
            img = cv2.imread(path)
            row.append(img)
        grid.append(row)
    print(f"✅ Loaded {grid_shape[0] * grid_shape[1]} tiles from '{input_dir}/'")
    return grid


get_images = False
stitch_images = False
find_offsets = True

# 🧪 Run the full pipeline
if __name__ == "__main__":

    house_path = "images/nav/home.jpg"

    if get_images:
        pyautogui.hotkey('alt', 'tab')
        sleep(0.5)
        grid = capture_farm_grid(house_path)
        save_grid_images(grid)
        sleep(0.5)
        pyautogui.hotkey('alt', 'tab')

    if stitch_images:
        grid = load_grid_images()
        stitched = stitch_by_house_alignment(grid, house_path)
        cv2.imwrite("farm_tiles/stitched_farm.png", stitched)
        print("✅ Farm image saved as stitched_farm.png")

    if find_offsets:
        buildings = ["bakery", "bbq_grill"]
        offsets = find_building_offsets("stitched_farm.png", "images/nav/home.jpg", buildings)

        for name in buildings:
            dx, dy = offsets[name]
            print(f"{name}: Δx={dx}, Δy={dy}")