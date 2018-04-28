import time;
from bs4 import BeautifulSoup;
from selenium import webdriver;
import os;

# 순서
# 1. 현재 날짜와 기사의 날짜가 같으면 date에 카운트 , page는 넘어갈때 마다 카운트 v
# 2. page와 date 숫자 만큼 반복문 실행 시켜 기사의 내용을 가지고 온다. (일단 1번은 사용하지 않는다)
# 3. 기사의 내용을 가지고 온다.
# 4. 단어(명사형태)로 출력
# 5. db에 저장

class ITNewsParsing :
    driver1, html, soup = '', '', '';  # 웹크롤링

    def __init__(self):
        chromedriver = "/home/hallym-dpac/문서/tool/etc/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver1 = webdriver.Chrome(chromedriver)
        self.driver1.implicitly_wait(3);

    # 데이터 가지고 오기
    def getDataFromSoup(self, url):
        self.driver1.get(url);
        self.html = self.driver1.page_source;
        self.soup = BeautifulSoup(self.html, 'html.parser');

        return self.soup;

    # 날짜 비교
    def find_news_until_today(self, soup, today) :
        index, flag = 1, True;
        pageCount, dateCount, date, time = 1, 0, '', '';  # 페이지, 날짜 저장
        self.soup = soup

        while flag :
            #print("while 1");
            notices = self.soup.select('.article_li .article_date');
            for i in notices:
                date = i.text;  # 배열 형태로 바꿔서 여러개의 시간들을 저장!
                time = date.strip('[]');
                time = time.split('.');  # type : list -> [0] : 연도, [1] : 월, [2] : 일, [3] : 시간
                #print(time);
                if int(time[0]) == today[0] and int(time[1]) == today[1] and int(time[2]) == today[2] :

                    ## 기사 안에 들어가기
                    url_soup = self.soup.select('.article_li h2 a');
                    for j in url_soup :
                        dateCount += 1;
                        print(dateCount,"번째 기사");
                        url = "http://www.zdnet.co.kr" + j.get('href');
                        print(url)
                        news_content = self.news_content_parsing(url);
                        #self.save_textFile('D:/Programing Folder/Python/Mining\parser/ITNews.txt', news_content);

                        if dateCount % 12 == 0 :
                            self.driver1.back();
                            pageCount += 1;
                        #print("페이지 : " , pageCount);
                else : # 오늘 쓴 기사가 아니면 중지
                    flag = False;
                    break;

            if dateCount % 12 == 0 :
                #print("오늘 기사 갯수 : ", dateCount)
                news_index = 'http://www.zdnet.co.kr/news/news_list.asp?zdknum=0000&page=' + str(pageCount);
                self.soup = self.getDataFromSoup(news_index);
            #print("while 끝")

        return ; # 전 기사가 담긴

        # 날짜 비교

    def find_news_until_the_year(self, soup, until_Year):
        index, flag = 1, True;
        pageCount, dateCount, date, time = 1, 0, '', '';  # 페이지, 날짜 저장
        self.soup = soup

        while flag:
            # print("while 1");
            notices = self.soup.select('.news_srch_li .article_date');
            for i in notices:
                date = i.text;  # 배열 형태로 바꿔서 여러개의 시간들을 저장!
                time = date.strip('[]');
                time = time.split('.');  # type : list -> [0] : 연도, [1] : 월, [2] : 일, [3] : 시간
                # print(time);
                if int(time[0]) >= until_Year :

                    ## 기사 안에 들어가기
                    url_soup = self.soup.select('.news_srch_li h4 a');
                    for j in url_soup:
                        dateCount += 1;
                        print(dateCount, "번째 기사");
                        url = j.get('href');
                        if 'http://www.zdnet.co.kr' in url :
                            pass
                        else :
                            url = 'http://www.zdnet.co.kr' + url
                        news_content = self.news_content_parsing(url);
                        print(news_content)
                        # self.save_textFile('D:/Programing Folder/Python/Mining\parser/ITNews.txt', news_content);

                        if dateCount % 14 == 0:
                            pageCount += 1;
                        # print("페이지 : " , pageCount);
                else:  # 오늘 쓴 기사가 아니면 중지
                    flag = False;
                    break;

            if dateCount % 14 == 0:
                # print("오늘 기사 갯수 : ", dateCount)
                news_index = 'http://search.zdnet.co.kr/news.jsp?kwd=%EA%B8%B0%EC%9E%90&collection=zdnet&pageno=' + str(pageCount);
                self.soup = self.getDataFromSoup(news_index);
            # print("while 끝")

        return;  # 전 기사가 담긴

    def news_content_parsing(self, url):
        news = [''];
        thisSoup = self.getDataFromSoup(url);
        notices = thisSoup.select('.sub_view_cont p');
        for i in notices:
            date = i.text;  # 배열 형태로 바꿔서 여러개의 시간들을 저장!
            word = date.split();
            for j in range(0, len(word),1) :
                if word[j] != '\u200b' :
                    #print("'", word[j], "'"); # db 저장 부분 넣기
                    news.append(word[j]);
        return news;

    def save_textFile(self,Path, mlist):
        file = open(Path, 'a');
        file.write("aaaaa")
        file.write("\n");
        for l in mlist :
            file.write(l);
            file.write('\n');
        file.write('\n');
        file.close();


## main() ##
now = time.localtime(); ## 현재시간

driver1, html, soup = '', '', '';  # 웹크롤링
notices, temp = '', ''  # 임시 변수
tupleCount = (); #(페이지수, 오늘자 뉴스기사)

it = ITNewsParsing();

# driver1.get('http://www.zdnet.co.kr/?lo=zv1');
# newest_news = driver1.find_element_by_xpath('//*[@id="wrap"]/div[1]/div[3]/div[1]/div/div/ul/li[1]/a');
# newest_news_href = newest_news.get_attribute('href');

# newest_news_href = 'http://search.zdnet.co.kr/news.jsp?kwd=%EA%B8%B0%EC%9E%90&collection=zdnet';
# soup = it.getDataFromSoup(newest_news_href);
# today = [now.tm_year, now.tm_mon, now.tm_mday];
# print("today :" , today);
#it.find_news_until_today(soup, today); # 오늘날짜 신문만 가져오기


newest_news_href = 'http://search.zdnet.co.kr/news.jsp?kwd=%EA%B8%B0%EC%9E%90&collection=zdnet';
soup = it.getDataFromSoup(newest_news_href);
it.find_news_until_the_year(soup, 2018)



