

# 得到下一步节点

def getNextPosition(allowedList, edgeMatrix):

	return allowedList[0]

# pv 表示充电速度
pv = 1 
def move(carIndex, position, s, aliveTime, power, weight, servedList, leftList):
	allowedList = calAllowedClientList(carIndex, position, s, aliveTime, power,
	 carWeightMatrix, servedList, leftList, nowTime)
	nextPosition = getNextPosition(allowedList)
	if nextPosition == -1:
		print("无解")
	else:
		# 更新总路程
		d = distanceMatrix[position][nextPosition]
		s += d

		# 更新电量和时间
		t0 = d / v
		expensePower = expensePower = (a * weight + b) * d;
		power -= expensePower;
		arrivalTime = nowTime + t0;
		part_update_pheromone(edgeMatrix);
		if nextPosition in chargerList:
			# 目标点为充电桩，充电时间为t1
			t1 = 0
			if (power < carPowerCapacity[carIndex]*0.8):
				t1 = (carPowerCapacity[carIndex]*0.8 - power) / pv;
				power = carPowerCapacity[carIndex]*0.8
			nowTime += t1

			# 更新重量
			for i in range(garbageNum):
				carWeightMatrix[garbageNum] += clientWeightMatrix[garbageNum]

		elif nextPosition in clientList:
			# 目标点为客户点，
			nowTime = max(clientWindow[nextPosition][0], nowTime) + clientServeTime[nextPosition]
		# 更新局部信息素浓度
		part_update_pheromone(edgeMatrix)
		


def global_update_pheromone(edgeMatrix):


# 局部更加信息素浓度
def part_update_pheromone(edgeMatrix):
