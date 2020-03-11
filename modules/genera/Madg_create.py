# from modules.messange_info import *
# from modules.modification_files import *
from modules.genera.modification_bashrc import *
from modules.genera.modification_card import *


def Madg_create(Dir_Madg,  # directory of install Madgraph
                Dir_temp_Madg,  # directory of temporal install Madgraph
                Mode,  # condicion using - in - or - out -
                info=None  # output of info for the process
                ):
    # *** | MODE USING FOR SIMULATION | *** #
    if Mode == "out":
        try:

            #  create temp MG5_aMC
            file_set(Dir_temp_Madg, info)

            NumberOfProcess = str(random.randint(0, 10000))  # NAME OF PROCESS
            ite = 100
            while file_exists(Dir_temp_Madg + "/Process_" + NumberOfProcess, info) and ite > 100:
                NumberOfProcess = str(random.randint(0, 10000))  # NAME OF PROCESS
                ite -= 1

            file_set(Dir_temp_Madg + "/Process_" + NumberOfProcess, info)  # create file
            file_set(Dir_temp_Madg + "/Process_" + NumberOfProcess + "/MG5_aMC", info)  # create file

            # Directory of Madgraph
            DirMadgraph = Dir_temp_Madg + "/Process_" + NumberOfProcess + "/MG5_aMC"
            file_copy(Dir_Madg, DirMadgraph, "tt", info)  # shutil.copytree(Dir_Madg, DirMadgraph)
        except:
            printG(" :: ERROR :: Execute Mode out :: EXIT PROGRAM ", info)
            return None
    elif Mode == "in":
        DirMadgraph = Dir_Madg
    else:
        printG(" :: ERROR :: Execute incorrect modet :: EXIT PROGRAM ", info)
        return None

    # *** | INCLUDE BASH | *** #
    Mad_bashrc(DirMadgraph)

    return DirMadgraph
