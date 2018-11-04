import numpy as np



def init():
    clientNum = 5 # 客户个数
    n = 4 # 垃圾种类数
    chargerNum = 3 #充电桩个数
    #每个客户的垃圾重量矩阵
    clientMatrix = np.zeros(shape=(clientNum,n))
    #每个客户所在位置
    vertexClient = np.zeros(shape=(clientNum,2))
    #每个客户的时间窗
    windowsClient = np.zeros(shape=(clientNum, 3))
    #每个充电桩的位置
    vertextCharger = np.zeros(shape=(chargerNum, n))
    collectorNum = 2 # 车型个数
    #每种车型的垃圾容量矩阵
    collectorMatrix = np.zeros(shape=(collectorNum, n))


if __name__ == "__main__":
    print("this is main function")
    init()