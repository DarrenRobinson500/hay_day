from nav import *
# from fields import *



# cows = Production("Cows", 10)
# pigs = Production("Pigs", 10, l_pigs)
# sheep = Production("Sheep", 4)
#
# sugar_mill = Production("Sugar mill", 1)
# bakery = Production("Bakery", 1)
# dairy = Production("Dairy", 1, l_dairy)
#
# apple_tree = Production("Apple tree", 3)
#
# popcorn_pot = Production("Popcorn pot", 1)
# bbq_grill = Production("BBQ grill", 1)
# Crops
wheat = Item(name="Wheat", creation_time=2, price=3, production=field, min_no=30)
corn = Item(name="Corn", creation_time=5, price=7, production=field, min_no=30)
carrots = Item(name="Carrots", creation_time=10, price=7, production=field, min_no=30)
soybeans = Item(name="Soybeans", creation_time=20, price=10, production=field, min_no=30)
sugarcane = Item(name="Sugarcane", creation_time=30, price=14, production=field, min_no=30)
# indigo = Item(name="Indigo", creation_time=120, price=25, production=field)
# pumkin = Item(name="Pumkin", creation_time=180, price=32, production=field)
# cotton = Item(name="Cotton", creation_time=, price=28, production=field)
# apples = Item(name="Apples", creation_time=8*60, price=39, production=apple_tree)
# raspberries = Item(name="Pumkin", creation_time=, price=46, production=unknown)

# Animal feed
chicken_feed = Item(name="Chicken_Feed", creation_time=5/3, price=7, production=feed_mill, ingredients={wheat: 2/3, corn: 1/3}, min_no=24, max_no=20)
cow_feed = Item(name="Cow_Feed", creation_time=10/3, price=10, production=feed_mill, ingredients={soybeans: 2/3, corn: 1/3}, min_no=15, max_no=20)
pig_feed = Item(name="Pig_Feed", creation_time=20/3, price=14, production=feed_mill, ingredients={soybeans: 1/3, carrots: 2/3}, min_no=8, max_no=15)
sheep_feed = Item(name="Sheep_Feed", creation_time=30/3, price=14, production=feed_mill, ingredients={soybeans: 1/3, corn: 3/3}, min_no=8, max_no=15)
goat_feed = Item(name="Goat_Feed", creation_time=30/3, price=14, production=feed_mill, ingredients={soybeans: 1/3, corn: 3/3}, min_no=8, max_no=15)

feeds = [chicken_feed, cow_feed, pig_feed, sheep_feed, goat_feed]
# Feed, animals, prod_time (hours)
feed_data = [(chicken_feed, 18, 1/3), (cow_feed, 15, 1), (pig_feed, 10, 4), (sheep_feed, 10, 6), (goat_feed, 8, 8)]


# Animal products
eggs = Item(name="Eggs", creation_time=20, price=18, production=chickens, ingredients={chicken_feed: 1}, min_no=10, max_no=15)
milk = Item("Milk", creation_time=60, price=32, production=cows, ingredients={cow_feed: 1}, min_no=10, max_no=15)
bacon = Item("Bacon", creation_time=240, price=50, production=pigs, ingredients={pig_feed: 1})
wool = Item("Wool", creation_time=240, price=34, production=sheep, ingredients={sheep_feed: 1})
honey = Item("Honey", creation_time=45, price=34, production=bees, ingredients={sheep_feed: 1})

# Animal Data
chicken_data = Animal_Data(production=chickens, position=chicken_position, feed=chicken_feed, image_marker_1=i_home, squares_x_1=-4, squares_y_1=6, image_marker_2=i_eggs_collect, squares_x_2=-4, squares_y_2=3, squares_width=11, squares_height=4, fine_tune_x=-20, fine_tune_y=0, image_marker_3=chicken_feed.image_menu)
cow_data = Animal_Data(production=cows, position=cow_position, feed=cow_feed, image_marker_1=i_home, squares_x_1=-5, squares_y_1=-3, image_marker_2=i_milk_collect, squares_x_2=-2, squares_y_2=4, squares_width=14, squares_height=5, fine_tune_x=-20, fine_tune_y=0, image_marker_3=cow_feed.image_menu)


