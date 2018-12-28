from HtmlDownload import HtmlDownloader
from UrlManager import UrlManager
from HtmlParser import HtmlParser
from DataOutput import DataOutput
from multiprocessing import Pool
import pandas as pd
import os
os.chdir("D:/Dr.HanInXMU/岳阳老师/Menet")


class MenetSpider:
    def __init__(self):
        self.downloader = HtmlDownloader()
        self.urlmanager = UrlManager()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, i):
        try:
            print(f"Process {i} is running")
            url = self.urlmanager.get_new_url(i)
            html = self.downloader.download(url)
            data = self.parser.parser(html)
            return data
        except:
            print(f"crawl failed at {i}")
            return pd.DataFrame([0,0,0,0,0,0,0,0,0],columns=[ '编码', "药品名称", "生产企业", "批文文号", "商品名", "剂型", "规格", "进口国产", "批准日期"])


if __name__ == "__main__":
    menet = MenetSpider()
    IndexList = [i for i in range(1,501)]
    p = Pool()
    print('start-------------------')
    result = p.map_async(menet.crawl, IndexList)
    p.close()
    p.join()
    print("All subprocesses done")
    output = pd.concat(result.get(), axis=0)
    output.to_excel("MID目录库1.xlsx")