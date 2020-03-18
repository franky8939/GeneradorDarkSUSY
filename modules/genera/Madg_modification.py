from modules.genera.card_modification import *
from modules.all.messange_info import *
import time

def Madg_modification(Event,  # number of event simulate
                      Ma_DNeu,  # value of mass of dark neutalino
                      Ma_LNeu,  # value of mass of lightest neutalino
                      Ma_DPho,  # value of mass of dark photon
                      DirMadgraph,  # directory of Madgraph
                      Dir_Source,  # directory where source stay
                      info=None  # out of info for the process
                      ):
    printG(" :: ********** Modification of Madgraph for using Dark Susy ********** :: ", info=info)

    # *** || Clear MSSMD_UFO || # Go to the folder MG5_aMC_vXXX/models. Copy the UFO model there in to folder MSSMD_UFO:
    file_clear(DirMadgraph + "/models/MSSMD_UFO/", "tree", info=info)  # Borrar el file con contenido

    printG(" *** || Introduce model MSSMD_UFO in Madgraph|| ***", info=info)
    # *** || copy info MSSMD_UFO || *** #
    position = DirMadgraph + "/models/MSSMD_UFO"
    ite = 20
    for j in range(ite):
        time.sleep(random.random())  # desincronizar los procesos
        if not file_exists(position, info=info, local=True):
            printG(" *** || copy info MSSMD_UFO || *** || intent : " + str(j), info=info)
            file_set(DirMadgraph + "/models/MSSMD_UFO", info=info)
            file_copy(Dir_Source + "/MSSMD_UFO", DirMadgraph + "/models/MSSMD_UFO", "tt", info=info)  # Copy the info
        else:
            if not file_exists(DirMadgraph + "/models/MSSMD_UFO/param_card.dat"):
                execute("python write_param_card.py", info=info, position=position)
            else:
                break

    printG(" *** || Change the mass || *** ", info=info)
    # *** || Change the mass of dark photon || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_DPho", Ma_DPho, info=info)
    # *** || Change the mass of lightest neutalino || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_LNeu", Ma_LNeu, info=info)
    # *** || Change the mass of dark neutalino || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_DNeu", Ma_DNeu, info=info)

    printG(" *** || COPY proc_card.dat || *** ", info=info)
    # *** || COPY proc_card.dat || *** # Remove the default proc_card.dat in the MG5_aMC_vXXX directory
    file_clear(DirMadgraph + "/proc_card.dat", "file", info=info)
    file_clear(DirMadgraph + "/MSSMD", "Tree", info=info)

    for j in range(ite):
        time.sleep(random.random())  # desincronizar los procesos
        if not file_exists(DirMadgraph + "/MSSMD", mode="not_empty", info=info, local=True):
            printG(" *** ||  Copy proc_card.dat || *** || intent : " + str(j), info=info)
            file_copy(Dir_Source + "/proc_card.dat", DirMadgraph, "ft", info=info)  # Copy proc_card.dat
            execute("./bin/mg5_aMC proc_card.dat", info=info, position=DirMadgraph)
        else:
            break
    if not file_exists(DirMadgraph + "/MSSMD", mode="not_empty", info=info, local=True):
        printG(" :: Stop simulation for problems in the execution of proc_card")
        raise

    printG(" *** || Copy madspin and Run_card || ***", info=info)
    # *** || Copy madspin || *** # Copy the madspin card to the Cards directory /MadGraph5/MG5_aMC_vXXX/MSSMD/Cards
    file_copy(Dir_Source + "/madspin_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info=info, local=True)
    # file_exists(DirMadgraph + "/MSSMD/Cards/madspin_card.dat", info=info, local=True)
    # *** || Change Run_card || *** # Copiar el file Run_card en el lugar correspondiente
    file_copy(Dir_Source + "/run_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info=info, local=True)
    # file_exists(DirMadgraph + "/MSSMD/Cards/run_card.dat", info=info, local=True)
    # realize the change correspondence in the file run_card.dat
    change(DirMadgraph + "/MSSMD/Cards/run_card.dat", "Events", Event, info=info)

    printG(" :: ********** Finally modification of Madgraph for using Dark Susy ********** :: ", info=info)
