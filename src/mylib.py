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

from src.utils.utils import get_datetime, flatten_list

Not_found = "NOT_FOUND"


def basic_simulation(sumo_cmd):
    """
    This function is used to simulate traffic in SUMO using the given SUMO command string.

    Args:
    sumo_cmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    Returns:

    """
    step = 0
    f_log_vehicle = open('log/log_vehicle.txt', 'w')
    print(datetime.now(), file=f_log_vehicle)

    traci.start(sumo_cmd)
    print("Execute: basic_simulation()")
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0:
        step = step + 1
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

    print(datetime.now(), file=f_log_vehicle)
    f_log_vehicle.close()
    traci.close()
    print("basic_simulation() is completed !")


def trajectory_to_csv(sumo_cmd):
    """
    This function is used to collect the tracks in the simulation process and output them as xlsx files

    Args:
    sumo_cmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    Returns:

    """
    step = 0
    pack_big_data = []

    traci.start(sumo_cmd)
    print("Execute: trajectory_to_csv()")
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0 & step < 400:
        step = step + 1
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

    Returns:

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
        step = step + 1
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

    Returns:

    """
    step = 0
    f_log__modify_traffic = open('log/log_modify_traffic.txt', 'w')
    print(datetime.now(), file=f_log__modify_traffic)

    traci.start(sumo_cmd)
    print("Execute: modify_traffic_control()")
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0:
        step = step + 1
        if step > 400:
            break

        traci.simulationStep()
        print(
            "====================the {0} st step====================".format(
                step),
            file=f_log__modify_traffic)

        vehicle_id_list = traci.vehicle.getIDList()
        print(
            "Existing vehicle id: ",
            vehicle_id_list,
            file=f_log__modify_traffic)

    print(datetime.now(), file=f_log__modify_traffic)
    f_log__modify_traffic.close()

    traci.close()
    print("modify_traffic_control is completed !")
