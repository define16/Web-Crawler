from socket import socket

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import multiprocessing
import queue

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

    def scroll_down(self):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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




# 인스타그램 게시물 path ( 스캐너 쓰레드 1개)
# //*[@id=\"react-root\"]/section/main/article/div[1]/div/div/div[1]/div[1]/a
# //*[@id=\"react-root\"]/section/main/article/div[1]/div/div/div[1]/div[2]/a
#react-root > section > main > article > div.EZdmt > div > div > div:nth-of-type(1) > div:nth-of-type(1) > a
#react-root > section > main > article > div.EZdmt > div > div > div:nth-of-type(1) > div:nth-of-type(2) > a
def search(p, blockqu) :
    while True :
        keyword = str(input('[검색어] (종료 - q) :'))
        if keyword == "q" or keyword == "Q" :
            break
        # 여기서부터 제작 시작
        search_url = "https://www.instagram.com/explore/tags/" + keyword
        soup = p.getDataFromSoup(search_url)
        i = 1
        while True :
            notices = soup.select('#react-root > section > main > article > div.EZdmt > div > div > div:nth-of-type(1) > div:nth-of-type('+ str(i) +') > a')
            print(notices) # 비어 있음

            contents_url = "https://www.instagram.com" + notices.get('href')

            ## 블록 큐에 삽입
            # blockqu.put(contents_url);

            i+=1

# 멀티 쓰레드 ( 큐 안에 있는 )
def parsing_contents(blockqu) :
    # while True:
        # soup = p.getDataFromSoup(blockqu.get());
    pass


# main
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
        blockqu = queue.Queue(50)
        soup = p.getDataFromSoup(url)
        notices = soup.select('#react-root > section > main > article > div.rgFsT > div:nth-of-type(2) > p > a')
        url += notices[0].get('href')

        soup = p.getDataFromSoup(url)
        p.driver.find_element_by_name('username').send_keys(id);
        p.driver.find_element_by_name('password').send_keys(pw);

        p.driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/article/div/div[1]/div/form/div[4]/button ").click()

        # 알림 여부 팝업창
        try :
            p.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click()
        except selenium.common.exceptions.NoSuchElementException :
            pass



    ## 오류 ##
    # 검색어 입력
    pool_scan = multiprocessing.Pool(processes=1)
    p1 = pool_scan.Process(target=search, args=(p))
    p1.start()

    sleep(2)
    pool_scroll = multiprocessing.Pool(processes=1)
    p2 = pool_scroll.Process(target=p.scroll_down)
    p2.start()

    # 본문 저장
    pool_parsing = multiprocessing.Pool(processes=4)
    p3 = pool_parsing.Process(target=parsing_contents)
    p3.start()


    # 종료
    p1.join()
    pool_scan.join()
    pool_parsing.join()

    print("[Done]")