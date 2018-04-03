import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .exceptions import InvalidLinkException


class DuckDuckGoBrowser:
    def __init__(self, query):
        self.query = query

    def get_driver(self, window_size='1280x720'):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--start-fullscreen')
        chrome_options.add_argument(f'window-size={window_size}')

        return webdriver.Chrome(chrome_options=chrome_options)

    def browse(self):
        driver = self.get_driver()
        driver.get(f'https://duckduckgo.com/?q={self.query}&ia=web')

        script = """
        results = document.getElementsByClassName('result__title');
        for (var i = 0; i < results.length; i++) {
            span_id = 'L' + (i+1);
            results[i].innerHTML += '<span id="' + span_id + '" style="color: red; margin-left: 10px;">' + span_id + '</span>';
        };
        """
        driver.execute_script(script)
        return driver.get_screenshot_as_base64()

    def access(self, link):
        pattern = re.compile(r'^L[0-9]+')
        if not pattern.match(link):
            raise InvalidLinkException(f'{link} is not a valid choice.')

        position = int(link[1]) - 1
        driver = self.get_driver(window_size='1280x2560')

        driver.get(f'https://duckduckgo.com/?q={self.query}&ia=web')

        a = driver.find_elements_by_class_name('result__title')[position].find_element_by_class_name('result__a')
        driver.get(a.get_attribute('href'))

        return driver.get_screenshot_as_base64()
