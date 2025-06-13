from fields import *


def feed_mill_coords(no):
    adj_x, adj_y = -50, -80
    size = 3
    marker = i_feed_mill_marker
    base_coords = marker.find(confidence=0.8)
    if not base_coords:
        move_to(field)
        base_coords = marker.find(confidence=0.8)
        if not base_coords: return
    base_x, base_y = base_coords
    pos_x, pos_y = [int(base_x + (no + 1) * gap_x * size + adj_x), int(base_y + (no + 1) * gap_y * size + adj_y)]
    return pos_x, pos_y


# for feed, count, prod_time in feed_data:
#     no_per_hour = count / prod_time
#     print(f"{feed}:, Feed production time: {round(feed.creation_time, 2)}, No of animals: {count}, Produce production time: {prod_time}, Feed required per hour: {round(no_per_hour, 2)}")

# def feed_cycle(item):
#     move_to(item.production)

# for x in feed_mill.items():
#     print(x)

