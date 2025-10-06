from nav import *
from account import *
# from fields import *



# Crops
# Min number used for starting production. Max number used in the market for selling
wheat = Item(name="Wheat", creation_time=2, price=3, production=field, max_no=30)
corn = Item(name="Corn", creation_time=5, price=7, production=field, max_no=30)
carrots = Item(name="Carrots", creation_time=10, price=7, production=field, max_no=30)
soybeans = Item(name="Soybeans", creation_time=20, price=10, production=field, max_no=30)
sugarcane = Item(name="Sugarcane", creation_time=30, price=14, production=field, max_no=30)
indigo = Item(name="Indigo", creation_time=120, price=25, production=field, menu_page=2, min_no=20)
pumpkin = Item(name="Pumpkin", creation_time=180, price=32, production=field, menu_page=2, min_no=20)
cotton = Item(name="Cotton", creation_time=0, price=28, production=field, menu_page=2, min_no=20)
chilli = Item(name="Chilli", creation_time=0, price=28, production=field, menu_page=2, min_no=20)
tomato = Item(name="Tomato", creation_time=0, price=28, production=field, menu_page=2, min_no=20)
potato = Item(name="Potato", creation_time=0, price=28, production=field, menu_page=3, min_no=20)
strawberry = Item(name="Strawberry", creation_time=0, price=28, production=field, menu_page=3, min_no=20)
chamomile = Item(name="Chamomile", creation_time=0, price=28, production=field, menu_page=3, min_no=20)
asparagus = Item(name="Asparagus", production=field, menu_page=3, min_no=20)
# apples = Item(name="Apples", creation_time=8*60, price=39, production=apple_tree)
# raspberries = Item(name="Pumkin", creation_time=, price=46, production=unknown)

# Animal feed
chicken_feed = Item(name="Chicken_Feed", creation_time=5/3, price=7, production=feed_mill, ingredients={wheat: 2/3, corn: 1/3}, min_no=10, max_no=20)
cow_feed = Item(name="Cow_Feed", creation_time=10/3, price=10, production=feed_mill, ingredients={soybeans: 2/3, corn: 1/3}, min_no=8, max_no=20)
pig_feed = Item(name="Pig_Feed", creation_time=20/3, price=14, production=feed_mill, ingredients={soybeans: 1/3, carrots: 2/3}, min_no=5, max_no=15)
sheep_feed = Item(name="Sheep_Feed", creation_time=30/3, price=14, production=feed_mill, ingredients={soybeans: 1/3, corn: 3/3}, min_no=5, max_no=15)
goat_feed = Item(name="Goat_Feed", creation_time=30/3, price=14, production=feed_mill, ingredients={soybeans: 1/3, corn: 3/3}, min_no=5, max_no=15)

feeds = [chicken_feed, cow_feed, pig_feed, sheep_feed, goat_feed]
# Feed, animals, prod_time (hours)
feed_data = [(chicken_feed, 18, 1/3), (cow_feed, 15, 1), (pig_feed, 10, 4), (sheep_feed, 10, 6), (goat_feed, 8, 8)]

print()
print("Create items")

# Animal products
eggs = Item(name="Eggs", creation_time=20, price=18, production=chickens, ingredients={chicken_feed: 1}, min_no=6, max_no=22)
milk = Item("Milk", creation_time=60, price=32, production=cows, ingredients={cow_feed: 1}, min_no=6, max_no=22)
bacon = Item("Bacon", creation_time=240, price=50, production=pigs, ingredients={pig_feed: 1}, min_no=6, max_no=12)
wool = Item("Wool", creation_time=240, price=34, production=sheep, ingredients={sheep_feed: 1}, min_no=6, max_no=12)
honey_comb = Item("Honey_comb", creation_time=45, price=34, production=bees, max_no=10)

