import requests

class ImageCache:
    def __init__(self):
        self.cache = {}
        
    def get_image(self, hero_name, hero_mapper, secure_data):
        if hero_name in self.cache:
            return self.cache[hero_name]
        
        # Fetch image if not in cache
        steam_api_key = secure_data.retrieve_data("steam_api_key")  # noqa: F841
        image_name = hero_mapper.get_hero_image_name(hero_name)
        
        if not image_name:
            return None
            
        url = f"http://cdn.dota2.com/apps/dota2/images/heroes/{image_name}_full.png"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                self.cache[hero_name] = response.content
                return response.content
        except:
            pass
            
        return None