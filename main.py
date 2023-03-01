import os
import sys
import time
from datetime import datetime

import mylib


def check_env():
    # check the env path of SUMO_HOME
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        print("SUMO_HOME is all right! The env path is " + tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")


if __name__ == "__main__":

    check_env()

    # You should design and call simulation functions between the following comment lines
    # Notice: you should choose the appropriate sumoCmd or you can definte it
    # by yourself
    sumo_cmd = ["sumo", "-c", " sumo/map.sumocfg"]
    sumo_cmd_gui = ["sumo-gui", "-c", "sumo/map.sumocfg"]

    start_time = time.time()
    print("{:=^50s}".format("Start!"))
    # =====================Start !======================

    # mylib.basic_simulation(sumo_cmd)
    mylib.trajectory_to_xlsx(sumo_cmd)
    # mylib.get_next_junction(sumo_cmd)

    # ======================End ! ======================
    print("{:=^50s}".format("End!"))
    end_time = time.time()
    run_time = round(end_time - start_time, 2)
    print("Run time is: " + str(run_time) + "s")
