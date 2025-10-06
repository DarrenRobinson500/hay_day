from animals import *
from feed_mill import *
from restart import *
from items import *


class Job:
    def __init__(self, name, function, reset_time, item=None, production=None, production_no=None, items=None, first_run=0):
        self.name = name
        self.function = function
        self.item = item
        self.production = production
        self.items = items
        if item:
            self.production = item.production
        self.production_no = production_no
        self.reset_time = reset_time
        if first_run > 0:
            self.runtime = datetime.now() + timedelta(minutes=first_run)
        else:
            self.runtime = datetime.now() + timedelta(minutes=len(jobs) * 0.25)
        jobs.append(self)

    def __str__(self):
        # if self.item:
        #     return f"{self.name} ({self.item})"
        # else:
            return self.name

    def run(self):
        print("Running:", self)
        if self.production:
            move_to(self.production)
            sleep(1.5)
        try:
            if self == j_truck:
                move_home_to_center()
                sleep(1.5)
        except: pass
        self.function(self)
        self.runtime = max(datetime.now() + timedelta(minutes=self.reset_time), self.runtime)
        # clear()
        sleep(1)
        # move_to_center()
        # sleep(1)

    def wait_time(self):
        return int((self.runtime - datetime.now()).total_seconds())

def run_job(jobs_to_run=jobs):
    clear()
    next_job = min(jobs_to_run, key=lambda job: job.runtime)
    time_to_wait = int((next_job.runtime - datetime.now()).total_seconds())
    if time_to_wait < 1:
        next_job.run()
        next_job = min(jobs_to_run, key=lambda job: job.runtime)
        time_to_wait = int((next_job.runtime - datetime.now()).total_seconds())
    return time_to_wait

def print_jobs(jobs_to_run=jobs):
    sorted_jobs = sorted(jobs_to_run, key=lambda job: job.runtime)
    print("\nUpcoming Jobs")
    for job in sorted_jobs[0:8]:
        if job.name == "Field":
            print(f" - {int(job.wait_time()/60)}min: {job.item} ")
        else:
            print(f" - {int(job.wait_time()/60)}min: {job} ")
    text = ""
    for job in sorted_jobs[8:]:
        text += f"{job}, "
    print(text)

def run_jobs(jobs_to_run=jobs):
    while True:
        wait_time = run_job(jobs_to_run)
        if wait_time > 60:
            sleep(2)
            pyautogui.hotkey('alt', 'tab')
            for production_unit in production_units:
                production_unit.print_count()
            print_jobs(jobs_to_run)
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
    in_orders, count = i_orders.find(), 0
    while not in_orders and count < 4:
        sleep(2)
        if i_truck.find():
            i_truck.click()
        in_orders = i_orders.find()
        count += 1
    if not in_orders:
        print("Couldn't get to order board")
        return
    # sleep(3) # To allow the swinging tick to stop swinging
    order = i_truck_tick.find(region=ORDER_REGION)
    count = 0
    while order and count < 5:
        sleep(3)
        i_truck_tick.click()
        # pyautogui.click(order)
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
        count += 1
    i_truck_cross.click()

def get_positions(position_1, rows):
    positions = [position_1]
    field_length = 6
    current_position = add(position_1, [gap_x * field_length, -gap_y * field_length])
    positions.append(current_position)

    remaining = rows - 1

    for row in range(remaining):
        current_position = add(current_position, [gap_x, gap_y])
        positions.append(current_position)
        if row % 2 == 0:
            current_position = add(current_position, [-gap_x * field_length, gap_y * field_length])
            positions.append(current_position)
        else:
            current_position = add(current_position, [gap_x * field_length, -gap_y * field_length])
            positions.append(current_position)

    return positions

def start_production_field_2(job): start_production_field(job, rows=2)
def start_production_field_3(job): start_production_field(job, rows=3)
def start_production_field_4(job): start_production_field(job, rows=4)
def start_production_field_6(job): start_production_field(job, rows=6)
def start_production_field_7(job): start_production_field(job, rows=7)

def get_to_menu_page(item):
    if item.menu_page == 1:
        if i_third_page.find():
            i_forward_arrows.click()
            sleep(0.3)
        elif i_second_page.find():
            i_back_arrows.click()
            sleep(0.3)
    if item.menu_page == 2:
        if i_first_page.find():
            i_forward_arrows.click()
            sleep(0.3)
        elif i_third_page.find():
            i_back_arrows.click()
            sleep(0.3)
    if item.menu_page == 3:
        if i_second_page.find():
            i_forward_arrows.click()
            sleep(0.3)
        elif i_first_page.find():
            i_back_arrows.click()
            sleep(0.3)


