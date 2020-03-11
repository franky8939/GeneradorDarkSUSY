from modules.genera.modification_card import *


def Madg_modification(Event,  # number of event simulate
                      Ma_DNeu,  # value of mass of dark neutalino
                      Ma_LNeu,  # value of mass of lightest neutalino
                      Ma_DPho,  # value of mass of dark photon
                      DirMadgraph,  # directory of Madgraph
                      Dir_Source,  # directory where source stay
                      info="off"  # output of info for the process
                      ):

    # *** || Clear MSSMD_UFO || # Go to the folder MG5_aMC_vXXX/models. Copy the UFO model there in to folder MSSMD_UFO:
    file_clear(DirMadgraph + "/models/MSSMD_UFO", "tree", info)  # Borrar el archivo con contenido

    # *** || copy info MSSMD_UFO || *** #
    file_copy(Dir_Source + "/MSSMD_UFO", DirMadgraph + "/models/MSSMD_UFO", "tt", info)  # Copy the info

    # *** || Go to the folder MSSMD_UFO and execute *.py || *** # :
    execute("python write_param_card.py", info=info, position=DirMadgraph + "/models/MSSMD_UFO")

    # *** || Change the mass of dark photon || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_DPho", Ma_DPho, info)

    # *** || Change the mass of lightest neutalino || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_LNeu", Ma_LNeu, info)

    # *** || Change the mass of dark neutalino || *** #
    change(DirMadgraph + "/models/MSSMD_UFO/param_card.dat", "Ma_DNeu", Ma_DNeu, info)

    # *** || COPY proc_card.dat || *** # Remove the default proc_card.dat in the MG5_aMC_vXXX directory
    file_clear(DirMadgraph + "/proc_card.dat", "file", info)

    # Copy the following proc_card.dat there:
    file_copy(Dir_Source + "/proc_card.dat", DirMadgraph, "ft", info)

    # *** || Generar MSSMD || *** # Run ./bin/mg5_aMC proc_card.dat and generate the folder called MSSMD.
    execute("./bin/mg5_aMC proc_card.dat", info=info, position=DirMadgraph)

    # *** || Copy madspin || *** # Copy the madspin card to the Cards directory /MadGraph5/MG5_aMC_vXXX/MSSMD/Cards
    file_copy(Dir_Source + "/madspin_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info)

    # *** || Change Run_card || *** # Copiar el archivo Run_card en el lugar correspondiente
    file_copy(Dir_Source + "/madspin_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info)

    # *** || Change Run_card || *** # Copiar el archivo Run_card en el lugar correspondiente
    file_copy(Dir_Source + "/run_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info)
    # realize the change correspondence in the file run_card.dat
    change(DirMadgraph + "/MSSMD/Cards/run_card.dat", "Events", Event, info)

