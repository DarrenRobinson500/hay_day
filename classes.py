from image import *
from num import *
from sql import *
import random


MENU_REGION = (0, 0, 1100, 900)
# chicken_position = (828, 374)
# cow_position = (1114, 580)

PRODUCTION_ZONE_A = (665, 651, 350, 200)
PRODUCTION_ZONE_B = (750, 604, 650, 250)

items = []
production_units = []
jobs = []


class Production:
    def __init__(self, name, count, image=None, location=None, clear_zone=None):
        self.name = name
        self.count = count
        production_units.append(self)
        self.location = location
        self.clear_zone = clear_zone
        if image:
            self.image = image
        else:
            self.add_images()
        self.coords_function = None
    def __str__(self):
        return self.name
    def click(self):
        self.image.click()
    def items(self):
        own_items = []
        for item in items:
            if item.production == self:
                own_items.append(item)
        return own_items

    def print_count(self):
        text = self.name + ":"
        made_any = False
        for item in self.items():
            if item.number_made > 0:
                text += f"{item}: {item.number_made} "
                made_any = True
        if made_any:
            print(text)

    def add_images(self):
        # Own Image
        dir = "images/production/"
        file = [f"{dir}{self.name.lower()}.jpg"]
        if self.name == "Lure_workbench":
            self.image = Image(file, name=self.name)
        else:
            self.image = Image(file, name=self.name, reference_point=True)

    def best_use(self, items):
        print()
        print(self, "Count:", self.count)
        best_item = None
        best_value_added_per_hour = 0
        for item in items:
            if item.production == self:
                print(item, int(item.value_added_per_hour() * 16 * self.count))
                if item.value_added_per_hour() > best_value_added_per_hour:
                    best_value_added_per_hour = item.value_added_per_hour()
                    best_item = item
        return best_item, best_value_added_per_hour

    def remaining(self):
        # Must be on the selected production unit to work
        remaining_dict = {}
        # coord = self.coords_function(0)
        # pyautogui.click(coord)
        sleep(0.5)
        for item in self.items():
            item_remaining = item.remaining()
            # print(f"Remaining {item}: {item_remaining}")
            remaining_dict[item] = item_remaining
        return remaining_dict

    def get_random(self):
        # Must be on the selected production unit to work
        if self == feed_mill:
            random_feed = self.get_random_feed()
            # print("Get random feedmill", random_feed)
            return self.items()[random_feed]
        remaining_dict = self.remaining()
        fruits = list(remaining_dict.keys())
        weights = list(remaining_dict.values())
        try:
            return random.choices(fruits, weights=weights, k=1)[0]
        except:
            print("All goods made")
            return None

    def get_random_feed(self):
        animals = [0,1,2,3,4]
        weights = [10, 6, 2, 2, 1]
        return random.choices(animals, weights=weights, k=1)[0]


