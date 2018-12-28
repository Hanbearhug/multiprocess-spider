from bs4 import BeautifulSoup
import json
import pandas as pd


class HtmlParser:
    def parser(self, html_cont):
        """
        用于解析网页内容，抽取数据
        :param html_cont:
        :return:
        """
        if html_cont is None:
            return
        #soup = BeautifulSoup(html_cont, 'lxml')
        new_data = self._get_new_data(html_cont)
        return new_data


    def  _get_new_data(self, html_cont):
        """
        抽取有效数据
        :param soup:
        :return:
        """
        #r = soup.find('p').get_text()
        p = json.loads(html_cont)
        table = pd.DataFrame(p[1:])
        table = table.rename(columns={'f1': '编码', 'f2': "药品名称", 'f3': "生产企业", 'f4': "批文文号",
                                      'f5': "商品名", 'f6': "剂型", 'f7': "规格", 'f8': "进口国产", 'f9': "批准日期"})
        return table