from fields import *

def chicken_coords(no):
    adj_x, adj_y = 0, -125
    size = 3
    marker = i_chicken_marker
    base_coords = marker.find(confidence=0.8)
    if not base_coords:
        move_to(chickens)
        base_coords = marker.find(confidence=0.8)
        if not base_coords:
            print(f"Chicken Coords: couldn't find {marker}")
            return
    base_x, base_y = base_coords
    pos_x, pos_y = [int(base_x + (no) * gap_x * size + adj_x), int(base_y + (no) * gap_y * size + adj_y)]
    # print("Chicken Coords (gaps):", gap_x, gap_y)
    # print("Chicken Coords:", base_coords, pos_x, pos_y)
    return pos_x, pos_y


def feed_chickens():
    print("Feed chickens")
    adj = (-77, -104)
    adj = (-60, 300)
    i_gnome.click()
    move_to(chickens)
    sleep(0.3)
    coord = chicken_coords(0)
    if coord:
        pyautogui.click(coord)
        chicken_basket_coords = i_chicken_basket.find()
        chicken_basket_active = find_image_and_check_color(i_chicken_basket.image)
        chicken_feed_coords = chicken_feed.image_menu.find()
        if chicken_basket_coords and chicken_basket_active:
            haze(pos_0=chicken_basket_coords, top_left=add(chicken_feed_coords, adj), squares_x=10, squares_y=4)
            print("Eggs collected")
        if not chicken_basket_active:
            print("Eggs not collected. No eggs to collect")

        if chicken_feed_coords:
            count = chicken_feed.count()
            if count > 0:
                haze(pos_0=chicken_feed_coords, top_left=add(chicken_feed_coords, adj), squares_x=10, squares_y=4)
                print("Chickens fed")
            else:
                print("Chickens not fed, no chicken feed")
        # print("Chicken feed coords", chicken_feed_coords)

    sleep(0.8)


def get_chicken_drag_coords(start_pos):
    adj = (-77, -104)
    gap_8 = (gap_x * 8, gap_y * 8)
    gap_neg_8 = (-gap_x * 8, -gap_y * 8)
    gap_neg_half_y = (gap_x, -gap_y/2)
    gap_neg_y = (gap_x, -gap_y)
    gap_neg = (-gap_x, -gap_y)
    marker = i_chicken_marker
    base_coords = marker.find(confidence=0.8)
    if not base_coords:
        print("Couldn't find base")
        base_coords = [846, 742]
    pos_1 = add(base_coords, adj)
    pos_2 = add(pos_1, gap_8)
    pos_3 = add(pos_2, gap_neg_half_y)
    pos_4 = add(pos_3, gap_neg_8)
    pos_5 = add(pos_4, gap_neg_half_y)
    pos_6 = add(pos_5, gap_8)
    pos_7 = add(pos_6, gap_neg_half_y)
    pos_8 = add(pos_7, gap_neg_8)
    pos_9 = add(pos_8, gap_neg_half_y)
    pos_10 = add(pos_9, gap_8)
    positions = [start_pos, pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9, pos_10]
    # print("Chicken positions:", positions)
    return positions
