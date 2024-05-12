import time
from typing import Union

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.webdriver.remote.webelement import WebElement

from .common import CHROMEDRIVER_EXECUTABLE
from .options import Options
from .scroll import Scroll
from .update import update_driver
from .useragent import UserAgentManager
from .wait import Wait, TimeoutSetting


class Driver(webdriver.Chrome):
    def __init__(self, options: Options = None):
        if not options:
            options = Options()
        update_driver()
        super().__init__(service=Service(CHROMEDRIVER_EXECUTABLE), options=options)
        self.options = options
        self.actions = webdriver.ActionChains(self)
        self.wait = Wait(self)
        self.scroll = Scroll(self)

    def refresh_user_agent(self, user_agent: str = None):
        if not user_agent:
            user_agent = self.options.user_agent
        if isinstance(self.options.user_agent, UserAgentManager):
            self.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': str(user_agent)})

    def get(self, url: str, sleep: int = 0, new_tab: bool = False):
        self.refresh_user_agent()
        if new_tab:
            self.execute_script(f'window.open("{url}");')
            self.switch_to.window(self.window_handles[-1])
        else:
            super().get(url)
            self.wait.for_page_to_load(timeout=1, timeout_setting=TimeoutSetting.RAISE)
        if sleep:
            time.sleep(sleep)

    def _get_element_by_text(self, text: str, results: list = None, root: WebElement = None):
        if not root:
            root = self.get_element('html')
        if not results:
            results = []
        children = [child for child in self.get_elements('./child::*', by=By.XPATH, element=root)]
        useful_children = [child for child in children if text.lower() in child.text.lower()]
        if not useful_children and text.lower() in root.text.lower():
            results.append(root)
            return results
        for child in useful_children:
            return self._get_element_by_text(text, results, child)

    def get_element(self, selector: str, by: By = By.CSS_SELECTOR, element: WebElement = None):
        if element:
            return element.find_element(by=by, value=selector)
        return super().find_element(by=by, value=selector)

    def get_elements(self, selector: str, by: By = By.CSS_SELECTOR, element: WebElement = None):
        if element:
            return element.find_elements(by=by, value=selector)
        return super().find_elements(by=by, value=selector)

    def get_element_by_text(self, text: str, element: WebElement = None):
        result = self._get_element_by_text(text, root=element)
        if result:
            return result[0]

    def get_elements_by_text(self, text: str, element: WebElement = None):
        return self._get_element_by_text(text=text, root=element)

    def get_shadow_root(self, selector: str, shadow_host: WebElement | ShadowRoot = None) -> ShadowRoot | None:
        if not shadow_host:
            shadow_host = self.get_element('body')
        element = shadow_host.find_elements(by=By.CSS_SELECTOR, value=selector)
        if not element:
            return None
        return self.execute_script('return arguments[0].shadowRoot', element[0])

    def get_shadow_root_layers(self, selectors: list):
        element = self.get_shadow_root(selectors[0])
        for selector in selectors[1:]:
            element = self.get_shadow_root(selector, element)
        return element

    def click_element(self, selector: Union[str, WebElement], by: By = By.CSS_SELECTOR, element: WebElement = None):
        if isinstance(selector, WebElement):
            element = selector
        else:
            element = self.get_element(selector, by, element)
        self.execute_script('arguments[0].click();', element)

    def fill_element(self, element: Union[str, WebElement], text: str, pause: float = 0, clear_first: bool = True,
                     by: By = By.CSS_SELECTOR):
        if isinstance(element, str):
            element = self.get_element(element, by)

        if clear_first:
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.DELETE)

        if pause == 0:
            element.send_keys(text)
        else:
            for k in text:
                element.send_keys(k)
                time.sleep(pause)

    def send_keys(self, keys: str, element: Union[str, WebElement], clear_first: bool = True):
        if isinstance(element, str):
            element = self.get_element(element)

        if clear_first:
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.DELETE)
        element.send_keys(keys)
