# kb 비타민 크롤링 해오기
import pandas as pd
import requests
from bs4 import BeautifulSoup
from news.models import column

class kb_report:
    def __init__(self):
        self.kb_url = "https://www.kbfg.com/kbresearch/vitamin/reportList.do"
        self.num_reports = 9
        self.kb_reports= []

    def requests(self):
        html = requests.get(self.kb_url).text
        parser = BeautifulSoup(html,'html.parser') 
        report_html = parser.select('td')

        for i in range(self.num_reports):
            title_str = str(report_html[6*i+2].select('a')[0]).split('"')
            url = "https://www.kbfg.com/" + title_str[1]
            title = title_str[2][1:-4]
            pub_date = str(report_html[6*i+4])[4:-5]
            self.kb_reports.append({"title":title, "url":url, "pub_date":pub_date})
            
        print(self.kb_reports)
        print("scrapping KB website...")

    def save_db(self):
        for i in range(self.num_reports):
            column = Column()
            column.subject = self.kb_reports[i]["title"]
            column.url = self.kb_reports[i]["url"]
            column.save()

test = kb_report()
test.requests()