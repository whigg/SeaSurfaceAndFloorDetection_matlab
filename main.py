# File      :main.py
# Author    :WJ
# Function  :
# Time      :2021/08/06
# Version   :
# Amend     :

import os, h5py
import time
import numpy as np
import pandas as pd
import SeaSurfaceAndseaFloorDetection_matlab as detect
# import SeaSurfaceAndseaFloorDetection_matlab_lat as detect
np.set_printoptions(suppress=True)
import Section as sction
import ReadH5 as readh5
from icecream import ic

if __name__ == '__main__':
    path0=os.getcwd()
    # bound = [111.59, 16.532, 111.62, 16.552]#20190222
    # bound = [111.455, 16.443, 111.845, 16.456]#20190222-2
    # bound = [111.455, 16.564, 111.845, 16.570]#20190222-3

    # bound = [111.59, 16.530, 111.62, 16.5476]#20190524
    # bound = [111.59, 16.442, 111.62, 16.459]#20200421-1
    # bound = [111.59, 16.461, 111.62, 16.4681]#20200421-2
    # bound = [111.59, 16.531, 111.62, 16.536]#20200421-3
    # bound = [111.45, 16.559, 111.84, 16.57]#20200421-4
    # bound = [111.45, 16.4412, 111.84, 16.4655]#20190524-2
    # bound = [111.455, 16.452, 111.845, 16.490]#20190524-3
    # bound = [111.455, 16.5640, 111.845, 16.5710]  # 20190721-gt1l-1
    # bound = [111.455, 16.565, 111.845, 16.577]  # 20190721-gt2l-1
    # bound = [111.455, 16.578, 111.845, 16.597]  # 20190721-gt2l-2
    # bound = [111.455, 16.466, 111.845, 16.481]  # 20190721-gt3l-1
    bound = [111.455, 16.530, 111.845, 16.5525]  # 20190721-gt3l-2   3+48


    step1 = 3
    step2 = 48
    print("********************************************")
    ##
    # 运行目录
    path_h5='D:/Program Files (x86)/PyCharm/PycharmProjects/PythonProject/BDModel/data/data2'
    os.chdir(path_h5)
    seasurface_all=[]
    seafloor_all=[]

    # for beam in ['gt1l','gt2l','gt3l']:  #循环处理3个激光波束
    for beam in ['gt3l']:  #循环处理3个激光波束
        # h5File = 'ATL03_20190222135159_08570207_003_01'
        h5File = 'ATL03_20190721183749_03620401_004_01'
        # h5File = 'ATL03_20190421225816_03620301_004_01'
        # h5File = 'ATL03_20190524093136_08570307_003_01'
        prefix = h5File +'+'+ beam
        print('------------------------------')
        ic(prefix)

        csv_ph= readh5.h5TOcsv(h5File+'.h5',beam,bound=bound)
        print(len(csv_ph))
        if len(csv_ph)>1000:
            ic(csv_ph)
            # csv_ph.to_csv('../output/' + prefix + '_all.csv')
            os.chdir(path0)
            ic(os.getcwd())
            seaSurface, aboveSurface, underSurface, seaFloor1, seaFloor2, seaFloor3 = detect.surfaceAndFloorDetection(
            csv_ph, step1, step2)
            ic()
            seasurface_all.extend(seaSurface.to_numpy())
            seafloor_all.extend(seaFloor3.to_numpy())
            ic()
            # seaSurface.to_csv('../output/' + prefix + '_seaSurface.csv')
            # seaFloor3.to_csv('../output/' + prefix + '_seaFloor_03.csv')
            sction.Section_all(csv_ph,seaSurface,seaFloor1,seaFloor2,seaFloor3, prefix + '_result_' + str(step1) + '+' + str(step2))
            sction.Section_one(seaSurface, prefix + '_surface_' + str(step1) + '+' + str(step2))
            sction.Section_one(seaFloor3, prefix + '_seafloor_' + str(step1) + '+' + str(step2))
            os.chdir(path_h5)

    os.chdir(path0)
    print(len(seasurface_all))
    seasurface_all=np.array(seasurface_all)
    seasurface_all_cut=seasurface_all[:,0:5]
    np.savetxt('./output/seasurface_20190721-gt3l-2.txt',seasurface_all_cut,delimiter=',',fmt='%.03f')

    print(len( seafloor_all))
    seafloor_all = np.array(seafloor_all)
    seafloor_all_cut =  seafloor_all[:, 0:5]
    np.savetxt('./output/seafloor_20190721-gt3l-2.txt', seafloor_all_cut, delimiter=',',fmt='%.03f')#,




