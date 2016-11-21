# -*-coding:utf8 -*-
import requests
import json
from lxml import etree
from bs4 import BeautifulSoup

class NFSCCrawler(object):
    def __init__(self):
        self.header = {
            "Host": "npd.nsfc.gov.cn",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Origin": "http://npd.nsfc.gov.cn",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "http://npd.nsfc.gov.cn/projectSearch!searchAjaxForBut.action",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Cookie": "_gscu_1512923953=79739154osesnl15; _gscbrs_1512923953=1; JSESSIONID=2A4F74CC5EED74873EF6222A70F7CB99",
        }

        self.url = "http://npd.nsfc.gov.cn/projectSearch!searchAjaxForBut.action?project.code=&sort=0&pageSize=2000&project.searchYearEnd=&currentPage={0}&project.name=&project.leader=&project.organization=&project.organizationCode=&project.applyCode=F&project.category=&project.fundedYearStart=&project.fundedYearEnd=&checkCode=kx2g"
    def set_url(self, num):
        self.url = self.url.format(str(num))
        pass


    def page_parser(self, html):
        title_xpath = html.xpath('//*[@id="project_result"]/li/dl/dt/a/text()')
        num_xpath = html.xpath('//*[@id="project_result"]/li/dl/dd[1]/text()')
        cate_xpath = html.xpath('//*[@id="project_result"]/li/dl/dd[2]/text()')
        org_xpath = html.xpath('//*[@id="project_result"]/li/dl/dd[3]/a/text()')
        leader_xpath = html.xpath('//*[@id="project_result"]/li/dl/dd[4]/a/text()')
        money_xpath = html.xpath('//*[@id="project_result"]/li/dl/dd[5]/text()')
        outcome_xpath = html.xpath('//*[@id="project_result"]/li/dl/dd[6]/a/text()')
        with open('data/project_info.txt', mode="a") as fo:
            for title, num, cate, org, leader, money, outcome in zip(title_xpath,num_xpath, cate_xpath, org_xpath,leader_xpath,money_xpath,outcome_xpath):
                tmp_str = "\t".join([title.strip(), num.strip(), cate.strip(), u"依托单位:{0}".format(org.strip()),u"项目负责人:", leader.strip(),money.strip(), u"项目成果:", outcome.strip()])
                fo.write(tmp_str.encode('utf8')+"\n")
                # result_list.append(tmp_str)
            # print tmp_str
        # return result_list
    def post_data(self):
        # form_data = {"project.applyCode":"F", "checkCode":"dcnf", "sort":0, "pageSize":21, "currentPage":4}
        # form_data = "project.code=&sort=0&pageSize=21&project.searchYearEnd=&currentPage=20&project.name=&project.leader=&project.organization=&project.organizationCode=&project.applyCode=F&project.category=&project.fundedYearStart=&project.fundedYearEnd=&checkCode=y9km"
        result = requests.post(self.url, headers=self.header)
        content = result.text
        html = etree.HTML(content)
        self.page_parser(html)

    def get_all_data(self):
        for i in range(10):
            self.set_url(i)
            self.post_data()
        pass


if __name__ == '__main__':
    nfsc = NFSCCrawler()
    nfsc.get_all_data()
