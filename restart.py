from image import *


def restart(job):
    close_app()
    open_app()

def close_app():
    pyautogui.press("f11")
    sleep(0.5)
    i_bluestacks_cross.click()
    sleep(0.5)
    i_bluestacks_icon.click()


def open_app():
    i_bluestacks_toolbar_icon.click()
    found = wait_for_images(images_to_click=[i_heyday_icon_small, i_hay_day_start_icon], destination_image=i_house_small, time_seconds=120)
    if found:
        sleep(1)
        position = i_house_small.find()
        pyautogui.moveTo(add(position, (100,0)))
    pyautogui.press("f11")
    zoom()

# pyautogui.hotkey('alt', 'tab')
# sleep(0.5)
# restart()
# sleep(0.5)
# pyautogui.hotkey('alt', 'tab')
