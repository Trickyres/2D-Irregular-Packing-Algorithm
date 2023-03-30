import json
from tools.geofunc import GeoFunc
from tools.nfp import NFP
import pandas as pd

# 计算NFP然后寻找最合适位置
def tryNFP():
    df = pd.read_csv("data/blaz1.csv")

    poly1=json.loads(df['polygon'][1]) # 序列化的点列表 # 从csv中读取polygon,列表的序号是从0开始的
    poly2=json.loads(df['polygon'][4])
    print('这是pl1{}，类型是{}'.format(poly1,type(poly1)))
    print('这是pl2{}，类型是{}'.format(poly2,type(poly2)))
    GeoFunc.normData(poly1,50) # 坐标扩大50倍
    GeoFunc.normData(poly2,50) 
    GeoFunc.slidePoly(poly1,500,500) # 平移500距离

    nfp=NFP(poly1,poly2,show=True)
    print(nfp.nfp)

if __name__ == '__main__':
    # PlacePolygons(getData())
    tryNFP()