# Animal Data
chicken_data = Animal_Data(production=chickens, position=center_position, feed=chicken_feed, image_marker_1=i_home, squares_x_1=-4, squares_y_1=6, image_marker_2=i_eggs_collect, squares_x_2=-4, squares_y_2=3, squares_width=11, squares_height=5, fine_tune_x=-20, fine_tune_y=0, image_marker_3=chicken_feed.image_menu)
cow_data = Animal_Data(production=cows, position=center_position, feed=cow_feed, image_marker_1=i_cows, squares_x_1=account.cow_squares_x_1, squares_y_1=account.cow_squares_y_1, image_marker_2=i_milk_collect, squares_x_2=0, squares_y_2=5, squares_width=14, squares_height=5, fine_tune_x=-20, fine_tune_y=0, image_marker_3=cow_feed.image_menu)
pigs_data = Animal_Data(production=pigs, position=center_position, feed=pig_feed, image_marker_1=i_cows, squares_x_1=-1, squares_y_1=-8, image_marker_2=i_bacon_collect, squares_x_2=0, squares_y_2=5, squares_width=14, squares_height=5, fine_tune_x=-20, fine_tune_y=0, image_marker_3=pig_feed.image_menu)
sheep_data = Animal_Data(production=sheep, position=center_position, feed=sheep_feed, image_marker_1=i_cows, squares_x_1=-1, squares_y_1=-12, image_marker_2=i_wool_collect, squares_x_2=0, squares_y_2=5, squares_width=14, squares_height=5, fine_tune_x=-20, fine_tune_y=0, image_marker_3=sheep_feed.image_menu)

# Dairy
cream = Item("Cream", creation_time=20, price=50, production=dairy, ingredients={milk:1}, min_no=5)
butter = Item("Butter", creation_time=30, price=82, production=dairy, ingredients={milk:2}, min_no=5)
cheese = Item("Cheese", creation_time=60, price=122, production=dairy, ingredients={milk:3}, min_no=5)
goat_cheese = Item("Goat_Cheese", creation_time=60, price=122, production=dairy, ingredients={milk:3}, min_no=3)

# Sugar Mill
brown_sugar = Item("Brown_Sugar", creation_time=20, price=25, production=sugar_mill, ingredients={sugarcane: 1}, min_no=5)
white_sugar = Item("White_Sugar", creation_time=40, price=50, production=sugar_mill, ingredients={sugarcane: 2}, min_no=5)
syrup = Item("Syrup", creation_time=90, price=90, production=sugar_mill, ingredients={sugarcane: 2}, min_no=5)

# Bakery
bread = Item("Bread", creation_time=5, price=21, production=bakery, ingredients={corn: 3}, min_no=4)
corn_bread = Item("Corn_bread", creation_time=30, price=72, production=bakery, ingredients={corn:2, eggs:2})
cookie = Item("Cookie", creation_time=60, price=104, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2})
raspberry_muffin = Item("Raspberry_Muffin", creation_time=45, price=140, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2})
blackberry_muffin = Item("Blackberry_Muffin", creation_time=45, price=226, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2})
Item("Pizza", creation_time=45, price=226, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2}, menu_page=2)
Item("Spicy_pizza", creation_time=45, price=226, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2}, menu_page=2)
Item("Potato_bread", creation_time=45, price=226, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2}, menu_page=2)
Item("Frutti_di_mare_pizza", production=bakery, menu_page=2)

# BBQ Grill
pancakes = Item("Pancakes", creation_time=30, price=108, production=bbq_grill, ingredients={eggs:3, brown_sugar:1})
bacon_and_eggs = Item("Bacon_and_eggs", creation_time=60, price=201, production=bbq_grill, ingredients={eggs:4, bacon:2})
hamburger = Item("Hamburger", creation_time=120, price=180, production=bbq_grill, ingredients={bread:2, bacon:2})
grilled_tomatoes = Item("Grilled_tomatoes", creation_time=120, price=180, production=bbq_grill, ingredients={bread:2, bacon:2})
fishburger = Item("Fishburger", creation_time=120, price=180, production=bbq_grill, ingredients={bread:2, bacon:2})
Item("Baked_potato", creation_time=120, price=180, production=bbq_grill, ingredients={bread:2, bacon:2}, menu_page=2)

