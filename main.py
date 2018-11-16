import numpy as np
import random

homeNum = 1 # 车场个数
carNum = 3 # 车型个数
clientNum = 5 # 客户个数
garbageNum = 4 #垃圾种类数
chargerNum = 3 #充电桩个数
#每个客户的垃圾重量规格矩阵
clientWeightMatrix = np.zeros(shape=(clientNum, garbageNum))
#每个客户的时间窗
clientWindow = np.zeros(shape=(clientNum, 2))
#每个客户需要的服务时间
clientServeTime = np.zeros(shape=(clientNum, 1))
#每种车型的垃圾容量矩阵
collectorMatrix = np.zeros(shape=(carNum, garbageNum))
#每种车型工作时长
carServeTime = np.zeros(shape=(carNum, 1))
#每种车型电池规格
carPowerCapacity = np.zeros(shape=(carNum, 1))
#车子运行速度
moveSpeed = 1
#充电速度
chargeSpeed = 1

antNum = 10 # 蚂蚁个数
times = 100 # 迭代次数

#节点个数，车场+客户+充电桩
nodeNum = homeNum + clientNum + chargerNum 
#距离矩阵（边矩阵 nodeNum * nodeNum)，第0个代表车场，第1到homeNum个为客户，第homeNum+1到nodeNum-1为充电桩
distanceMatrix = np.zeros(shape=(nodeNum, nodeNum))
#信息素浓度矩阵，同上
distanceMatrix = np.zeros(shape=(nodeNum, nodeNum))



def init():# 变量初始化
    

def random():
	return 1

def roulette(allowedList):
	return 1

def allowed():
	return allowedList

def initial():
	# 剩余车型
	leftCarList = [i for i in range(0, carNum)]
	# 随机从剩余车型选择一种车型，并从列表删除该车型
	carIndx = getRandCar(leftCarList)
	# 当前位置，初始在车场
	position = 0
	# 经过的路程
	s = 10
	# 已服务时间
	aliveTime = 0
	# 电量
	power = 100
	# 已载的重量
	weight = 0
	# 已服务过的客户列表
	servedList = []
	# 剩下未服务的客户列表
	leftList = [i for i range(1, clientNum)]
	#delta信息素浓度矩阵，本次迭代信息素浓度增量
	deltaEdgeMatrix = np.zero(shap=(nodeNum, 2))
	serve(carIndex, position, s, aliveTime, power, weight, servedList, leftList)

def getRandCar(leftCarList):
	rand = random.randint(0, len(leftCarList)-1)
	randCar = leftCarList[rand]
	leftCarList.remove(randCar)
	return randCar


def serve(carIndex, position, s, aliveTime, power, weight, servedList, leftList):
	if len(leftList) == 0:
		print("收集完毕")
		return
	if position == 0:#0代表当前在车场，选择去另一个客户点
		nextClientPosition = getNextClient(carIndex, position, s, aliveTime, power, weight, leftList)
	elif position > clientNum: #表示当前位置在充电桩
		nextClientPosition = getNextClient(carIndex, position, s, aliveTime, power, weight, leftList)
	else:
		# 当前在客户点，可能去车场，可能去充电桩，可能去客户点
		nextPostion = getNextPostion

# 从一个客户点去下一个位置：可能去车场，可能去充电桩，可能去客户点
def getNextPostion(carIndex, position, s, aliveTime, power, weight, leftList):
	rand = random.randint(len(leftList)-1)
	return leftList[rand]

# 从剩下未服务的客户节点返回一个节点
def getNextClient(carIndex, position, s, aliveTime, power, weight, leftList):
	rand = random.randint(len(leftList)-1)
	return leftList[rand]

def iterate:
	k = 0
	s = 10
	aliveTime = 0
	power = 80
	weight = 90
	allowedList = allowed()
	next = roulette(allowedList)
	aliveTime += distance(k, next) / v
	if next == 0:#回到车场
		power = power >= 20? 100: power+100

	part_update_pheromone(k, next)








if __name__ == "__main__":
    print("this is main function")
    init()