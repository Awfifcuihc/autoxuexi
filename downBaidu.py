from selenium import  webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import requests

class downloader:
    def __init__(self):
        self.browser =webdriver.Chrome()
        self.wait =wait = WebDriverWait(self.browser,3)
        self.i=0
        self.pattern =re.compile('.*?url\("(.*?)"\)',re.S)
       

    def __call__(self,url):
        self.download(url)
        while True:
            for i in self.parse_link():
                self.save(i)
            
            sub =self.browser.find_element_by_id('next-pageList-1')
            self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded(true);",sub)
            sub.click()
            
                
        self.browser.quit()
        

    def download(self,url):
        self.browser.get(url)
        submit =self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="html-reader-go-more"]/div[2]/div[1]/span/span[1]')))
        self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded(true);",submit)
        submit.click()


                    
    def parse_link(self):
        self.elem=self.wait.until(EC.presence_of_element_located((By.ID,'reader-container-inner-1')))
        for i in self.elem.find_elements_by_class_name('bd'):
            try:
                self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded(true);",i)
                time.sleep(0.6)    
                i =i.find_element_by_class_name('reader-pic-item')
                        
                js=i.get_attribute('style')

                href =self.pattern.findall(js)
                yield href[0]
            except NoSuchElementException:
                continue

    def save(self,link):
        html =requests.get(link).content
        with open('{}.png'.format(self.i),'wb') as f:
            f.write(html)
        self.i +=1


D =downloader()
D('https://wenku.baidu.com/view/d86fe3436c175f0e7dd13731')