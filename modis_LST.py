# -*- coding: utf-8 -*-

from osgeo import gdal
import numpy as np
import os

path = r'F:\dongji\jieguo'
tiflists = os.listdir(path)
temp = np.full((121,131),np.nan)
for tiflist in tiflists:
    dataset = gdal.Open(path + '\\' + tiflist)
    im_col = dataset.RasterXSize
    im_row = dataset.RasterYSize
    im_geotrans = dataset.GetGeoTransform()
    x = np.linspace(im_geotrans[0],im_geotrans[0]+im_geotrans[1]*im_col,im_col,dtype=float)
    y = np.linspace(im_geotrans[3],im_geotrans[3]+im_geotrans[5]*im_row,im_row,dtype=float)
    mx,my = np.meshgrid(x,y)
    band = dataset.GetRasterBand(1)   
    im_datas = band.ReadAsArray(0, 0, im_col, im_row)
    data = im_datas[86:207,976:1107]
    mx = mx[86:207,976:1107]
    my = my[86:207,976:1107]
    tem = 0.02 * data - 273.15
    tem[tem<0] = np.nan
    temp = np.vstack((temp,tem))

    
temp_del = np.delete(temp,range(121),axis = 0)   # 删除最初的空数组 
temp_3 = np.resize(temp_del,[92,121,131])    # 变成三维矩阵
mean_temp = np.nanmean(temp_3,axis = 0)
heatisland = mean_temp - 27 # 郊区平均地温27℃

row_data_temp = np.full((1,3),np.nan)
for i in range(121):
    for j in range(131):
        row_data = np.array([mx[i,j],my[i,j],mean_temp[i,j]])
        row_data_temp = np.vstack((row_data_temp,row_data))

data_lonlat = np.delete(row_data_temp,0,axis=0) #南昌市LST

# 保存到txt
# np.savetxt(r'冬季平均LST.txt',data_lonlat,fmt = '%0.8f')

#释放内存。如果不释放，在arcgis或envi中打开该图像时显示文件已被占用
del dataset
'''
借鉴以下代码！！！
#栅格矩阵的列数
im_col = dataset.RasterXSize

#栅格矩阵的行数
im_row = dataset.RasterYSize

#波段数
im_bands = dataset.RasterCount

#仿射矩阵，左上角像素的大地坐标和像素分辨率。
#共有六个参数，分表代表左上角x坐标；东西方向上图像的分辨率；如果北边朝上，地图的旋转角度，0表示图像的行与x轴平行；左上角y坐标；
#如果北边朝上，地图的旋转角度，0表示图像的列与y轴平行；南北方向上地图的分辨率。
im_geotrans = dataset.GetGeoTransform()

# 生成经纬度网格
x = np.linspace(im_geotrans[0],im_geotrans[0]+im_geotrans[1]*im_col,im_col,dtype=float)
y = np.linspace(im_geotrans[3],im_geotrans[3]+im_geotrans[5]*im_row,im_row,dtype=float)
mx,my = np.meshgrid(x,y)

#地图投影信息
im_proj = dataset.GetProjection()

#读取某一像素点的值
#（1）读取一个波段，其参数为波段的索引号，波段索引号从1开始(我打开的这幅图像只有一个波段)
band = dataset.GetRasterBand(1)

#（2）用ReadAsArray(<xoff>, <yoff>, <xsize>, <ysize>)，读出从(xoff,yoff)开始，大小为(xsize,ysize)的矩阵。以下为读取整幅图像
im_datas = band.ReadAsArray(0, 0, im_col, im_row)

#（3）获取某一或某几个像素的值
data = im_datas[86:207,976:1107]
tem = 0.02*data-273.15

#释放内存。如果不释放，在arcgis或envi中打开该图像时显示文件已被占用
del dataset
'''
