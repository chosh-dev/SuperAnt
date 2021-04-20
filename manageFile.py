import os 
import time

# 오늘 날짜를 가져오는 함수
def get_today() :
    now = time.localtime()
    s = "%04d_%02d_%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    return s

# 폴더 생성 함수
def make_folder(folder_name):
    if not os.path.isdir(folder_name) :
        os.mkdir(folder_name)