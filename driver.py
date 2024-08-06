from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os

def get_driver() -> webdriver.Firefox:

    options = Options()
    # options.add_argument('--headless')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(current_dir, 'temp')

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    firefox_profile = webdriver.FirefoxProfile()

    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.download.dir", download_dir)
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    firefox_profile.set_preference("pdfjs.disabled", True)  # PDF dosyasını doğrudan indirmek için PDF görüntüleyicisini devre dışı bırak

    options.profile = firefox_profile

    driver = webdriver.Firefox(options=options)
    
    return driver