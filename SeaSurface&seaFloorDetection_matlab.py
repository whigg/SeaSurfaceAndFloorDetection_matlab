# File      :SeaSurface&seaFloorDetection_matlab.py
# Author    :WJ
# Function  :
# Time      :2021/07/03
# Version   :
# Amend     :


import math
import pandas as pd
import numpy as np
import time
import Double_Gaussian_02 as Gauss2
import matlab.engine


def get_v(D, n):
    return D / (1 + math.log(n, 2))


def hist(array, step=0.1):
    print(len(array))
    x = np.arange(np.min(array), np.max(array) + step, step)
    hist = np.zeros((len(x), 1))
    for i in range(0, len(array)):
        for j in range(0, len(x) - 1):
            if array[i] >= x[j] and array[i] < x[j + 1]:
                hist[j] = hist[j] + 1
    Hist = np.vstack((x.transpose(), hist.transpose()))
    return Hist.transpose()


def get_u1sigma1(para):
    if para[1] > para[4]:
        u1 = para[1]
        sigma1 = para[2]
    else:
        u1 = para[4]
        sigma1 = para[5]
    return u1, sigma1


def surfaceAndFloorDetection(csvfile):
    '''海表光子与海底光子检测'''
    # 1.导入光子数据
    ATL03 = pd.read_csv(csvfile)
    # ATL03.sort_values('dist_ph_along', inplace=True, ignore_index=True)
    ATL03.sort_values('dist_ph_along', inplace=True, ignore_index=True)
    print('数据组织形式：')
    print(ATL03.columns.values)

    # beg = np.min(ATL03['dist_ph_along'])
    beg = np.min(ATL03['dist_ph_along'])

    # 2.设置输出格式
    aboveSurface = pd.DataFrame(columns=ATL03.columns.values)
    seaSurface = pd.DataFrame(columns=ATL03.columns.values)
    underSurface = pd.DataFrame(columns=ATL03.columns.values)
    seaFloor_01 = pd.DataFrame(columns=ATL03.columns.values)
    seaFloor_02 = pd.DataFrame(columns=ATL03.columns.values)
    seaFloor_03 = pd.DataFrame(columns=ATL03.columns.values)

    # 启动MATLAB引擎
    eng = matlab.engine.start_matlab()

    # 3.进行光子检测
    # while beg < np.max(ATL03['dist_ph_along']):
    while beg < np.max(ATL03['dist_ph_along']):
        # end = beg + 1
        end = beg + 0.7
        print(beg, end)

        # 3.1 对原数据切片
        # data_atl03 = ATL03[(beg <= ATL03['dist_ph_along']) & (ATL03['dist_ph_along'] < end)]
        data_atl03 = ATL03[(beg <= ATL03['dist_ph_along']) & (ATL03['dist_ph_along'] < end)]
        # 3.2 计算总直方图
        n=len(data_atl03)
        # D = 1
        # v=get_v(D,n)
        # print('v:',v)
        v = 0.1
        hist_ = hist(data_atl03['h_ph'].values, v)
        # 以文件与MATLAB引擎进行数据传输
        np.savetxt('./output/data_2fit.txt', hist_, delimiter=' ')

        # 3.3 双峰高斯分布拟合
        para = Gauss2.run_double_Gaussian(eng)
        print(para)
        u1, sigma1 = get_u1sigma1(para)
        # 绘制双峰高斯分布曲线
        Gauss2.visualize_double_Gaussian(hist_, para,u1,sigma1,beg)

        # 3.4 海表探测
        aboveSurface_ = data_atl03[data_atl03['h_ph'] >= u1 + 3 * abs(sigma1)]
        seaSurface_ = data_atl03[
            (u1 - 3 * abs(sigma1) <= data_atl03['h_ph']) & (data_atl03['h_ph'] < u1 + 3 * abs(sigma1))]
        underSurface_ = data_atl03[data_atl03['h_ph'] <= u1 - 3 * abs(sigma1)]

        aboveSurface = pd.concat([aboveSurface, aboveSurface_], ignore_index=False)
        seaSurface = pd.concat([seaSurface, seaSurface_], ignore_index=False)
        underSurface = pd.concat([underSurface, underSurface_], ignore_index=False)
        seafloor_=underSurface_

        # 3.5 海底探测
        for i in range(3):
            # 中值滤波迭代3次
            median=np.median( seafloor_['h_ph'])
            hist_2 = hist(seafloor_['h_ph'].values, v)
            np.savetxt('./output/data_1fit.txt', hist_2, delimiter=' ')
            para = Gauss2.run_gaussian(eng)
            sigma2 = para[2]
            seafloor_0=seafloor_[
                    (median - 2 * abs(sigma2) <= seafloor_['h_ph']) & (seafloor_['h_ph'] < median + 2 * abs(sigma2))]
            if len(seafloor_0)>3:
                seafloor_=seafloor_0


            Gauss2.visualize_gaussian(hist_2, median, sigma2,beg,i)
            if i==0:
                seaFloor_01 = pd.concat([seaFloor_01, seafloor_], ignore_index=False)
            elif i==1:
                seaFloor_02 = pd.concat([seaFloor_02, seafloor_], ignore_index=False)
            elif i==2:
                seaFloor_03 = pd.concat([seaFloor_03, seafloor_], ignore_index=False)

        # beg += 1
        beg += 0.7
    return seaSurface, aboveSurface, underSurface,seaFloor_01, seaFloor_02, seaFloor_03


if __name__ == '__main__':
    start=time.time()
    print('Running...')
    csvfile = './data/ATL03_20190222135159_08570207_003_01_gt3l.csv'
    seaSurface, aboveSurface, underSurface ,seaFloor_01, seaFloor_02, seaFloor_03= surfaceAndFloorDetection(csvfile)
    seaSurface.to_csv('./output/seaSurface.csv')
    aboveSurface.to_csv('./output/aboveSurface.csv')
    underSurface.to_csv('./output/underSurface.csv')
    seaFloor_01.to_csv('./output/seaFloor_01.csv')
    seaFloor_02.to_csv('./output/seaFloor_02.csv')
    seaFloor_03.to_csv('./output/seaFloor_03.csv')
    print('Running time:',time.time()-start)
