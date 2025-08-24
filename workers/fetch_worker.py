import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PyQt5.QtCore import QThread, pyqtSignal

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
            self.progress.emit(10)
            
            # Initialize webdriver only when needed (lazy loading)
            options = Options()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=options)
            self.driver.implicitly_wait(5)
            
            self.progress.emit(30)
            url = "https://dotabuff.com"
            path = f"/heroes/{self.hero_name}/counters"
            path2 = f"/heroes/{self.hero_name}"
            
            self.progress.emit(40)
            counters_link = self.parse(url, path)
            
            self.progress.emit(60)
            winrate_page = self.parse(url, path2)
            
            self.progress.emit(70)
            hero_info = self.get_hero_info(counters_link, winrate_page)
            
            
            self.progress.emit(90)
            # Get hero image
            hero_image = self.get_hero_image(self.hero_name)
            
            self.progress.emit(100)
            self.finished.emit(hero_info, hero_image)
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            self.finished.emit({}, None)
        finally:
            # Clean up driver
            if self.driver:
                self.driver.quit()
    
    def parse(self, url: str, path: str):
        self.driver.get(url + path)
        soup = bs(self.driver.page_source, "lxml")
        return soup

    def get_hero_info(self, soup, soup2):
        hero_list = list()
        counters_list = list()
        info = dict()
        x = 1
        
        while x <= 6:
            contrpeek = soup.select(f"div.col-6:nth-child(1) > section:nth-child(1) > article:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > td:nth-child(2)")
            counters = soup.select(f"div.col-6:nth-child(2) > section:nth-child(1) > article:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > td:nth-child(2)")
            x = x + 1
            
            for hvalue in contrpeek:
                hvalue = hvalue.string
                hero_list.append(hvalue)
            
            for value in counters:
                value = value.string
                counters_list.append(value)
        
        try:
            winrate = soup2.find("span", class_="won").get_text()
        except:
            winrate = "N/A"
        
        info.update({"Counter peeks": hero_list})
        info.update({"Countered by": counters_list})
        info.update({"Winrate": winrate})
        
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