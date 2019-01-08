import numpy as np
import random

homeNum = 1  # 车场个数
carNum = 3  # 车型个数
clientNum = 5  # 客户个数
garbageNum = 4  # 垃圾种类数
chargerNum = 3  # 充电桩个数
# 每个客户的垃圾重量规格矩阵
clientWeightMatrix = np.zeros(shape=(clientNum, garbageNum))
# 每个客户的时间窗
clientTimeWindow = np.zeros(shape=(clientNum, 2))
# 每个客户需要的服务时间
clientServeTime = np.zeros(shape=(clientNum, 2))
# 每种车型的垃圾容量矩阵
collectorMatrix = np.zeros(shape=(carNum, garbageNum))
# 每种车型工作时长
carServeTime = np.zeros(shape=(carNum, 1))
# 每种车型电池规格
carPowerCapacity = np.zeros(shape=(carNum, 1))
# 车子运行速度
moveSpeed = 1
# 充电速度
chargeSpeed = 1

antNum = 10  # 蚂蚁个数
times = 100  # 迭代次数

# 节点个数，车场+客户+充电桩
nodeNum = homeNum + clientNum + chargerNum
# 距离矩阵（边矩阵 nodeNum * nodeNum)，第0个代表车场，第1到homeNum个为客户，第homeNum+1到nodeNum-1为充电桩
distanceMatrix = np.zeros(shape=(nodeNum, nodeNum))
# 信息素浓度矩阵，同上
pheromoneMatrix = np.zeros(shape=(nodeNum, nodeNum))

# 每个客户点最近距离的充电桩
leastCloseChargerList = np.zeros(shape=(clientNum, 1))

# 当前车型重量矩阵
curCarWegithMatrix = np.zeros(shape=(1, garbageNum))
# 当前车型号
curCarIndex = 0
# 蚂蚁行走路径
route = []

# 移动速度
move_speed = 1;

# 充电速度
charge_speed = 1;

# 计算重量备选集，表示当前能够去服务的客户点，只考虑重量约束
def getAllowedWeightList(leftList, clientWeightMatrix, curCarWegithMatrix, curCarIndex):
    resList = []
    for i in range(len(leftList)):
        clientId = leftList[i];
        realClientId = clientId - homeNum;
        can = True;
        for j in range(garbageNum):
            if curCarWegithMatrix[0][j] + clientWeightMatrix[realClientId][j] > collectorMatrix[curCarIndex][j]:
                can = False;
                break;
        if can:
            resList.append(clientId)
    return resList;


# 计算时间窗约束备选集1, 从当前点直接去下一个客户点
def getAllowedTimeList1(leftList, curTime, curPosition, clientTimeWindow, distanceMatrix, v):
    resList = []
    for i in range(len(leftList)):
        clientId = leftList[i]
        realClientId = clientId - homeNum;
        expandTime = distanceMatrix[curPosition][clientId] / v;
        if curTime + expandTime <= clientTimeWindow[realClientId][1]:
            resList.append(clientId)
    return resList;


# 计算时间窗约束备选集2，从当前点去最近充电桩，然后去下一个客户点
def getAllowedTimeList2(leftList, curtimme, curPower, curPosition, curCarIndex, clientTimeWindow, distanceMatrix, v,
                        chargeV):
    resList = []
    for i in range(len(leftList)):
        clientId = leftList[i]
        realClientId = clientId - homeNum
        leastCloseChargerId = leastCloseChargerList[realClientId];
        distance = distanceMatrix[curPosition][leastCloseChargerId] + distanceMatrix[leastCloseChargerId][clientId];
        chargePower = carPowerCapacity[curCarIndex] * 0.8 + calPower(
            distanceMatrix[curPosition][leastCloseChargerId]) - curPower;
        chargeTime = chargePower / chargeV;
        expandTime = distance / v + chargeTime;
        if expandTime + curtimme <= clientTimeWindow[realClientId][1]:
            resList.append(clientId)
    return resList;


