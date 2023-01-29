import sys
sys.path.append(r"C:\Users\A\quant")

from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  

class SSEReader(object):
    def __init__(self, output_path, debug=False):
        self.options = webdriver.ChromeOptions()

        if not debug:
            self.options.add_argument("headless") # turn it off to see the visualized execution
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--allow-insecure-localhost")
            self.options.add_argument("--window-size=1280,800")
        prefs = {"download.default_directory": output_path}
        self.output_path = output_path
        self.options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=self.options)
        self.url = "http://www.sse.com.cn/market/othersdata/refinancing/" # const
    
    def run(self):
        return self.get_info_selenium(self.url)

    @staticmethod
    def getDownLoadedFileName(driver, waitTime):
        driver.execute_script("window.open()")
        # switch to new tab
        driver.switch_to.window(driver.window_handles[-1])
        # navigate to chrome downloads
        driver.get('chrome://downloads')
        # define the endTime
        endTime = time.time() + waitTime
        while True:
            try:
                # get downloaded percentage
                downloadPercentage = driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
                # check if downloadPercentage is 100 (otherwise the script will keep waiting)
                if downloadPercentage == 100:
                    # return the file name once the download is completed
                    return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
            except:
                pass
            time.sleep(1)
            if time.time() > endTime:
                break
    
    def get_info_selenium(self, url):
        # open url
        self.driver.get(url)
        # wait 30 second until page loaded
        _ = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.LINK_TEXT, u"下载数据"))
        )

        # download
        self.driver.find_element(By.LINK_TEXT, u"下载数据").click()

        # get downloaded filename
        latestDownloadedFileName = self.getDownLoadedFileName(self.driver, 10) # waiting 3 minutes to complete the download
        print(latestDownloadedFileName)
        self.driver.quit()  
        return str(Path(self.output_path) / latestDownloadedFileName)


if __name__ == "__main__":
    crawler = SSEReader(r"C:\Users\A\quant\downloaded", debug=True) # modified the filepath accordingly
    print(crawler.run())