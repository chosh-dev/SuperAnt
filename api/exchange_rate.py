# 환율 데이터 api, from fixer
# https://fixer.io/documentation
import requests 
from config import key

class exchangeRate:
    def __init__(self):
        self.url = "http://data.fixer.io/api/latest"
        self.token = key.FIXER_KEY

        self.data={
            "access_key" : self.token,
            "symbols" : "USD,KRW,JPY,CNY"
        }

    def update(self):
        res = requests.get(self.url, self.data)
        self.data = {} 

        self.data["KRW_USD"] = (1/res.json()["rates"]['USD']*res.json()["rates"]["KRW"])
        self.data["KRW_EUR"] = (res.json()["rates"]["KRW"])
        self.data["KRW_CNY"] = (1/res.json()["rates"]['CNY']*res.json()["rates"]["KRW"])
        self.data["KRW_JPY"] = (1/res.json()["rates"]['JPY']*res.json()["rates"]["KRW"])

    def updatedMessage(self):
        self.update()

        message = "------금일 환율------\n"
        message = message + ("달러: %.2f 원\n" % self.data["KRW_USD"])
        message = message + ("유로: %.2f 원\n" % self.data["KRW_EUR"])
        message = message + ("위안: %.2f 원\n" % self.data["KRW_CNY"])
        message = message + ("옌 : %.2f 원\n" % self.data["KRW_JPY"])

        return message
         