# 计算电量备选集1, 从当前点直接去客户点
def getAllowedPowerList1(leftList, curPosition, curPower, distanceMatrix):
    resList = []
    for i in range(len(leftList)):
        clientId = leftList[i];
        distance = distanceMatrix[curPosition][clientId] + distanceMatrix[0][clientId];
        if curPower >= calPower(distance):
            resList.append(clientId);
    return resList;


# 计算电量备选集2，从当前点（不为车场和充电桩），先去最近的充电桩，然后再去客户点
def getAllowedPowerList2(leftList, curPosition, curPower, distanceMatrix):
    resList = []
    for i in range(len(leftList)):
        clientId = leftList[i];
        realClientId = clientId - homeNum;
        # 获取最近的充电桩
        leastCloseChargerId = leastCloseChargerList[realClientId];
        distance = distanceMatrix[curPosition][leastCloseChargerId];
        if curPower >= calPower(distance):
            resList.append(distance)
    return resList;


# 计算耗电量
def calPower(x):
    a = 1;
    b = 1;
    return a * x + b;



# 计算Transition rule
alpha = 1;
beta = 1;
gamma = 1;

# 计算转移概率，并且根据轮盘赌返回一个客户点
def getClientIdByTransitionRule(resList, curPosition):
    xi_list = [];
    for clientId in resList:
        # 节约数
        mu = distanceMatrix[curPosition][0] + distanceMatrix[0][clientId] - distanceMatrix[curPosition][clientId];
        xi = pheromoneMatrix[curPosition][clientId] ** alpha + \
             distanceMatrix[curPosition][clientId] ** beta + \
             mu ** gamma
        last_xi = 0;
        if len(xi_list) > 0:
            last_xi = xi_list[-1];
        xi_list.append(last_xi + xi);
    start = 0;
    end = xi_list[-1];
    rand_xi = random.uniform(start, end);

    for i in range(len(xi_list)-1):
        if xi_list[i] <= rand_xi and rand_xi < xi_list:
            return resList[i];
    return resList[-1];



# 初始化
def initial():
    print("initializing");
    carNumMatrix = np.zeros(shape=(carNum, 1));
    print(carNumMatrix);


def process_when_is_depot(leftList, carFistVisited, curCarWeightMatrix, curCarIndex, curTime):
    curPosition = 0; # 代表当前在车场
    if carFistVisited == True:
        # 表示当前车辆第一次访问车场
        nextClientId = getClientIdByTransitionRule(leftList, curPosition);
        return nextClientId;
    else:
        allowed_list = getAllowedTimeList1(leftList, curTime, curPosition, clientTimeWindow, distanceMatrix, move_speed)
        if len(allowed_list) == 0:
            ## 方案不可行
            return -1;
        else:
            nextClientId = getClientIdByTransitionRule(allowed_list, curPosition);
            return nextClientId;


def process_when_is_customer(leftList, curCarIndex, curCarWeightMatrix, curTime, curPosition, curPower):
    weight_allowed_list = getAllowedWeightList(leftList, clientWeightMatrix, curCarWeightMatrix, curCarIndex);
    if len(weight_allowed_list) == 0:
        # 只能返回车场
        return 0;
    else:
        # 时间窗约束, 直接从当前客户点到下一个客户点
        time_allowed_list1 = getAllowedTimeList1(weight_allowed_list, curTime, curPosition, clientTimeWindow, distanceMatrix, move_speed);
        if len(time_allowed_list1) > 0:
            nextCientId = getClientIdByTransitionRule(time_allowed_list1, curPosition);
            return nextCientId;
        else:
            time_allowed_list2 = getAllowedTimeList2(weight_allowed_list, curTime, curPower, curPosition, curCarIndex
                                                     ,clientTimeWindow, distanceMatrix, move_speed, charge_speed);
            if len(time_allowed_list2) > 0:
                nextClientId = getClientIdByTransitionRule(time_allowed_list2, curPosition);
                return nextClientId;
            else:
                # 返回车场
                return 0;










if __name__ == "__main__":
    initial();
