from scraper.scraper import Scraper
from bs4 import BeautifulSoup

class Bs4Scraper(Scraper):
    def __init__(self, headers, url):
        self.headers = headers
        self.url = url
        self.text = None

    def create_soup(self, parser):
        self.get_text()
        self.soup = BeautifulSoup(self.text, parser)
    
    def remove_tags(self):
        self.text = str(self.soup.get_text())