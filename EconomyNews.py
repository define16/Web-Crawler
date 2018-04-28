from bs4 import BeautifulSoup;
from selenium import webdriver;
import time
import os;

class News :
    driver, html= '', '';  # 웹크롤링
    urlA = [];

    def __init__(self):
        chromedriver = "/home/hallym-dpac/문서/tool/etc/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        self.driver.implicitly_wait(3);

    def clearUrlA(self):
        del self.urlA[:]

    # 데이터 가지고 오기
    def getDataFromSoup(self, url):
        self.driver.get(url);
        self.html = self.driver.page_source;
        soup = BeautifulSoup(self.html, 'html.parser');

        return soup;

    def save_textFile(self,Path, mlist):
        file = open(Path, 'a');
        file.write("aaaaa")
        file.write("\n");
        for l in mlist :
            file.write(l);
            file.write('\n');
        file.write('\n');
        file.close();

    def find_news_to_the_end(self, url, page):
        content_cnt = 0;
        soup = news.getDataFromSoup(url);
        notices = soup.select('#wraper > div.container.clearfix > div.section > div.list_vt > ul > li > dl > dt > a');

        #print(notices);
        print("find_news1")
        print(notices)

        for ii in notices :
            content_url = 'http://biz.chosun.com' + ii.get('href');
            print(content_url);
            self.urlA.append(content_url);
            content_cnt += 1;

        # 마지막 페이지인지 체크
        if content_cnt % 10 == 0 :
            print("if content_cnt % 10 == 0 : ")
            if page % 100 == 0 : #124까지 지원
                print("break")
                time.sleep(60)
            page += 1;
            print("page ", page)
            new_url = self.explore_page(url, page)
            print("new_url ", new_url)
            self.find_news_to_the_end(new_url, page);

        return self.urlA

    def find_news_until_the_time(self, url, page, year):
        content_cnt = self.check_Date(url,year)
        ###############################
        flag = False # ture 로 바꾸기 < 기사 출력 TEST중... >
        ###############################
        soup = news.getDataFromSoup(url);
        notices = soup.select('#wraper > div.container.clearfix > div.section > div.list_vt > ul > li > dl > dt > a');

        print("find_news_until_the_time")
        temp = 0
        for ii in notices:
            if content_cnt % 10 != 0 and temp == content_cnt or content_cnt == 0 :
                flag = False
                break;
            temp += 1
            content_url = 'http://biz.chosun.com' + ii.get('href');
            print(content_url);
            self.urlA.append(content_url);


        if flag :
            print("flag ")
            if page % 100 == 0 : #124까지 지원
                print("break")
                time.sleep(60)
            page += 1;
            print("page ", page)
            new_url = self.explore_page(url, page)
            print("new_url ", new_url)
            self.find_news_until_the_time(new_url, page, year);

        return self.urlA

    def explore_page(self, url, page) :
        if '&pn=' in url :
            next_url = url.replace('&pn='+str(page-1), '&pn='+str(page))
        else :
            next_url = url + '&pn=' + str(page)
        return next_url;

    def check_Date(self, url,year):
        count = 0
        soup = news.getDataFromSoup(url);
        notices = soup.select('#wraper > div.container.clearfix > div.section > div.list_vt > ul > li > dl > dt > span');
        #print("Date notice : " , notices)
        for ii in notices:
            date = ii.text.split('.')
            #print("year : ", date[0], "input : " , year)
            if year <= int(date[0]) :
                count += 1
        print("count : " , count)

        return count

    def news_content_parsing(self, url):
        news = [''];
        thisSoup = self.getDataFromSoup(url);
        notices = thisSoup.select('#article_2011');

        for i in notices:
            date = i.text;  # 배열 형태로 바꿔서 여러개의 시간들을 저장!
            word = date.split();
            for j in range(2, len(word),1) :
                if word[j] != '\u200b' :
                    #print("'", word[j], "'"); # db 저장 부분 넣기
                    if j == 2 :
                        news.append(word[j] + " " + word[j+1]);
                    elif j == 3 :
                        continue
                    else :
                        news.append(word[j]);
        return news;


## main() ##

news = News();
# 분야 선택
## kind = 1 증권, 2 부동산 3 정책 금융
kind = ['catid=2&gnb_marketlist', 'catid=4&gnb_global', 'catid=1A&gnb_npolicy']
url = 'http://biz.chosun.com/svc/list_in/list.html?'
filename = ['증권', '부동산','정책과금융']


urlA = []
for i in range(0, len(kind), 1) :
    del urlA[:] #배열 초기화
    news.clearUrlA()

    path = "/home/hallym-dpac/문서/program files/python/news/경제(" + filename[i] + ").txt"  ## 파일 저장 주소

    kind_url = url + kind[i];
    urlA = news.find_news_until_the_time(kind_url, 1, 2013)
    for u in urlA :
        print(news.news_content_parsing(u))
        news.save_textFile(path, news.news_content_parsing(u))

    print("kind change")
    time.sleep(60)

