import numpy as np
import copy
import xlrd
import random

class Solution:
    garbage_num = 2  # 垃圾种类数
    client_num = 20  # 客户数
    depot_num = 1  # 车场数，为1
    charger_num = 3  # 充电桩数
    collector_num = 3  # 垃圾收集车型种类数

    c_speed = 200.0  # 充电速度
    r_speed = 1.0  # 耗电速度
    g_speed = 3.47  # 充电速度
    v_speed = 1.0  # 车速
    unload_speed = 1.0 # 卸货速度

    # 客户垃圾矩阵
    gar_client_matrix = np.zeros(shape=(client_num, garbage_num))

    # 车型垃圾容量矩阵
    gar_collector_matrix = np.zeros(shape=(collector_num, garbage_num))

    # 车型电量矩阵
    power_capacity_collector_matrix = np.zeros(shape=(collector_num, 1))

    # 车场和客户时间窗
    time_windows = np.zeros(shape=(depot_num + client_num, 2))

    # 已经服务过的客户点列表
    served_client_list = []

    # 未服务的客户点列表
    un_served_client_list = [i for i in range(client_num)]

    # 运行路线
    route = []

    # 信息素浓度，第一个点为车场，中间为客户点，最后为充电站
    node_num = depot_num + client_num + charger_num
    pheromone_matrix = np.zeros(shape=(node_num, node_num))

    # 距离矩阵
    dis_matrix = np.zeros(shape=(node_num, node_num))

    # 每个客户点最近的充电桩位置，为position_id
    client_closest_charger = []

    def __init__(self):
        print("数据初始化")
        data = xlrd.open_workbook(r"data.xlsx")
        dis_data = data.sheet_by_index(0)

        Solution.garbage_num = 2
        Solution.client_num = 20
        Solution.depot_num = 1
        Solution.charger_num = 3
        Solution.collector_num = 3
        Solution.node_num = Solution.depot_num + Solution.client_num + Solution.collector_num

        print("读取距离虚信息")
        for i in range(Solution.node_num):
            for j in range(i):
                Solution.dis_matrix[i][j] = dis_data.cell(i+2, j+1).value

        for i in range(Solution.node_num):
            for j in range(i):
                Solution.dis_matrix[j][i] = Solution.dis_matrix[i][j]

        print("读取客户需求信息")
        client_data = data.sheet_by_index(1)
        for i in range(Solution.garbage_num):
            for j in range(Solution.client_num):
                Solution.gar_client_matrix[j][i] = client_data.cell(2+i, 2+j).value

        # print(Solution.gar_client_matrix)

        print("读取车型信息")
        collector_data = data.sheet_by_index(2)
        for i in range(Solution.garbage_num):
            for j in range(Solution.collector_num):
                Solution.gar_collector_matrix[j][i] = collector_data.cell(2+i, 2+j).value

        # print(Solution.gar_collector_matrix)

        for i in range(Solution.collector_num):
            Solution.power_capacity_collector_matrix[i] = collector_data.cell(4, i+2).value

        # print(Solution.power_capacity_collector_matrix)

        Solution.g_speed = 3.47
        Solution.v_speed = 1

        print("读取时间窗信息")
        time_data = data.sheet_by_index(3)
        for i in range(Solution.depot_num + Solution.client_num):
            for j in range(2):
                Solution.time_windows[i][j] = time_data.cell(2+i, j+1).value
        # print(Solution.time_windows)

        print("计算每个客户点最近的充电站")
        for i in range(Solution.client_num):
            tmp_closest_charge_id = 1
            for j in range(1, Solution.charger_num+1):
                if Solution.dis_matrix[i+Solution.charger_num][j] < Solution.dis_matrix[i+Solution.charger_num][tmp_closest_charge_id]:
                    tmp_closest_charge_id = j
            Solution.client_closest_charger.append(tmp_closest_charge_id)




