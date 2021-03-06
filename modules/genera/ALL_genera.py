from modules.genera.Madg_genera import *
from modules.genera.lhe_genera import *
from modules.genera.out_genera import *
from modules.genera.root_genera import *


def genera(Event,  # number of event simulate
           Ma_DNeu,  # value of mass of dark neutalino
           Ma_LNeu,  # value of mass of lightest neutalino
           Ma_DPho,  # value of mass of dark photon
           Tc_DPho,  # value of life time of dark photon
           Dir_Madg,  # directory of install Madgraph
           Dir_temp_Madg,  # directory of temporal install Madgraph
           Dir_Source,  # directory where source stay
           Dir_Out,  # directory of out resolution
           Mode,  # condicion using - in - or - out -
           Card,  # card using - CMS - or - HL -
           Name="DarkSUSY",  # name of root file out
           info=None,  # out of info for the process
           tyout="lhe"  # condicion if save files -lhe- or -root-
           ):
    # *** | COPY Madgraph in the place of work | *** #
    DirMadgraph, Folder = Madg_create(Dir_Madg,  # directory of install Madgraph
                                      Dir_temp_Madg,  # directory of temporal install Madgraph
                                      Mode,  # condition using - in - or - out -
                                      info  # out of info for the process
                                      )

    DirOutput = Dir_Out + "/Events_" + str(Event) + "/MneuL_" + str(Ma_LNeu) + \
                "/MneuD_" + str(Ma_DNeu) + "/MphoD_" + str(Ma_DPho)  # new directory of out
    NameOutput = Name + "_" + Card + "_Event_" + str(Event) + "_MNeuL_" + str(Ma_LNeu) + \
                 "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_TcPhoD_" + str(Tc_DPho) + "_"

    printG(" :: ****** DARKSUSY METHODOLOGY ****** ", info=info)

    Madg_modification(Event,  # number of event simulate
                      Ma_DNeu,  # value of mass of dark neutalino
                      Ma_LNeu,  # value of mass of lightest neutalino
                      Ma_DPho,  # value of mass of dark photon
                      DirMadgraph,  # directory of install Madgraph
                      Dir_Source,  # directory where source stay
                      info=info  # out of info for the process
                      )
    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Mu_min4 || ***
    out_genera(Event,  # number of event simulate
               Ma_DNeu,  # value of mass of dark neutalino
               Ma_LNeu,  # value of mass of lightest neutalino
               Ma_DPho,  # value of mass of dark photon
               Dir_Out,  # directory of out resolution
               info  # out of info for the process
               )
    # ****** || CREATE LHE FILE || ****** #
    if tyout == "lhe":
        printG(" :: ****** DARKSUSY METHODOLOGY, GENERA LHE ****** ", info=info)
        if lhe_genera(DirMadgraph, info):
            printG(" :: GENERATE  *.LHE FILE :: ", info=info)
            file_clear(DirOutput + "/lhe", "Tree", info=info)  # clear directory
            file_set(DirOutput + "/lhe", info=info)
            file_copy(DirMadgraph + "/MSSMD/Events", DirOutput + "/lhe", "tt", info=info)  # Copy the lhe
            execute("gzip -d " + DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz",
                    info=info, position=None)  # DECOMPILE
        else:
            printG(" :: ****** PROBLEM IN THE OBTEIN OF *.LHE FILE ****** :: ", info=info)

    # ****** || CREATE ROOT FILE || ****** #
    elif tyout == "root":
        printG(" :: ****** DARKSUSY METHODOLOGY, GENERA ROOT ****** ", info=info)
        # ****** || Preparando Madgraph de previos calculos || ****** #
        file_clear(DirMadgraph + "/MSSMD/Events", "Tree", info=info, local=True)  # CLEAR
        file_set(DirMadgraph + "/MSSMD/Events", info=info)

        # ****** || Copiar a Madgraph *.lhe || ****** #
        execute("gzip -d " + DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz",
                info=info, position=None)  # DECOMPILE
        file_copy(DirOutput + "/lhe", DirMadgraph + "/MSSMD/Events", "tt", info=info)

        # ****** || Change life time in lhe || ****** #
        if Tc_DPho is not 0:
            lifetime(Tc_DPho, inp=DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe",
                     out=DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe")  # CHANGE TC
            printG(" :: ****** Change the life time in ****** :: " + str(Tc_DPho), info=info)
        else:
            printG(" :: ****** Not posible change the life time in, using default ****** :: ", info=info)

        # *** || Comprise *.lhe in Madg || *** #
        execute("gzip -1 " + DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe",
                info=info,
                position=None)  # DECOMPILE

        # *** || Obtein file root in Madg || *** #
        printG(" :: ****** Generate *.root file ****** :: ", info=info)

        if root_genera(DirMadgraph,
                       Dir_Source,  # directory where source stay
                       Card,  # card using - CMS - or - HL -
                       info  # out of info for the process
                       ):
            # *** || Encuentra file *.root creado || *** #
            outROOT = []
            for i in os.listdir(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/"):
                if i.find(".root") != -1:
                    outROOT = i

            file_copy(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + outROOT,
                      DirOutput + "/" + NameOutput + ".root", "ff", info=info)
            printG(' :: ****** Generate correct the *.root ****** :: ', info=info)
        else:
            printG(' :: ****** Not generate correct the *.root ****** :: ', info=info)

    else:
        printG(" :: ERROR :: Tyout execution unknown :: ", info=info)

    # *** || Borrar temporates Madgraph de previos calculos || *** #
    if Mode == "out":
        file_clear(Folder, "Tree", info=info, local=True)
        printG(' :: ****** Mode "out" using :: clear Folder ****** :: ', info=info)
    else:
        printG(' :: ****** Mode "in" using :: No clear :: ****** :: ', info=info)

    printG(" :: ************** FINALLY DARKSUSY METHODOLOGY ************** ", info=info)
    if tyout == "lhe":
        return file_exists(DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe", info=info, local=True)
    elif tyout == "root":
        return file_exists(DirOutput + "/" + NameOutput + ".root", info=info, local=True)
    else:
        return False
