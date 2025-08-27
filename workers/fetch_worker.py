from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from datetime import datetime
import requests


class FetchWorker(QThread):
    finished = pyqtSignal(dict, object)
    progress = pyqtSignal(int)
    
    def __init__(self, hero_name, hero_mapper, secure_data):
        super().__init__()
        self.hero_name = hero_name
        self.hero_mapper = hero_mapper
        self.secure_data = secure_data
        self.driver = None
        
    def run(self):
        try:
            start = datetime.now()
            self.progress.emit(10)
            
            # Initialize webdriver only when needed (lazy loading)
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-images")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-application-cache")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-cache")
            options.add_argument("--disk-cache-size=0")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-logging")
            options.add_argument("--log-level=3")
            options.add_argument("--output=/dev/null")
            options.add_argument("--blink-settings=imagesEnabled=false")
            options.page_load_strategy = 'eager'
            self.driver = webdriver.Firefox(options=options)
            self.driver.implicitly_wait(2)
            
            self.progress.emit(30)
            url = f"https://dotabuff.com/heroes/{self.hero_name}/counters"
            
            self.progress.emit(40)
            hero_info = self.parse_hero_data(url)
            
            self.progress.emit(90)
            # Get hero image
            hero_image = self.get_hero_image(self.hero_name)
            
            self.progress.emit(100)
            self.finished.emit(hero_info, hero_image)
            
            print(datetime.now() - start)
        except Exception as e:
            print(f"Error fetching data: {e}")
            self.progress.emit(f"Error fetching data: {e}")
            self.finished.emit({}, None)
        finally:
            # Clean up driver
            if self.driver:
                self.driver.quit()
    
    def parse_hero_data(self, url: str):
        self.driver.get(url)
        
        hero_list = []
        counters_list = []
        winrate = "N/A"
        
        # Get counter peeks (heroes this hero counters)
        counter_peek_rows = self.driver.find_elements(
            By.CSS_SELECTOR, 
            "div.col-6:nth-child(1) > section:nth-child(1) > article:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr"
        )
        
        for row in counter_peek_rows[:6]:  # Limit to top 6
            try:
                hero_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
                hero_list.append(hero_name)
            except:
                continue
        
        # Get counters (heroes that counter this hero)
        counter_rows = self.driver.find_elements(
            By.CSS_SELECTOR, 
            "div.col-6:nth-child(2) > section:nth-child(1) > article:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr"
        )
        
        for row in counter_rows[:6]:  # Limit to top 6
            try:
                hero_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
                counters_list.append(hero_name)
            except:
                continue
        
        # Try to get winrate from the page
        try:
            # First check if winrate is available on the counters page
            winrate_element = self.driver.find_element(By.CSS_SELECTOR, "dd:nth-child(4)")
            winrate = winrate_element.text
        except:
            try:
                # Alternative selector for winrate
                winrate_element = self.driver.find_element(By.CSS_SELECTOR, ".won")
                winrate = winrate_element.text
            except:
                winrate = "N/A"
        
        info = {
            "Counter peeks": hero_list,
            "Countered by": counters_list,
            "Winrate": winrate
        }
        
        return info
    
    def get_hero_image(self, hero_name):
        steam_api_key = self.secure_data.retrieve_data("steam_api_key")
        image_name = self.hero_mapper.get_hero_image_name(hero_name)
        
        if not image_name:
            return None
            
        url = f"http://cdn.dota2.com/apps/dota2/images/heroes/{image_name}_full.png"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.content
        except:
            pass
            
        return None