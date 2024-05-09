import time
from typing import Union
from enum import Enum

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class TimeoutSetting(Enum):
    IGNORE = 0
    RAISE = 1
    LOG = 2

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        return super().__eq__(other)


class Wait:
    """A wrapper for WebDriverWait that allows for more flexibility in timeout handling."""

    def __init__(self, driver):
        self.driver = driver
        self._timeout = 10
        self._timeout_setting = TimeoutSetting.RAISE
        self._wait = None

    @staticmethod
    def _timeout_manager(func):
        def wrapper(self, *args, **kwargs):
            timeout = kwargs.get('timeout', self._timeout)
            self._wait = WebDriverWait(self.driver, timeout)

            timeout_setting = kwargs.get('timeout_setting', self._timeout_setting)
            if timeout_setting == TimeoutSetting.IGNORE:
                try:
                    return func(self, *args, **kwargs)
                except TimeoutException:
                    return None
            elif timeout_setting == TimeoutSetting.LOG:
                try:
                    return func(self, *args, **kwargs)
                except TimeoutException:
                    print(f'TimeoutException occurred in {func.__name__}')
                    return None
            else:
                return func(self, *args, **kwargs)

        return wrapper

    @_timeout_manager
    def for_page_to_load(self, timeout: int = None, timeout_setting: Union[int, TimeoutSetting] = None):
        self._wait.until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')

    @_timeout_manager
    def for_dom_ready(self, timeout: int = None, timeout_setting: Union[int, TimeoutSetting] = None):
        self._wait.until(lambda driver: driver.execute_script('return document.readyState;') == 'interactive')

    @_timeout_manager
    def for_presence_of_element(self, selector: Union[str, WebElement], by: By = By.CSS_SELECTOR, timeout: int = None,
                                timeout_setting: Union[int, TimeoutSetting] = None) -> Union[WebElement, None]:
        element = (by, selector) if isinstance(selector, str) else selector
        return self._wait.until(EC.presence_of_element_located(element))

    @_timeout_manager
    def for_element_to_be_clickable(self, selector: Union[str, WebElement], by: By = By.CSS_SELECTOR,
                                    timeout: int = None, timeout_setting: Union[int, TimeoutSetting] = None
                                    ) -> Union[WebElement, None]:
        element = (by, selector) if isinstance(selector, str) else selector
        return self._wait.until(EC.element_to_be_clickable(element))

    @_timeout_manager
    def for_visibility_of_element(self, selector: Union[str, WebElement], by: By = By.CSS_SELECTOR, timeout: int = None,
                                  timeout_setting: Union[int, TimeoutSetting] = None) -> Union[WebElement, None]:
        element = (by, selector) if isinstance(selector, str) else selector
        return self._wait.until(EC.visibility_of_element_located(element))

    @_timeout_manager
    def for_element_to_contain_text(self, selector: Union[str, WebElement], text: str, by: By = By.CSS_SELECTOR,
                                    element: Union[WebElement, None] = None, timeout: int = None,
                                    timeout_setting: Union[int, TimeoutSetting] = None
                                    ) -> Union[WebElement, None]:
        total_time = 0
        while True:
            time.sleep(0.2)
            target = self.driver.get_elements(selector, by, element) if isinstance(selector, str) else [selector]
            if not target:
                continue
            if text in target[0].text:
                return target
            total_time += 0.2
            if total_time >= timeout:
                raise TimeoutException

    @_timeout_manager
    def for_element_to_have_attribute_with_text(self, selector: Union[str, WebElement], attribute: str, text: str,
                                                by: By = By.CSS_SELECTOR, timeout: int = None,
                                                timeout_setting: Union[int, TimeoutSetting] = None
                                                ) -> Union[WebElement, None]:
        element = (by, selector) if isinstance(selector, str) else selector
        return self._wait.until(EC.text_to_be_present_in_element_attribute(element, attribute, text))

    @_timeout_manager
    def for_url_to_be(self, expected_url: str, timeout: int = None,
                      timeout_setting: Union[int, TimeoutSetting] = None) -> str:
        return self._wait.until(EC.url_changes(expected_url))

    @_timeout_manager
    def for_url_to_contain(self, text: str, timeout: int = None, timeout_setting: Union[int, TimeoutSetting] = None
                           ) -> str:
        return self._wait.until(EC.url_contains(text))

    @_timeout_manager
    def for_url_to_match(self, regex: str, timeout: int = None,
                         timeout_setting: Union[int, TimeoutSetting] = None) -> str:
        return self._wait.until(EC.url_matches(regex))
