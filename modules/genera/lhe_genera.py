from modules.genera.modification_card import *


def genera_lhe(DirMadgraph,  # directory of temporal install Madgraph
               info=None  # output of info for the process
               ):
    printG(" :: ********** Generate LHE file for using Dark Susy ********** :: ", info=info)
    # *** || Deactivate or activate Shower || *** #
    activate("pythia8", "OFF", DirMadgraph + "/MSSMD/Cards/", info=info)

    # *** || Desactiva or activate Delphes || *** #
    activate("delphes", "OFF", DirMadgraph + "/MSSMD/Cards/", info=info)

    # *** || genera datos || *** #
    position = DirMadgraph + "/MSSMD/"
    execute("./bin/generate_events <<< 0 <<< 0 ", info=info, position=position, local=True)

    return file_exists(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe", info=info, local=True)
