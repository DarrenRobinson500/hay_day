from utilities import *

PRODUCTION_ZONE = (574, 604, 600, 250)
centre = 1920 / 2, 1080 / 2
confidence = 0.8
full_screen_region = (0, 0, pyautogui.size().width, pyautogui.size().height)

class Image:
    def __init__(self, file_locations, name=None):
        if not name: name = file_locations[0]
        self.name = name
        self.file_locations = file_locations
        self.loaded_images = {file: self.load_image(file) for file in self.file_locations}
        self.image = self.load_image(file_locations[0])

    def __str__(self):
        return self.file_locations[0]

    def load_image(self, file_path):
        try:
            image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            if image is None:
                print(f"Error: Could not load '{file_path}'.")
            return image
        except Exception as e:
            print(f"Error loading image '{file_path}': {e}")
            return None

    def show(self, dur=500):
        for file, image in self.loaded_images.items():
            show(image, file, dur)

    # def image(self):
    #     next(iter(self.loaded_images.items()))

    def find(self, confidence=confidence, region=full_screen_region):
        best_match = None
        best_confidence = 0

        for file, image in self.loaded_images.items():
            if image is None:
                continue  # Skip if the image couldn't be loaded

            try:
                for x in range(3):
                    location = pyautogui.locateCenterOnScreen(file, confidence=confidence, region=region)
                    if location:
                        match_confidence = confidence
                        if match_confidence > best_confidence:
                            best_match = (int(location.x), int(location.y))
                            best_confidence = match_confidence
                    # print("Image confidence:", self, best_confidence, confidence)
                if best_confidence < confidence:
                    print("Image confidence:", self, best_confidence, confidence)
            except: pass
            # except Exception as e:
            #     print(f"Did not find: '{file}'")

        return best_match

    # def find_all_old(self, confidence=confidence):
    #     all_matches = []
    #     for file, image in self.loaded_images.items():
    #         if image is None: continue
    #
    #         try:
    #             locations = list(pyautogui.locateAllOnScreen(file, confidence=confidence))
    #             for loc in locations:
    #                 center_x = int(loc.left + loc.width // 2)
    #                 center_y = int(loc.top + loc.height // 2)
    #                 all_matches.append((center_x, center_y))
    #         except Exception as e:
    #             print(f"Did not find '{file}': {e}")
    #     return all_matches
    #
    def find_all(self, confidence=confidence):
        all_matches = []
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        for file, image in self.loaded_images.items():
            if image is None: continue

            # Convert images to grayscale
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Template matching
            result = cv2.matchTemplate(screenshot, image, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= confidence)

            # Store detected positions
            detected_points = list(zip(locations[1], locations[0]))  # (x, y) coordinates

            # Filter out close detections
            min_distance = 20
            filtered_points = []
            for point in detected_points:
                if all(np.linalg.norm(np.array(point) - np.array(existing)) > min_distance for existing in all_matches):
                    all_matches.append(point)

        return all_matches

    def click(self, confidence=confidence):
        position = self.find(confidence)

        if position:
            pyautogui.click(position)
            # print(f"Clicked on {self} image at {position}")
            return position
        else:
            # print("Image not found. No click performed.")
            return False

    # def move_to_centre(self, confidence=confidence, duration=0.25):
    #     position = self.find(confidence)
    #
    #     if position:
    #         pyautogui.moveTo(position)
    #         pyautogui.mouseDown()
    #         pyautogui.moveTo(centre[0], centre[1], duration=duration)
    #         pyautogui.mouseUp()
    #         return True
    #     else:
    #         print("Image not found. No drag performed.")
    #         return False

    def food_drag(self, field_coord, confidence=confidence, duration=1):
        position = self.find(confidence)

        if position:
            pyautogui.moveTo(position)
            pyautogui.mouseDown()
            pyautogui.moveTo(field_coord[0], field_coord[1], duration=duration)
            pyautogui.moveRel(320, 160, duration=duration)
            pyautogui.mouseUp()
            return True
        else:
            print("Image not found. No drag performed.")
            return False

