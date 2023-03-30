# -*- coding: utf-8 -*-
import json
from imp import reload
from tools import geofunc_rh
from tools.nfp import NFP
reload(geofunc_rh)
import pandas as pd
import rhinoscriptsyntax as rs
import Rhino as rc


def addLastPoint(ptlist):
    '''根据rhino的需要，添加一个末尾的点，和第一个点的坐标一样'''
    assert isinstance(ptlist,list) and len(ptlist)>0,"ptlist的长度必须大于0,且是列表,它目前是{}".format(ptlist)
    ptlist.append(ptlist[0])
    return ptlist

# 计算NFP然后寻找最合适位置
def tryNFP():
    # df = pd.read_csv("data/blaz1.csv")
    df = pd.read_csv(r"D:\02_Netsore_drive\TJU_Net\02_AutoDispartCoding\2D_Irregular\2D-Irregular-Packing-Algorithm\data\blaz1.csv")

    # 读取csv文件，这个文件是从blaz1.json中提取出来的，用于测试
    poly1=json.loads(df['polygon'][1]) # 序列化的二维点坐标的列表 # 从csv中读取polygon,列表的序号是从0开始的
    poly2=json.loads(df['polygon'][4])
    # 坐标变换
    poly1 = geofunc_rh.GeoFuncRH.normData(poly1,50) # 坐标扩大50倍
    poly2 = geofunc_rh.GeoFuncRH.normData(poly2,50) 
    geofunc_rh.GeoFuncRH.slidePoly(poly1,500,500) # 平移500距离

    # 对于rc来说，增加一个末尾点的坐标，和第一个点的坐标一样
    # closedpoly1 = addLastPoint(poly1) # 闭合多边形的点
    # closedpoly2 = addLastPoint(poly2)
    print('这是pl1{}，类型是{}'.format(poly1,type(poly1)))
    print('这是pl2{}，类型是{}'.format(poly2,type(poly2)))
    
    # zyf 尝试用rhino的方法画出来
    ptlist1 = [rc.Geometry.Point3d(pt[0],pt[1],0) for pt in poly1]
    ptlist2 = [rc.Geometry.Point3d(pt[0],pt[1],0) for pt in poly2]

    # 画出polilinecurve
    plcurve1 = rc.Geometry.PolylineCurve(ptlist1)
    plcurve2 = rc.Geometry.PolylineCurve(ptlist2)
    
    startptindex = geofunc_rh.GeoFuncRH.checkBottom(poly1)
    startpt = rc.Geometry.Point3d(poly1[startptindex][0],poly1[startptindex][1],0.0)
    return [plcurve1,plcurve2,startpt]
    
    # zyf修改 20230327
    # assert 2<1,"zyfdebuging中"
    nfp=NFP(poly1,poly2,show=True)
    # print(nfp.nfp)


def test():
    print("test成功!")

if __name__ == '__main__':
    # PlacePolygons(getData())
    tryNFP()