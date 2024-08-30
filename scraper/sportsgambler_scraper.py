import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.utils import scroll_down, wait_for_element
from config import URLS
from data import  predictions2

class SportsManGambler(webdriver.Chrome):
    def __init__(self, driver_path=r"chromedriver.exe", teardown=True):
        os.environ['PATH'] += os.pathsep + os.path.dirname(driver_path)
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        super(SportsManGambler, self).__init__(options=options)
        self.implicitly_wait(5)
        self.maximize_window()

    def __enter__(self):
        return self

    def land_first_page(self):
        self.get(URLS["sportsgambler"])

    def get_the_games(self):
        try:
            games_container = wait_for_element(self, By.CSS_SELECTOR, "div.bodds-container")
            full_game_elements = games_container.find_elements(By.CSS_SELECTOR, "div.bodds-row")
            return full_game_elements
        except Exception as e:
            print(f"Error retrieving games: {e}")
            return []

    def get_predictions(self):
        self.land_first_page()
        games = self.get_the_games() 
        for i in range(len(games)):
            if i == 0:
                continue
            game = games[i]
            self.scrape_prediction(game)

    def scrape_prediction(self,game):
        total = game.text
        lines = total.split("\n")
        team1 = lines[2].strip().lower()
        team2 = lines[4].strip().lower()
        p = float(lines[5].strip())
        d = float(lines[7].strip())
        tot = p + d
        team1per = p/tot
        team2per = d/tot
        predictions2.append({
            team1: team1per,
            team2: team2per,
        })

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
