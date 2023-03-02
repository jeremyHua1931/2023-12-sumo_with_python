# -*- encoding: utf-8 -*-
"""
@File    :   mylib.py
@Contact :   jeremyhua@foxmail.com

@Modify Time      @Author       @Version     @Description
------------      -------       --------     -----------
2023/3/1 21:59   HuaZhangzhao    1.0          some function examples of sumo simulation
"""
import pandas as pd
from datetime import datetime
import traci
import sumolib
import src.utils.colors as color

from src.utils.utils import get_datetime, flatten_list

Not_found = "NOT_FOUND"


def basic_simulation(sumo_cmd):
    """
    This function is used to simulate traffic in SUMO using the given SUMO command string.

    Args:
    sumo_cmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    Returns: the log_*.txt is in /log folder

    """
    step = 0
    f_log_vehicle = open('log/log_vehicle.txt', 'w')
    print(datetime.now(), file=f_log_vehicle)

    traci.start(sumo_cmd)
    print("Execute: basic_simulation()")
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0:
        step += 1
        if step > 400:
            break

        traci.simulationStep()
        print(
            "====================the {0} st step====================".format(
                step),
            file=f_log_vehicle)

        vehicle_id_list = traci.vehicle.getIDList()
        # Write vehicle number information and id information into the
        # log/log_vehicle.txt
        print("vehicle_number: " + str(len(vehicle_id_list)), file=f_log_vehicle)
        print("vehicle_id_list: " + str(vehicle_id_list), file=f_log_vehicle)
        # print(traci.vehicle.getRoute(vehicle_id_list[0]))

    print(datetime.now(), file=f_log_vehicle)
    f_log_vehicle.close()
    traci.close()
    print("basic_simulation() is completed !")


def trajectory_to_csv(sumo_cmd):
    """
    This function is used to collect the tracks in the simulation process and output them as xlsx files

    Args:
    sumo_cmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    Returns: the *.csv is in /output folder

    """
    step = 0
    pack_big_data = []

    traci.start(sumo_cmd)
    print("Execute: trajectory_to_csv()")
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0 & step < 400:
        step += 1
        if step > 400:
            break

        traci.simulationStep()

        # get all vehicle_id_list
        vehicle_id_list = traci.vehicle.getIDList()

        for i in range(0, len(vehicle_id_list)):
            vehid = vehicle_id_list[i]
            x, y = traci.vehicle.getPosition(
                vehicle_id_list[i])
            coord = [x, y]
            lon, lat = traci.simulation.convertGeo(x, y)  # (lon,lat)
            gps_coord = [lon, lat]
            speed = round(
                traci.vehicle.getSpeed(
                    vehicle_id_list[i]) * 3.6,
                2)  # speed
            edge = traci.vehicle.getRoadID(vehicle_id_list[i])
            lane = traci.vehicle.getLaneID(vehicle_id_list[i])
            displacement = round(
                traci.vehicle.getDistance(
                    vehicle_id_list[i]), 2)
            turn_angle = round(traci.vehicle.getAngle(vehicle_id_list[i]), 2)
            next_tls = traci.vehicle.getNextTLS(vehicle_id_list[i])

            # Packing of all the data for export to CSV/XLSX
            vehicle_list = [
                get_datetime(),
                vehid,
                coord,
                gps_coord,
                speed,
                edge,
                lane,
                displacement,
                turn_angle,
                next_tls]
            pack_big_data_line = flatten_list([vehicle_list])
            pack_big_data.append(pack_big_data_line)

    traci.close()

    # Generate csv file
    column_names = [
        'date_time',
        'vehicle_id',
        'coord',
        'gps_coord',
        'spd',
        'edge',
        'lane',
        'displacement',
        'turn_angle',
        'next_tls']
    dataset = pd.DataFrame(pack_big_data, index=None, columns=column_names)
    dataset = dataset.sort_values(['vehicle_id', 'date_time'], ascending=False)

    # write to csv for following processing
    dataset[:1000].to_csv('output/output_to_1000.csv', index=False)
    dataset.to_csv('output/output.csv', index=False)

    print("trajectory_to_csv() is completed !")


def get_next_junction(sumo_cmd):
    """This function is used to simulate traffic in SUMO using the given SUMO command string.

    Args:
        sumo_cmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    Returns: the *.csv is in /output folder

    """
    step = 0
    f_log_get_next_junction = open('log/log_get_next_junction.txt', 'w')
    print(datetime.now(), Not_found, file=f_log_get_next_junction)

    net = sumolib.net.readNet('sumo/map.net.xml')

    traci.start(sumo_cmd)

    print("Execute: getNextJunction()")
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    junction_info = []

    while traci.simulation.getMinExpectedNumber() > 0:
        step += 1
        if step > 400:
            break

        traci.simulationStep()

        id_list = traci.vehicle.getIDList()

        print("====================the {0} st step====================".format(
            step), file=f_log_get_next_junction)

        for x_id in id_list:
            lane_id = traci.vehicle.getLaneID(x_id)
            edge_id = traci.vehicle.getRoadID(x_id)
            x_position = traci.vehicle.getPosition(x_id)[0]
            y_position = traci.vehicle.getPosition(x_id)[1]
            try:
                next_node_id = net.getEdge(edge_id).getToNode().getID()
                from_node_id = net.getEdge(edge_id).getFromNode().getID()
                info = [
                    get_datetime(),
                    x_id,
                    x_position,
                    y_position,
                    edge_id,
                    lane_id,
                    from_node_id,
                    next_node_id]
            except Exception as e:
                print(get_datetime(), '|', x_id, '|', edge_id, '|', lane_id, '|', Not_found, '|', e,
                      file=f_log_get_next_junction)
                info = [
                    get_datetime(),
                    x_id,
                    x_position,
                    y_position,
                    edge_id,
                    lane_id,
                    Not_found,
                    Not_found]

            info_element = flatten_list([info])
            junction_info.append(info_element)

    traci.close()
    print(datetime.now(), file=f_log_get_next_junction)
    f_log_get_next_junction.close()

    # Generate csv file
    column_names = [
        'date_time',
        'vehicle_id',
        'x_position',
        'y_position',
        'edge_id',
        'land_id',
        'from_node_id',
        'next_node_id']
    dataset = pd.DataFrame(junction_info, index=None, columns=column_names)
    dataset = dataset.sort_values(['vehicle_id', 'date_time'], ascending=False)

    # write to csv for following processing
    dataset[:1000].to_csv('output/vehicle_junction_to_1000.csv', index=False)
    dataset.to_csv('output/vehicle_junction.csv', index=False)

    print("get_next_junction() is completed !")


