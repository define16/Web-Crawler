from socket import socket

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium.common.exceptions import ElementNotVisibleException
import csv


class Parsing :
    global driver
    global html
    global soup
    flag = True

    def __init__(self,flag):
        if flag == 0 :
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('disable-gpu')
            self.driver = webdriver.Chrome("D:/Programing Folder/Tools/chromedriver_win32/chromedriver.exe", options=options)
        else :
            self.driver = webdriver.Chrome("D:/Programing Folder/Tools/chromedriver_win32/chromedriver.exe")

        self.driver.implicitly_wait(3)

    # 데이터 가지고 오기
    def getDataFromSoup(self, url):
        sleep(3)
        self.driver.get(url)
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, 'html.parser')

        return self.soup;

    def button_click(self,btn_xpath):
        delay = 10  # seconds
        print("delay :", delay)
        wait = WebDriverWait(self.driver, delay)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"react-root\"]/section/main/article/div[2]/div[2]/p/a")))


    def saveFile(self,Path, mlist):
        file = open(Path, 'a', newline='')
        csvFile = csv.writer(file)
        csvFile.writerow(['날짜','본문','해시태크'])
        csvFile.writerow(mlist)
        self.flag = False
        file.close()

def login() :
    isLogin = int(input('로그인 상태면 0, 아니면 1 입력 :'))
    if isLogin == 1 :
        id = str(input('ID : '))
        pw = str(input('PW : '))

        return id, pw
    else :
        return '',''

def search(p) :
    keyword = str(input('[검색어] :'))
    # 여기서부터 제작 시작
    p.driver.find_element_by_name('username').send_keys(id);


    pass


if __name__ == '__main__':
    isChromDriver = int(input('[ Chrom Driver : Inactive - 0, Active - 1 ] 입력 :'))
    id, pw = login()
    url = 'https://www.instagram.com'
    print("ID :", id, "PW :", pw)
    p = Parsing(isChromDriver)

    if id == '' and pw == '' :
        pass
    else :
        # 로그인
        soup = p.getDataFromSoup(url)
        notices = soup.select('#react-root > section > main > article > div.rgFsT > div:nth-of-type(2) > p > a')
        url += notices[0].get('href')

        soup = p.getDataFromSoup(url)
        p.driver.find_element_by_name('username').send_keys(id);
        p.driver.find_element_by_name('password').send_keys(pw);

        p.driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/article/div/div[1]/div/form/div[4]/button").click()

        # 알림 여부 팝업창
        try :
            print(p.driver.find_element_by_xpath("/html/body/div[3]/div"))
            p.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click()
        except selenium.common.exceptions.NoSuchElementException :
            pass

    # 검색어 입력
    search(p)


    print("[Done]")