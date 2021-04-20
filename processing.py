import pandas as pd
import numpy as np
import manageFile

# CSV 읽어오기
root_dir = "C:/Users/조성현/Desktop/super_ant/backup/sise/"
today = manageFile.get_today()
#siseResult.to_csv(root_dir +'{}_sise.csv'.format(today))
processData = pd.read_csv(root_dir +'{}_sise.csv'.format(today),thousands = ',')

# 적정 주가 
properPrice = processData['EPS'] * processData['ROE'] * 1.2 # EPS * ROE
processData['proper price'] = properPrice

properPriceRatio = processData['now price'] / processData['proper price']
processData['proper price ratio'] = round(properPriceRatio,2)

# 적정 시가총액
properValue1 = processData['operating profit'] * processData['ROE'] # 영업이익 * ROE
#properValue1 = processData['operating profit'] * 20 # 영업이익 * ROE
properValue2 = processData['operating profit'] * 10 # 영업이익 * multiple 10
properValue = pd.concat([properValue1,properValue2],axis=1)
processData['proper value'] = properValue.min(axis=1)

properValueRatio = processData['market value'] / processData['proper value'] # 비율
processData['proper value ratio'] = round(properValueRatio,2)


# 적정 배당금
properDividend = 4
DividendRate = processData['dividend'] / processData['now price'] * 100
processData['dividend rate'] = round(DividendRate,2)


# 조건에 만족하는 종목
passStock = processData
passStock = passStock[passStock['now price'] < passStock['proper price']]  # 현재가 > 적정가
passStock = passStock[passStock['market value'] < passStock['proper value']] # 시가총액 > 적정시가총액
# passStock = passStock[passStock['dividend rate'] > properDividend] # 배당금 > 기준치

# passStock = passStock[passStock['market value'] <= 1000] # 1000억 이하 중소형주

print(passStock)

# CSV 파일로 저장
root_dir = "C:/Users/조성현/Desktop/super_ant/backup/checkList/"
passStock.to_csv(root_dir +'{}_checkList.csv'.format(today))
