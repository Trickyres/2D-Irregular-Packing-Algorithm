# -*- coding: utf-8 -*-
import json
import rhinoscriptsyntax as rs
import Rhino as rc


class GeoFuncRH(object):
    '''
    几何相关函数
    '''
    def normData(ptlist,num):
        '''二维坐标扩大num倍'''
        assert isinstance(ptlist,list) and len(ptlist)>0,"ptlist的长度必须大于0,且是列表,它目前是{}".format(ptlist)
        for ver in ptlist:
            ver[0]=ver[0]*num
            ver[1]=ver[1]*num
        
        return ptlist
    
    def slidePoly(poly,x,y):
        '''平移二维多边形'''
        assert isinstance(poly,list) and len(poly)>0,"poly的长度必须大于0,且是列表,它目前是{}".format(poly)
        for point in poly:
            point[0]=point[0]+x
            point[1]=point[1]+y
    
    def checkBottom(poly):
        '''找到多边形的最低点的序号,目前只能处理多边形的最低点是根据列表中的输入顺序来实现的 TODO'''
        assert isinstance(poly,list) and len(poly)>0,"poly的长度必须大于0,且是列表,它目前是{}".format(poly)
        pointindex = None
        # polyP=Polygon(poly)
        poly = [rc.Geometry.Point3d(pt[0],pt[1],0) for pt in poly]
        plcurve = rc.Geometry.PolylineCurve(poly) # 画出polilinecurve
        bbox = plcurve.GetBoundingBox(True)

        if not bbox.IsValid:
            raise Exception('Error:bbox创建未成功')
        else:
            # Print the min and max box coordinates in world coordinates
            min_x,min_y = bbox.Min[0],bbox.Min[1] # 最小的x,y坐标值
            max_x,max_y = bbox.Max[0],bbox.Max[1] # 最大的x,y坐标值
        
        for index,point in enumerate(poly):
            if point[1]== min_y:
                pointindex = index
                break
        
        assert pointindex is not None,"未找到最低点"
        return pointindex
    
    def checkTop(poly):
        '''找到多边形的最高点的序号,目前只能处理多边形的最高点是根据列表中的输入顺序来实现的 TODO'''
        assert isinstance(poly,list) and len(poly)>0,"poly的长度必须大于0,且是列表,它目前是{}".format(poly)
        pointindex = None
        poly = [rc.Geometry.Point3d(pt[0],pt[1],0) for pt in poly]
        plcurve = rc.Geometry.PolylineCurve(poly) # 画出polilinecurve
        bbox = plcurve.GetBoundingBox(True)

        if not bbox.IsValid:
            raise Exception('Error:bbox创建未成功')
        else:
            # Print the min and max box coordinates in world coordinates
            min_x,min_y = bbox.Min[0],bbox.Min[1] # 最小的x,y坐标值
            max_x,max_y = bbox.Max[0],bbox.Max[1] # 最大的x,y坐标值
        
        for index,point in enumerate(poly):
            if point[1]== max_y:
                pointindex = index
                break
        
        assert pointindex is not None,"未找到最高点"
        return pointindex
    
    def checkLeft(poly):
        pass
        # polyP=Polygon(poly)
        # min_x=polyP.bounds[0]
        # for index,point in enumerate(poly):
        #     if point[0]==min_x:
        #         return index
    
    def checkRight(poly):
        pass
        # polyP=Polygon(poly)
        # max_x=polyP.bounds[2]
        # for index,point in enumerate(poly):
        #     if point[0]==max_x:
        #         return index

    def slideToPoint(slidepoly,locus_pt,start_station_pt):
        '''
        slidepoly:滑动的多边形
        locus_pt:滑动多边形的轨迹点
        start_station_pt:固定poly的起点
        函数:移动slidepoly的locuspt到start_pt的位置
        '''
        GeoFuncRH.slidePoly(slidepoly,start_station_pt[0]-locus_pt[0],start_station_pt[1]-locus_pt[1])

    # 获得某个多边形的边
    def getPolyEdges(poly):
        edges=[]
        for index,point in enumerate(poly):
            if index < len(poly)-1:
                edges.append([poly[index],poly[index+1]])
            else:
                edges.append([poly[index],poly[0]])
        return edges

    
    def intersection(line1,line2):
        '''用于touching计算交点 可以与另一个交点计算函数合并,超多次调用'''
        # 如果可以直接计算出交点
        Line1=LineString(line1)
        Line2=LineString(line2)
        inter=Line1.intersection(Line2)
        # 如果相交
        if inter.is_empty==False:
            mapping_inter=mapping(inter)
            if mapping_inter["type"]=="LineString":
                inter_coor=mapping_inter["coordinates"][0]
            else:
                inter_coor=mapping_inter["coordinates"]
            return inter_coor

        # 对照所有顶点是否相同
        res=[]
        for pt1 in line1:
            for pt2 in line2:
                if GeoFunc.almostEqual(pt1,pt2)==True:
                    # print("pt1,pt2:",pt1,pt2)
                    res=pt1
        if res!=[]:
            return res

        # 计算是否存在almostContain
        for pt in line1:
            if GeoFunc.almostContain(line2,pt)==True:
                return pt
        for pt in line2:
            if GeoFunc.almostContain(line1,pt)==True:
                return pt
        return []