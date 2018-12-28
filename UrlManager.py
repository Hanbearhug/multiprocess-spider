class UrlManager:
    def get_new_url(self,urlFeature):
        """
        获取一个未爬取的URL
        :return:
        """
        path = "http://shuju.menet.com.cn/NEWVIPZone/MID/productComprehensiveDatabaseListAction.action?" \
               "sAll=1&pcdProductName=&pcdCommodityName=&pcdApprovalNumber=&pcdProductionUnit=&pcdRelation" \
               "UpMarketCompany=&pcdRemark3=&pcdRemark4=&pcdProductSort=&pcdInternationOrLocal=&pcdFormulations" \
               "=注射剂,其他剂型,贴膏剂,胶囊剂,口服液体剂,片剂,其他吸入剂,颗粒剂,栓剂,吸入剂,凝胶剂,散剂,外用液体剂" \
               ",喷雾剂,软膏剂,丸剂,其它剂型,滴眼剂,贴剂,煎膏剂,滴鼻剂,涂剂,滴耳剂,硬膏剂&pcdBigSort=&pcdAreaSort" \
               "=&pcdApproveDate=&pcdMedicareSort=&pcdRemark1=&pcdRemark2=&pcdIsSingle=&pcdBaseMedicineName=&pcdRemark15=&pageNow="
        new_url = path+str(urlFeature)
        return new_url