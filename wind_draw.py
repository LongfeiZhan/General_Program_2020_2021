# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:19:26 2020

@author: ZhanLF
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import math
import matplotlib as mpl
mpl.rcParams['font.sans-serif']=['SimHei']


data = pd.read_csv('1961-2019TEM_WIN_MON.txt', header=1, sep=' ', na_values = range(999000,1000000)) #读取并存为dataframe格式

dataarray = data.values  #将dataframe转为数组

# 按站名和月份整理数据
def get_seasondata(sta_name,mon1,mon2,mon3):
    sta_data = dataarray[dataarray[:,0] == sta_name,:]
    r = -1
    final_data = []
    for mon in sta_data[:,6]:
        r = r + 1
        if mon == mon1 or mon == mon2 or mon == mon3:
            final_data.append(sta_data[r,:])
    final_data = np.array(final_data)

    mark = []
    for i in range(1,len(final_data[:,6])):
        if final_data[i-1,6] == final_data[i,6]:
            mark.append(i)
    final_data = np.delete(final_data, mark, axis=0)
    return final_data

# 整理成季节平均风速 日平均风速即2min平均风速位于第22列
def wind_ave(data):
    avelist = []
    for i in range(0,177,3):
        ave = np.nanmean(data[i:(i+3),22], dtype = np.float64) # i:i+3,不包含i+3
        avelist.append(ave)
    return avelist

# 计算历年夏季平均风速
xinjian_sm = get_seasondata('新建', 6, 7, 8)
xj_sm_wind = wind_ave(xinjian_sm)
nanchang_sm = get_seasondata('南昌', 6, 7, 8)
nc_sm_wind = wind_ave(nanchang_sm)
anyi_sm = get_seasondata('安义', 6, 7, 8)
anyi_sm_wind = wind_ave(anyi_sm)
jinxian_sm = get_seasondata('进贤', 6, 7, 8)
jx_sm_wind = wind_ave(jinxian_sm)

# 计算历年冬季平均风速
xinjian_wt = get_seasondata('新建', 12, 1, 2)
xj_wt_wind = wind_ave(xinjian_wt)
nanchang_wt = get_seasondata('南昌', 12, 1, 2)
nc_wt_wind = wind_ave(nanchang_wt)
anyi_wt = get_seasondata('安义', 12, 1, 2)
anyi_wt_wind = wind_ave(anyi_wt)
jinxian_wt = get_seasondata('进贤', 12, 1, 2)
jx_wt_wind = wind_ave(jinxian_wt)

# 风速折线图
plt.figure(num=1,dpi=80)
plt.plot(range(1961,2020),xj_sm_wind,'y',label='新建夏季')
plt.plot(range(1961,2020),xj_wt_wind,'y--',label='新建冬季')
plt.plot(range(1961,2020),nc_sm_wind,'r',label='南昌夏季')
plt.plot(range(1961,2020),nc_wt_wind,'r--',label='南昌冬季')
plt.plot(range(1961,2020),anyi_sm_wind,'b',label='安义夏季')
plt.plot(range(1961,2020),anyi_wt_wind,'b--',label='安义冬季')
plt.plot(range(1961,2020),jx_sm_wind,'g',label='进贤夏季')
plt.plot(range(1961,2020),jx_wt_wind,'g--',label='进贤冬季')
plt.xlabel('年份')
plt.ylabel('平均风速(m/s)')
plt.legend(ncol=4,fontsize=9,edgecolor='w')

# 根据逐月各方位平均风速，绘制风玫瑰图，47~62列为风速NNE~N的16方位平均风速 26~41列为风向频率
def get_wdws(data):
    wd = np.arange(22.5,360,22.5)
    wd = np.append(wd,0) #16方位风向，拼接北风
    temp = wd
    ws = data[0,47:63] #风速
    freqs = data[0,26:42] #频次
    for i in range(1,len(data)):
        ws = np.hstack((ws,data[i,47:63])) #  风速拼接
        wd = np.hstack((wd,temp))                # 风向拼接
        freqs = np.hstack((freqs,data[i,26:42]))  # 风向频次拼接
    # 按照风向频次累堆成新数据
    ws_mul = []
    wd_mul = []
    i = -1
    for freq in freqs:
        i = i + 1
        if math.isnan(freq):
            pass
        else:
            for times in range(int(freq)):   #有多少次频次就重复叠加几次
                ws_mul = np.hstack((ws_mul,ws[i]))
                wd_mul = np.hstack((wd_mul,wd[i]))
    return wd_mul,ws_mul
    

# 风玫瑰图
wd_mul,ws_mul = get_wdws(jinxian_sm)
ax = WindroseAxes.from_ax()
ax.bar(wd_mul, ws_mul, normed=True,bins=np.arange(0,8,2), opening=0.8, edgecolor='w')
ax.set_legend(loc = (-0.2,-0.1),title = '风速(m/s)',edgecolor='w')
