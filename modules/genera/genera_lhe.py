from modules.genera.modification_card import *


def genera_lhe(DirMadgraph,  # directory of temporal install Madgraph
               info=None  # output of info for the process
               ):
    # *** || Deactivate or activate Shower || *** #
    activate("pythia8", "OFF", DirMadgraph + "/MSSMD/Cards/", info=info)

    # *** || Desactiva or activate Delphes || *** #
    activate("delphes", "OFF", DirMadgraph + "/MSSMD/Cards/", info=info)

    # *** || genera datos || *** #
    execute("./bin/generate_events <<< 0 <<< 0 ", info=info, position=DirMadgraph + "/MSSMD/")

    return file_exists(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe", info)