# Pie oven
Item("Carrot_pie", production=pie_oven)
Item("Pumpkin_pie", production=pie_oven)
Item("Bacon_pie", production=pie_oven)
Item("Apple_pie", production=pie_oven)
Item("Fish_pie", production=pie_oven)
Item("Feta_pie", production=pie_oven, menu_page=2)
Item("Casserole", production=pie_oven, menu_page=2)
Item("Shepherds_pie", production=pie_oven, menu_page=2)

# Cake oven
Item("Carrot_cake", production=cake_oven)
Item("Cream_cake", production=cake_oven)
Item("Red_berry_cake", production=cake_oven)
Item("Cheese_cake", production=cake_oven)
Item("Strawberry_cake", production=cake_oven)
chocolate_cake = Item("Chocolate_cake", production=cake_oven, menu_page=2)
Item("Potato_feta_cake", production=cake_oven, menu_page=2)
Item("Honey_apple_cake", production=cake_oven, menu_page=2)

# Popcorn Pop

# Soup Kitchen
Item("Lobster_soup", production=soup_kitchen)
Item("Tomato_soup", production=soup_kitchen)
Item("Pumpkin_soup", production=soup_kitchen)
Item("Asparagus_soup", production=soup_kitchen)
Item("Fish_soup", production=soup_kitchen)

# Icecreamery
Item("Vanilla_icecream", creation_time=120, price=180, production=icecream_maker, ingredients={cream:1, milk:1, white_sugar:1})
Item("Cherry_popsicle", creation_time=120, price=180, production=icecream_maker, ingredients={cream:1, milk:1, white_sugar:1})
strawberry_icecream = Item("Strawberry_icecream", creation_time=120, price=180, production=icecream_maker, ingredients={cream:1, milk:1, white_sugar:1})
Item("Chocolate_icecream", creation_time=120, price=180, production=icecream_maker, ingredients={cream:1, milk:1, white_sugar:1})

# Honey extractor
honey = Item("Honey", creation_time=20, price=0, production=honey_extractor, min_no=20)

# Candle maker
Item("Strawberry_candle", production=candle_maker)
Item("Raspberry_candle", production=candle_maker)

# Juice Press
Item("carrot_juice", production=juice_press)
Item("apple_juice", production=juice_press)
Item("cherry_juice", production=juice_press)
Item("tomato_juice", production=juice_press)
Item("berry_juice", production=juice_press)

# Jam maker
Item("Apple_jam", production=jam_maker)
Item("Raspberry_jam", production=jam_maker)
Item("Blackberry_jam", production=jam_maker)
Item("Cherry_jam", production=jam_maker)

# Coffee Kiosk
Item("Espresso", production=coffee_kiosk)
Item("Cafe_Latte", production=coffee_kiosk)
Item("Cafe_Mocha", production=coffee_kiosk)
Item("Raspberry_Mocha", production=coffee_kiosk)
Item("Hot_chocolate", production=coffee_kiosk)

# Loom
sweater = Item("Sweater", creation_time=120, price=0, production=loom)
cotton_fabric = Item("Cotton_Fabric", creation_time=30, price=0, production=loom, min_no=8)
blue_woolly_hat = Item("Blue_Woolly_Hat", creation_time=60, price=0, production=loom)
blue_sweater = Item("Blue_sweater", creation_time=180, price=0, production=loom)
red_scarf = Item("Red_scarf", production=loom)

# Sewing machine
Item("Cotton_shirt", production=sewing_machine)
Item("Wooly_chaps", production=sewing_machine)
Item("Violet_dress", production=sewing_machine)
Item("Soothing_pad", production=sewing_machine)
Item("Pillow", production=sewing_machine)

# Sauce maker
Item("Soy_sauce", production=sauce_maker)

# Sushi bar
Item("Sushi", production=sushi_bar)

# Fishery
Item("Red_lure", creation_time=85, price=0, production=lure_workbench, min_no=10)
Item("Lobster_trap", creation_time=120, price=0, production=net_maker, min_no=10)


if account == baby:
    for x in [eggs, bacon, wool, chicken_feed, pig_feed, sheep_feed, goat_feed, honey_comb, goat_cheese, sweater, blue_sweater, blue_woolly_hat]:
        x.min_no = 0



print()
print("Saved and reloaded relative locations")
for image in reference_images:
    print(f" - {image}, {image.relative_location}")

