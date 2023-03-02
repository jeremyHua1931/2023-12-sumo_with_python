# -*- encoding: utf-8 -*-
"""
@File    :   test.py   
@Contact :   jeremyhua@foxmail.com
 
@Modify Time      @Author       @Version     @Description
------------      -------       --------     -----------
2023/3/2 10:17   HuaZhangzhao    1.0         test demo for new feature
"""
from datetime import datetime

import traci
import sumolib


def test_new_feature(sumo_cmd):
    """
    This function is used to test new test_new_feature

    Args:
        sumo_cmd: A string that contains the SUMO command with all the necessary parameters for the simulation.

    Returns:

    """
    step = 0
    traci.start(sumo_cmd)
    print("Execute: modify_traffic_control()")
    if sumo_cmd[0] == 'sumo-gui':
        traci.gui.setSchema("View #0", "real world")

    while traci.simulation.getMinExpectedNumber() > 0:
        step = step + 1
        if step > 400:
            break
        if step < 20:
            continue


if __name__ == '__main__':
    sumo_cmd = ["sumo", "-c", " sumo/map.sumocfg"]
    # test_new_feature(sumo_cmd)
