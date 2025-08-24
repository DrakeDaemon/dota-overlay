import json

class HeroMapper:
    def __init__(self):
        self.hero_map = {}
        self.load_hero_mapping()
        
    def load_hero_mapping(self):
        try:
            with open('hero_mapping.json', 'r') as f:
                data = json.load(f)
                self.hero_map = data.get('heroes', {})
        except FileNotFoundError:
            # Fallback to default mapping if file not found
            self.setup_default_mapping()
        except json.JSONDecodeError:
            # Fallback to default mapping if JSON is invalid
            self.setup_default_mapping()
            
    def setup_default_mapping(self):
        # This is a fallback in case the JSON file is missing or corrupted
        self.hero_map = {
            "abaddon": {"id": 102, "name": "abaddon"},
            "alchemist": {"id": 73, "name": "alchemist"},
            "ancient-apparition": {"id": 68, "name": "ancient_apparition"},
            "anti-mage": {"id": 1, "name": "antimage"},
            "arc-warden": {"id": 113, "name": "arc_warden"},
            "axe": {"id": 2, "name": "axe"},
            "bane": {"id": 3, "name": "bane"},
            "batrider": {"id": 65, "name": "batrider"},
            "beastmaster": {"id": 38, "name": "beastmaster"},
            "bloodseeker": {"id": 4, "name": "bloodseeker"},
            "bounty-hunter": {"id": 62, "name": "bounty_hunter"},
            "brewmaster": {"id": 78, "name": "brewmaster"},
            "bristleback": {"id": 99, "name": "bristleback"},
            "broodmother": {"id": 61, "name": "broodmother"},
            "centaur-warrunner": {"id": 96, "name": "centaur"},
            "chaos-knight": {"id": 81, "name": "chaos_knight"},
            "chen": {"id": 66, "name": "chen"},
            "clinkz": {"id": 56, "name": "clinkz"},
            "clockwerk": {"id": 51, "name": "rattletrap"},
            "crystal-maiden": {"id": 5, "name": "crystal_maiden"},
            "dark-seer": {"id": 55, "name": "dark_seer"},
            "dark-willow": {"id": 119, "name": "dark_willow"},
            "dawnbreaker": {"id": 135, "name": "dawnbreaker"},
            "dazzle": {"id": 50, "name": "dazzle"},
            "death-prophet": {"id": 43, "name": "death_prophet"},
            "disruptor": {"id": 87, "name": "disruptor"},
            "doom": {"id": 69, "name": "doom_bringer"},
            "dragon-knight": {"id": 49, "name": "dragon_knight"},
            "drow-ranger": {"id": 6, "name": "drow_ranger"},
            "earth-spirit": {"id": 107, "name": "earth_spirit"},
            "earthshaker": {"id": 7, "name": "earthshaker"},
            "elder-titan": {"id": 103, "name": "elder_titan"},
            "ember-spirit": {"id": 106, "name": "ember_spirit"},
            "enchantress": {"id": 58, "name": "enchantress"},
            "enigma": {"id": 33, "name": "enigma"},
            "faceless-void": {"id": 41, "name": "faceless_void"},
            "grimstroke": {"id": 121, "name": "grimstroke"},
            "gyrocopter": {"id": 72, "name": "gyrocopter"},
            "hoodwink": {"id": 123, "name": "hoodwink"},
            "huskar": {"id": 59, "name": "huskar"},
            "invoker": {"id": 74, "name": "invoker"},
            "io": {"id": 91, "name": "wisp"},
            "jakiro": {"id": 64, "name": "jakiro"},
            "juggernaut": {"id": 8, "name": "juggernaut"},
            "keeper-of-the-light": {"id": 90, "name": "keeper_of_the_light"},
            "kunkka": {"id": 23, "name": "kunkka"},
            "legion-commander": {"id": 104, "name": "legion_commander"},
            "leshrac": {"id": 52, "name": "leshrac"},
            "lich": {"id": 31, "name": "lich"},
            "lifestealer": {"id": 54, "name": "life_stealer"},
            "lina": {"id": 25, "name": "lina"},
            "lion": {"id": 26, "name": "lion"},
            "lone-druid": {"id": 80, "name": "lone_druid"},
            "luna": {"id": 48, "name": "luna"},
            "lycan": {"id": 77, "name": "lycan"},
            "magnus": {"id": 97, "name": "magnataur"},
            "marci": {"id": 136, "name": "marci"},
            "mars": {"id": 129, "name": "mars"},
            "medusa": {"id": 94, "name": "medusa"},
            "meepo": {"id": 82, "name": "meepo"},
            "mirana": {"id": 9, "name": "mirana"},
            "monkey-king": {"id": 114, "name": "monkey_king"},
            "morphling": {"id": 10, "name": "morphling"},
            "naga-siren": {"id": 89, "name": "naga_siren"},
            "natures-prophet": {"id": 53, "name": "furion"},
            "necrophos": {"id": 36, "name": "neroclyte"},
            "night-stalker": {"id": 60, "name": "night_stalker"},
            "nyx-assassin": {"id": 88, "name": "nyx_assassin"},
            "ogre-magi": {"id": 84, "name": "ogre_magi"},
            "omniknight": {"id": 57, "name": "omniknight"},
            "oracle": {"id": 111, "name": "oracle"},
            "outworld-destroyer": {"id": 76, "name": "obsidian_destroyer"},
            "pangolier": {"id": 120, "name": "pangolier"},
            "phantom-assassin": {"id": 44, "name": "phantom_assassin"},
            "phantom-lancer": {"id": 12, "name": "phantom_lancer"},
            "phoenix": {"id": 110, "name": "phoenix"},
            "puck": {"id": 13, "name": "puck"},
            "pudge": {"id": 14, "name": "pudge"},
            "pugna": {"id": 45, "name": "pugna"},
            "queen-of-pain": {"id": 39, "name": "queenofpain"},
            "razor": {"id": 15, "name": "razor"},
            "riki": {"id": 32, "name": "riki"},
            "rubick": {"id": 86, "name": "rubick"},
            "sand-king": {"id": 16, "name": "sand_king"},
            "shadow-demon": {"id": 79, "name": "shadow_demon"},
            "shadow-fiend": {"id": 11, "name": "nevermore"},
            "shadow-shaman": {"id": 27, "name": "shadow_shaman"},
            "silencer": {"id": 75, "name": "silencer"},
            "skywrath-mage": {"id": 101, "name": "skywrath_mage"},
            "slardar": {"id": 28, "name": "slardar"},
            "slark": {"id": 93, "name": "slark"},
            "snapfire": {"id": 128, "name": "snapfire"},
            "sniper": {"id": 35, "name": "sniper"},
            "spectre": {"id": 67, "name": "spectre"},
            "spirit-breaker": {"id": 71, "name": "spirit_breaker"},
            "storm-spirit": {"id": 17, "name": "storm_spirit"},
            "sven": {"id": 18, "name": "sven"},
            "techies": {"id": 105, "name": "techies"},
            "templar-assassin": {"id": 46, "name": "templar_assassin"},
            "terrorblade": {"id": 109, "name": "terrorblade"},
            "tidehunter": {"id": 29, "name": "tidehunter"},
            "timbersaw": {"id": 98, "name": "shredder"},
            "tinker": {"id": 34, "name": "tinker"},
            "tiny": {"id": 19, "name": "tiny"},
            "treant-protector": {"id": 83, "name": "treant"},
            "troll-warlord": {"id": 95, "name": "troll_warlord"},
            "tusk": {"id": 100, "name": "tusk"},
            "underlord": {"id": 108, "name": "abyssal_underlord"},
            "undying": {"id": 85, "name": "undying"},
            "ursa": {"id": 70, "name": "ursa"},
            "vengeful-spirit": {"id": 20, "name": "vengefulspirit"},
            "venomancer": {"id": 40, "name": "venomancer"},
            "viper": {"id": 47, "name": "viper"},
            "visage": {"id": 92, "name": "visage"},
            "void-spirit": {"id": 126, "name": "void_spirit"},
            "warlock": {"id": 37, "name": "warlock"},
            "weaver": {"id": 63, "name": "weaver"},
            "windranger": {"id": 21, "name": "windrunner"},
            "winter-wyvern": {"id": 112, "name": "winter_wyvern"},
            "witch-doctor": {"id": 30, "name": "witch_doctor"},
            "wraith-king": {"id": 42, "name": "skeleton_king"},
            "zeus": {"id": 22, "name": "zuus"}
        }
    
    def get_hero_id(self, hero_name):
        return self.hero_map.get(hero_name, {}).get("id", None)
    
    def get_hero_image_name(self, hero_name):
        return self.hero_map.get(hero_name, {}).get("name", None)
    
    def get_hero_names(self):
        return list(self.hero_map.keys())