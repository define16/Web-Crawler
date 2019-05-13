import os
import selenium
import queue
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random
import platform

from tqdm import tqdm
import threading
from queue import Queue

import csv


class Parsing :
    driver = None
    html = None
    soup = None
    flag = True

    def __init__(self,flag):
        options = webdriver.ChromeOptions()
        if flag == 0 :
            options.add_argument('headless')
            options.add_argument('disable-gpu')

            self.driver = webdriver.Chrome("D:/Programing Folder/Tools/chromedriver_win32/chromedriver.exe", options=options)
        elif flag == 1 :
            if platform.system() == 'Windows':
                options.add_argument("--start-maximized")
            else :
                options.add_argument("--kiosk")
            self.driver = webdriver.Chrome("D:/Programing Folder/Tools/chromedriver_win32/chromedriver.exe" ,options=options)

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

    def getDriver(self, url):
        sleep(3)
        self.driver.get(url)

    def button_click(self,btn_xpath):
        delay = 10  # seconds
        print("delay :", delay)
        wait = WebDriverWait(self.driver, delay)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"react-root\"]/section/main/article/div[2]/div[2]/p/a")))

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def find_one(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
            WebDriverWait(obj, waittime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )

        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None



    def find(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
            WebDriverWait(obj, waittime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )

        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def scroll_down(self, wait=0.3):
        self.driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight)')
        self.randmized_sleep(wait)

    def scroll_up(self, offset=-1, wait=2):
        if (offset == -1):
            self.driver.execute_script('window.scrollTo(0, 0)')
        else:
            self.driver.execute_script('window.scrollBy(0, -%s)' % offset)
        self.randmized_sleep(wait)

    def randmized_sleep(self, average=1):
        _min, _max = average * 1 / 2, average * 3 / 2
        sleep(random.uniform(_min, _max))

    def saveFile(self,Path, mlist):
        if not os.path.exists(os.path.abspath("saveFile")) :
            os.makedirs(os.path.abspath("saveFile"))
        file = open(Path, 'a', encoding="utf-8", newline='')
        csvFile = csv.writer(file)
        for row in mlist :
            csvFile.writerow(row) # ['날짜', '본문', '해시태크']
        self.flag = False
        file.close()

def login() :
    isLogin = int(input('비로그인 모드 : 0, 로그인 모드 1 입력 :'))
    if isLogin == 1 :
        id = str(input('ID : '))
        pw = str(input('PW : '))

        return id, pw
    else :
        return '',''



def search() :
    global search_flag
    p = Parsing(isChromDriver_search)
    TIMEOUT = 20
    pre_post_num = 0
    wait_time = 1
    url_set = set()
    id, pw = login()
    url = 'https://www.instagram.com'

    if id == '' and pw == '' :
        pass
    else :
        # 로그인
        print("ID :", id, "PW :", pw)
        soup = p.getDataFromSoup(url)
        notices = soup.select('#react-root > section > main > article > div.rgFsT > div:nth-of-type(2) > p > a')
        url += notices[0].get('href')

        p.getDriver(url)
        p.driver.find_element_by_name('username').send_keys(id);
        p.driver.find_element_by_name('password').send_keys(pw);

        p.driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/article/div/div[1]/div/form/div[4]/button ").click()

        # 알림 여부 팝업창
        try :
            p.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click()
        except selenium.common.exceptions.NoSuchElementException :
            pass


    keyword = str(input('[검색어] :'))

    # 여기서부터 제작 시작
    search_url = "https://www.instagram.com/explore/tags/" + keyword
    p.driver.get(search_url)
    sleep(3)

    content_cnt = int(str(p.find_one("span .g47SY").text).replace(",", ""))

    pbar = tqdm(total=content_cnt)

    def start_fetching(pre_post_num, wait_time):
        ele_posts = p.find('.v1Nh3 a')
        for ele in ele_posts:
            key = ele.get_attribute('href')
            url = str(key).split("/")[4]

            if url not in list(url_set) :
                print("link : "  + key)
                url_set.add(url)

                # 큐 삽입
                que.put(key)

        if pre_post_num == len(list(url_set)):
            pbar.set_description('Wait for %s sec' % (wait_time))
            sleep(wait_time)
            pbar.set_description('fetching')
            wait_time *= 2
            p.scroll_up(300)
        else:
            wait_time = 1
        pre_post_num = len(list(url_set))
        p.scroll_down()

        return pre_post_num, wait_time

    pbar.set_description('fetching')
    while len(list(url_set)) < content_cnt and wait_time < TIMEOUT:
        post_num, wait_time = start_fetching(pre_post_num, wait_time)
        pbar.update(post_num - pre_post_num)
        pre_post_num = post_num

        loading = p.find_one('.W1Bne')
        if (not loading and wait_time > TIMEOUT / 2):
            break

    pbar.close()
    print('Done. Fetched %s posts.' % (min(len(list(url_set)), content_cnt)))
    search_flag = False
    print("Search Thread 종료")



# 멀티 쓰레드
def parsing_contents(id) :
    global search_flag
    p = Parsing(isChromDriver_parsing)
    idx = 1
    mlist = []
    while search_flag :
        row = []
        try:
            p.driver.get(que.get(timeout = 40))
        except queue.Empty :
            break;
        userID, txt, hashtag = "", "", ""
        # 저장 부분 제작하기
        # userID = p.find_one("div .C4VMK h2 .FPmhX").text
        t_date = p.find_one("div.eo2As div.k_Q0X.NnvRN a time").get_attribute("datetime")
        ele_contents = p.find("li:nth-of-type(1) div .C4VMK span")
        for content in ele_contents :
            txt += content.text
        txt = txt.replace("\n", " ")
        ele_tags = p.find("div.C4VMK span a")
        for tag in ele_tags :
            if "@" not in tag.text:
                hashtag += tag.text

        # row.append(userID)
        row.append(t_date)
        row.append(txt)
        row.append(hashtag)

        mlist.append(row)

        # 저장 부분
        if idx % 50 == 0 :
            path = os.path.abspath(os.path.join("saveFile", "file"+str(id)+".csv"))
            p.saveFile(path, mlist)
            print(mlist)
            mlist = []

        idx += 1
        print("search_flag",search_flag, "que.qsize()", que.qsize())

    print("search_flag",search_flag)
    if not search_flag :
        path = os.path.abspath(os.path.join("saveFile", "file" + str(id) + ".csv"))
        p.saveFile(path, mlist)
        print(mlist)
        mlist = []

    print("Worer Thread 종료")

# main
if __name__ == '__main__':
    global que, content_cnt, search_flag, isChromDriver_parsing, isChromDriver_search
    search_flag = True
    content_cnt = 7
    que = Queue(100)
    worker_threads = []
    print("Web Driver 옵션 권장 사항 : SEARCH용 browser은 Active, PARSING용 browser은 Inactive")
    isChromDriver_search = int(input('[ Chrom Driver For SEARCH : Inactive - 0, Active - 1 ] 입력 :'))
    isChromDriver_parsing = int(input('[ Chrom Driver For PARSING : Inactive - 0, Active - 2 ] 입력 :'))

    print("Search Thread 시작")
    search_thread = threading.Thread(target=search)
    search_thread.start()

    while que.qsize() < 10 :
        pass


    for i in range(0,7,1):
        print(str(i)+"번째 Worker Thread 시작")
        worker_thread = threading.Thread(target=parsing_contents, args=(i,))
        worker_threads.append(worker_thread)
        worker_threads[i].start()

    print("for : start")
    search_thread.join()
    print("search_thread.join()")
    for i in range(0,7,1):
        worker_threads[i].join()

    print("[Done]")