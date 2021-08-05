# File      :Double_Gaussian_02.py
# Author    :WJ
# Function  :双峰正态分布拟合(结合matlab)
# Time      :2021/07/01
# Version   :
# Amend     :

import numpy as np
import matlab.engine
import matplotlib.pyplot as plt

def Gaussian1(x, a,u, sigma):
    return a * np.exp(-((x - u) /sigma)**2)

def Gaussian2(x, a1, u1, sigma1, a2, u2, sigma2):
     return a1 * np.exp(-((x - u1) / sigma1) ** 2) + a2 * np.exp(-((x - u2) / sigma2) ** 2)

def Gaussian1_fit(eng = matlab.engine.start_matlab(),hist=[0,1]):
     np.savetxt('./output/data_1fit.txt', hist, delimiter=' ')
     try:
          eng.eval(
               "data=textread('D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\data_1fit.txt');",
               nargout=0)
          eng.eval("X=data(:,1);", nargout=0)
          eng.eval("Y=data(:,2);", nargout=0)
          eng.eval("fre = fit( X, Y, 'Gauss1');", nargout=0)
          eng.eval("beta=[fre.a1,fre.b1,fre.c1]';", nargout=0)
          eng.eval(
               "save -ascii 'D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\Gaus1_para.txt' beta;",
               nargout=0)
          eng.eval("clear", nargout=0)
          Gaus_para = np.loadtxt(
               'D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\Gaus1_para.txt')
     except:
          data=np.loadtxt(
               'D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\data_1fit.txt',delimiter=' ')
          Gaus_para=[1,np.median(data[:,0]),(np.max(data[:,0])-np.min(data[:,0]))/2]
     return Gaus_para

def Gaussian2_fit(eng = matlab.engine.start_matlab(),hist=[0,1]):
     np.savetxt('./output/data_2fit.txt', hist, delimiter=' ')
     eng.eval(
          "data=textread('D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\data_2fit.txt');",
          nargout=0)
     eng.eval("X=data(:,1);", nargout=0)
     eng.eval("Y=data(:,2);", nargout=0)
     eng.eval("fre = fit( X, Y, 'Gauss2');", nargout=0)
     eng.eval("beta=[fre.a1,fre.b1,fre.c1,fre.a2,fre.b2,fre.c2]';", nargout=0)
     eng.eval(
          "save -ascii 'D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\Gaus2_para.txt' beta;",
          nargout=0)
     eng.eval("clear", nargout=0)
     Gaus_para = np.loadtxt(
          'D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\Gaus2_para.txt')
     return Gaus_para


def Gaussian1_show(data, med, sigma2, num, times):
    plt.figure(figsize=(8, 4.5))
    # plt.scatter(data[:,0],data[:,1],marker='.',c='r',label='true')
    x = np.linspace(np.min(data[:, 0]), np.max(data[:, 0]), 100)
    # y=gaussian(x,para[0],para[1],para[2])
    # plt.plot(x,y,c='r',label='fit')
    plt.bar(data[:, 0], data[:, 1], label='hist_h', width=0.1)
    plt.axvline(x=med, ls='-', c='r', label='median=' + str(format(med, '.3f')))  # 添加垂直线
    plt.axvline(x=med - 2 * abs(sigma2), ls='--', c='gray')  # 添加垂直线
    plt.axvline(x=med + 2 * abs(sigma2), ls='--', c='gray', )  # 添加垂直线
    plt.xlabel('h')
    plt.ylabel('count')
    plt.legend(loc='best')
    plt.savefig('./pic/seaFloor/Gaussian1&Hist_' + str(format(times, '1d')) + '_' + str(format(num, '1.3f')) + '.png')
    # plt.pause(10)
    plt.close()


def Gaussian2_show(data,para,u1, sigma1, num):
    plt.figure(figsize=(8, 4.5))
    # plt.scatter(data[:,0],data[:,1],marker='.',c='r',label='true')
    x = np.linspace(np.min(data[:, 0]), np.max(data[:, 0]), 100)
    y = Gaussian2(x, para[0], para[1], para[2], para[3], para[4], para[5])
    plt.plot(x, y, c='r', label='fit')
    plt.bar(data[:, 0], data[:, 1], label='hist_h', width=0.1)
    plt.axvline(x=u1, ls='-', c='deeppink', label='u1=' + str(format(u1, '.3f')))  # 添加垂直线
    # plt.axvline(x=para[4], ls='-', c='red',label='u2='+str(format(para[4], '.3f'))) # 添加垂直线
    plt.axvline(x=u1 - 3 * abs(sigma1), ls='--', c='gray')  # 添加垂直线
    plt.axvline(x=u1 + 3 * abs(sigma1), ls='--', c='gray')  # 添加垂直线
    plt.xlabel('h')
    plt.ylabel('count')
    plt.legend(loc='best')
    plt.savefig('./pic/seaSurface/Gaussian2&Hist_' + str(format(num, '1.3f')) + '.png')
    # plt.pause(10)
    plt.close()


if __name__=='__main__':

     # <editor-fold desc="test01">
     x = [[129.2926, 122.5626, 117.0427, 109.4045, 101.8072, 97.1049, 88.5742, 78.3659, 67.9594, 59.6875, 52.5793, 47.9517,
          41.0180, 33.7457, 26.0918]]
     y = [[ 80,155.88, 174.5, 165.87, 159.03, 123.98, 72.22, 41.8,18.33, 50, 60, 80, 90, 60, 30]]

     x=np.transpose(x)
     y=np.transpose(y)
     data=np.hstack((x,y))
     np.savetxt('./output/data_2fit.txt',data,delimiter=' ')

     eng = matlab.engine.start_matlab()
     eng.eval("data=textread('D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\data_2fit.txt');", nargout=0)
     eng.eval("X=data(:,1);", nargout=0)
     eng.eval("Y=data(:,2);", nargout=0)
     eng.eval("fre = fit( X, Y, 'Gauss2');", nargout=0)
     eng.eval("beta=[fre.a1,fre.b1,fre.c1,fre.a2,fre.b2,fre.c2]';", nargout=0)
     eng.eval("save -ascii 'D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\data_ok.txt' beta;", nargout=0)
     ok=np.loadtxt('D:\Program Files (x86)\PyCharm\PycharmProjects\PythonProject\BathymetricDepthModel\output\data_ok.txt')
     print(ok)



     plt.figure(figsize=(16,9))
     plt.scatter(data[:,0],data[:,1],marker='.',c='r',label='true')
     x=np.linspace(np.min(data[:,0]),np.max(data[:,0]),100)
     y=Gaussian2(x,ok[0],ok[1],ok[2],ok[3],ok[4],ok[5])
     plt.plot(x,y,c='b',label='fit')
     plt.axvline(x=ok[1], ls='--', c='red',label='u1='+str(ok[1])) # 添加垂直线
     plt.axvline(x=ok[4], ls='--', c='red',label='u2='+str(ok[4])) # 添加垂直线
     plt.legend(loc='best')
     plt.show()
     # </editor-fold>
     # eng = matlab.engine.start_matlab()
     # a=run_double_Gaussian(eng)
     # print(a)