def start_production_field_extras(job):
    speed = 1.8
    spots = [(x, -1) for x in range(9)] #+ [(x, 8) for x in range(3)]
    items = [strawberry, potato, chamomile, tomato, chilli, cotton, indigo, pumpkin, None]
    item_no = 0
    item = items[item_no]

    for row, column in spots:
        if not item: continue
        position_1 = field_coords(row, column)
        pyautogui.click(position_1)
        sleep(0.3)
        if i_scythe.find():
            position_1 = field_coords(row, column)
            position_0 = i_scythe.find()
            if position_1:
                drag_many([position_0, position_1], speed=speed)
                sleep(4.5)
                pyautogui.click(field_coords(row, column))
                sleep(0.3)
        get_to_menu_page(item)
        # Plant
        if item and item.image_menu.find():
            while item and (item.count() >= item.min_no or item.count() == 0):
                item_no += 1
                item = items[item_no]
                if item:
                    get_to_menu_page(item)
                    sleep(0.1)
            if item:
                print(f"Plant {item}")
                position_0 = item.image_menu.find(confidence=0.87)
                position_1 = field_coords(row, column)
                if position_0 and position_1:
                    drag_many([position_0, position_1], speed=speed)
                    sleep(2.0)
                    item_no += 1
                    item = items[item_no]
                    if item:
                        get_to_menu_page(item)
                        sleep(0.1)



def start_production_field(job, rows=1):
    speed = 1
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
            if position_1:
                positions = [position_0] + get_positions(position_1=position_1, rows=rows)
                drag_many(positions, speed=speed)
                sleep(4.5)
                if i_silo_full.find():
                    print("Silo full - pausing production")
                    i_silo_full_cross.click()
                    pause_field_production()
                pyautogui.click(field_coords(row))
                sleep(0.3)

        # Check menu position
        if i_second_page.find():
            print("Second page found")
            i_back_arrows.click()
            sleep(0.3)

        # Plant
        if job.item.image_menu.find():
            print(f"Plant {job.item}")
            position_0 = job.item.image_menu.find(confidence=0.87)
            position_1 = field_coords(row)
            if position_0 and position_1:
                positions = [position_0] + get_positions(position_1=position_1, rows=rows)
                drag_many(positions, speed=speed)
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
        # print("Production slot (pre):", production_slot)
        while production_slot and count < 7 and not mill_is_full:
            count += 1
            if chicken_feed.image_menu.find() and production_slot:
                item = feed_mill.get_random()
                # print("Produce:", item)
                a = item.image_menu.find()
                item_count = item.count(forced=False)
                print("Produce:", item, item_count, item.min_no, item_count < item.min_no)
                need_more = item_count < item.min_no
                if not need_more:
                    print("Feed mill - no further need for:", item)
                if a and production_slot and need_more:
                    drag(a, production_slot)
                    item.number_made += 3
                if i_not_enough_resources_cross.find():
                    print("Clicking not enough resources cross")
                    i_not_enough_resources_cross.click()
                    item.number_made -= 3
                    count += 5
                if i_last_crop_cross.find():
                    print("Clicking last crop cross")
                    i_last_crop_cross.click()
                    item.number_made -= 3
                    count += 5
            sleep(0.7)
            production_slot = i_production_slot.find()
            # print("Production slot (loop):", production_slot)
        if not production_slot:
            print(f"Mill: {job.production_no} is full.")
    drag((400, 2000), (100, 1000))
    sleep(2)

def find_yourself(job):
    found = i_home.find()
    if not found:
        found = move_home_to_center()
    if found:
        move_to(job.production)

    sleep(0.3)

def feed_animals(job):
    if job.item == eggs: data = chicken_data
    if job.item == milk: data = cow_data
    # if job.item == bacon: data = pigs_data
    # if job.item == wool: data = sheep_data
    sleep(0.3)
    if not data.image_marker_1.find():
        find_yourself(job)
    if data.image_marker_1.find():
        data.collect_and_feed()
        if job.item == eggs:
            i_chicken_marker.click()
            i_gnome.click()
        else:
            i_lady_bug.click()


        # for x in [i_cows, i_chicken_marker]:
        #     if x.find(confidence=0.85) and not clicked_out:
        #         x.click()
        #         clicked_out = True
    # if job.item == eggs:
    #     sleep(0.3)
    #     if not chicken_data.image_marker_1.find():
    #         find_yourself(job)
    #     if chicken_data.image_marker_1.find():
    #         chicken_data.collect_and_feed()
    #         for x in [i_gnome, i_field_marker, i_chicken_marker]:
    #             if x.find(confidence=0.85): x.click()
    # if job.item == milk:
    #     if not cow_data.image_marker_1.find():
    #         find_yourself(job)
    #     if cow_data.image_marker_1.find():
    #         cow_data.collect_and_feed()
    #         for x in [i_gnome, i_field_marker, i_chicken_marker]:
    #             if x.find(confidence=0.85): x.click()
    #     else:
    #         print("Cow data image marker not found")

