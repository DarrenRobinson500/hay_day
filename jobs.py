from animals import *
from feed_mill import *


class Job:
    def __init__(self, name, function, reset_time, item=None, production=None, production_no=None, items=None):
        self.name = name
        self.function = function
        self.item = item
        self.production = production
        self.items = items
        if item:
            self.production = item.production
        self.production_no = production_no
        self.reset_time = reset_time
        self.runtime = datetime.now() + timedelta(minutes=len(jobs) * 0.25)
        jobs.append(self)

    def __str__(self):
        return self.name

    def run(self):
        print("Running:", self)
        if self.production:
            move_to(self.production)
            sleep(1.5)
        if self == j_truck:
            move_to_center()
            sleep(1.5)
        self.function(self)
        self.runtime = datetime.now() + timedelta(minutes=self.reset_time)
        # clear()
        sleep(1)
        # move_to_center()
        # sleep(1)

    def wait_time(self):
        return int((self.runtime - datetime.now()).total_seconds())

def run_job():
    clear()
    next_job = min(jobs, key=lambda job: job.runtime)
    time_to_wait = int((next_job.runtime - datetime.now()).total_seconds())
    if time_to_wait < 1:
        next_job.run()
        next_job = min(jobs, key=lambda job: job.runtime)
        time_to_wait = int((next_job.runtime - datetime.now()).total_seconds())
    return time_to_wait

def print_jobs():
    sorted_jobs = sorted(jobs, key=lambda job: job.runtime)
    print("\nUpcoming Jobs")
    for job in sorted_jobs:
        if job.name == "Field":
            print(f" - {int(job.wait_time()/60)}min: {job.item} ")
        else:
            print(f" - {int(job.wait_time()/60)}min: {job} ")

def run_jobs():
    while True:
        wait_time = run_job()
        if wait_time > 60:
            # print("Waiting:", wait_time, "seconds")
            sleep(2)
            pyautogui.hotkey('alt', 'tab')
            print_jobs()
            sleep(wait_time)
            pyautogui.hotkey('alt', 'tab')
        elif wait_time > 1:
            print("Waiting:", wait_time, "seconds")
            sleep(wait_time)

ORDER_REGION = (200, 200, 900, 850)

def truck(job):
    if not i_truck.find():
        print("Couldn't find the truck")
        return
    i_truck.click()
    sleep(2)
    order = i_truck_tick.find(region=ORDER_REGION)
    while order:
        i_truck_tick.click()
        pyautogui.click(order)
        sleep(0.3)
        pyautogui.click(1603, 922)
        found_truck = False
        while not found_truck:
            sleep(0.1)
            found_truck = i_truck.find()
        sleep(0.3)
        pyautogui.click(found_truck)
        sleep(2)
        pyautogui.click(found_truck)
        sleep(2)
        order = i_truck_tick.find(region=ORDER_REGION)
    i_truck_cross.click()

def start_production_field(job):
    field_length = 6
    row = job.production_no
    coord = job.item.production.coords_function(job.production_no)
    if not coord:
        find_yourself(job)
        sleep(0.5)
        coord = job.item.production.coords_function(job.production_no)
    if coord:
        pyautogui.click(coord)
        sleep(0.3)
        # Collect if ready
        if i_scythe.find():
            position_0 = i_scythe.find()
            position_1 = field_coords(row)
            # position_half = coords(position_1, 0.5, -1)
            if position_1:
                position_2 = add(position_1, [gap_x * field_length, -gap_y * field_length])
                if position_0 and position_1 and position_2:
                    drag_many([position_0, position_1, position_2], 0.85)
                    sleep(4.5)
                    pyautogui.click(field_coords(row))
                    sleep(0.3)
        # Plant
        if i_second_page.find():
            print("Second page found")
            i_back_arrows.click()

        if job.item.image_menu.find():
            sleep(0.3)
            field_coord_start = field_coords(row)
            print(f"Plant {job.item}")
            menu_coord = job.item.image_menu.find(confidence=0.87)

            if field_coord_start and menu_coord:
                field_coord_end = add(field_coord_start, [gap_x * field_length, -gap_y * field_length])
                drag_many([menu_coord, field_coord_start, field_coord_end], duration=0.85)
                sleep(2.0)

    sleep(0.3)

