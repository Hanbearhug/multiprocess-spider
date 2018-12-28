# multiprocess-spider
## 目标介绍
米内网是一个医药数据库，前天老师找我帮忙爬取其中的数据，因此就这个机会试了一下标准化的爬虫格式以及多进程爬虫，下面是详细过程

## 架构
一般而言，爬虫的架构由四个部分组成，其一是url管理器，用于未爬取url和已爬取url的存储，url的解析等功能，其二是html下载器，用于接收url管理器分发的url任务并且向目标服务器发送请求头获取相应的网页内容(这里往往要设置自己的请求头格式，例如使用浏览器、版本等等信息，有时还要附带相应的cookie信息，否则服务器可能识别出请求不是来自用户点击而将请求重定向，百度百科、大众点评等均有此设置，大众点评暂时还不知道怎样骗过服务器，貌似服务端的做法是在运输层做手脚。。)，其三是html解析器，接收html下载器中得到的数据，并且解析我们需要的部分(这里要墙裂推荐一下Beatuifulsoup，非常好用)，其四是数据输出器，用于数据的格式化和存储。

## url管理器
我们在爬取网站的过程中，根据不同的需求对于url管理器也有不同的设定，例如，如果我们需要从网站中不断获取新的url并且添加到任务列表里，就需要设置一个set存储未爬取的url列表并且动态更新，也可以设置一个set存储已爬取过的列表避免重复爬取，在我们这里由于只需要爬取固定数据库的数据就不用费事了。\
首先要分析对应网站的数据存储在哪里，我比较喜欢用火狐浏览器去分析网页，这里叙述分析过程:\
一般而言最简单的网页爬虫是静态网页爬虫，即我们可以直接在网页端找到相应数据的元素，具体可以通过标签、XPATH等方式查找这里不做赘述，但米内网在查询数据的时候网页链接并不会跳转，因此我们不能直接通过变动url的方式获取数据，如下图所示:

![米内网主页面](https://github.com/Hanbearhug/multiprocess-spider/blob/master/%E7%B1%B3%E5%86%85%E7%BD%91MID%E7%9B%AE%E5%BD%95%E5%BA%93.png)
![点击前界面](https://github.com/Hanbearhug/multiprocess-spider/blob/master/%E7%82%B9%E5%87%BB%E4%B8%8B%E4%B8%80%E9%A1%B5%E5%89%8D%E7%95%8C%E9%9D%A2.jpg)
![点击后界面](https://github.com/Hanbearhug/multiprocess-spider/blob/master/%E7%82%B9%E5%87%BB%E4%B8%8B%E4%B8%80%E9%A1%B5%E5%90%8E%E7%95%8C%E9%9D%A2.png)

这说明Menet是一个动态网站，我们无法直接从网页中获取数据，因此要分析当我们点击检索以及下一页时这个网站干了什么。我们按F12，打开“网络栏”，监测这个网页的行为，如下图所示:
![](https://github.com/Hanbearhug/multiprocess-spider/blob/master/GET%E8%AF%B7%E6%B1%82.jpg)
![](https://github.com/Hanbearhug/multiprocess-spider/blob/master/%E6%B6%88%E6%81%AF%E5%A4%B4.jpg)
![](https://github.com/Hanbearhug/multiprocess-spider/blob/master/%E5%93%8D%E5%BA%94%E6%95%B0%E6%8D%AE.jpg)

因此我们知道每一次点击下一页的时候米内网就会往一个url地址发送GET请求，然后返回相应的相应数据，因此我们可以直接从这个对应的网址直接请求数据就可以得到想要的信息了。\

## html下载器
我们html下载器对url管理器分发的url进行数据的请求和下载，请求头的信息如下:
```
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {'User-Agent': agent}
```

## html解析器
这里有的数据库例如医药目录库等需要使用soup进行元素的定位，而MID则不需要，直接对json格式的文本进行解析转成pandas文件即可
```
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
```

## 最后是多进程
我们使用的库是multiprocessing，使用方法是Pool
通过这个函数我们建立了一个进程池，默认使用系统的最大进程数，然后对于相应的url进行多进程爬虫
```
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
```
这里map_async方法和map函数类似，返回的是一个列表形式(需要用get方法获取)
