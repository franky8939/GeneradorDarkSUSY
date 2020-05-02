from modules.genera.card_modification import *
from modules.all.messange_info import *
import time
import sys

def Madg_modification(Event,  # number of event simulate
                      Ma_DNeu,  # value of mass of dark neutalino
                      Ma_LNeu,  # value of mass of lightest neutalino
                      Ma_DPho,  # value of mass of dark photon
                      DirMadgraph,  # directory of Madgraph
                      Dir_Source,  # directory where source stay
                      info=None  # out of info for the process
                      ):
    printG(" :: ********** MODIFICATION OF MADGRAPH FOR USING DARKSUSY ********** :: ", info=info)

    # *** || Clear MSSMD_UFO || # Go to the folder MG5_aMC_vXXX/models. Copy the UFO model there in to folder MSSMD_UFO:
    file_clear(DirMadgraph + "/models/MSSMD_UFO/", "tree", info=info)  # Borrar el file con contenido

    printG(" ****** || INCLUDE MODEL MSSMD_UFO IN MADGRAPH || ****** ", info=info)
    # *** || copy info MSSMD_UFO || *** #
    position = DirMadgraph + "/models/MSSMD_UFO"
    printG(" :: TRY TO COPY MSSMD_UFO :: ", info=info)
    while file_exists(Dir_Source + "/COPY_MSSMD_UFO.txt", local=True):
        time.sleep(random.random())  # wait
    mssm = open(Dir_Source + "/COPY_MSSMD_UFO.txt", "w+")
    mssm.close()  # DECLARATION DE COPIA
    file_set(DirMadgraph + "/models/MSSMD_UFO", info=info)
    file_copy(Dir_Source + "/MSSMD_UFO", DirMadgraph + "/models/MSSMD_UFO", "tt", info=info)  # Copy the info
    file_clear(Dir_Source + "/COPY_MSSMD_UFO.txt", "File", local=True)

    printG(" :: EXECUTE :: python write_param_card.py :: ", info=info)
    execute("python write_param_card.py", info=info, position=position)

    printG(" ****** || Change the mass || ****** ", info=info)
    # *** || Change the mass of dark photon || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_DPho", Ma_DPho, info=info)
    # *** || Change the mass of lightest neutalino || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_LNeu", Ma_LNeu, info=info)
    # *** || Change the mass of dark neutalino || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_DNeu", Ma_DNeu, info=info)

    printG(" ****** || COPY proc_card.dat || ****** ", info=info)
    # *** || COPY proc_card.dat || *** # Remove the default proc_card.dat in the MG5_aMC_vXXX directory
    file_clear(DirMadgraph + "/proc_card.dat", "file", info=info)  # PREPARATION
    file_clear(DirMadgraph + "/MSSMD", "Tree", info=info)  # PREPARATION

    while file_exists(Dir_Source + "/COPY_proc_card.txt", local=True):
        time.sleep(random.random())  # wait
    proc = open(Dir_Source + "/COPY_proc_card.txt", "w+")
    proc.close()  # DECLARATION DE COPY
    file_copy(Dir_Source + "/proc_card.dat", DirMadgraph, "ft", info=info)  # Copy proc_card.dat
    execute("./bin/mg5_aMC proc_card.dat", info=info, position=DirMadgraph)
    file_clear(Dir_Source + "/COPY_proc_card.txt", "File", local=True)

    printG(" *** || Copy madspin and Run_card || ***", info=info)
    # *** || Copy madspin || *** # Copy the madspin card to the Cards directory /MadGraph5/MG5_aMC_vXXX/MSSMD/Cards

    while file_exists(Dir_Source + "/COPY_madspin_card.txt", local=True):
        time.sleep(random.random())  # wait
    mads = open(Dir_Source + "/COPY_madspin_card.txt", "w+")  # DECLARATION DE COPIA
    mads.close()  # DECLARATION DE COPY
    file_copy(Dir_Source + "/madspin_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info=info, local=True)
    file_clear(Dir_Source + "/COPY_madspin_card.txt", "File", local=True)

    # ****** || Change Run_card || ****** # Copiar el file Run_card en el lugar correspondiente
    while file_exists(Dir_Source + "/COPY_run_card.dat", local=True):
        time.sleep(random.random())  # wait
    run = open(Dir_Source + "/COPY_run_card.dat", "w+")  # DECLARATION DE COPY
    run.close()  # DECLARATION DE COPY
    file_copy(Dir_Source + "/run_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info=info, local=True)
    file_clear(Dir_Source + "/COPY_run_card.dat", "File", local=True)

    # realize the change correspondence in the file run_card.dat
    change(DirMadgraph + "/MSSMD/Cards/run_card.dat", "Events", Event, info=info)

    printG(" :: ********** FINALLY MODIFICATION OF MADGRAPH FOR USING DARK SUSY ********** :: ", info=info)