def start_production_feed_mill(job):
    # Clear produced goods
    opened, count = False, 0
    while not opened and count < 4:
        coord = job.production.coords_function(job.production_no)
        if not coord:
            find_yourself(job)
            sleep(0.5)
            coord = job.production.coords_function(job.production_no)
        if coord:
            pyautogui.click(coord)
        sleep(0.5)
        if chicken_feed.image_menu.find():
            opened = True
        count += 1
        sleep(0.3)
    # Load up production slots
    if opened:
        mill_is_full = False
        count = 0
        production_slot = i_production_slot.find()
        print("Production slot (pre):", production_slot)
        while production_slot and count < 4 and not mill_is_full:
            count += 1
            if chicken_feed.image_menu.find() and production_slot:
                item = feed_mill.get_random()
                print("Produce:", item)
                a = item.image_menu.find()
                if a and production_slot:
                    drag(a, production_slot)
                if i_not_enough_resources_cross.find():
                    print("Clicking not enough resources cross")
                    i_not_enough_resources_cross.click()
                if i_last_crop_cross.find():
                    print("Clicking last crop cross")
                    i_last_crop_cross.click()
            sleep(0.7)
            production_slot = i_production_slot.find()
            print("Production slot (loop):", production_slot)
        if not production_slot:
            print(f"Mill: {job.production_no} is full.")
    drag((400, 2000), (100, 1000))
    sleep(2)

def find_yourself(job):
    found = i_home.find()
    if not found and i_dairy.find():
        print("i_dairy found - dragging")
        drag(i_dairy.find(), (1383, 754))
        sleep(0.3)
        found = i_home.find()
    if not found and i_gnome.find():
        print("i_gnome found = dragging")
        drag(i_gnome.find(), (240, 600))
        sleep(0.3)
        found = i_home.find()
    if not found and i_field_marker.find():
        print("i_gnome found = dragging")
        drag(i_gnome.find(), (240, 900))
        sleep(0.3)
        found = i_home.find()
    if i_home.find():
        move_to(job.production)
        sleep(0.3)
    sleep(0.3)

def feed_animals(job):
    if job.item == eggs:
        sleep(0.3)
        if not chicken_data.image_marker_1.find():
            find_yourself(job)
        if chicken_data.image_marker_1.find():
            chicken_data.collect_and_feed()
            for x in [i_gnome, i_field_marker, i_chicken_marker]:
                if x.find(confidence=0.85): x.click()
    if job.item == milk:
        if not cow_data.image_marker_1.find():
            find_yourself(job)
        if cow_data.image_marker_1.find():
            cow_data.collect_and_feed()
            for x in [i_gnome, i_field_marker, i_chicken_marker]:
                if x.find(confidence=0.85): x.click()
        else:
            print("Cow data image marker not found")

def start_production_machine(job):
    move_to(job.production)
    sleep(2)
    # Get an image of a production item
    test_image = job.production.items()[0].image_menu
    # Clear produced goods
    opened, count = False, 0
    while not opened and count < 4:
        coord = job.production.image.find()
        if coord:
            pyautogui.click(coord)
            sleep(2)
            if test_image.find():
                opened = True
        count += 1
        sleep(0.3)
    # Load up production slots
    slots_are_full = False
    count = 0
    production_slot = i_production_slot.find()
    print("Production slot (pre):", production_slot)
    while production_slot and count < 4 and not slots_are_full:
        count += 1
        if i_second_page.find():
            i_back_arrows.click()
            sleep(0.3)
        if test_image.find() and production_slot:
            item = job.production.get_random()
            if item:
                if i_second_page.find() and item.menu_page == 1:
                    i_back_arrows.click()
                    sleep(0.3)
                if i_first_page.find() and item.menu_page == 2:
                    i_forward_arrows.click()
                    sleep(0.3)
                print(f"Produce in {job.production}:", item)
                a = item.image_menu.find()
                if a and production_slot:
                    drag(a, production_slot)
                if i_not_enough_resources_cross.find():
                    print("Clicking not enough resources cross")
                    i_not_enough_resources_cross.click()
                if i_last_crop_cross.find():
                    print("Clicking last crop cross")
                    i_last_crop_cross.click()
            else:
                count = 5
        sleep(0.7)
        production_slot = i_production_slot.find()
        print("Production slot (loop):", production_slot)
    if not production_slot:
        print(f"{job.production}: is full.")
    if job.production == bbq_grill:
        pyautogui.click(818, 1178)
    elif job.production == dairy:
        pyautogui.click(518, 878)
    elif job.production == loom:
        pyautogui.click(504, 1014)
    else:
        pyautogui.click(1118, 878)
    # drag((400, 2000), (300, 1000))
    sleep(2)

