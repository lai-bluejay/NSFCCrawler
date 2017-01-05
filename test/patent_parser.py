# -*- coding:utf-8 -*-

"""
nfsc_crawler --  patent_parser
This file was created at 17/1/3 BY laihongchang
"""

__author__ = 'laihongchang'
__author_email__ = 'laihongchang@wecash.net'

import os
# import untangle
# import xmltodict
from lxml import etree
import codecs
import re

from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd


class MultiPatentsParser(object):
    def __init__(self):
        pass

    def get_patents_file_list(self, patent_dir):
        patent_list = list()
        patent_list = [os.path.join(patent_dir, file_name) for file_name in os.listdir(patent_dir)]
        # 列表推导式, 代码等价于
        # for file_list in os.listdir(patent_dir): 
        #     path = os.path.join(patent_dir, file_list) 
        #     if os.path.isdir(path): 
        #         print("暂时只做一层目录, 如果有多层目录, 比如多个专利类别, 可以考虑一个目录一个文件输出. 现在看不到需求.")
        return patent_list

    def clean_dict(self, patent_dict):
        for k, v in patent_dict.items():
            patent_dict[k] = v.replace("\t", "")
        return patent_dict

    
    def parse_patent(self, path='data/test.xml'):
        patent = dict()
        with codecs.open(path, encoding="utf8") as fd:
            xml_obj = etree.XML(fd.read())
            doc_id_list = xml_obj.xpath("//cn-publication-reference//document-id/*/text()")
            patent_id = ''.join(doc_id_list[:3])
            public_date = doc_id_list[3]
            apply_type = xml_obj.xpath("//*/application-reference/@appl-type")[0]
            apply_list = xml_obj.xpath("//application-reference//document-id/*/text()")
            apply_id = "".join(apply_list[:2])
            apply_date = apply_list[2]
            ipc_no = ','.join(xml_obj.xpath("//classification-ipcr/text/text()"))
            invention_title = xml_obj.xpath("//invention-title/text()")[0]
            assignees = ",".join(xml_obj.xpath("//assignees/*//name/text()"))
            ass_add = xml_obj.xpath("//assignees/assignee//address/text/text()")[0]
            abstract = ",".join(xml_obj.xpath("//abstract/*/text()"))
            inventors = ','.join(xml_obj.xpath("//cn-inventors//name/text()"))
            agency_org = ",".join(xml_obj.xpath("//cn-agency/name/text()"))
            agency_name = ",".join(xml_obj.xpath("//cn-agent/name/text()"))
            claims_text_list = [line.strip() for line in xml_obj.xpath("//claims//claim-text/text()") if
                                len(line.strip()) > 3]
            claim_text = "".join(claims_text_list)
            patent["patent_id"] = patent_id
            patent["public_date"] = public_date
            patent["apply_type"] = apply_type
            patent["apply_id"] = apply_id
            patent["apply_date"] = apply_date
            patent["ipc_no"] = ipc_no
            patent["invention_title"] = invention_title
            patent["assignees"] = assignees
            patent["ass_add"] = ass_add
            patent["abstract"] = abstract
            patent["inventors"] = inventors
            patent["agency_org"] = agency_org
            patent["agency_name"] = agency_name
            patent["claim_text"] = claim_text
        patent = self.clean_dict(patent)
        return patent

    def multi_patent_parser(self, patent_dir, output_path = "output/final_patent_result.tsv"):
        pool = ThreadPool(16)
        patent_file_list = self.get_patents_file_list(patent_dir)
        # 返回的是list ,每个元素是dict
        patent_result = pool.map(self.parse_patent, patent_file_list)
        pool.close()
        pool.join()
        parse_result = pd.DataFrame.from_records(patent_result)
        # 不知道有没有重复的文件, 这里按照ipc号去重, 防止被坑
        parse_result.drop_duplicates(subset=['ipc_no'])
        parse_result.to_csv(output_path, index=False, encoding="utf8", sep='\t')
        # 也可以写成Excel, 随意
        # ew = pd.ExcelWriter(output_path)
        # parse_result.to_excel(ew, sheet_name='patent', index=False)
        # ew.save()


if __name__ == '__main__':
    # PatentPaser().parse_xml()
    pp = MultiPatentsParser()
    pp.multi_patent_parser()