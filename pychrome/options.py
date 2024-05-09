from typing import Union

from selenium import webdriver

from .useragent import UserAgentManager


class Options(webdriver.ChromeOptions):
    def __init__(
            self,
            headless: bool = True,
            incognito: bool = False,
            start_maximized: bool = True,
            window_size: tuple = None,
            disable_gpu: bool = False,
            user_agent: Union[str, UserAgentManager] = None,
            disable_notifications: bool = True,
            disable_infobars: bool = True,
            disable_javascript: bool = False,
            disable_images: bool = False,
            ignore_certificate_errors: bool = True,
            ignore_ssl_errors: bool = True
    ):
        super().__init__()
        self.headless = headless
        self.incognito = incognito
        self.start_maximized = start_maximized
        self.window_size = window_size
        self.disable_gpu = disable_gpu
        self.user_agent = user_agent
        self.disable_notifications = disable_notifications
        self.disable_infobars = disable_infobars
        self.disable_javascript = disable_javascript
        self.disable_images = disable_images
        self.ignore_certificate_errors = ignore_certificate_errors
        self.ignore_ssl_errors = ignore_ssl_errors

        self._set_options()

    def _set_options(self):
        if self.headless:
            self.add_argument('--headless')
        if self.incognito:
            self.add_argument('--incognito')
        if self.start_maximized:
            self.add_argument('--start-maximized')
        if self.window_size:
            self.add_argument(f'--window-size={self.window_size[0]},{self.window_size[1]}')
        if self.disable_gpu:
            self.add_argument('--disable-gpu')
        if isinstance(self.user_agent, str):
            self.add_argument(f'user-agent={self.user_agent}')
        if self.disable_notifications:
            self.add_argument('--disable-notifications')
        if self.disable_infobars:
            self.add_argument('--disable-infobars')
        if self.disable_javascript:
            self.add_argument('--disable-javascript')
        if self.disable_images:
            self.add_argument('--blink-settings=imagesEnabled=false')
        if self.ignore_certificate_errors:
            self.add_argument('--ignore-certificate-errors')
        if self.ignore_ssl_errors:
            self.add_argument('--ignore-ssl-errors')

        self.add_experimental_option('excludeSwitches', ['enable-automation'])
        return self
