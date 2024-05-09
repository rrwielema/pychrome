import time

from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement


class Scroll:
    def __init__(self, driver):
        self.driver = driver

    @property
    def scroll_position(self) -> int:
        return self.driver.execute_script('return window.scrollY')

    def _scroll(self, direction: str):
        key = Keys.PAGE_DOWN if direction.lower() == 'down' else Keys.PAGE_UP

        last_scroll_position = self.scroll_position
        while True:
            self.driver.actions.send_keys(key).perform()
            time.sleep(0.1)
            if self.scroll_position == last_scroll_position:
                break
            last_scroll_position = self.scroll_position

    def to_bottom(self, element: WebElement = None):
        if not element:
            element = self.driver.get_element('body')
        self.driver.actions.move_to_element(element).perform()
        self._scroll('down')

    def to_top(self, element: WebElement = None):
        if not element:
            element = self.driver.get_element('body')
        self.driver.actions.move_to_element(element).perform()
        self._scroll('up')
