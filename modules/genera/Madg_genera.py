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
        # noinspection PyBroadException
        try:

            #  create temp MG5_aMC
            file_set(Dir_temp_Madg, info=info, local=True)

            NumberOfProcess = str(random.randint(0, 10000))  # NAME OF PROCESS
            ite = 100
            while file_exists(Dir_temp_Madg + "/Process_" + NumberOfProcess, info=info) and ite > 100:
                NumberOfProcess = str(random.randint(0, 10000))  # NAME OF PROCESS
                ite -= 1

            file_set(Dir_temp_Madg + "/Process_" + NumberOfProcess, info=info, local=True)  # create file
            # file_set(Dir_temp_Madg + "/Process_" + NumberOfProcess + "/MG5_aMC", info=info)  # create file not necesary

            # Directory of Madgraph
            Folder_DirMadgraph = Dir_temp_Madg + "/Process_" + NumberOfProcess
            DirMadgraph = Folder_DirMadgraph + "/MG5_aMC"

            execute("tar -zxvf " + Dir_Madg + "/MG5_aMC.tar.gz -C " + Folder_DirMadgraph + " >/dev/null 2>&1",
                    info=info,
                    position=None,
                    local=True)  # descomprime
            file_exists(DirMadgraph, mode="empty", info=info, local=True)

            #file_set(DirMadgraph, info=info, local=True)
            #file_copy(Dir_Madg, DirMadgraph, "tt", info=info, local=True)  # shutil.copytree(Dir_Madg, DirMadgraph)
        except:
            printG(" :: ERROR :: Execute Mode out :: EXIT PROGRAM ", info=info)
            return None
    elif Mode == "in":
        DirMadgraph = Dir_Madg
        Folder_DirMadgraph = None
    else:
        printG(" :: ERROR :: Execute incorrect mode :: EXIT PROGRAM ", info=info)
        return None

    # *** | INCLUDE BASH | *** #
    Mad_bashrc(DirMadgraph, info=info, local=True)
    printG(" :: Complete copy of Madgraph programs ::", info=info)

    return DirMadgraph, Folder_DirMadgraph
