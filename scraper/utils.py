import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_down(driver):
    """Scrolls down to the bottom of the page to load all content."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def wait_for_element(driver, by, value, timeout=10):
    """Waits for an element to appear on the page."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
