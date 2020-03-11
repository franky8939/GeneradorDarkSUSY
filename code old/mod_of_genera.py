
# from modules.messange_info import *
# from modules.modification_files import *
from modules.modification_bashrc import *
from modules.modification_card import *
# from modules.


def genera_data(Event,  # number of event simulate
                Ma_DNeu,  # value of mass of dark neutalino
                Ma_LNeu,  # value of mass of lightest neutalino
                Ma_DPho,  # value of mass of dark photon
                Tc_DPho,  # value of life time of dark photon
                Dir_Madg,  # directory of install Madgraph
                Dir_temp_Madg,  # directory of temporal install Madgraph
                Dir_Source,  # directory where source stay
                Dir_Out,  # directory of output resolution
                Card,  # card using - CMS - or - HL -
                Mode,  # condicion using - in - or - out -
                Pyt_bool=None,  # desactivacion o no de Pythia
                Del_bool=None,  # desactivacion o no de Delphes
                tyout="lhe",  # condicion if save files -lhe- or -root-tyout="lhe",  # condicion if save files -lhe- or -root-
                Name="DarkSUSY",  # name of root file output
                info="off"  # output of info for the process
                ):
    NumberOfProcess = None
    # *** | Log of process | *** #
    if info == "off":
        info = open("LOG.txt", 'w')  # CREATE TXT FILE TO SAVE THE CHARACTERIZATION PROCESS INFO

    # *** | MODE USING FOR SIMULATION | *** #
    DirMadgraph = ""
    if Mode == "out":
        try:
            # create file in temp MG5_aMC
            file_set(Dir_temp_Madg, info)

            NumberOfProcess = str(random.randint(0, 10000))  # NAME OF PROCESS
            ite = 100
            while file_exists(Dir_temp_Madg + "/Process_" + NumberOfProcess, info) and ite > 100:
                NumberOfProcess = str(random.randint(0, 10000))  # NAME OF PROCESS
                ite -= 1

            file_set(Dir_temp_Madg + "/Process_" + NumberOfProcess, info)  # create file
            file_set(Dir_temp_Madg + "/Process_" + NumberOfProcess + "/MG5_aMC", info)  # create file

            # Directory of Madgraph
            DirMadgraph = Dir_temp_Madg + "/Process_" + NumberOfProcess + "/MG5_aMC"
            file_copy(Dir_Madg, DirMadgraph, "tt", info)  # shutil.copytree(Dir_Madg, DirMadgraph)

        except:

            print(" :: ERROR :: Execute Mode out :: EXIT PROGRAM ")
            info.write("\n" + " :: ERROR :: Execute Mode out :: EXIT PROGRAM ")
            return False, False

    elif Mode == "in":
        DirMadgraph = Dir_Madg
    else:
        print(" :: ERROR :: Execute incorrect modet :: EXIT PROGRAM ")
        info.write("\n" + " :: ERROR :: Execute incorrect modet :: EXIT PROGRAM ")
        return False, False

    # *** | INCLUDE BASH | *** #
    Mad_bashrc(DirMadgraph)

    # *** || Clear MSSMD_UFO || # Go to the folder MG5_aMC_vXXX/models. Copy the UFO model there in to folder MSSMD_UFO:
    file_clear(DirMadgraph + "/models/MSSMD_UFO", "tree", info)  # Borrar el archivo con contenido

    # *** || copy info MSSMD_UFO || *** #
    if not file_copy(Dir_Source + "/MSSMD_UFO", DirMadgraph + "/models/MSSMD_UFO", "tt", info):  # Copy the info

        # *** || Borrar temporates Madgraph de previos calculos || *** #
        if Mode == "out":
            file_clear(Dir_temp_Madg + "/Process_" + NumberOfProcess, "Tree", info)
        return False, False

    # *** || Go to the folder MSSMD_UFO and execute *.py || *** # :
    execute("python write_param_card.py", info, position=DirMadgraph + "/models/MSSMD_UFO")

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
    if not execute("./bin/mg5_aMC proc_card.dat", info, position=DirMadgraph):
        # *** || Borrar temporates Madgraph de previos calculos || *** #
        if Mode == "out":
            file_clear(Dir_temp_Madg + "/Process_" + NumberOfProcess, "Tree", info)
        return False, False

    # *** || Copy madspin || *** # Copy the madspin card to the Cards directory /MadGraph5/MG5_aMC_vXXX/MSSMD/Cards
    file_copy(Dir_Source + "/madspin_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info)

    # *** || Change Run_card || *** # Copiar el archivo Run_card en el lugar correspondiente
    file_copy(Dir_Source + "/madspin_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info)

    # *** || Change Run_card || *** # Copiar el archivo Run_card en el lugar correspondiente
    file_copy(Dir_Source + "/run_card.dat", DirMadgraph + "/MSSMD/Cards", "ft", info)
    # realize the change correspondence in the file run_card.dat
    change(DirMadgraph + "/MSSMD/Cards/run_card.dat", "Events", Event, info)

    # *** || Deactivate or activate Shower || *** #
    activate("pythia8", Pyt_bool, DirMadgraph + "/MSSMD/Cards/", info=info)

    # *** || Desactiva or activate Delphes || *** #
    activate("delphes", Del_bool, DirMadgraph + "/MSSMD/Cards/", Dir_Source, info=info, type=Card)

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Mu_min4 || ***
    file_set(Dir_Out + "/Events_" + str(Event), info)
    file_set(Dir_Out + "/Events_" + str(Event) +
             "/MneuL_" + str(Ma_LNeu), info)
    file_set(Dir_Out + "/Events_" + str(Event) +
             "/MneuL_" + str(Ma_LNeu) + "/MneuD_" + str(Ma_DNeu), info)
    file_set(Dir_Out + "/Events_" + str(Event) +
             "/MneuL_" + str(Ma_LNeu) + "/MneuD_" + str(Ma_DNeu) + "/MphoD_" + str(Ma_DPho), info)
    DirOutput = Dir_Out + "/Events_" + str(Event) + \
                "/MneuL_" + str(Ma_LNeu) + "/MneuD_" + str(Ma_DNeu) + "/MphoD_" + str(Ma_DPho)  # new directory of out

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/lhe || ***
    file_set(DirOutput + "/lhe", info)

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Mu_min4 || ***
    file_set(DirOutput + "/Mu_min4", info)  # crea carpeta

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Bad_log || ***
    # file_set(DirOutput + "/Bad_log", info)  # crea carpeta

    # *** || Genera datos || *** #
    # try:
    if tyout == "lhe":
        # Genera
        if execute("./bin/generate_events <<< 0 <<< 0 ", info, DirMadgraph + "/MSSMD/"):
            file_clear(DirOutput + "/lhe", "Tree")  # clear directory
            file_copy(DirMadgraph + "/MSSMD/Events", DirOutput + "/lhe", "tt", info)  # Copy the info
            execute("gzip -d " + DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz", info)  # descomprime



    elif tyout == "root":

        # *** || Preparando Madgraph de previos calculos || *** #
        file_clear(DirMadgraph + "/MSSMD/Events/*", "Tree", info)  # borrar resultados

        # *** || Copiar a Madgraph *.lhe || *** #
        execute("gzip -d " + DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz", info)  # decompiler
        # copy file
        file_copy(DirOutput + "/lhe/", DirMadgraph + "/MSSMD/Events", "tt", info)

        # *** || Change life time in lhe || *** #
        if Tc_DPho is not 0:
            lifetime(Tc_DPho,
                     input=DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe",
                     output=DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe")  # change Tc
            print(" :: Se cambio el life time por : " + str(Tc_DPho))
            info.write("\n" + " :: Se cambio el life time por : " + str(Tc_DPho))
        else:
            print(" :: Se mantuvo el life time default : ")
            info.write("\n" + " :: Se mantuvo el life time default : ")

        # *** || Comprise *.lhe in Madg || *** #
        execute("gzip -1 " + DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe", info)  # comprime

        # *** || Obtein file root in Madg || *** #
        if execute("./bin/madevent pythia8 run_01_decayed_1 <<< 0", info, DirMadgraph + "/MSSMD/"):  # genera root
            # *** || Encuentra archivo *.root creado || *** #
            outROOT = []
            for i in os.listdir(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/"):
                if i.find(".root") != -1:
                    outROOT = i

            file_exists(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + outROOT)
            NameOutput = Name + "_" + Card + "_Event_" + str(Event) + "_MNeuL_" + str(Ma_LNeu) + \
                         "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_TcPhoD_" + str(Tc_DPho) + "_"
            if len(outROOT) > 0:
                file_copy(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + outROOT,
                          DirOutput + "/" + NameOutput + ".root", "ff", info)
            else:
                print(" :: ERROR :: ROOT not correcting generate  :: ")
                info.write("\n" + " :: ERROR :: ROOT not correcting generate  :: ")

            # *** || Borrar temporates Madgraph de previos calculos || *** #
            if Mode == "out":
                file_clear(Dir_temp_Madg + "/Process_" + NumberOfProcess, "Tree", info)

            return True, file_exists(DirOutput + "/" + NameOutput + ".root")
        else:
            print(" ::  Execution problems in madevent :: ")
            info.write("\n" + " ::  Execution problems in madevent :: ")

        return True, False

    else:
        # *** || Borrar temporates Madgraph de previos calculos || *** #
        if Mode == "out":
            file_clear(Dir_temp_Madg + "/Process_" + NumberOfProcess, "Tree", info)
        return False, False
    # except:


'''        print(" :: ERROR :: Problems in Execution :: ")
        info.write("\n" + " :: ERROR :: Problems in Execution :: ")
        # *** || Borrar temporates Madgraph de previos calculos || *** #
        if Mode == "out":
            file_clear(Dir_temp_Madg + "/Process_" + NumberOfProcess, "Tree", info)

        return False, False'''