def modify_traffic_control(sumo_cmd):
    """
    This function  is used to modify traffic condition dynamically, mainly focusing vehicles.

    Args:
        sumo_cmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    Returns: none

    """
    step = 0
    f_log_modify_traffic = open('log/log_modify_traffic.txt', 'w')
    print(datetime.now(), file=f_log_modify_traffic)

    traci.start(sumo_cmd)
    print("Execute: modify_traffic_control()")
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0:
        step += 1
        if step > 400:
            break

        traci.simulationStep()

        vehicle_id_list = traci.vehicle.getIDList()
        vehicle_id_list_int = list(map(int, vehicle_id_list))
        new_vehicle_list = []
        for vehicle in vehicle_id_list_int:
            if vehicle < 0:
                new_vehicle_list.append(vehicle)

        if len(new_vehicle_list) > 0:
            print("====================the {0} st step====================".format(
                step), file=f_log_modify_traffic)
            print(
                "Existing and new vehicle id: ",
                new_vehicle_list,
                file=f_log_modify_traffic)

        # traci.vehicle.add() 向仿真中添加新车辆的函数，具有以下参数：
        # vehID：车辆ID，必须是唯一的字符串。
        # routeID：车辆将要按照的路线ID。
        # typeID：车辆类型ID，默认为DEFAULT_VEHTYPE。
        # depart：车辆出发时间，默认为now。
        # departLane：车辆出发的车道，默认为first。
        # departPos：车辆出发位置，默认为base。
        # departSpeed：车辆出发速度，默认为0。
        # arrivalLane：车辆到达的车道，默认为current。
        # arrivalPos：车辆到达位置，默认为max。
        # arrivalSpeed：车辆到达速度，默认为current。
        # fromTaz：车辆出发区域（TAZ）ID，默认为空字符串。
        # toTaz：车辆到达区域（TAZ）ID，默认为空字符串。
        # line：车辆所在的线路ID，默认为空字符串。
        # personCapacity：车辆的最大载客量，默认为0。
        # personNumber：车辆的当前载客数，默认为0。

        # add(self, vehID, routeID, typeID="DEFAULT_VEHTYPE", depart="now",
        #     departLane="first", departPos="base", departSpeed="0",
        #     arrivalLane="current", arrivalPos="max", arrivalSpeed="current",
        #     fromTaz="", toTaz="", line="", personCapacity=0, personNumber=0):
        # """
        # Add a new vehicle (new style with all possible parameters)
        # If routeID is "", the vehicle will be inserted on a random network edge
        # if route consists of two disconnected edges, the vehicle will be treated
        # like a <trip> and use the fastest route between the two edges.
        # """

        # departLane definition
        # must be one of ("random", "free", "allowed", "best", "first", or an int>=0)
        # departLane
        # 参数用于指定车辆出发时所在的道路上的车道，其取值为以下之一：
        # "random"：随机选择一个可用车道
        # "free"：选择一个可用的自由流车道
        # "allowed"：选择一个可用的允许车辆行驶的车道
        # "best"：选择一个最佳车道
        # "first"：选择编号最小的车道
        # 一个非负整数：选择编号为该整数的车道
        # arrivalLane
        # 参数可以填写以下两种类型的参数：
        # "current"：表示车辆会停在当前所在的车道上。
        # 一个非负整数：表示车辆应该到达的车道编号。
        # 需要注意的是，如果 arrivalLane
        # 参数为一个整数，则必须保证该车道是车辆可达的。
        # TODO: https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-add
        # arrivalLane="-998139957"

        if step % 10 == 0:
            print("====================the {0} st step====================".format(
                step), file=f_log_modify_traffic)
            traci.vehicle.add(vehID=str(-step), routeID="", typeID="DEFAULT_VEHTYPE", depart="now",
                              departLane="best", departPos="base", departSpeed="0",
                              arrivalLane="current", arrivalPos="max", arrivalSpeed="current",
                              fromTaz="", toTaz="", line="", personCapacity=0, personNumber=0)
            traci.vehicle.setColor(str(-step), color.blue)
            # print("last id: ", vehicle_id_list[-1], " : ", traci.vehicle.getRoute(vehicle_id_list[-1]))
            # print("new  id: ", -step, " : ", traci.vehicle.getRoute(str(-step)))
            print("New vehicle id is {}, color is {}, ".format(str(-step), traci.vehicle.getColor(str(-step))),
                  file=f_log_modify_traffic)

    traci.close()
    print(datetime.now(), file=f_log_modify_traffic)
    f_log_modify_traffic.close()
    print("modify_traffic_control is completed !")
