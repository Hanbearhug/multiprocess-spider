import os
import pandas as pd
os.chdir("D:/Dr.HanInXMU/岳阳老师/Menet")


class DataOutput:
    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_pandas(self, filename):
        output = pd.concat(self.datas, axis=0)
        output.to_xlsx(filename+".xlsx")