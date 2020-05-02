from modules.genera.card_modification import *
import sys


def lhe_genera(DirMadgraph,  # directory of temporal install Madgraph
               info=None  # out of info for the process
               ):
    printG(" :: ********** Generate LHE file for using Dark Susy ********** :: ", info=info)

    # *** || Deactivate or activate Shower || *** #
    activate("pythia8", "OFF", DirMadgraph + "/MSSMD/Cards/", info=info)

    # *** || Desactiva or activate Delphes || *** #
    activate("delphes", "OFF", DirMadgraph + "/MSSMD/Cards/", info=info)

    # *** || genera datos || *** #
    position = DirMadgraph + "/MSSMD/"

    execute("./bin/generate_events", info=info, position=position, local=True)
    #sys.exit()
    printG(" :: ********** Finally generate LHE file for using Dark Susy ********** :: ", info=info)
    return file_exists(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe.gz", info=info, local=True)