# Nav
dir = "images/nav/"
i_bluestacks_icon = Image([dir + "bluestacks_icon.jpg", dir + "green_grass.jpg", dir + "road_grass.jpg"])
i_pycharm_icon = Image([dir + "pycharm_icon.jpg"])
i_hay_day_start_icon = Image(["images/nav/hey_day_start_icon.jpg"], name="Hay Day Start Icon")
i_home = Image([dir + "home.jpg"])
i_zoomed_in_house = Image(['images/nav/zoomed_in_house.jpg'], name="Zoomed in house")
i_road = Image(["images/nav/road.jpg"], name="Road")
i_gnome = Image(["images/nav/gnome.jpg"], name="Gnome")
i_worm = Image(["images/nav/worm.jpg"], name="Worm")

# Crosses
i_home_cross = Image([dir + "house_cross.jpg"])
i_silo_full_cross = Image([dir + "silo_full_cross.jpg"])
i_farm_pass_cross = Image([dir + "farm_pass_cross.jpg"])
i_event_board_cross = Image(["images/nav/event_board_cross.jpg"])

# Menu
i_first_page = Image(["images/nav/first_page.jpg"], name="First Page")
i_second_page = Image(["images/nav/second_page.jpg"], name="Second Page")
i_back_arrows = Image(["images/nav/back_arrows.jpg"], name="Back Arrows")
i_forward_arrows = Image(["images/nav/forward_arrows.jpg"], name="Forward Arrows")

# Market
i_barn = Image(["images/sales/barn.jpg"], name="Barn")
i_silo_tab = Image(["images/sales/silo_tab.jpg"], name="Silo tab")
i_barn_tab = Image(["images/sales/barn_tab.jpg"], name="Barn tab")

# Warnings
i_reload = Image(['images/warnings/reload.jpg'], name="Reload")
i_try_again = Image(['images/warnings/try_again.jpg'], name="Try again")
i_continue = Image(['images/warnings/level_up_continue.jpg'], name="Try again")

# Misc
dir = "images/fields/"
i_scythe = Image([dir + "scythe.jpg"])
i_field_marker = Image(["images/fields/field_marker.jpg"], name="Field marker")
i_feed_mill_marker = Image(["images/nav/gnome.jpg"], name="Feed Mill marker")
i_chicken_marker = Image(["images/nav/chicken_tree.jpg", "images/nav/chicken_tree_2.jpg", "images/nav/chicken_tree_3.jpg"], name="Chicken marker")
i_chicken_basket = Image(["images/production/chicken_basket.jpg", "images/production/chicken_basket_2.jpg"], name="Chicken basket")
i_not_enough_resources_cross = Image(["images/production/not_enough_resources_cross.jpg"], name="not_enough_resources_cross")
i_last_crop_cross = Image(["images/production/last_crop_cross.jpg"], name="Last crop cross")

# Production
i_production_slot = Image(["images/production/empty_1.jpg", "images/production/empty_2.jpg", "images/production/empty_3.jpg"])

# Sales
i_market = Image(["images/nav/market.jpg","images/nav/market_2.jpg"], name="Market")
i_new_sale = Image(["images/sales/new_sale.jpg"], name="New sale")
i_max_price = Image(["images/sales/max_price.jpg"], name="Max price")
i_put_on_sale = Image(["images/sales/put_on_sale.jpg"], name="Put on sale")
i_market_cross = Image(["images/sales/market_cross.jpg"], name="Market cross")
i_market_cross_2 = Image(["images/sales/market_cross_2.jpg"], name="Market cross 2")
i_sold = Image(["images/sales/sold.jpg"], name="Sold")
i_existing_sale_box = Image(["images/sales/existing_sale_box.jpg"], name="Existing sale box")
i_create_advertisement = Image(["images/sales/create_advertisement.jpg"], name="Create advertisement")
i_roadside_shop = Image(["images/nav/roadside_shop.jpg"], name="Roadside shop")
i_advertise_now = Image(["images/sales/advertise_now.jpg"])

# Collect
i_milk_collect = Image(["images/collect/milk.jpg", "images/collect/milk_2.jpg"])
i_eggs_collect = Image(["images/collect/eggs.jpg", "images/collect/eggs_2.jpg"])

# Bees
i_beehive = Image(["images/bees/beehive.jpg", "images/bees/beehive_2.jpg", "images/bees/beehive_3.jpg"])
i_beehive_collect = Image(["images/bees/beehive_collect.jpg"])

# Truck
i_truck = Image(["images/truck/truck.jpg"])
i_truck_tick = Image(["images/truck/truck_tick.jpg"])
i_truck_cross = Image(["images/truck/truck_cross.jpg"])