class Item:
    def __init__(self, name, creation_time=0, price=0, production=None, ingredients=None, min_no=2, max_no=20, menu_page=1):
        self.name = name
        self.creation_time = creation_time
        self.price = price
        self.production = production
        self.location = production.location
        self.ingredients = ingredients if ingredients else {}
        self.min_no = min_no
        self.max_no = max_no
        self.menu_page = menu_page
        self.current_number = 0
        self.current_number_time = datetime.now()
        self.add_images()
        self.number_made = 0
        self.tab = i_barn_tab
        if self.production == field: self.tab = i_silo_tab

        items.append(self)
    def __str__(self):
        # ingredients_str = ', '.join([f"{qty:.0f}x{ing.name}" for ing, qty in self.ingredients.items()])
        return self.name
        # return f"{self.name} (Creation Time: {self.creation_time:.0f} mins, Price: {self.price} Ingredients: {ingredients_str if ingredients_str else 'None'})"
    def add_images(self):
        self.image_ready = None

        # Menu
        dir = "images/menu/"
        file = [f"{dir}{self.name.lower()}.jpg"]
        # print(f"New item: {self.name}. Menu item file: {file}")
        if self.production not in [chickens, cows, sheep, pigs, bees]:
            self.image_menu = Image(file)

            image = self.image_menu.image
            height, width = image.shape[:2]
            new_width = int(width * 0.92)
            new_height = int(height * 0.92)
            resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            mini_path = f"images/menu_mini_1/{self.name}.jpg"
            cv2.imwrite(mini_path, resized_image)
            self.image_menu_mini_1 = Image([mini_path])

            image = self.image_menu.image
            height, width = image.shape[:2]
            new_width = int(width * 0.8)
            new_height = int(height * 0.8)
            resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            mini_path = f"images/menu_mini_2/{self.name}.jpg"
            cv2.imwrite(mini_path, resized_image)
            self.image_menu_mini_2 = Image([mini_path])


        # Market
        dir = "images/sales/"
        file = [f"{dir}{self.name.lower()}.jpg"]
        # print("Item creation:", file)
        if os.path.isfile(file[0]):
            self.image_market = Image(file)

        # Ready
        # if self.production.name == "Field":
        #     dir = "images/ready/"
        #     files = find_files_with_word(directory=dir, word=self.name)
        #     self.image_ready = Image(files)
    def show(self, dur=500):
        self.image_menu.show(dur)
        self.image_ready.show(dur)

    def set(self, min, max):
        self.min = min
        self.max = max
    def value(self):
        return int(self.price / self.creation_time * 60)
    def value_text(self):
        return f"{self.value()}cph x {self.production.count}"
    def value_added(self):
        input_cost = 0
        for ingredient, qty in self.ingredients.items():
            input_cost += ingredient.price * qty
        value_added = self.price - input_cost
        return value_added
    def value_added_per_hour(self):
        return self.value_added() / self.creation_time * 60

    def total_time(self):
        total_time = self.creation_time
        for ingredient, qty in self.ingredients.items():
            total_time += ingredient.total_time() * qty
        return total_time
    def time_dictionary(self, time_dict=None):
        if time_dict is None: time_dict = {}

        # Add this item's production time to its respective production place
        time_dict[self.production] = time_dict.get(self.production, 0) + self.creation_time

        # Recursively add ingredient production times
        for ingredient, qty in self.ingredients.items():
            ingredient.time_dictionary(time_dict)

        # for place, time in time_dict.items():
        #     print()
        #     print(f"{place}: {time} mins")

        return time_dict

    def total_clicks(self):
        total_clicks = 1
        for ingredient, qty in self.ingredients.items():
            total_clicks += ingredient.total_clicks() * qty
        return total_clicks

    def count(self, forced=False):
        if datetime.now() < self.current_number_time and not forced:
            return self.current_number
        if i_second_page.find() and self.menu_page == 1:
            # print("Second page found")
            i_back_arrows.click()
            sleep(0.3)
        if i_first_page.find() and self.menu_page == 2:
            # print("First page found")
            i_forward_arrows.click()
            sleep(0.3)
        if not self.image_menu.find():
            print(f"Item Count. Could not find {self.image_menu}")
            return self.current_number
        menu = pyautogui.screenshot(region=MENU_REGION)
        menu.save("images/screen/temp.jpg")
        menu_image = cv2.imread("images/screen/temp.jpg", cv2.IMREAD_COLOR)
        # show(menu_image)
        region = extract_region(self.image_menu.image, menu_image, -170, -150, 120, 150)
        if region is not None:
            cv2.imwrite("images/screen/temp_number_region.jpg", region)
        count = menu_numbers.read(region)
        if not count: count = 0
        if self.image_menu_mini_1.find(region=PRODUCTION_ZONE_A): count += 1
        if self.image_menu_mini_2.find(region=PRODUCTION_ZONE_B): count += 1
        self.current_number = count
        self.current_number_time = datetime.now() + timedelta(minutes=180 + self.creation_time)
        return count

    def remaining(self):
        return max(self.min_no - self.count(), 0)

class Loc:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.coords = db_load(name)

    def __str__(self):
        return str(self.image)

    def find(self):
        return self.image.find()

