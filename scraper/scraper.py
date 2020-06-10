import urllib
import ssl

class Scraper():
    def __init__(self, headers, url):
        self.headers = headers
        self.url = url
        self.text = None

    def get_text(self):
        request = urllib.request.Request(self.url, headers=self.headers)
        response = urllib.request.urlopen(request, context=ssl.SSLContext())
        self.text = str(response.read().decode('utf-8'))
        return
    
    def save_text(self, file_name):
        with open('training_set/%s' % file_name, 'w') as output_file:
            output_file.write(self.text)
        return