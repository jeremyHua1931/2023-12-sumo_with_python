# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Contact :   jeremyhua@foxmail.com

@Modify Time      @Author       @Version     @Description
------------      -------       --------     -----------
2023/3/1 22:00   HuaZhangzhao    1.0          main() function
"""
import os
import sys
import time

from src import mylib


def check_env():
    """check the env path of SUMO_HOME

    Returns:

    """

    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        print("SUMO_HOME is all right! The env path is " + tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")


if __name__ == "__main__":

    check_env()

    # You should design and call simulation functions between the following comment lines
    # Notice: you should choose the appropriate sumoCmd, or you can define it
    # by yourself
    sumo_cmd = ["sumo", "-c", " sumo/map.sumocfg"]
    sumo_cmd_gui = ["sumo-gui", "-c", "sumo/map.sumocfg"]

    start_time = time.time()
    print("======================Start!======================")

    # =====================Start !======================

    # mylib.basic_simulation(sumo_cmd)
    # mylib.trajectory_to_xlsx(sumo_cmd)
    mylib.get_next_junction(sumo_cmd)

    # ======================End ! ======================
    print("=======================End!=======================")
    end_time = time.time()
    run_time = round(end_time - start_time, 2)
    print("Running time is: " + str(run_time) + "s")
