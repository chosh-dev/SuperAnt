from config import key
from api.ExchangeRate import ExchangeRate
from api.MySQL import DB    
from model.ExchangeRate import ExchangeRateModel
from model.StockInfo import StockInfoModel
from crawler.StockInfo import StockInfo

## main-------------------------------------------------------------
if __name__ == '__main__':
    print("init...")
    #! 시세 크롤링 해서 적당한 종목들을 찾음
    # import crawling
    # import processing
    #! 적당한 종목들을 데이터 크롤링 분석해서 점수를 매김
    # import analyzing

    #! 환율정보
    # exchangeRate = ExchangeRate()
    # exchangeRate.updateDB()

    #! 주식 정보
    stockInfo = StockInfo()
    stockInfo.updateDB()

    #! table 생성
    # DB = DB()
    # DB.createTable(ExchangeRateModel)
    # DB.createTable(StockInfoModel)
    # DB.printLog()

