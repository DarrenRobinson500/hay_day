from classes import *

current_position = None

def goto(destination):
    print("Goto:", destination)
    if type(destination) == Production: destination = destination.location
    global current_location
    if current_location == l_pycharm and destination != l_pycharm:
        print("Pressing alt tab")
        pyautogui.hotkey('alt', 'tab')
        i_pycharm_icon.click()
        return
        i_bluestacks_icon.click()
        current_location = l_home
        sleep(0.2)
        if i_farm_pass_cross.find():
            print("Clicking farm pass cross")
            i_farm_pass_cross.click()
            sleep(0.2)
    if current_location != l_pycharm and destination == l_pycharm:
        print("Pressing alt tab")
        pyautogui.hotkey('alt', 'tab')
        return

    home_coords = l_home.find()
    dest_coords = destination.find()
    # print("Goto find", home_coords, dest_coords)

    if home_coords and dest_coords and destination != l_home:
        destination.image.click()
        current_location = destination
        save_rel_position(destination, home_coords, dest_coords)
        print(f"Made it to: {destination}")
    else:
        print(f"Failed to arrive: {destination}")

def save_rel_position(destination, position_0, position_1):
    relative_position = str(difference(position_1, position_0))
    db_save(destination.name, relative_position)

def move_to(thing):
    global current_position
    if type(thing) == Production:
        position = thing.location
    elif type(thing) == Item:
        position = thing.production.location
    else:
        position = thing
    if current_position == position:
        print(f"Move to: {position}: already there")
        return
    print("Move to:", thing, position)
    sleep(0.5)
    result = i_home.find()
    if result:
        drag(result, position, speed=0.5)
        current_position = position
        print("Reset current position to:", current_position)
    sleep(0.3)
    # if i_home_cross.find():
    #     i_home_cross.click()

def move_to_center():
    print("Move to center")
    global current_position
    if current_position == center_position:
        print("Move to center - Already there")
        return
    sleep(1)
    if current_position:
        if current_position == south_west_position:
            drag((1552,535), (1278,745), speed=0.5)
        else:
            drag(current_position, center_position, speed=0.5)
        current_position = center_position
    sleep(1)


def reload():
    sleep(0.5)

    if i_reload.find():
        i_reload.click()
        result, count = None, 0
        while not result and count < 40:
            result = i_zoomed_in_house.find()
            print("Reload (loops):", count, result)
            sleep(0.1)
            count += 1
        if result:
            spot_to_move_to = result[0] - 150, result[1]
            pyautogui.moveTo(spot_to_move_to)

    zoom()
    move_to(field)

def restart():
    sleep(0.5)

    if i_hay_day_start_icon.find():
        i_hay_day_start_icon.click()
        result, count = None, 0
        while not result and count < 40:
            result = i_zoomed_in_house.find()
            print("Reload (loops):", count, result)
            sleep(0.5)
            count += 1
        if result:
            spot_to_move_to = result[0] - 150, result[1]
            pyautogui.moveTo(spot_to_move_to)

    if i_event_board_cross.find(): i_event_board_cross.click()

    zoom()
    move_to(field)


l_pycharm = Loc("Pycharm", i_pycharm_icon)
l_home = Loc("Home", i_home)

current_location = l_pycharm

