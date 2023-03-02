# -*- encoding: utf-8 -*-
"""
@File    :   test.py
@Contact :   jeremyhua@foxmail.com

@Modify Time      @Author       @Version     @Description
------------      -------       --------     -----------
2023/3/2 10:17   HuaZhangzhao    1.0         test demo for new feature
"""
import traci
import sumolib


def test_new_feature():
    """
    This function is used to test new test_new_feature

    Returns: None

    """
    cmd = ["sumo", "-c", "/Users/jemeryhua/Desktop/EastLake/sumo/map.sumocfg"]
    step = 0
    traci.start(cmd)
    print("Execute: modify_traffic_control()")
    if cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0:
        step += 1
        if step > 100:
            break
        traci.simulationStep()

        print("====================the {0} st step====================".format(step))
        vehicle_id = traci.vehicle.getIDList()
        print(vehicle_id)

        for vehicle in vehicle_id:
            if vehicle == "-1":
                print("New vehicle has been added to the map")
                print("vehicle: -1", traci.vehicle.getRoadID("-1"), traci.vehicle.getLaneID("-1"))

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

        if step == 10:
            traci.vehicle.add("-1", "", 'DEFAULT_VEHTYPE', 'now', 'first', 'base', '0', 'current', 'max', 'current')


if __name__ == '__main__':
    test_new_feature()
