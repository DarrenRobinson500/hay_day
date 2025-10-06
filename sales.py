from items import *
from num import *

MARKET_REGION = (450, 150, 800, 830)


def sell(job):
    sleep_period = 0.1
    print("Sell")
    move_to(field)
    sleep(0.3)
    if not i_market.click():
        print("Could not find i_market")
        return
    sleep(0.3)

    # Clear sold items
    while i_sold.find():
        i_sold.click()
        sleep(sleep_period)

    # Check there is a spare spot
    if not i_new_sale.click():
        print("No spare spot for sales")
        advertise_existing()
        i_market_cross.click()
        return
    sleep(0.3)

    tab = None

    item_sold = False
    for item in job.items:
        # Select a spare crate
        i_new_sale.click()
        sleep(0.2)

        # Select the appropriate tab
        # print("Item tab:", item, item.tab)
        if item.tab != tab:
            # print(f"Clicking on {item.tab}")
            item.tab.click()
            tab = item.tab
            sleep(sleep_period)

        still_selling, no_of_loops = True, 0

        while still_selling and no_of_loops <= 8:
            # Get Screenshot
            market = pyautogui.screenshot(region=MARKET_REGION)
            market.save("images/screen/temp_market.jpg")
            market_image = cv2.imread("images/screen/temp_market.jpg", cv2.IMREAD_COLOR)

            # Count and sell
            if item.image_market.find():
                try:
                    region = extract_region(item.image_market.image, market_image, 30, -20, 120, 120)
                    cv2.imwrite("images/screen/temp_market_region.jpg", region)
                    count = market_numbers.read(region)
                    if item.name != "Wheat" and count > 100: count = int(count / 10)
                    print(f"Market count ({item}): {count} vs Max: {item.max_no}", count >= item.max_no)
                    if count >= item.max_no:
                        sleep(sleep_period)
                        item.image_market.click()
                        sleep(sleep_period)
                        i_max_price.click()
                        sleep(sleep_period)
                        if i_advertise_now.find():
                            pyautogui.click(1290, 829)
                        sleep(sleep_period)
                        i_put_on_sale.click()
                        sleep(sleep_period)
                        item_sold = True
                    else:
                        still_selling = False
                except:
                    print(f"Could not see {item} in market")
                    still_selling = False
            if i_new_sale.find():
                i_new_sale.click()
                sleep(sleep_period)
            else:
                still_selling = False

            no_of_loops += 1

    sleep(0.2)
    i_market_cross_2.click()
    i_market_cross.click()
    sleep(0.2)

    return item_sold

def pause_field_production():
    pause_until = datetime.now() + timedelta(minutes=20)
    for job in jobs:
        if job.item and job.item.production == field:
            if job.runtime < pause_until:
                job.runtime = pause_until

def advertise_existing():
    print("Advertise existing - waiting 5 minutes")
    pause_field_production()
    if not i_roadside_shop.find():
        print("Not in the shop")
        return
    count, no_new_sales = 0, True
    while count < 5 * 10 and no_new_sales:
        if i_sold.find():
            no_new_sales = False
            i_sold.click()
        sleep(6)

    if no_new_sales:
        i_existing_sale_box.click()
        sleep(0.8)
        pyautogui.click(1189, 507)
        # pyautogui.click(1189, 507)
        sleep(0.3)
        i_create_advertisement.click()
        sleep(0.5)
