from modules.genera.card_modification import *


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
    execute("./bin/generate_events <<< 0 <<< 0 ", info=info, position=position, local=True)

    printG(" :: ********** Finally generate LHE file for using Dark Susy ********** :: ", info=info)
    return file_exists(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe", info=info, local=True)
