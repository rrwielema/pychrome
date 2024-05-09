import os


PYCHROME_FOLDER = os.path.join(os.getenv('APPDATA'), 'pychrome')
CHROMEDRIVER_FOLDER = os.path.join(PYCHROME_FOLDER, 'chromedriver-win32')
CHROMEDRIVER_ZIP_FILE = os.path.join(PYCHROME_FOLDER, 'chromedriver.zip')
CHROMEDRIVER_VERSION_FILE = os.path.join(PYCHROME_FOLDER, 'version.txt')
CHROMEDRIVER_EXECUTABLE_ = os.path.join(CHROMEDRIVER_FOLDER, 'chromedriver.exe')
CHROMEDRIVER_EXECUTABLE = os.path.join(PYCHROME_FOLDER, 'chromedriver.exe')

LATEST_STABLE_URL = 'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE'
DOWNLOAD_URL = 'https://storage.googleapis.com/chrome-for-testing-public/{}/win32/chromedriver-win32.zip'

USER_AGENT_DB = os.path.join(os.getenv('APPDATA'), 'pychrome', 'useragents.db')
