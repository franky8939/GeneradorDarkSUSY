from modules.Genera.Madg_create import *
from modules.Genera.genera_lhe import *
from modules.Genera.genera_root import *
from modules.Genera.genera_out import *


def genera_ini(Event,  # number of event simulate
               Ma_DNeu,  # value of mass of dark neutalino
               Ma_LNeu,  # value of mass of lightest neutalino
               Ma_DPho,  # value of mass of dark photon
               Tc_DPho,  # value of life time of dark photon
               Dir_Madg,  # directory of install Madgraph
               Dir_temp_Madg,  # directory of temporal install Madgraph
               Dir_Source,  # directory where source stay
               Dir_Out,  # directory of output resolution
               Mode,  # condicion using - in - or - out -
               Card,  # card using - CMS - or - HL -
               Name="DarkSUSY",  # name of root file output
               info=None,  # output of info for the process
               tyout="lhe"  # condicion if save files -lhe- or -root-
               ):
    # *** | COPY Madgraph in the place of work | *** #
    DirMadgraph = Madg_create(Dir_Madg,  # directory of install Madgraph
                              Dir_temp_Madg,  # directory of temporal install Madgraph
                              Mode,  # condition using - in - or - out -
                              info  # output of info for the process
                              )

    Madg_modification(Event,  # number of event simulate
                      Ma_DNeu,  # value of mass of dark neutalino
                      Ma_LNeu,  # value of mass of lightest neutalino
                      Ma_DPho,  # value of mass of dark photon
                      DirMadgraph,  # directory of install Madgraph
                      Dir_Source,  # directory where source stay
                      info  # output of info for the process
                      )

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Mu_min4 || ***
    genera_out(Event,  # number of event simulate
               Ma_DNeu,  # value of mass of dark neutalino
               Ma_LNeu,  # value of mass of lightest neutalino
               Ma_DPho,  # value of mass of dark photon
               Dir_Out,  # directory of output resolution
               info  # output of info for the process
               )
    DirOutput = Dir_Out + "/Events_" + str(Event) + \
                "/MneuL_" + str(Ma_LNeu) + "/MneuD_" + str(Ma_DNeu) + "/MphoD_" + str(Ma_DPho)  # new directory of out

    # CREATE LHE FILE#
    if tyout == "lhe":
        if genera_lhe(DirMadgraph,  # directory of install Madgraph
                      info  # output of info for the process
                      ):
            file_clear(DirOutput + "/lhe", "Tree", info)  # clear directory
            file_copy(DirMadgraph + "/MSSMD/Events", DirOutput + "/lhe", "tt", info)  # Copy the lhe
            execute("gzip -d " + DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz", info)  # descomprime
        else:
            Mess(" :: Problem in the obtein of *.lhe file :: ")

        # *** || Borrar temporates Madgraph de previos calculos || *** #
        if Mode == "out":
            file_clear(DirMadgraph, "Tree", info)
        return os.path.exists(DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe", info)

    # CREATE ROOT FILE #
    elif tyout == "root":

        # *** || Preparando Madgraph de previos calculos || *** #
        file_clear(DirMadgraph + "/MSSMD/Events/*", "Tree", info)  # borrar resultados

        # *** || Copiar a Madgraph *.lhe || *** #
        execute("gzip -d " + DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz", info)  # decompiler
        file_copy(DirOutput + "/lhe/", DirMadgraph + "/MSSMD/Events", "tt", info)

        # *** || Change life time in lhe || *** #
        if Tc_DPho is not 0:
            lifetime(Tc_DPho,
                     input=DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe",
                     output=DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe")  # change Tc
            Mess(" :: Se cambio el life time por : " + str(Tc_DPho), info)
        else:
            Mess(" :: Se mantuvo el life time default : ", info)

        # *** || Comprise *.lhe in Madg || *** #
        execute("gzip -1 " + DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe", info)  # comprime

        # *** || Obtein file root in Madg || *** #
        if genera_root(DirMadgraph,
                       Dir_Source,  # directory where source stay
                       Card,  # card using - CMS - or - HL -
                       info  # output of info for the process
                       ):
            # *** || Encuentra archivo *.root creado || *** #
            outROOT = []
            for i in os.listdir(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/"):
                if i.find(".root") != -1:
                    outROOT = i

            NameOutput = Name + "_" + Card + "_Event_" + str(Event) + "_MNeuL_" + str(Ma_LNeu) + \
                         "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_TcPhoD_" + str(Tc_DPho) + "_"
            file_copy(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + outROOT,
                      DirOutput + "/" + NameOutput + ".root", "ff", info)

            # *** || Borrar temporates Madgraph de previos calculos || *** #
            if Mode == "out":
                file_clear(DirMadgraph, "Tree", info)

            return file_exists(DirOutput + "/" + NameOutput + ".root", info)
        else:
            Mess(" ::  Execution problems in madevent :: ", info)
            return False

    else:
        Mess(" :: ERROR :: Tyout execution unknown :: ", info)
        return False
