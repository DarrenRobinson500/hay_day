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
