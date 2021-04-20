import schedule
import time
import slack_bot
import exchange_rate
import index_info
from datetime import datetime,timedelta


test = slack_bot.slack_bot()

def morning_routine():
    #미국 시차 적용
    init_time = (datetime.today() - timedelta(hours=8)).strftime("%m/%d %H:%M")

    # 지수변동
    idx = index_info.index()
    index_msg = idx.get_index_info()

    # 환율 정보
    exg = exchange_rate.exchange_rate()
    exchange_msg = exg.get_message()


    # 메시지 보내기
    test.add_text(f"간밤에 안녕하셨습니까? --- {init_time}\n")
    test.add_text(index_msg)
    test.add_text(exchange_msg)
    test.add_img("good morning","https://blog.kakaocdn.net/dn/bSAefe/btqzhJ4ScmE/apRbS1RIpMKcaF3Ed0Muk0/img.gif")

    test.send();
    test.remove_block();


morning_routine()

# schedule.every().day.at("16:56").do(morning_routine)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
