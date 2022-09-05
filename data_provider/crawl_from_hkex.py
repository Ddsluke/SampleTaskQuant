import string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
# from urllib.request import urlopen
# from bs4 import BeautifulSoup


class HKEXReader(object):
    def __init__(self, date, connect_type, debug=False):
        if not debug:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("headless")

        self.driver = webdriver.Chrome(options=self.options)

        url = "https://www.hkex.com.hk/Mutual-Market/Stock-Connect/Statistics/Historical-Daily?sc_lang=en" # const
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])
        connect_options = ["Shanghai Connect Northbound", "Shanghai Connect Southbound", "Shenzhen Connect Northbound", "Shenzhen Connect Southbound"]
        connect_rel = dict(zip(connect_options, range(4)))

        pattern = f"#select4=0&select5={connect_rel[connect_type]}&select3={2022-year}&select2={month-1}&select1={day-1}"
        self.url_final = url + pattern

    def run(self):
        return self.get_info_selenium(self.url_final)

    def get_info_selenium(self, url, timeout=10):
        self.driver.get(url)
        # self._wait_strategy(timeout)
        try:
            table_trlist = self.driver.find_element("xpath", "//div[@id='tbl__1']/div/table").find_elements(By.TAG_NAME, "tr")
        except NoSuchElementException:
            print("Invalid date.")
            exit(0)
        table_th_list = table_trlist[0].find_elements(By.TAG_NAME, "th")
        lines_th = (list(map(lambda x: x.text, table_th_list)))

        trs = []
        for tr in table_trlist[1:]:
            tds = tr.find_elements(By.TAG_NAME, "td")
            tds_ = list(map(lambda x: x.text, tds))
            trs.append(tds_)

        return pd.DataFrame(trs, columns=lines_th)

    def _wait_strategy(self, timeout):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC  
        wait = WebDriverWait(self.driver, timeout)
        try:
            EC.text_to_be_present_in_element = self._text_to_be_present_in_element_
            _ = wait.until(EC.text_to_be_present_in_element((By.XPATH, "//div[@id='tbl__1']/div/table/tbody/tr/td[2]"), string.digits()))
        except:
            print("Timeout")
            return

    @staticmethod
    def _text_to_be_present_in_element_(locator, texts_):
        """ An expectation for checking if the given text is present in the
        specified element.
        locator, text
        """
        from selenium.common.exceptions import StaleElementReferenceException
        def _predicate(driver):
            try:
                element_text = driver.find_element(*locator).text
                for text_ in texts_:
                    if text_ in element_text:
                        print(element_text)
                        return True
            except StaleElementReferenceException:
                return False

        return _predicate


# Sample execution
if __name__ == "__main__":
    crawler = HKEXReader("20220904", "Shanghai Connect Southbound")
    print(crawler.run())