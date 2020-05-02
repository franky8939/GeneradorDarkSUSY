# from modules.messange_info import *
# from modules.modification_files import *
from modules.genera.bashrc_modification import *
from modules.genera.card_modification import *
import time

def Madg_create(Dir_Madg,  # directory of install Madgraph
                Dir_temp_Madg,  # directory of temporal install Madgraph
                Mode,  # condicion using - in - or - out -
                info=None  # out of info for the process
                ):
    printG(" :: ********** CREATE FOLDER OF MADGRAPH FOR USING DARKSUSY ********** :: ", info=info)
    # ********** | MODE USING FOR SIMULATION | ********** #
    if Mode == "out":
        #  CREATE TEMP OF MG5_aMC  #
        file_set(Dir_temp_Madg, info=info, local=True)  # NOT PROBLEMS IF EXIST
        NumberOfProcess = str(random.randint(0, 1e5))  # NAME OF PROCESS
        while file_exists(Dir_temp_Madg + "/Process_" + NumberOfProcess, info=info):
            NumberOfProcess = str(random.randint(0, 1e5))  # NAME OF PROCESS
        file_set(Dir_temp_Madg + "/Process_" + NumberOfProcess, info=info, local=True)  # create file

        # DIRECTORY OF MADGRAPH
        Folder_DirMadgraph = Dir_temp_Madg + "/Process_" + NumberOfProcess
        DirMadgraph = Folder_DirMadgraph + "/MG5_aMC"

        # DECLARACION PARA QUE SOLO SE ACCEDA AL COMPRIMIDO UNA A LA VEZ
        printG(" :: TRY TO COPY MADGRAPH :: ", info=info)
        while file_exists(Dir_Madg + "/COPY_MG5_aMC.txt", local=True):
            time.sleep(random.random())  # wait
        mg5 = open(Dir_Madg + "/COPY_MG5_aMC.txt", "w+")
        mg5.close()  # DECLARACION DE COPIA
        execute("tar -zxvf " + Dir_Madg + "/MG5_aMC.tar.gz -C " + Folder_DirMadgraph + " >/dev/null 2>&1",
                info=info, position=None, local=True)  # DECOMPILE
        file_clear(Dir_Madg + "/COPY_MG5_aMC.txt", "File", local=True)

    elif Mode == "in":
        DirMadgraph = Dir_Madg
        Folder_DirMadgraph = None
    else:
        printG(" :: ERROR :: EXECUTE INCORRECT MODE :: EXIT PROGRAM ", info=info)
        return None, None

    # *** | INCLUDE BASH | *** #
    Mad_bashrc(DirMadgraph, info=info, local=True)
    printG(" :: COMPLETE COPY OF MADGRAPH PROGRAMS ::", info=info)

    printG(" :: ********** FINALLY CREATION OF FOLDER OF MADGRAPH FOR USING DARKSUSY ********** :: ", info=info)

    return DirMadgraph, Folder_DirMadgraph
