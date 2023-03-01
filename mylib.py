import os
import sys
import time
import pytz
import pandas as pd
from datetime import datetime
import traci
import sumolib

Running_sign = "Running....Wait for end..."


def _getdatetime():
    utc_now = pytz.utc.localize(datetime.now())
    current_dt = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
    DATIME = current_dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return DATIME


def _flatten_list(_2d_list):
    flat_list = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


def basic_simulation(sumo_cmd):
    '''
    This function is used to simulate traffic in SUMO using the given SUMO command string.

    Args:
    sumoCmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    '''
    step = 0
    f_log_vehicle = open('log/log_vehicle.txt', 'w')
    print(datetime.now(), file=f_log_vehicle)

    traci.start(sumo_cmd)
    print("Execute: basic_simulation()")
    print(Running_sign)
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0:
        step = step + 1
        if step > 400:
            break
        traci.simulationStep()
        print(
            "{:=^50s}".format(
                "the " +
                str(step) +
                " st"),
            file=f_log_vehicle)

        vehicle_id_list = traci.vehicle.getIDList()
        # Write vehicle number information and id information into the log_ In
        # vehicle.txt

        print("vehicle_number: " + str(len(vehicle_id_list)), file=f_log_vehicle)
        print("vehicle_id_list: " + str(vehicle_id_list), file=f_log_vehicle)

        # if step==5:
        #     break

    print(datetime.now(), file=f_log_vehicle)
    f_log_vehicle.close()
    traci.close()


def trajectory_to_xlsx(sumo_cmd):
    '''
    This function is used to collect the tracks in the simulation process and output them as xlsx files

    Args:
    sumoCmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    '''
    step = 0
    pack_big_data = []

    traci.start(sumo_cmd)
    print("Execute: trajectory_to_xlsx()")
    print(Running_sign)

    while traci.simulation.getMinExpectedNumber() > 0 & step < 400:
        step = step + 1
        if step > 400:
            break
        traci.simulationStep()

        vehicle_id_list = traci.vehicle.getIDList()  # get all vehicle_id_list

        for i in range(0, len(vehicle_id_list)):

            vehid = vehicle_id_list[i]  # vehicle id
            x, y = traci.vehicle.getPosition(
                vehicle_id_list[i])  # GPS position
            coord = [x, y]
            lon, lat = traci.simulation.convertGeo(x, y)  # (lon,lat)
            gpscoord = [lon, lat]
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
                _getdatetime(),
                vehid,
                coord,
                gpscoord,
                speed,
                edge,
                lane,
                displacement,
                turn_angle,
                next_tls]
            pack_big_data_line = _flatten_list([vehicle_list])
            pack_big_data.append(pack_big_data_line)

    traci.close()

    # Generate Excel file
    columnnames = [
        'dateandtime',
        'vehid',
        'coord',
        'gpscoord',
        'spd',
        'edge',
        'lane',
        'displacement',
        'turn_angle',
        'next_tls']
    dataset = pd.DataFrame(pack_big_data, index=None, columns=columnnames)
    # write to excel for following processing
    dataset.to_excel("output/output.xlsx", index=False)


def get_next_junction(sumo_cmd):
    '''
    This function is used to simulate traffic in SUMO using the given SUMO command string.

    Args:
    sumoCmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    '''
    net = sumolib.net.readNet('sumo/map.net.xml')
    step = 0

    traci.start(sumo_cmd)
    print("Execute: getNextJunction()")
    print(Running_sign)
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0:
        step = step + 1
        if step > 400:
            break
        traci.simulationStep()

        id_list = traci.vehicle.getIDList()

        print("{:=^50s}".format("the " + str(step) + " st"))
        print("vehicle_ID: ", id_list[0])
        print("Position: " + str(traci.vehicle.getPosition(id_list[0])))
        print("LanePosition: " +
              str(traci.vehicle.getLanePosition(id_list[0])))

        lane_id = traci.vehicle.getLaneID(id_list[0])
        edge_id = traci.vehicle.getRoadID(id_list[0])
        print("edge_id: " + edge_id)
        print("lane_id: " + lane_id)

        next_node_id = net.getEdge(edge_id).getToNode().getID()
        from_node_id = net.getEdge(edge_id).getFromNode().getID()
        print(next_node_id)
        print(from_node_id)

        # if step==5:
        #     break
    traci.close()
