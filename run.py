from farm import *
from jobs import *
from feed_mill import *

# To Do:
#  - Fields - Done
#  - Mill - Testing
#  - Chickens - Testing
#  - Cows - Testing
#  - Dairy

# Non-loop testing
pyautogui.hotkey('alt', 'tab')
sleep(0.5)


# result = brown_sugar.image_menu.find(region=PRODUCTION_ZONE)
# print(result)

# production = loom
# for x in production.items(): print(x, x.count())
# j_icecream_maker.run()
# j_sugar_mill.run()
# j_bakery.run()
# j_bbq_grill.run()
# j_honey.run()
# j_loom.run()

# result_1 = i_beehive_collect.find()
# result_2 = i_beehive.find()
# print(result_1, result_2,      difference(result_1, result_2))

# j_truck.run()

run_jobs()

sleep(1)
pyautogui.hotkey('alt', 'tab')

