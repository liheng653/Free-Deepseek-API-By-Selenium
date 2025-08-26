from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException
import json,os

COOKIEPATH = "cookies.json"
edge_options = Options()
#edge_options.add_argument("--disable-blink-features=AutomationControlled")
#edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#edge_options.add_experimental_option('useAutomationExtension', False)
edge_options.add_argument("--headless=new")
#edge_options.add_argument("--user-data-dir=User Data")


class Deepseek:
    def _login(self,driver,phonenum,password):
        driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div').click()
        driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[1]/div[3]/div[1]/div/input').send_keys(phonenum)
        driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[1]/div[4]/div[1]/div/input').send_keys(password)
        driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[1]/div[6]').click()
        with open(COOKIEPATH,'w') as f:
            json.dump(driver.get_cookies(),f)

    def locateElem(self):

        self.msgbar = self.driver.find_element(By.ID,'chat-input')
        self.chattoolbar = self.driver.find_element(By.CLASS_NAME,'ec4f5d61')
        self._deepthink,self._search,_ = self.chattoolbar.find_elements(By.CSS_SELECTOR,"div[role='button']")
        self._send = self.chattoolbar.find_element(By.CLASS_NAME,'bf38813a').find_element(By.CSS_SELECTOR,"div[role='button']")
        self._file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")


    def __init__(self,phonenum,password) -> None:

        driver = webdriver.Edge(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe",options=edge_options)
        driver.get("https://chat.deepseek.com")
#        if os.path.exists(COOKIEPATH):
#            with open(COOKIEPATH,'r') as f:
#                driver.delete_all_cookies()
#                for cookie in json.load(f):
#                    driver.add_cookie(cookie)
#            driver.get("https://chat.deepseek.com")

        if 'sign_in' in driver.current_url:
            print(driver.get_cookies())
            self._login(driver,phonenum,password)
            print("Failed to load cookies.")
        self.driver = driver

        wait = WebDriverWait(self.driver,timeout=5,poll_frequency=.2,ignored_exceptions=[NoSuchElementException])
        def get_chatbar_callback(_):
            self.chatbar = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div')
            return True
        wait.until(get_chatbar_callback)

        self.locateElem()
        
        self.history = []
        self.setDeepThink(True)
        self.setSearch(True)

    def uploadFile(self,path):
        self._file_input.send_keys(path)
        self.driver.find_element(By.ID, "file-submit").click()

    def setDeepThink(self,stat):
        if stat != self.isDeepThinkOn():
            self._deepthink.click()

    def setSearch(self,stat):
        if stat != self.isSearchOn():
            self._search.click()

    def isDeepThinkOn(self):
        bdcolor = self._deepthink.get_attribute('style')
        assert 'rgba(0, 122, 255, 0.15)'in bdcolor or 'rgba(0, 0, 0, 0.12)' in bdcolor
        return 'rgba(0, 122, 255, 0.15)' in bdcolor

    def isSearchOn(self):
        bdcolor = self._deepthink.get_attribute('style')
        assert 'rgba(0, 122, 255, 0.15)'in bdcolor or 'rgba(0, 0, 0, 0.12)' in bdcolor
        return 'rgba(0, 122, 255, 0.15)' in bdcolor

    def _lastMsg(self,usrmsg):
        wait = WebDriverWait(self.driver,timeout=200,poll_frequency=1,ignored_exceptions=[NoSuchElementException,IndexError])

        def cb(_):
            return self.driver.find_element(By.CLASS_NAME,'dad65929').find_elements(By.CSS_SELECTOR,'._4f9bf79.d7dc56a8._43c05b5')[-1]
        x = wait.until(cb)
        answer = x.find_element(By.CSS_SELECTOR,".ds-markdown.ds-markdown--block").text
        self.history.append({'user':usrmsg,'ds':answer})
        self.locateElem()
        return answer

        
    def send(self,text):
        self.msgbar.send_keys(text)
        self.chattoolbar.find_element(By.CLASS_NAME,'bf38813a').find_element(By.CSS_SELECTOR,"div[role='button']").click()
        return self._lastMsg(text)





    def __del__(self):
        self.driver.quit()

    


