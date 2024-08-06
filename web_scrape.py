from driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

def web_scrape(doc_code: str, id_number: str):
        
        driver = get_driver()
        driver.get('https://www.turkiye.gov.tr/belge-dogrulama')

        #Page 1
        doc_code_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "sorgulananBarkod"))
        )
        doc_code_input.send_keys(doc_code)
        doc_code_submit = driver.find_element(By.NAME, 'btn')
        driver.execute_script('arguments[0].click();', doc_code_submit)

        #Page 2
        id_number_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ikinciAlan"))
        )
        id_number_input.send_keys(id_number)
        id_number_submit = driver.find_element(By.NAME, 'btn')
        driver.execute_script('arguments[0].click();', id_number_submit)

        #Page3
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "chkOnay"))
        )
        driver.execute_script('arguments[0].click();', checkbox)
        checkbox_submit = driver.find_element(By.NAME, 'btn')
        driver.execute_script('arguments[0].click();', checkbox_submit)

        #Last Page
        try:
            pdf = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.TAG_NAME, "object"))
            )
        except TimeoutException:
            raise TimeoutException('Document could not be verified.')

        pdf_download = WebDriverWait(pdf, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        driver.execute_script('arguments[0].click();', pdf_download)

        time.sleep(1)

        driver.quit()
        driver.close()