class Animal_Data:
    def __init__(self, production, position, feed, image_marker_1, squares_x_1, squares_y_1, image_marker_2, squares_x_2, squares_y_2, squares_width, squares_height, fine_tune_x, fine_tune_y, image_marker_3):
        self.production = production
        self.position = position
        self.feed = feed
        self.image_marker_1 = image_marker_1
        self.squares_x_1 = squares_x_1
        self.squares_y_1 = squares_y_1
        self.image_marker_2 = image_marker_2
        self.squares_x_2 = squares_x_2
        self.squares_y_2 = squares_y_2
        self.squares_width = squares_width
        self.squares_height = squares_height
        self.fine_tune_x = fine_tune_x
        self.fine_tune_y = fine_tune_y
        self.image_marker_3 = image_marker_3

    def __str__(self):
        return f"Animal Data: {self.production}"

    def collect_and_feed(self):
        # Select animals
        marker_1 = self.image_marker_1.find()
        if not marker_1:
            print("Collect and Feed. Couldn't find marker 1 for:", self)
            return
        #  Click on chickens, cows etc
        pyautogui.click(coords(marker_1, self.squares_x_1, self.squares_y_1))
        sleep(1)
        # Collect
        marker_2 = self.image_marker_2.find()
        collection_active = find_image_and_check_color(self.image_marker_2.image)
        if marker_2 and collection_active:
            print("Collect and Feed. Collecting:", self)
            pos_left = coords(marker_2, -4, 4)
            haze(pos_0=marker_2, pos_left=pos_left, width=self.squares_width, height=self.squares_height)
        if not marker_2:
            print("Collect and Feed. Couldn't find marker 2 for:", self, self.image_marker_2)
        if not collection_active:
            print("Collect and Feed. Colection not active:", self)

        # Feed
        marker_3 = self.image_marker_3.find()
        feed_count = self.feed.count()
        if marker_3 and feed_count > 0:
            pos_left = coords(marker_3, -6, 5)
            haze(pos_0=marker_3, pos_left=pos_left, width=self.squares_width, height=self.squares_height)
        if not marker_3:
            print("Collect and Feed. Couldn't find marker 3 for:", self, self.image_marker_3)
        if feed_count == 0:
            print("Collect and Feed. No feed for:", self)

# Images
dir = "images/production/"
i_feed_mill = Image([dir + "feed_mill.jpg"])
i_chickens = Image([dir + "chickens.jpg"])
i_cows = Image([dir + "cows.jpg"])
i_pigs = Image([dir + "pigs.jpg"])
# i_dairy = Image([dir + "dairy.jpg"])
# i_sugar_mill = Image([dir + "sugar_mill.jpg"])
# i_bakery = Image([dir + "bakery.jpg"])

# Production Locations
l_feed_mill = Loc("Feed mill", i_feed_mill)
l_chickens = Loc("Chickens", i_chickens)
l_pigs = Loc("Pigs", i_pigs)
# l_dairy = Loc("Dairy", i_dairy)
# l_lure_workbench = Loc("Fishery", i_lure_workbench)

dir = "images/production/"
i_field = Image([dir + "field.jpg", dir + "field_2.jpg"], name="Field")
l_field = Loc("Field", i_field)

print()
print("Create production")

# Fields
field = Production("Field", 30, image=i_field, location=south_west_position)
# Animals
feed_mill = Production("Feed mill", 2, image=i_feed_mill, location=south_west_position)
chickens = Production("Chickens", 18, image=i_chickens, location=center_position)
cows = Production("Cows", 15, image=i_cows, location=center_position)
pigs = Production("Pigs", 10, image=i_chickens, location=north_west_position)
sheep = Production("Sheep", 10, image=i_chickens, location=north_west_position)
goats = Production("Goats", 8, image=i_chickens, location=north_west_position)
bees = Production("Bees", 1, image=i_beehive, location=north_west_position)
# Production
dairy = Production("Dairy", 1, location=south_east_position, clear_zone=(1148, 535))
sugar_mill = Production("Sugar_mill", 2, location=south_east_position)
bakery = Production("Bakery", 2, location=south_east_position, clear_zone=(983, 546))
bbq_grill = Production("BBQ_Grill", 1, location=south_east_position, clear_zone=(1054, 526))
icecream_maker = Production("Icecream_maker", 1, location=south_east_position)
pie_oven = Production("Pie_oven", 1, location=east_position, clear_zone=(1148, 976))
cake_oven = Production("Cake_oven", 1, location=east_position, clear_zone=(1098, 567))
loom = Production("Loom", 1, location=east_position, clear_zone=(599, 1021))
honey_extractor = Production("Honey_extractor", 1, location=south_east_position)
jam_maker = Production("Jam_maker", 1, location=south_east_position)
juice_press = Production("Juice_press", 1, location=center_position)

lure_workbench = Production("Lure_workbench", 1, location=north_west_position)
net_maker = Production("Net_maker", 1, location=north_west_position)

for image in reference_images: print(image, image.relative_location)