def collect_honey(job):
    print("Collecting Honey")
    confidence = 0.78
    sleep(0.3)
    if job.production.image.find(confidence=confidence):
        job.production.image.click(confidence=confidence)
        sleep(0.5)
        a = i_beehive_collect.find(confidence=confidence)
        if not a:
            job.production.image.click(confidence=confidence-0.02)
            sleep(0.5)
            a = i_beehive_collect.find(confidence=confidence-0.02)
        b = add(a, (220, 105))
        if a and b:
            drag(a, b, speed=0.5)
        elif not a:
            print("Couldn't find beehive_collect")
        elif not b:
            print("Couldn't find beehive")
    else:
        print("Could not find beehive")


field.coords_function = field_coords
feed_mill.coords_function = feed_mill_coords

default_sale_items = [wheat, wheat, wheat, wheat, corn, corn, carrots, soybeans, sugarcane, eggs, chicken_feed, pig_feed, cow_feed, sheep_feed]

# Crops
Job(name="Field", function=start_production_field, reset_time=2, item=wheat, production_no=0)
Job(name="Field", function=start_production_field, reset_time=2, item=wheat, production_no=1)
Job(name="Field", function=start_production_field, reset_time=5, item=corn, production_no=2)
Job(name="Sell", function=sell, reset_time=5, items=default_sale_items, production=field)  #Production added for location only
Job(name="Field", function=start_production_field, reset_time=10, item=carrots, production_no=3)
Job(name="Field", function=start_production_field, reset_time=20, item=soybeans, production_no=4)
Job(name="Field", function=start_production_field, reset_time=20, item=soybeans, production_no=5)
Job(name="Field", function=start_production_field, reset_time=30, item=sugarcane, production_no=6)
Job(name="Field", function=start_production_field, reset_time=30, item=sugarcane, production_no=7)
Job(name="Field", function=start_production_field, reset_time=30, item=sugarcane, production_no=8)
# Market
# Job(name="Sell", function=sell, reset_time=5, items=default_sale_items, production=field)  #Production added for location only
# Feed mill
j_feed_mill_0 = Job(name="Feed mill", function=start_production_feed_mill, reset_time=30, item=None, production=feed_mill, production_no=0)
# Animals
j_eggs = Job(name="Eggs", function=feed_animals, reset_time=20, item=eggs)
j_feed_mill_1 = Job(name="Feed mill", function=start_production_feed_mill, reset_time=30, item=None, production=feed_mill, production_no=1)
j_milk = Job(name="Milk", function=feed_animals, reset_time=60, item=milk)
j_honey = Job(name="Honey", function=collect_honey, reset_time=35, item=honey)
# Production
j_dairy = Job(name="Dairy", function=start_production_machine, reset_time=20, item=None, production=dairy)
j_sugar_mill = Job(name="Sugar mill", function=start_production_machine, reset_time=20, item=None, production=sugar_mill)
j_bakery = Job(name="Bakery", function=start_production_machine, reset_time=20, item=None, production=bakery)
j_bbq_grill = Job(name="BBQ_Grill", function=start_production_machine, reset_time=20, item=None, production=bbq_grill)
j_icecream_maker = Job(name="Icecream_maker", function=start_production_machine, reset_time=20, item=None, production=icecream_maker)
j_loom = Job(name="Loom", function=start_production_machine, reset_time=20, item=None, production=loom)

# Sales
j_truck = Job(name="Truck", function=truck, reset_time=45)
