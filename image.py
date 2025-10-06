from utilities import *
from sql import *

print()
print("Create images")


PRODUCTION_ZONE = (574, 604, 600, 250)
centre = int(screen_width / 2), int(screen_height / 2)
south_west_position = (1388, 252)
south_east_position = (200, 300)
east_position = (200, 800)
center_position = (1000, 560)
north_west_position = (1700, 700)
north_east_position = (200, 700)
all_positions = [south_west_position, south_east_position, east_position, north_west_position, center_position, north_east_position]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


confidence = 0.8
full_screen_region = (0, 0, pyautogui.size().width, pyautogui.size().height)

reference_images = []

class Image:
    def __init__(self, file_locations, name=None, reference_point=None):
        if type(file_locations) != list:
            file_locations = [file_locations]
        if not name: name = file_locations[0]
        self.name = name
        self.file_locations = file_locations
        self.loaded_images = {file: self.load_image(file) for file in self.file_locations}
        self.image = self.load_image(file_locations[0])
        self.reference_point = reference_point
        if reference_point:
            reference_images.append(self)
            self.relative_location = string_to_tuple(db_load(self.name))
            # print("Made relative location:", self.name)

    def __str__(self):
        return self.name

    def load_image(self, file_path):
        try:
            # print("Load image:", os.path.join(BASE_DIR, file_path))
            image = cv2.imread(os.path.join(BASE_DIR, file_path), cv2.IMREAD_COLOR)

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

    def move_to_center(self):
        result = self.image.find()
        if result:
            drag(result, centre, speed=1)
        else:
            if self.reference_point:
                move_home_to_center()
                drag(self.relative_location, centre)
                print("Couldn't find image")

    def find(self, confidence=confidence, region=full_screen_region, use_implied=True):
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
                # if best_confidence < confidence:
                #     print("Image confidence:", self, file, best_confidence, confidence)
            except: pass
            # except Exception as e:
            #     print(f"Did not find: '{file}'")
        use_implied = False
        if not best_match and use_implied and self.reference_point:
            home_loc = i_home.find()
            if home_loc:
                best_match = add(home_loc, self.relative_location)
                print("Using implied", self.name, best_match)

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


# Nav
dir = os.path.join(BASE_DIR, "images/nav/")

i_bluestacks_icon = Image([dir + "bluestacks_icon.jpg", dir + "green_grass.jpg", dir + "road_grass.jpg"])
i_pycharm_icon = Image([dir + "pycharm_icon.jpg"])
i_hay_day_start_icon = Image(["images/nav/hey_day_start_icon.jpg"], name="Hay Day Start Icon")
i_home = Image([dir + "home.jpg"])
i_zoomed_in_house = Image(['images/nav/zoomed_in_house.jpg'], name="Zoomed in house")
i_gnome = Image(["images/nav/gnome.jpg"], name="Gnome", reference_point=True)
i_end_of_path = Image("images/nav/end_of_path.jpg", name="End of path", reference_point=True)
# i_worm = Image(["images/nav/worm.jpg"], name="Worm", reference_point=True)
i_go_home = Image(["images/nav/go_home.jpg"], name="Go home")
i_lady_bug = Image(["images/nav/lady_bug.jpg"])

# Restart
i_bluestacks_cross = Image(["images/restart/bluestacks_cross.jpg"])
i_heyday_icon_small = Image(["images/restart/heyday_icon_small.jpg"])
i_full_screen = Image(["images/restart/full_screen.jpg"])
i_bluestacks_toolbar_icon = Image("images/restart/bluestacks_toolbar_icon.jpg")
i_house_small = Image("images/restart/house_small.jpg")
i_ld_player_not_max = Image("images/restart/ld_player_not_max.jpg")
i_oink = Image("images/nav/oink.jpg")

# Crosses
i_home_cross = Image([dir + "house_cross.jpg"])
i_silo_full_cross = Image([dir + "silo_full_cross.jpg"])
i_farm_pass_cross = Image([dir + "farm_pass_cross.jpg"])
i_event_board_cross = Image(["images/nav/event_board_cross.jpg"])
i_country_fair_cross = Image("images/nav/country_fair_cross.jpg")
i_silo_full = Image("images/fields/silo_full.jpg")

# Menu
i_first_page = Image(["images/nav/first_page.jpg", ], name="First Page")
i_second_page = Image(["images/nav/second_page.jpg",], name="Second Page")
i_third_page = Image(["images/nav/third_page.jpg"], name="Second Page")
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
i_field_marker = Image(["images/fields/field_marker.jpg", "images/fields/field_marker_2.jpg", "images/fields/field_marker_3.jpg", "images/fields/field_marker_4.jpg"], name="Field marker", reference_point=True)
i_feed_mill_marker = Image(["images/nav/gnome.jpg"], name="Feed Mill marker")
i_chicken_marker = Image(["images/nav/chicken_tree.jpg", "images/nav/chicken_tree_2.jpg", "images/nav/chicken_tree_3.jpg"], name="Chicken marker", reference_point=True)
i_chicken_basket = Image(["images/production/chicken_basket.jpg", "images/production/chicken_basket_2.jpg"], name="Chicken basket")
i_not_enough_resources_cross = Image(["images/production/not_enough_resources_cross.jpg"], name="not_enough_resources_cross")
i_last_crop_cross = Image(["images/production/last_crop_cross.jpg"], name="Last crop cross")