def start_production_machine(job):
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
    if not opened:
        print("Start Production Machine. Couldn't find:", job.production)
        return

    # Load up production slots
    slots_are_full = False
    count = 0
    production_slot = i_production_slot.find()
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
                    item.current_number += 1
                    item.number_made += 1
                if i_not_enough_resources_cross.find():
                    print("Clicking not enough resources cross")
                    i_not_enough_resources_cross.click()
                    item.number_made -= 1
                    count = 5 # Stop trying
            else:
                count = 5
        sleep(0.7)
        production_slot = i_production_slot.find()
        # print("Production slot (loop):", production_slot)
    if not production_slot:
        print(f"{job.production}: is full.")
    if job.production.clear_zone:
        pyautogui.click(job.production.clear_zone)
    # if job.production == bbq_grill:
    #     pyautogui.click(818, 1178)
    # elif job.production == dairy:
    #     pyautogui.click(518, 878)
    # elif job.production == loom:
    #     pyautogui.click(504, 1014)
    elif job.name != "Bait":
        pyautogui.click(1118, 878)
    # drag((400, 2000), (300, 1000))
    sleep(2)

def collect_honey_comb(job):
    print("Collecting Honey")
    confidence = 0.78
    sleep(0.3)
    if job.production.image.find(confidence=confidence):
        job.production.image.click(confidence=confidence)
        sleep(0.5)
        a = i_beehive_collect.find(confidence=confidence)
        if not a:
            job.production.image.click(confidence=confidence-0.03)
            sleep(0.5)
            a = i_beehive_collect.find(confidence=confidence-0.03)
        b = add(a, (210, 135))
        if a and b:
            drag(a, b, speed=0.5, add_spiral=True)
            # spiral
        elif not a:
            print("Couldn't find beehive_collect")
        elif not b:
            print("Couldn't find beehive")
    else:
        print("Could not find beehive")

def bait(job):
    print("Make bait")
    result = i_boat.find()
    if not result:
        print("Couldn't find boat")
        return
    pyautogui.click(result)
    found, count = False, 0
    while not found and count < 60:
        if lure_workbench.image.find(): found = True
        count += 1
        sleep(0.5)
    if found:
        print("Found the workbench")
        start_production_machine(job)
    sleep(0.5)
    if i_go_home.find():
        i_go_home.click()

def move_fishery(destination):
    sleep(0.5)
    a = i_fish_cabin.find()
    if a:
        drag(a, destination, speed=0.5)

def lobster(job):
    left_side, right_side = (400, 400), (1600, 200)
    print("Lobsters")
    result = wait_for_images(images_to_click=[i_boat], destination_image=i_fish_cabin_close, time_seconds=120)
    if not result:
        print("Didn't get to the fishery")
        return
    zoom()

    move_fishery(left_side)

    if wait_for_images(images_to_click=[], destination_image=net_maker.image, time_seconds=5):
        start_production_machine(job)
    if wait_for_images(images_to_click=[], destination_image=i_lobster_pool, time_seconds=5):
        i_lobster_pool.click()
        sleep(0.5)
        a = i_lobster_net.find()
        b = i_lobster_pool.find()
        if a and b:
            if a:
                drag(a, add(b, (100, -90)))

    move_fishery(right_side)

    sleep(0.5)
    if i_caught_lobster.find():
        print("Found a caught lobster")
    # else:
    #     print("couldn't find the pool")
    #     return
    #
    # a = i_fishery_rock.find()
    # if a:
    #     print("Found the rock")
    #     drag(a, (1800, 200))
    #     for x in range(1):
    #         if i_caught_lobster.find():
    #             i_caught_lobster.click()
    #         a = i_log.find()
    #         if a: drag(a, add(a, (600, 400)))
    # wait_for_images(images_to_click=[i_go_home], destination_image=i_boat, time_seconds=120)


field.coords_function = field_coords
feed_mill.coords_function = feed_mill_coords

