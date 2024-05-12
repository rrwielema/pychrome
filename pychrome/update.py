import re
import urllib.request
from zipfile import ZipFile

from .common import *


def get_chrome_version() -> tuple:
    stream = os.popen('reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon"')
    output = stream.read()
    regex = r'(\d+)\.(\d+)\.(\d+)\.(\d+)'
    version = re.findall(regex, output)[0]
    print(f'Current chrome version: {".".join(version)}')
    return version


def get_chromedriver_version() -> tuple | None:
    if not os.path.exists(CHROMEDRIVER_VERSION_FILE):
        print('No chromedriver version file found')
        return None
    with open(CHROMEDRIVER_VERSION_FILE, 'r') as f:
        regex = r'(\d+)\.(\d+)\.(\d+)\.(\d+)'
        version = re.findall(regex, f.read())[0]
        print(f'Current chromedriver version: {".".join(version)}')
        return version


def version_is_compatible() -> bool:
    chrome_version = get_chrome_version()
    chromedriver_version = get_chromedriver_version()
    if not chromedriver_version:
        return False
    conditions = [
        chrome_version[0] == chromedriver_version[0],
        chrome_version[1] == chromedriver_version[1],
        chrome_version[2] == chromedriver_version[2],
        int(chrome_version[3]) >= int(chromedriver_version[3])
    ]
    if all(conditions):
        return True
    if all(conditions[:-1]):
        print('Chromedriver version is outdated')
    if int(chrome_version[3]) < int(chromedriver_version[3]):
        print('Update your Google Chrome browser through the browser settings')
    return False


def get_latest_chromedriver_version() -> str:
    r = urllib.request.urlopen(LATEST_STABLE_URL)
    return r.read().decode('utf-8')


def extract_zip_file():
    with ZipFile(CHROMEDRIVER_ZIP_FILE, 'r') as z:
        z.extractall(PYCHROME_FOLDER)
    os.remove(CHROMEDRIVER_ZIP_FILE)
    os.rename(TEMP_CHROMEDRIVER_EXECUTABLE, CHROMEDRIVER_EXECUTABLE)
    for file in os.listdir(TEMP_CHROMEDRIVER_FOLDER):
        os.remove(os.path.join(TEMP_CHROMEDRIVER_FOLDER, file))
    os.rmdir(TEMP_CHROMEDRIVER_FOLDER)


def download_chromedriver():
    version = get_latest_chromedriver_version()
    print(f'Downloading chromedriver version {version}')
    download_url = DOWNLOAD_URL.format(version)
    urllib.request.urlretrieve(download_url, CHROMEDRIVER_ZIP_FILE)
    extract_zip_file()

    with open(CHROMEDRIVER_VERSION_FILE, 'w') as f:
        f.write(version)
    print(f'Chromedriver version {version} downloaded')
    print(20 * '=')


def chromedriver_exists() -> bool:
    return os.path.exists(CHROMEDRIVER_EXECUTABLE)


def chromedriver_folder_exists() -> bool:
    return os.path.exists(PYCHROME_FOLDER)


def update_driver():
    print('Checking for chromedriver updates')
    if not chromedriver_folder_exists():
        os.mkdir(PYCHROME_FOLDER)
    if not chromedriver_exists():
        print('No current chromedriver executable found')
        download_chromedriver()
        update_driver()
    elif not version_is_compatible():
        print('Status: NOT COMPATIBLE')
        os.remove(CHROMEDRIVER_EXECUTABLE)
        download_chromedriver()
        update_driver()
    else:
        print('Status: COMPATIBLE')
