import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import manageFile

# 크롬 드라이버 실행
driver = webdriver.Chrome('/Users/조성현/Desktop/super_ant/chromedriver')
driver.implicitly_wait(3)
driver.get("https://finance.naver.com/sise/sise_market_sum.nhn")

#초기화 되있는 외국인비율, 상장주식주, PER 체크 제거
driver.find_element_by_id('option15').click()
driver.find_element_by_id('option21').click()
driver.find_element_by_id('option6').click()


#영업이익,주당순이익, 보통주배당금 체크
driver.find_element_by_id('option5').click()
driver.find_element_by_id('option23').click()
driver.find_element_by_id('option26').click()


#적용 클릭
driver.find_element_by_xpath("//a[@href='javascript:fieldSubmit()']").click()

# 주가 정보 추출
def getStockInfo(tr):
    tds = tr.findAll("td")
    rank = tds[0].text
    aTag = tds[1].find("a")
    href = aTag["href"]
    name = aTag.text
    nowPrice = tds[2].text
    MarketValue = tds[7].text
    OperatingProfit = tds[8].text
    EPS = tds[9].text
    Dividend = tds[10].text
    ROE = tds[11].text

    stockInfo = pd.Series([rank, name, href[20:],nowPrice,MarketValue,OperatingProfit,EPS, Dividend, ROE])
    
    return stockInfo

# 주가 정보까지 찾아가기
def parse(pageString):
    bsObj = BeautifulSoup(pageString,'html.parser')
    box_type_l = bsObj.find("div",{"class":"box_type_l"})
    type_2 = box_type_l.find("table",{"class":"type_2"})
    tbody = type_2.find("tbody")
    trs = tbody.findAll("tr")

    stockData = pd.Series([])

    for tr in trs:
        try:
            stockInfo = getStockInfo(tr)
            stockData = pd.concat([stockData,stockInfo],axis=1)
        except Exception as e:
            pass
    return stockData

#시세불러오기
def getSiseMarketSum(sosok,page):
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?&sosok={}&page={}".format(sosok,page)
    driver.get(url)
    pageString = driver.page_source 
    
    stockData = parse(pageString)
    return stockData


## main--------------------------------------------------------
siseResult = pd.Series([])

# 코스피는 0 코스닥 1 , page 당 50 종목
for page in range(1,30+1):
    stockData  = getSiseMarketSum(0, page)
    siseResult = pd.concat([siseResult,stockData],axis=1)

for page in range(1,29+1):
    stockData  = getSiseMarketSum(1, page)
    siseResult = pd.concat([siseResult,stockData],axis=1)

#결과 출력
siseResult = siseResult.T                 # 전치
siseResult = siseResult.dropna(how='any') # 빈칸 지우기
siseResult.columns=['rank','name','code','now price','market value','operating profit','EPS','dividend','ROE']
siseResult = siseResult.set_index('rank')

#print(siseResult)
#print(len(siseResult))

#결과 파일 저장
root_dir = "C:/Users/조성현/Desktop/super_ant/backup/sise/"
today = manageFile.get_today()
siseResult.to_csv(root_dir +'{}_sise.csv'.format(today))

print('loaded {} of data from Naver...'.format(len(siseResult)))

driver.close()