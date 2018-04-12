import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .exceptions import InvalidChoiceException


class DuckDuckGoBrowser:
    def __init__(self, query: str):
        self.query = query

    def get_driver(self, window_size='1280x720') -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--start-fullscreen')
        chrome_options.add_argument(f'window-size={window_size}')

        return webdriver.Chrome(chrome_options=chrome_options)

    def get_base64_image(self, driver: webdriver.Chrome) -> str:
        base64_image = driver.get_screenshot_as_base64()
        driver.close()
        return base64_image

    def results(self) -> str:
        driver = self.get_driver()
        driver.get(f'https://duckduckgo.com/?q={self.query}&ia=web')

        script = """
        results = document.getElementsByClassName('result__title');
        for (var i = 0; i < results.length; i++) {
            results[i].innerHTML += '<span style="color: red; margin-left: 10px;">' + (i+1) + '</span>';
        };
        """
        driver.execute_script(script)
        return self.get_base64_image(driver=driver)

    def result_page(self, choice: str) -> str:
        pattern = re.compile(r'^L[0-9]+')
        if not pattern.match(choice):
            raise InvalidChoiceException(f'"{choice}" is not a valid choice.')

        position = int(choice[1]) - 1
        driver = self.get_driver(window_size='1280x2560')

        driver.get(f'https://duckduckgo.com/?q={self.query}&ia=web')

        a = driver.find_elements_by_class_name('result__title')[position].find_element_by_class_name('result__a')
        driver.get(a.get_attribute('href'))

        return self.get_base64_image(driver=driver)
