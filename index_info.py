#지수 변동 정보 가져오기
import FinanceDataReader as fdr
class index:
    def __init__(self):
        self.temp = "hi"

    def get_index_info(self):
        indexes = ['KS11','KQ11','KS50','KS100','KRX100','KS200','DJI','IXIC','US500','VIX','JP225','CSI300','HSI','FTSE','DAX']
        names = ['KOSPI','KOSDAQ','KOSPI 50','KOSPI 100','KRX 100','KOSPI 200','다우존스','나스닥','S&P 500','VIX','닛케이 225','CSI300','항셍','FTSE','DAX']
        columns = ['Close', 'Open', 'High', 'Low', 'Volume', 'Change']
        korean = ['종가', '시가', '최고가', '최저가', '거래량', '변동률']
        messages = ""
        for i in range(len(indexes)):
            index = indexes[i]
            name = names[i]
            df = fdr.DataReader(index, '2021').tail(1)
            tmp = f"이름: {name}\n"
            for c in range(len(columns)):
                col = columns[c]
                kol = korean[c]
                val = df[[col]].values[0][0]*100 if col=="Change" else (df[[col]].values[0][0])
                val = "{:.2f}".format(val)
                tmp = f"{tmp}{kol}: {val}\n"
            messages = f"{messages}{tmp}\n"
        return messages 

