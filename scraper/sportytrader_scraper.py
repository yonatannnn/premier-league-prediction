import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.utils import scroll_down, wait_for_element
from config import URLS
from data import predictions3

class SportyTrader(webdriver.Chrome):
    def __init__(self, driver_path=r"chromedriver.exe", teardown=True):
        os.environ['PATH'] += os.pathsep + os.path.dirname(driver_path)
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        super(SportyTrader, self).__init__(options=options)
        self.implicitly_wait(5)
        self.maximize_window()

    def __enter__(self):
        return self

    def land_first_page(self):
        self.get(URLS["sportytrader"])

    def get_the_games(self):
        try:
            games_container = wait_for_element(self, By.ID, "1x2wrap")
            full_game_elements = games_container.find_elements(By.XPATH, ".//*[contains(@class, 'p-2') and contains(@class, 'items-center')]")

            return full_game_elements
        except Exception as e:
            print(f"Error retrieving games: {e}")
            return []

    def get_predictions(self):
        self.land_first_page()
        games = self.get_the_games() 
        for i in range(len(games)):
            game = games[i]
            self.scrape_prediction(game)

    def scrape_prediction(self,game):
        odds = game.find_element(By.CLASS_NAME , "w-36")
        spans = odds.find_elements(By.TAG_NAME , "span")
        winner = 0
        for i in range(len(spans)):
            class_attribute = spans[i].get_attribute("class")
            if "bg-primary-green" in class_attribute:
                winner = spans[i].text
        lines = game.text.split("\n")
        team1 = lines[2].lower()
        team2 = lines[3].lower()
        prc = int(lines[7].split(" ")[-1][:2])
        if winner == 'X':
            return
        if winner == '1':
            predictions3.append({
                team1: prc/100,
                team2: 1 - prc/100
            })
        if winner == '2':
            predictions3.append({
                team1: 1 - prc/100,
                team2: prc/100
            })

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
