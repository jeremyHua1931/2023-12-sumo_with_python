import os
import sys
import time
import pytz
import pandas as pd
from datetime import datetime
import traci
import sumolib


def _getdatetime():
    utc_now = pytz.utc.localize(datetime.now())
    currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
    DATIME = currentDT.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
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





def basic_simulation(sumoCmd):
    '''
    This function is used to simulate traffic in SUMO using the given SUMO command string.

    Args:
    sumoCmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    '''
    net = sumolib.net.readNet('sumo/map.net.xml')
    step = 0
    f_log_vehicle=open('log/log_vehicle.txt','w')
    print(datetime.now(), file=f_log_vehicle)  

    traci.start(sumoCmd)
    print("Execute: basic_simulation()")
    print("Running....Wait for end...")
    if sumoCmd[0]=='sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() >0 :
        traci.simulationStep()
        step=step+1
        print("{:=^50s}".format("the "+str(step)+" st"),file=f_log_vehicle)

        ID_List=traci.vehicle.getIDList()
        # Write vehicle number information and id information into the log_ In vehicle.txt

        print("vehicle_number: "+str(len(ID_List)),file=f_log_vehicle)
        print("ID_List: "+str(ID_List),file=f_log_vehicle)
    
        # if step==5:
        #     break

    print(datetime.now(), file=f_log_vehicle) 
    f_log_vehicle.close()
    traci.close()

def trajectory_to_xlsx(sumoCmd):
    '''
    This function is used to collect the tracks in the simulation process and output them as xlsx files

    Args:
    sumoCmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    '''
    step=0
    packVehicleData = []
    packTLSData = []
    packBigData = []

    traci.start(sumoCmd)
    print("Execute: trajectory_to_xlsx()")
    print("Running....Wait for end...")

    while traci.simulation.getMinExpectedNumber() > 0 & step < 400:
        step=step+1
        traci.simulationStep();

        ID_List = traci.vehicle.getIDList();  # get all ID_List
        trafficlights_ID_List = traci.trafficlight.getIDList();  # get all trafficlights_ID_List

        for i in range(0, len(ID_List)):

            vehid = ID_List[i]  # vehicle id
            x, y = traci.vehicle.getPosition(ID_List[i])  # GPS position
            coord = [x, y]
            lon, lat = traci.simulation.convertGeo(x, y)  # (lon,lat)
            gpscoord = [lon, lat]
            speed = round(traci.vehicle.getSpeed(ID_List[i]) * 3.6, 2)  # speed
            edge = traci.vehicle.getRoadID(ID_List[i])
            lane = traci.vehicle.getLaneID(ID_List[i])
            displacement = round(traci.vehicle.getDistance(ID_List[i]), 2)
            turnAngle = round(traci.vehicle.getAngle(ID_List[i]), 2)
            nextTLS = traci.vehicle.getNextTLS(ID_List[i])

            # Packing of all the data for export to CSV/XLSX
            vehList = [_getdatetime(), vehid, coord, gpscoord, speed, edge, lane, displacement, turnAngle, nextTLS]

            # print("Vehicle: ", ID_List[i], " at datetime: ", _getdatetime())
            # print(ID_List[i], " >>> Position: ", coord, " | GPS Position: ", gpscoord, " |", \
            #   " Speed: ", round(traci.vehicle.getSpeed(ID_List[i]) * 3.6, 2), "km/h |", \
            #   # Returns the id of the edge the named vehicle was at within the last step.
            #   " EdgeID of veh: ", traci.vehicle.getRoadID(ID_List[i]), " |", \
            #   # Returns the id of the lane the named vehicle was at within the last step.
            #   " LaneID of veh: ", traci.vehicle.getLaneID(ID_List[i]), " |", \
            #   # Returns the distance to the starting point like an odometer.
            #   " Distance: ", round(traci.vehicle.getDistance(ID_List[i]), 2), "m |", \
            #   # Returns the angle in degrees of the named vehicle within the last step.
            #   " Vehicle orientation: ", round(traci.vehicle.getAngle(ID_List[i]), 2), "deg |", \
            #   # Return list of upcoming traffic lights [(tlsID, tlsIndex, distance, state), ...]
            #   " Upcoming traffic lights: ", traci.vehicle.getNextTLS(ID_List[i]), \
            #   )
            packBigDataLine = _flatten_list([vehList])
            packBigData.append(packBigDataLine)

    traci.close()

    # Generate Excel file
    columnnames = ['dateandtime', 'vehid', 'coord', 'gpscoord', 'spd', 'edge', 'lane', 'displacement', 'turnAngle','nextTLS']
    dataset = pd.DataFrame(packBigData, index=None, columns=columnnames)
    # write to excel for following processing
    dataset.to_excel("output/output.xlsx", index=False)


def getNextJunction(sumoCmd):
    '''
    This function is used to simulate traffic in SUMO using the given SUMO command string.

    Args:
    sumoCmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    '''
    net = sumolib.net.readNet('sumo/map.net.xml')
    step = 0

    traci.start(sumoCmd)
    print("Execute: getNextJunction()")
    print("Running....Wait for end...")
    if sumoCmd[0]=='sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() >0 :
        traci.simulationStep()
        step=step+1

        ID_List=traci.vehicle.getIDList() 

        print("{:=^50s}".format("the "+str(step)+" st"))
        print("vehicle_ID: ", ID_List[0])
        print("Position: "+str(traci.vehicle.getPosition(ID_List[0])))
        print("LanePosition: "+str(traci.vehicle.getLanePosition(ID_List[0])))

        lane_id = traci.vehicle.getLaneID(ID_List[0])
        edge_id=traci.vehicle.getRoadID(ID_List[0])
        print("edge_id: "+edge_id)
        print("lane_id: "+lane_id)

        nextNodeID = net.getEdge(edge_id).getToNode().getID()

        print(nextNodeID)
        fromNodeID=net.getEdge(edge_id).getFromNode().getID()
        print(fromNodeID)
    
        # if step==5:
        #     break

    print("The result is writed in /output/output.xlsx")
    traci.close()

