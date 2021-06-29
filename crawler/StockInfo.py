from logging import NullHandler
import pandas as pd
from bs4 import BeautifulSoup
from requests import check_compatibility
from selenium import webdriver
from config import key
from api.MySQL import DB


class StockInfo:
    def __init__(self):
        self.stockInfos = pd.Series([])
        self.KOSPI = 0
        self.KOSDAQ = 1
        # self.KOSPI_PAGE_LENGTH = 30
        self.KOSPI_PAGE_LENGTH = 30
        self.KOSDAQ_PAGE_LENGTH = 29

    def openChromeDriver(self,url):
        self.driver = webdriver.Chrome(key.CHROME_DRIVER_PATH)
        self.driver.implicitly_wait(3)
        self.driver.get(url)

    def closeChromeDriver(self):
        self.driver.close()

    def parseStockInfo(self,tr):
        tds = tr.findAll("td")
        rank = tds[0].text
        code = tds[1].find("a")["href"][20:]
        name = tds[1].find("a").text
        nowPrice = tds[2].text
        marketValue = tds[7].text
        operatingProfit = tds[8].text
        eps = tds[9].text
        dividend = tds[10].text
        roe = tds[11].text
        
        stockInfo = [rank, name, code, nowPrice, marketValue, operatingProfit, eps, dividend, roe]

        for idx,check in enumerate(stockInfo):
            stockInfo[idx] = stockInfo[idx].replace(',','')
            if check == 'N/A':
                stockInfo[idx] = 0

        return pd.Series(stockInfo)

    #시세불러오기
    def crawlStockInfo(self,url):
        self.driver.get(url)
        bsObj = BeautifulSoup(self.driver.page_source,'html.parser')
        trs = bsObj.find("div",{"class":"box_type_l"}).find("table",{"class":"type_2"}).find("tbody").findAll("tr")

        stockInfos = pd.Series([])

        for tr in trs:
            try:
                stockInfo = self.parseStockInfo(tr)
                stockInfos = pd.concat([stockInfos,stockInfo],axis=1)
            except Exception as e:
                pass

        return stockInfos

    def getStockInfo(self):
        self.openChromeDriver("https://finance.naver.com/sise/sise_market_sum.nhn")

        #* 초기화 되있는 외국인비율,상장주식주,PER 체크 제거
        self.driver.find_element_by_id('option15').click()
        self.driver.find_element_by_id('option21').click()
        self.driver.find_element_by_id('option6').click()

        #* 영업이익,주당순이익,보통주배당금 체크
        self.driver.find_element_by_id('option5').click()
        self.driver.find_element_by_id('option23').click()
        self.driver.find_element_by_id('option26').click()

        #* 적용 클릭
        self.driver.find_element_by_xpath("//a[@href='javascript:fieldSubmit()']").click()

        #* 코스피는 0 코스닥 1 , page 당 50 종목
        for page in range(1,self.KOSPI_PAGE_LENGTH+1):
            url = f"https://finance.naver.com/sise/sise_market_sum.nhn?&sosok={self.KOSPI}&page={page}"
            stockData  = self.crawlStockInfo(url)
            self.stockInfos = pd.concat([self.stockInfos,stockData],axis=1)

        # for page in range(1,self.KOSDAQ_PAGE_LENGTH+1):
        #     url = f"https://finance.naver.com/sise/sise_market_sum.nhn?&sosok={self.KOSDAQ}&page={page}"
        #     stockData  = self.crawlStockInfo(url)
        #     self.stockInfos = pd.concat([self.stockInfos,stockData],axis=1)

        #결과 출력
        self.stockInfos = self.stockInfos.T                 # 전치
        self.stockInfos = self.stockInfos.dropna(how='any') # 빈칸 지우기
        self.stockInfos.columns=['rank','name','code','nowPrice','marketValue','operatingProfit','EPS','dividend','ROE']
        # self.stockInfos = self.stockInfos.set_index('rank')

        self.closeChromeDriver()

    def truncateDB(self):
        db = DB()
        sql = "TRUNCATE StockInfo"
        db.cursor.execute(sql)
        db.close()

    def updateDB(self):
        self.truncateDB()
        self.getStockInfo()
        db = DB()
        cols = ",".join([str(i) for i in self.stockInfos.columns.tolist()])
        for _,row in self.stockInfos.iterrows():
            sql = "INSERT INTO StockInfo (" + cols + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (tuple(row))
            db.cursor.execute(sql,val)
        db.commit()
        db.close()
        print(f"UPDATED {len(self.stockInfos)} of stock information...")