# default_sale_items = [wheat, sheep_feed, eggs, chixcken_feed, wool, milk, honey_comb, pig_feed, cow_feed, corn, carrots, soybeans, sugarcane,]
# default_sale_items = [wheat, corn, carrots, soybeans, sugarcane]
default_sale_items = [wheat, corn, soybeans, sugarcane, cow_feed]

# Crops
j_wheat = Job(name="Wheat", function=start_production_field_4, reset_time=2, item=wheat, production_no=0)
j_sell = Job(name="Sell", function=sell, reset_time=2.5, items=default_sale_items, production=field)  #Production added for location only
# Job(name="Wheat", function=start_production_field_2, reset_time=2, item=wheat, production_no=2, first_run=1)
# Job(name="Wheat", function=start_production_field_2, reset_time=2, item=wheat, production_no=4, first_run=2)
# j_wheat = Job(name="Wheat", function=start_production_field, reset_time=2, item=wheat, production_no=6)
j_corn = Job(name="Corn", function=start_production_field, reset_time=5, item=corn, production_no=4)
# j_carrots = Job(name="Carrots", function=start_production_field, reset_time=10, item=carrots, production_no=5)
Job(name="Soybeans", function=start_production_field, reset_time=20, item=soybeans, production_no=5)
j_sugarcane = Job(name="Sugar cane", function=start_production_field_2, reset_time=30, item=sugarcane, production_no=6)
# j_field_extras = Job(name="Field extras", function=start_production_field_extras, reset_time=60)

# Market

# Feed mill
j_feed_mill_0 = Job(name="Feed mill", function=start_production_feed_mill, reset_time=30, item=None, production=feed_mill, production_no=0)
# j_feed_mill_1 = Job(name="Feed mill", function=start_production_feed_mill, reset_time=30, item=None, production=feed_mill, production_no=1, first_run=5)

# Animals
# j_eggs = Job(name="Eggs", function=feed_animals, reset_time=20, item=eggs)
j_milk = Job(name="Milk", function=feed_animals, reset_time=60, item=milk)
# j_bacon = Job(name="Bacon", function=feed_animals, reset_time=60, item=bacon)
# j_wool = Job(name="Wool", function=feed_animals, reset_time=60, item=wool)
# j_honey_comb = Job(name="Honey_comb", function=collect_honey_comb, reset_time=35, item=honey_comb, first_run=10)

# Production
production_reset = 60
j_dairy = Job(name="Dairy", function=start_production_machine, reset_time=production_reset, item=None, production=dairy, first_run=5)
j_sugar_mill = Job(name="Sugar mill", function=start_production_machine, reset_time=production_reset, item=None, production=sugar_mill, first_run=10)
# j_bakery = Job(name="Bakery", function=start_production_machine, reset_time=production_reset, item=None, production=bakery, first_run=15)
# j_bbq_grill = Job(name="BBQ_Grill", function=start_production_machine, reset_time=production_reset, item=None, production=bbq_grill, first_run=20)
# j_pie_oven = Job(name="Pie_oven", function=start_production_machine, reset_time=production_reset, item=None, production=pie_oven, first_run=22)
# j_cake_oven = Job(name="Cake_oven", function=start_production_machine, reset_time=production_reset, item=None, production=cake_oven, first_run=25)
# j_icecream_maker = Job(name="Icecream_maker", function=start_production_machine, reset_time=production_reset, item=None, production=icecream_maker, first_run=25)
# j_loom = Job(name="Loom", function=start_production_machine, reset_time=production_reset, item=None, production=loom, first_run=30)
# j_honey_extractor = Job(name="Honey extractor", function=start_production_machine, reset_time=35, item=None, production=honey_extractor, first_run=37)
# j_jam_maker = Job(name="Jam maker", function=start_production_machine, reset_time=production_reset, item=None, production=jam_maker, first_run=40)
# j_juice_press = Job(name="Juice press", function=start_production_machine, reset_time=production_reset, item=None, production=juice_press, first_run=40)

# Fishery
# j_bait = Job(name="Bait", function=bait, reset_time=60*6, item=None, production=lure_workbench, first_run=50)
# j_lobster = Job(name="Lobster", function=lobster, reset_time=60*6, item=None, production=net_maker, first_run=40)

# Sales
# j_truck = Job(name="Truck", function=truck, reset_time=60, first_run=5)

# Restart
# j_restart = Job(name="Restart", function=restart, reset_time=120, first_run=120)

print()
print("Scheduled Jobs at inception")
for job in jobs:
    run_time = job.runtime.strftime("%H:%M:%S")
    print(f" - {job}, {run_time}")