# Dairy
cream = Item("Cream", creation_time=20, price=50, production=dairy, ingredients={milk:1}, min_no=4)
butter = Item("Butter", creation_time=30, price=82, production=dairy, ingredients={milk:2}, min_no=3)
cheese = Item("Cheese", creation_time=60, price=122, production=dairy, ingredients={milk:3}, min_no=2)
goat_cheese = Item("Goat_Cheese", creation_time=60, price=122, production=dairy, ingredients={milk:3}, min_no=2)

# Sugar Mill
brown_sugar = Item("Brown_Sugar", creation_time=20, price=25, production=sugar_mill, ingredients={sugarcane: 1}, min_no=3)
white_sugar = Item("White_Sugar", creation_time=40, price=50, production=sugar_mill, ingredients={sugarcane: 2}, min_no=3)
syrup = Item("Syrup", creation_time=90, price=90, production=sugar_mill, ingredients={sugarcane: 2}, min_no=3)

# Bakery
bread = Item("Bread", creation_time=5, price=21, production=bakery, ingredients={corn: 3}, min_no=4)
corn_bread = Item("Corn_bread", creation_time=30, price=72, production=bakery, ingredients={corn:2, eggs:2})
cookie = Item("Cookie", creation_time=60, price=104, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2})
raspberry_muffin = Item("Raspberry_Muffin", creation_time=45, price=140, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2})
blackberry_muffin = Item("Blackberry_Muffin", creation_time=45, price=226, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2})
Item("Pizza", creation_time=45, price=226, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2}, menu_page=2)
Item("Spicy_pizza", creation_time=45, price=226, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2}, menu_page=2)
Item("Potato_bread", creation_time=45, price=226, production=bakery, ingredients={wheat: 2, brown_sugar: 1, eggs: 2}, menu_page=2)


# BBQ Grill
pancakes = Item("Pancakes", creation_time=30, price=108, production=bbq_grill, ingredients={eggs:3, brown_sugar:1})
bacon_and_eggs = Item("Bacon_and_eggs", creation_time=60, price=201, production=bbq_grill, ingredients={eggs:4, bacon:2})
hamburger = Item("Hamburger", creation_time=120, price=180, production=bbq_grill, ingredients={bread:2, bacon:2})
grilled_tomatoes = Item("Grilled_tomatoes", creation_time=120, price=180, production=bbq_grill, ingredients={bread:2, bacon:2})
fishburger = Item("Fishburger", creation_time=120, price=180, production=bbq_grill, ingredients={bread:2, bacon:2})
Item("Baked_potato", creation_time=120, price=180, production=bbq_grill, ingredients={bread:2, bacon:2}, menu_page=2)

# Icecreamery
Item("Vanilla_icecream", creation_time=120, price=180, production=icecream_maker, ingredients={cream:1, milk:1, white_sugar:1})
Item("Cherry_popsicle", creation_time=120, price=180, production=icecream_maker, ingredients={cream:1, milk:1, white_sugar:1})
Item("Strawberry_icecream", creation_time=120, price=180, production=icecream_maker, ingredients={cream:1, milk:1, white_sugar:1})
Item("Chocolate_icecream", creation_time=120, price=180, production=icecream_maker, ingredients={cream:1, milk:1, white_sugar:1})

# Loom
Item("Sweater", creation_time=120, price=0, production=loom)
Item("Cotton_Fabric", creation_time=30, price=0, production=loom)
Item("Blue_Woolly_Hat", creation_time=60, price=0, production=loom)
Item("Blue_sweater", creation_time=180, price=0, production=loom)


# popcorn = Item("Popcorn", creation_time=30, price=32, production=popcorn_pot, ingredients={})

# pyautogui.hotkey('alt', 'tab')
# sleep(0.5)
#
# print(cookie.count())
#
# # sleep(0.5)
# pyautogui.hotkey('alt', 'tab')
