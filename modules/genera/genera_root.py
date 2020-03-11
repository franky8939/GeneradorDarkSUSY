from modules.Genera.Madg_modification import *


def genera_root(DirMadgraph,
                Dir_Source,  # directory where source stay
                Card,  # card using - CMS - or - HL -
                info=None  # output of info for the process
                ):
    # *** || Deactivate or activate Shower || *** #
    activate("pythia8", "ON", DirMadgraph + "/MSSMD/Cards/", info=info)

    # *** || Desactiva or activate Delphes || *** #
    activate("delphes", "ON", DirMadgraph + "/MSSMD/Cards/", Dir_Source, info=info, type=Card)

    # *** || Obtein file root in Madg || *** #
    execute("./bin/madevent pythia8 run_01_decayed_1 <<< 0", info, DirMadgraph + "/MSSMD/")  # genera root
    # *** || Encuentra archivo *.root creado || *** #
    outROOT = []
    for i in os.listdir(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/"):
        if i.find(".root") != -1:
            outROOT = i

    return file_exists(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + outROOT, info)
