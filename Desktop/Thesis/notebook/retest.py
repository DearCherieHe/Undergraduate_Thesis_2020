import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import bs4
import csv
from fake_useragent import UserAgent
ua = UserAgent()
agent = ua.chrome
Cookie = '''st_si=20884223359566; st_asi=delete; HAList=a-sz-002230-%u79D1%u5927%u8BAF%u98DE; cowCookie=true; qgqp_b_id=36bf1ed0bb15c4aebfa296ef3100166d; intellpositionL=1332px; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; EmPaVCodeCo=8308cfa268b54d26b090f11f8f4e10c0; uidal=7381325832412590%e8%82%a1%e5%8f%8bXuFqhk; intellpositionT=752px; ct=EBFYxUZZFu-dO14ZFx61-CKqe4OKBk4fV2xrM1QiQdv6Za-5VKuqifoxQM3ZsOL95H5AJoXFU-nwGSc0rd1j2UrmWjo7FEWSS7XBJNU4zqzaQzAhrxHSz-8JsGJY3aZDxrQ8oqgNbTXSnuS510nBpZtiSg3I__37IX8IEZDHEd4; ut=FobyicMgeV54OLFNgnrRk7CV_sZnBDhICpmkVXvCMsNktzBPQWXGN2-ZCJ5X9AYcqQEc7XXW7WnlDi_AAVs7Q4FYDMBvHZASYIDUz6PRRDMcmC4MckMxMZLRr4AZZa_xfNUYrPnXiIhjHXTDq2_biuP4RaaA6QbFrooMmrzgBJWVGLiQBuENCWGu_ym_UsY1__H3LPpzQLbUDAJm9DTYOPBYSs5XecgIVRWnl_8_uV_YcdygKjJhiIxj6FxtUYDdCCdzDFNHPT8t9TrH8cUBGTrXKlBd3oms; pi=7381325832412590%3bp7381325832412590%3b%e8%82%a1%e5%8f%8bXuFqhk%3b3m0U0km73WF5C0HvwWMgEZLpSj0YLDb8e2UMMbQ1yALC5LBUvxwWDLAgmy0XSTywPHHzluJOUaOu9WpUhCMfxC3qnHUfveiblfpYvLu35Bz74Zysv2Y71KHeJZ9FFeEFRW55kHXYjil02wW9qz7HVloQ8por%2bWCUklzZLZ3I0V4MaAdIdZS%2bagQcrHtfYH7OGcmvW5L1%3bq69suhpJnjmf4mUtXNrUvZQLH%2bqPXv667CLFsR8hJZx5AKsv42KxPiPRj8ntCmafCeBPg5aLpIPQLOVSTk19flf5BYzYCZyC5lomAbVL7%2bVYDo5q6borc8Drg0BZjIo%2b1wJe%2bq0Xg1%2b0YbP2JGkmiqNCw0Cs4A%3d%3d; testtc=0.2726496242672396; st_pvi=91116827875848; st_sp=2020-03-03%2017%3A06%3A09; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=78; st_psi=20200306000438640-117001301474-6870651882'''


def get_data(name, code, pagen):
    url_list = []
    file_name = name + '_news' + f'{pagen-4, pagen}' + '.csv'
    f = open(file_name, 'w')
    f_writer = csv.writer(f)
    f_writer.writerow(['title', 'content', 'date', 'comments_num'])
    for page in range(pagen-4, pagen+1):
        url = 'http://guba.eastmoney.com/list,{}_{}.html'.format(code, page)
        url_list.append(url)
        webpage = requests.get(
            url, headers={'Cookie': Cookie, 'user-agent': agent}).text
        bsobj = BeautifulSoup(webpage, 'lxml')
        # print(bsobj.prettify())
        article = bsobj.find('div', class_='all hs_list')

        # print(article)
        # post = article.find_all('div', class_="articleh normal_post")
        # print(post)
        num = 0
        # if isinstance(post, bs4.element.Tag):
        for posts in article.find_all('div', class_="articleh normal_post"):
            try:
                comment = posts.find('span', class_="l3 a3").a['title']
                # print(comment)
                comments_num = posts.find('span', class_="l2 a2").text
                postcode = posts.find('span', class_="l3 a3").a['href'].split(",")[
                    2].split(".")[0]
                # print(postcode)
                # times = posts.find('span', class_='l5 a5').text
                # pattern = '\d{6}'
                # postlk = str(re.findall(pattern, url))
                post_link = 'http://guba.eastmoney.com/news,' + code + f",{postcode}" + '.html'
                postdetail = requests.get(post_link).text
                # print(postdetail)
            #         # com_cont = re.compile('<div id="mainbody">.*?zwconttbn.*?<a.*?<font>(.*?)</font>.*?<div.*?class="zwcontentmain.*?">.*?"zwconttbt">(.*?)</div>.*?social clearfix', re.DOTALL)
                pub_elems = re.search(
                    '<div class="zwfbtime">.*?</div>', postdetail).group()
                # <div class="zwfbtime">发表于 2020-02-11 09:54:48 东方财富Android版</div>
                postweb = BeautifulSoup(postdetail, 'lxml')
                pub_time = re.search(
                    '\d\d\d\d-\d\d-\d\d', pub_elems).group()
                # pub_times.append(pub_time)
                post_content = postweb.find(
                    'div', class_="zwcontentmain xeditor")
                # print(post_content)
                content = post_content.find(
                    'div', class_="stockcodec .xeditor").text.strip()
                print(content)
                f_writer.writerow(
                    [comment, content, pub_time, comments_num])
            except Exception as e:
                pass

            num += 1
            print(f"loop {num} times")

        print(f"get page{page} comments done")
        print(f"get page{page} contents done")


    f.close()

for i in 5*np.arange(208,301):
    get_data('zgpa', '601318', i)

