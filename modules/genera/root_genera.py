from modules.genera.Madg_modification import *


def root_genera(DirMadgraph,
                Dir_Source,  # directory where source stay
                Card,  # card using - CMS - or - HL -
                info=None  # out of info for the process
                ):
    printG(" :: ********** Generate ROOT file for using Dark Susy ********** :: ", info=info)
    # *** || Deactivate or activate Shower || *** #
    activate("pythia8", "ON", DirMadgraph + "/MSSMD/Cards", info=info)
    # *** || Desactiva or activate Delphes || *** #
    activate("delphes", "ON", DirMadgraph + "/MSSMD/Cards", position_of_Source=Dir_Source, info=info, typ=Card)

    # *** || Obtein file root in Madg || *** #
    position = DirMadgraph + "/MSSMD"
    ite = 3
    outROOT = None
    for j in range(ite):
        if outROOT is None:
            execute("./bin/madevent pythia8 run_01_decayed_1", info=info, position=position, local=True)  # genera root
            # *** || Encuentra file *.root creado || *** #
            for i in os.listdir(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/"):
                if ".root" in i:
                    outROOT = i

        if outROOT is None:
            execute("./bin/madevent delphes run_01_decayed_1/", info=info, position=position, local=True)  # genera root
            for i in os.listdir(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/"):
                if ".root" in i:
                    outROOT = i

    if outROOT is None:
        printG(" :: Not find file *.root :: ", info=info)
        return False
    else:
        printG(" :: Find file *.root :: " + outROOT, info=info)
        name = DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + outROOT
    printG(" :: ********** Finally generate ROOT file for using Dark Susy ********** :: ", info=info)

    return file_exists(str(name), info=info, local=True)

