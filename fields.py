from items import *
from image import *
from sales import *

def field_coords(row_no, col_no=0):
    adj_x, adj_y = 35, -10
    adj_x, adj_y = adj_x - 5 * gap_x, adj_y + 5 * gap_y
    base_coords = i_field_marker.find(confidence=0.88)
    if not base_coords:
        # print("Couldn't find field marker - trying gnome")
        i_gnome.click(confidence=0.85)
        sleep(0.5)
        base_coords = i_field_marker.find(confidence=0.88)
        if not base_coords:
            print("Couldn't find field marker or gnome")
            move_to_center()
            return
    base_x, base_y = base_coords
    field_x, field_y = [int(base_x + row_no * gap_x + col_no * gap_x + adj_x), int(base_y + row_no * gap_y - col_no * gap_y + adj_y)]
    # print(f"Field Coords. Base: {base_coords}. Field: {field_x} {field_y}")
    return field_x, field_y

def field_coord_check():
    # move_to(field)
    coords_1 = field_coords(0, 5)
    coords_2 = field_coords(0, 0)
    coords_3 = field_coords(7, 0)
    coords_4 = field_coords(7, 5)
    # for coords in [coords_1, coords_2, coords_3, coords_4]:
    #     pyautogui.moveTo(coords, duration=2)
    #     sleep(2)
    for coords in [coords_1, coords_2, coords_3, coords_4, coords_1]:
        pyautogui.moveTo(coords, duration=2)
        # pyautogui.click(coords)
        sleep(2)


def field_loop(crops=(wheat, corn, carrots, soybeans, sugarcane, sugarcane, sugarcane, sugarcane)):
    move_to(field)
    # for row, crop in enumerate([soybeans, soybeans, soybeans, sugarcane, sugarcane, sugarcane, sugarcane, sugarcane]):
    for row, crop in enumerate(crops):
    # for row, crop in enumerate([wheat, wheat, corn, corn, carrots, soybeans, sugarcane, sugarcane]):
        sleep(0.3)
        coord = field_coords(row)
        if coord:
            pyautogui.click(coord)
            sleep(0.3)
            # Collect if ready
            if i_scythe.find():
                position_0 = i_scythe.find()
                position_1 = field_coords(row)
                if position_1:
                    position_2 = add(position_1, [gap_x * 6.5, -gap_y * 6.5])
                    if position_0 and position_1 and position_2:
                        drag_many([position_0, position_1, position_2], 1)
                        sleep(4.5)
                        pyautogui.click(field_coords(row))
                        sleep(0.3)
            # Plant
            if i_second_page.find():
                print("Second page found")
                i_back_arrows.click()

            if crop.image_menu.find():
                field_coord_start = field_coords(row)
                print(f"Plant {crop}")
                menu_coord = crop.image_menu.find(confidence=0.87)

                if field_coord_start and menu_coord:
                    field_coord_end = add(field_coord_start, [gap_x * 6.5, -gap_y * 6.5])
                    drag_many([menu_coord, field_coord_start, field_coord_end], speed=1.15)
                    sleep(2.0)
        sleep(0.3)

def sell_crops():
    item_sold, count = True, 0
    while item_sold and count < 3:
        item_sold = sell([wheat, corn, carrots, soybeans, sugarcane, eggs])
        count += 1
    sleep(0.3)
    if i_market_cross_2.find(): i_market_cross_2.click()
    if i_market_cross.find(): i_market_cross.click()


def loop_wait(minutes=2):
    if i_gnome.find(): i_gnome.click()
    elif i_field_marker.find(): i_field_marker.click()
    move_to(field)
    if i_reload.find():
        print(f"Reload: Waiting 8 min")
        sleep(8 * 60)
        reload()
        return
    # if i_hay_day_start_icon.find():
    #     print(f"Restart")
    #     restart()
    #     return
    for x in [i_try_again, i_farm_pass_cross, i_home_cross, i_market_cross, i_market_cross_2, i_silo_full_cross, i_continue, i_not_enough_resources_cross, i_last_crop_cross]:
        if x.find():
            sleep(0.5)
            x.click()
            sleep(2)
            if x in [i_silo_full_cross,]:
                print("Loop wait - found i_silo_full_cross")
                pause_field_production()

    print(f"Waiting {minutes} min")
    sleep(minutes * 60)

def clear():
    for x in [i_home, i_field_marker, i_gnome, i_go_home]:
        if x.find(): return
    zoom()
    # if i_help_marker.find():
    #     clear_help_markers()
    if i_reload.find():
        print(f"Reload: Waiting 8 min")
        sleep(8 * 60)
        reload()
        return
    for x in [i_help_marker, i_try_again, i_farm_pass_cross, i_home_cross, i_market_cross, i_market_cross_2, i_silo_full_cross, i_continue, i_not_enough_resources_cross, i_last_crop_cross]:
        if x.find():
            sleep(0.5)
            x.click()
            sleep(2)
            if x in [i_silo_full_cross,]:
                print("Clear - found i_silo_full_cross")
                pause_field_production()