# Help markers
i_help_marker = Image(["images/nav/help_marker.jpg", "images/nav/help_marker_2.jpg"])

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
i_create_advertisement_pre = Image(["images/sales/create_advertisement_pre.jpg"], name="Create advertisement (pre)")
i_roadside_shop = Image(["images/nav/roadside_shop.jpg"], name="Roadside shop")
i_advertise_now = Image(["images/sales/advertise_now.jpg"])

# Collect
i_milk_collect = Image(["images/collect/milk.jpg", "images/collect/milk_2.jpg"])
i_eggs_collect = Image(["images/collect/eggs.jpg", "images/collect/eggs_2.jpg"])
i_bacon_collect = Image(["images/collect/bacon.jpg"])
i_wool_collect = Image(["images/collect/wool.jpg"])

# Bees
i_beehive = Image(["images/bees/beehive.jpg"], name="Beehive", reference_point=True)
i_beehive_collect = Image(["images/bees/beehive_collect.jpg"])

# Truck
i_truck = Image(["images/truck/truck.jpg", "images/truck/order_board.jpg"], name="Truck", reference_point=True)
i_truck_tick = Image(["images/truck/truck_tick.jpg"])
i_truck_cross = Image(["images/truck/truck_cross.jpg"])
i_orders = Image(["images/truck/orders.jpg"])

# Fishery
i_boat = Image(["images/fishery/boat_1.jpg"], name="Boat", reference_point=True)
i_fish_cabin_close = Image("images/fishery/fish_cabin_close.jpg")
i_fish_cabin = Image("images/fishery/fish_cabin.jpg")
i_fishery_rock = Image(["images/nav/fishery_rock.jpg"])
i_lobster_pool = Image(["images/fishery/lobster_pool.jpg"])
i_lobster_net = Image(["images/fishery/lobster_net.jpg"])
i_caught_lobster = Image(["images/fishery/caught_lobster.jpg"])
i_mushrooms = Image(["images/fishery/mushrooms.jpg"])
i_log = Image(["images/fishery/log.jpg"])

def clear_help_markers():
    home_position = i_home.find()
    if not home_position: return
    for position in all_positions:
        drag(home_position, position, speed=0.3)
        while i_help_marker.click(): sleep(0.1)
        drag(position, home_position, speed=0.3)

def set_relative_locations(replace=True):
    home_position = i_home.find()
    if not home_position: return
    for position in [south_east_position, south_west_position, north_west_position]:
        drag(home_position, position, speed=0.3)
        sleep(0.5)
        set_relative_locations_screen(position, replace=replace)
        drag(position, home_position, speed=0.3)

def set_relative_locations_screen(position=None, replace=True):
    home_position = i_home.find()
    if not home_position:
        print("Couldn't find home:", position)
        move_home_to_center()
        home_position = i_home.find()
        if not home_position:
            print("Couldn't find home (again):", position)
            return
    for image in reference_images:
        if image.relative_location and not replace:
            print(f"Not setting relative location: {image}, Already set: {image.relative_location}")
        if not image.relative_location or replace:
            result = image.find(use_implied=False)
            if result:
                image.relative_location = difference(home_position, result)
                relative_location_string = f"{image.relative_location}"
                print(f"Setting relative location: {image}, {relative_location_string}. Home: {home_position} vs {result}")
                db_save(image.name, relative_location_string)
            home_position = i_home.find()


def move_home_to_center():
    found = False
    i_help_marker.click()
    if i_hay_day_start_icon.find():
        found = wait_for_images(images_to_click=[i_hay_day_start_icon], destination_image=i_house_small, time_seconds=120)
        if found:
            sleep(1)
            position = i_house_small.find()
            pyautogui.moveTo(add(position, (100, 0)))
        pyautogui.press("f11")
        zoom()
        return

    if i_ld_player_not_max.find():
        pyautogui.press("f11")
        zoom()

    for image in reference_images:
        # print(image, image.relative_location, not found)
        if image.relative_location and not found:
            actual = image.find()
            if actual:
                desired = add(centre, image.relative_location)
                print("Moving:", image, image.relative_location, actual, desired)
                drag(actual, desired, speed=0.5)
                found = True
            else:
                print("Moving (couldn't see):", image, image.relative_location)

    if not found:
        print("Move to centre - found nothing")
        i_go_home.click()
        i_country_fair_cross.click()
        i_oink.click()
        sleep(10)
        zoom()



    return found

