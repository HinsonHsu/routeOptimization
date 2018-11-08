

# 计算备选集
def calAllowedClientList(carIndex, position, s, aliveTime, power, carWeightMatrix, servedList, leftList, nowTime):
	weight = carWeightMatrix.sum()
	resList1 = calWindowAllowedList(carIndex, position, leftList, nowTime, aliveTime)
	resList2 = calPowerAllowedList(carIndex, position, resList1, power)
	resList3 = calWeightAllowedList(carIndex, position, leftList, carWeightMatrix)
	return resList2

# 计算备选集1，时间窗约束+时长约束
def calWindowAllowedList(carIndex, position, leftList, nowTime, aliveTime):
	resList = []
	for clientId in leftList:
		d = distanceMatrix[clientId][position]
		t = d/v
		if nowTime + t <= clientServeTime[clientId][0] 
		and max(nowTime+t, clientServeTime[clientId][0])+aliveTime<carServeTime[0][carIndex]:
			resList.append(clientId)
	return resList

# 耗电量计算公式 y = ax + b, y为单位路程内耗电量，a是比例，x是重量，b是常量
a = 1
b = 10

# 计算备选集2，电量约束
def calPowerAllowedList(carIndex, position, leftList, power,weight):
	resList = []
	for clientId in leftList:
		d = distanceMatrix[clientId][position]
		# y = ax + b 耗电量计算公式
		expensePower = (a * weight + b) * d;
		if power - expensePower >= 0:
			resList.append(clientId)
	return resList

# 计算备选集3，重量约束
def calWeightAllowedList(carIndex, position, leftList, carWeightMatrix):
	resList = []
	for clientId in leftList:
		flag = True;
		for i in range(garbageNum):
			if carWeightMatrix[carIndex][i] < clientWeightMatrix[clientId]:
				flag = False;
				break;
		if flag:
			resList.append(clientId)



# chargerList 充电桩列表，每个列表保存charger所在位置
def calAllowedChargerList(carIndex, position, chargerList,power,weight):
	resList = []
	for i in chargerList:
		if (i != carIndex):
			d = distanceMatrix[position][i]
			expensePower = (a * weight + b) * d
			if expensePower <= power:
				resList.append(i)
	return resList;