class Ant():

    def __init__(self, s):
        self.s = s

        # 信心素浓度
        self.pheromone_matrix = np.zeros(shape=(self.s.node_num, self.s.node_num))

        # 已经服务过的客户点列表
        self.served_client_list = []

        # 未服务的客户点列表
        self.un_served_client_list = [i for i in range(Solution.client_num)]

        # 第一次位置, 0表示车场，1-client_num表示客户点，后面表示充电站
        self.cur_postion = 0

        # 该蚂蚁行走路线
        self.routes = [[]]

        # 该蚂蚁行走的tour装载情况
        self.routes_collect = [[]]

        # 当前时间, 默认当前时刻为 0
        self.cur_time = 0

        # 表示车型是否用过
        self.collected_used = [False for i in range(Solution.collector_num)]

    def run(self):
        car_index = 0
        collector0 = Collector(self, car_index)
        collector0.serve()
        self.routes.append(collector0.route)
        self.cur_time = collector0.cur_time
        self.un_served_client_list = copy.deepcopy(collector0.un_served_client_list)


class Collector:

    def __init__(self, ant, car_index):

        self.ant = ant
        # 信心素浓度
        self.pheromone_matrix = copy.deepcopy(np.zeros(shape=(self.ant.s.node_num, self.ant.s.node_num)))

        # 该车辆行走路线
        self.route = []
        self.route.append(0)

        # 当前最大电量
        self.battery = Solution.power_capacity_collector_matrix[car_index]

        # 当前最大容量
        self.gar_max_list = Solution.gar_collector_matrix[car_index]

        # 未服务的客户点列表
        self.un_served_client_list = self.ant.un_served_client_list

        # 已经服务的客户点列表
        self.served_client_list = []

        # 当前位置，第一次位置为 0
        self.cur_position = 0

        # 当前电量
        self.cur_power = self.battery

        # 当前剩余容量
        self.gar_list = np.zeros(self.ant.s.garbage_num)

        # 当前时间
        self.cur_time = ant.cur_time

        # 最大电量
        self.max_power = self.battery

        # 当前总重量
        self.cur_weight = 0


    # 容量判断
    def cal_tabu_by_capacity(self):
        tabu = []
        for client_id in self.un_served_client_list:
            can = True
            for i in range(Solution.garbage_num):
                if self.gar_list[i] < Solution.gar_client_matrix[client_id][i]:
                    can = False
                    break
            if can:
                tabu.append(client_id)
        return tabu

    # 时间窗判断
    # 从当前点去客户点，并且能从客户点回到车场
    def cal_tabu_by_time_to_client_and_back_to_depot(self):
        tabu = []
        if self.cur_position == 0:

            # 在车场

            for client_id in self.un_served_client_list:
                client_position_id = client_id + Solution.depot_num + Solution.charger_num
                dis1 = Solution.dis_matrix[0][client_position_id]
                # 到达下一个客户点时间
                time1 = self.cur_time + dis1 / Solution.v_speed

                if time1 <= Solution.time_windows[client_id+1][1]:
                    # 装货时间
                    load_time = 0
                    # 从下一个客户点出发时间
                    time2 = max(time1, Solution.time_windows[client_id+1][0]) + load_time

                    dis2 = Solution.dis_matrix[client_position_id][0]
                    time_back_take = dis2 / Solution.v_speed

                    # 回到车场时间
                    time3 = time2 + time_back_take

                    if time3 <= Solution.time_windows[0][1]:
                        tabu.append(client_id)

        elif self.cur_position > Solution.charger_num:

            # 在客户点

            for client_id in self.un_served_client_list:
                client_position_id = client_id + Solution.depot_num + Solution.charger_num
                dis1 = Solution.dis_matrix[self.cur_position][client_position_id]
                # 到达下一个客户点时间
                time1 = self.cur_time + dis1 / Solution.v_speed
                if time1 <= Solution.time_windows[client_id+1][1]:
                    #装货时间
                    load_time = 0
                    # 从下一个客户点出发时间
                    time2 = max(time1, Solution.time_windows[client_id+1][0]) + load_time

                    dis2 = Solution.dis_matrix[client_position_id][0]
                    time_back_take = dis2 / Solution.v_speed

                    # 回到车场时间
                    time3 = time2 + time_back_take

                    if time3 <= Solution.time_windows[0][1]:
                        tabu.append(client_id)
        else:

            # 在充电站

            for client_id in self.un_served_client_list:
                client_position_id = client_id + Solution.depot_num + Solution.charger_num
                dis1 = Solution.dis_matrix[self.cur_position][client_position_id]
                # 到达下一个客户点时间
                time1 = self.cur_time + dis1 / Solution.v_speed
                if time1 <= Solution.time_windows[client_id+1][1]:
                    # 装货时间
                    load_time = 0
                    # 从下一个客户点出发时间
                    time2 = max(time1, Solution.time_windows[client_id+1][0]) + load_time

                    dis2 = Solution.dis_matrix[client_position_id][0]
                    time_back_take = dis2 / Solution.v_speed

                    # 回到车场时间
                    time3 = time2 + time_back_take

                    if time3 <= Solution.time_windows[0][1]:
                        tabu.append(client_id)
        return tabu

    # 时间窗判断
    # 从当前点去客户点，然后去最近的充电站，最后从充电站回到车场
    def cal_tabu_by_time_to_client_and_to_charger_and_back_to_depot(self):

        tabu = []
        for client_id in self.un_served_client_list:
            client_position_id = client_id + Solution.depot_num + Solution.charger_num
            dis1 = Solution.dis_matrix[self.cur_position][client_position_id]
            # 到达下一个客户点时间
            time1 = self.cur_time + dis1 / Solution.v_speed
            if time1 <= Solution.time_windows[client_id+1][1]:
                # 装货时间
                load_time = 0
                # 从下一个客户点出发时间
                time2 = max(time1, Solution.time_windows[client_id+1][0]) + load_time

                # 最近的充电站
                closest_charger_position_id = Solution.client_closest_charger[client_id]

                # 到达最近的充电站时间为
                dis2 = Solution.dis_matrix[client_position_id][closest_charger_position_id]
                time3 = time2 + dis2 / Solution.v_speed

                # 充电时间，充电至80%
                charge_power = self.cur_power - self.max_power * 0.8
                charge_time = 0
                if charge_power > 0:
                    charge_time = charge_power / Solution.g_speed

                # 从充电站出发时间
                time4 = time3 + charge_time

                # 回到车场时间
                dis3 = Solution.dis_matrix[closest_charger_position_id][0]
                time5 = time4 + dis3 / Solution.v_speed

                if time5 < Solution.time_windows[0][1]:
                    tabu.append(client_id)
        return tabu


    # 电量判断
    # 从当前点去客户点，并且能够回到车场
    def cal_tabu_by_power_to_client_and_back_depot(self):
        tabu = []

        for client_id in self.un_served_client_list:
            client_position_id = client_id + Solution.depot_num + Solution.charger_num

            dis = Solution.dis_matrix[self.cur_position][client_position_id] + Solution.dis_matrix[client_position_id][0]

            power = self.cal_power_take(dis)

            if (power <= self.cur_power):
                tabu.append(client_id)

        return tabu

    # 电量判断
    # 从当前点去客户点，然后去最近的充电桩，并且保证能回到车场
    def cal_tabu_by_power_to_client_and_to_charger(self):
        tabu = []

        for client_id in self.un_served_client_list:
            client_position_id = client_id + Solution.depot_num + Solution.charger_num

            # 最近的充电站
            closest_charger_position_id = Solution.client_closest_charger[client_id]

            dis = Solution.dis_matrix[self.cur_position][client_position_id] + Solution.dis_matrix[client_position_id][
                closest_charger_position_id]

            power = self.cal_power_take(dis)

            if (power <= self.cur_power):
                tabu.append(client_id)

        return tabu


    # 返回值，下一个要去的点，返回-1表示不可行（只会在车场出现-1）
    def get_next_position(self):

        if self.cur_position == 0:
            # 电量和容量都不需要判断，只需要判断时间窗
            tabu = self.cal_tabu_by_time_to_client_and_back_to_depot()

            if len(tabu) > 0:
                return self.get_next_client_id_by_tabu(tabu)
            tabu = self.cal_tabu_by_power_to_client_and_to_charger()
            if len(tabu) > 0:

                return self.get_next_client_id_by_tabu(tabu)
            return -1
        elif self.cur_position > Solution.charger_num:
            # 在客户点
            # 容量判断
            tabu1 = self.cal_tabu_by_capacity()
            if len(tabu1) > 0:

                tabu2_1 = self.cal_tabu_by_time_to_client_and_back_to_depot()
                tabu2_2 = self.cal_tabu_by_power_to_client_and_back_depot()

                tabu2 = [val for val in tabu2_1 if val in tabu2_2]

                if len(tabu2) > 0:
                    # 先去客户点，然后回车场
                    return self.get_next_client_id_by_tabu(tabu2)

                tabu3_1 = self.cal_tabu_by_time_to_client_and_to_charger_and_back_to_depot()
                tabu3_2 = self.cal_tabu_by_power_to_client_and_to_charger()

                tabu3 = [val for val in tabu3_1 if val in tabu3_2]
                if len(tabu3) > 0:
                    # 先去客户点，然后去充电站，然后回车场
                    return self.get_next_client_id_by_tabu(tabu3)
            # 否则去最近的充电站
            client_id = self.cur_position - Solution.charger_num - 1
            return Solution.client_closest_charger[client_id]
        else:
            # 在充电站
            # 容量判断
            tabu1 = self.cal_tabu_by_capacity()
            if len(tabu1) > 0:

                tabu2_1 = self.cal_tabu_by_time_to_client_and_back_to_depot()
                tabu2_2 = self.cal_tabu_by_power_to_client_and_back_depot()

                tabu2 = [val for val in tabu2_1 if val in tabu2_2]

                if len(tabu2) > 0:
                    # 先去客户点，然后回车场
                    return self.get_next_client_id_by_tabu(tabu2)

                tabu3_1 = self.cal_tabu_by_time_to_client_and_to_charger_and_back_to_depot()
                tabu3_2 = self.cal_tabu_by_power_to_client_and_to_charger()

                tabu3 = [val for val in tabu3_1 if val in tabu3_2]
                if len(tabu3) > 0:
                    # 先去客户点，然后去充电站，然后回车场
                    return self.get_next_client_id_by_tabu(tabu3)
            # 否则，返回车场
            return 0

    # 轮盘赌
    # 返回的 position_id

    def get_next_client_id_by_tabu(self, tabu):
        print("备选集：{0}".format(tabu))
        rand = random.randint(0, len(tabu)-1)
        return tabu[rand] + Solution.charger_num + Solution.depot_num

    def cal_power_take(self, dis):

        a = 1
        b = 0

        return a * self.cur_weight * dis + b


    def serve(self):

        next_position = self.get_next_position()
        while next_position != -1:

            print()
            print("地图地点：{0}".format(next_position))

            self.update(next_position)
            next_position = self.get_next_position()

        print("route路线 = {0}".format(self.route))
        print("未服务客户点 = {0}".format(self.un_served_client_list))
        print("已经服务客户点 = {0}".format(self.served_client_list))




    def update(self, next_position):

        dis = Solution.dis_matrix[self.cur_position][next_position]
        time_take = dis / Solution.v_speed
        # 到达时间
        arrival_time = self.cur_time + time_take
        self.cur_time = arrival_time
        took_power = self.cal_power_take(dis)
        self.cur_power -= took_power
        self.route.append(next_position)
        self.cur_position = next_position

        if next_position == 0:
            # 回到车场
            # 当前车辆结束
            print("车场")
            print("结束本次tour")
            return -1
        elif next_position > Solution.charger_num:
            # 去客户点
            print("客户点")
            next_client_id = next_position - 4
            print("服务客户点：{0}".format(next_client_id))
            for i in range(Solution.garbage_num):
                self.gar_list[i] += Solution.gar_client_matrix[next_client_id][i]
                self.cur_weight += Solution.gar_client_matrix[next_client_id][i]
            start_time = Solution.time_windows[next_client_id + 1][0]
            wait_time = 0
            if start_time > self.cur_time:
                wait_time = start_time - self.cur_time
            print("本次等待时间为：{0}".format(wait_time))
            load_time = 0
            print("本次装货时间为：{0}".format(load_time))
            self.cur_time += wait_time + load_time
            self.un_served_client_list.remove(next_client_id)
            self.served_client_list.append(next_client_id)

        else:
            # 去充电站
            # 充电到 80%
            print("充电站")
            charge_power = self.max_power * 0.8 - self.cur_power
            charge_time = charge_power / Solution.g_speed

            self.cur_power = self.max_power * 0.8
            self.cur_time += charge_time






if __name__ == "__main__":
    s = Solution()
    ant0 = Ant(s)
    ant0.run()


