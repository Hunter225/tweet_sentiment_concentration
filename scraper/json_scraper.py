from scraper.scraper import Scraper
import json

class JsonScraper(Scraper):
    def __init__(self, headers, url):
        super().__init__(self, headers, url)

    def parse_json(self):
        self.get_text()
        self.json_dict = json.loads(self.text)
        return
