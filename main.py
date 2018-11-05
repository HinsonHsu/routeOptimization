import numpy as np




homeNum = 1 # 车场个数
vertexHome = np.zeros(shape=(homeNum, 2)); # 默认车场位置为0,0
windowsHome = np.zeros(shape=(homeNum, 2)); # 车场工作时间

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

antNum = 10 # 蚂蚁个数
times = 100 # 迭代次数

#节点个数，车场+客户+充电桩
nodeNum = homeNum + clientNum + chargerNum 
#信息素浓度矩阵（边矩阵 nodeNum * nodeNum)
edgeMatrix = np.zeros(shape=(nodeNum, 2))

def init():# 变量初始化
    


def iterate:


def global_update_pheromone():


def 


if __name__ == "__main__":
    print("this is main function")
    init()