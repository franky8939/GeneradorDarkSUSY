import os
import shutil
import random
import argparse
import random
from modules.messange_info import *
from modules.modification_files import *


#  FUNCION PARA CAMBIAR UNA LINEA DE UN ARCHIVO POR OTRA #
def modificarLinea(archivo, buscar, reemplazar):
    with open(archivo, "r") as f:
        lines = (line.rstrip() for line in f)
        altered_lines = [reemplazar if line == buscar else line for line in lines]

    with open(archivo, "w") as f:
        f.write('\n'.join(altered_lines) + '\n')


def lifetime(ctau_mean_mm, input="unweighted_events.lhe", output="unweighted_events_new.lhe"):
    '''
    function using in replace_lifetime_in_LHE.py
    necesita estar en la carpeta para que funcione
    '''
    # set input file name
    # filename = "unweighted_events.lhe"
    f = open(input, 'r')
    g = open(output, 'w')
    event_begin = False
    event_end = True
    for line in f:
        if line == '<event>\n':
            event_begin = True
            event_end = False
        if line == '</event>\n':
            event_begin = False
            event_end = True
        new_line = ''
        if event_begin == True and event_end == False:
            word_n = 0
            for word in line.split():
                if word == '3000022' or word_n > 0:
                    word_n = word_n + 1
                    if word_n < 13:
                        if word_n == 12:
                            if ctau_mean_mm is not 0:
                                ctau_mm = '%E' % random.expovariate(
                                    1.0 / float(ctau_mean_mm))  # exponential distribution
                                # print "ctau (mm) mean: ", ctau_mean_mm, " actual: ", ctau_mm
                            else:
                                ctau_mm = '%E' % float(0)
                            new_line = new_line + ctau_mm + '   '
                        else:
                            new_line = new_line + word + '   '
                    else:
                        new_line = new_line + word + '\n'
                        word_n = 0
        if new_line == '':
            g.write(line.rstrip('\n') + "\n")
            # print line.rstrip('\n')
        else:
            g.write(new_line.rstrip('\n') + "\n")
            # print new_line.rstrip('\n')
    f.close()
    g.close()


def Mad_bashrc(Dir, info=None):
    try:
        os.environ["MAD_N"] = Dir  # base
        os.environ["Deph_N"] = os.environ["Delph"] + ":" + os.environ["MAD_N"] + "/Delph"  # base
        os.environ["ExRoot_N"] = os.environ["Delph"] + "/external" + ":" + \
                                 os.environ["Delph"] + "/external/ExRootAnalysis" + ":" + \
                                 os.environ["Delph"] + "/classes" + ":"
        os.environ["Pythia8_N"] = os.environ["MAD_N"] + "/HEPTools/pythia8"
        os.environ["Heptools_N"] = os.environ["MAD_N"] + "/HEPTools"
        os.environ["lhapdf6"] = os.environ["Heptools_N"] + "/lhapdf6"
        os.environ["PATH"] = os.environ["PATH"] \
                             + ":" + os.environ["MAD_N"] + "/bin" + ":" + \
                             os.environ["ExRoot_N"] + ":" + \
                             os.environ["ExRoot_N"] + "/bin" + ":" + \
                             os.environ["Pythia8_N"] + "/bin" + ":" + \
                             os.environ["lhapdf6"] + "/bin" + ":" + \
                             os.environ["Heptools_N"] + "/bin" + ":"
        os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"] + ":" + \
                                        os.environ["ExRoot_N"] + ":" + \
                                        os.environ["ExRoot_N"] + "/lib" + ":" + \
                                        os.environ["Pythia8_N"] + "/lib" + ":" + \
                                        os.environ["lhapdf6"] + "/lib" + ":" + \
                                        os.environ["Heptools_N"] + "/lib" + ":"
        os.environ["ROOT_INCLUDE_PATH"] = os.environ["ROOT_INCLUDE_PATH"] + ":" + \
                                          os.environ["ExRoot_N"] + ":"
        os.environ["PYTHONPATH"] = os.environ["PYTHONPATH"] + ":" + \
                                   os.environ["ExRoot_N"] + ":"
        Mess(" :: Bash execution :: ", info)
    except:
        Mess(" :: ERROR :: Incorrect bash execution :: ", info)


def change(inp, var, num, info=None):
    try:
        if var == "Ma_DPho":
            modificarLinea(inp, "  3000022 2.500000e-01 # MAD", "  3000022 " + str(num) + " # MAD ")

            Mess(" :: Change mass of dark photon to :: " + str(num), info)
            return True
        elif var == "Ma_LNeu":
            # *** || Change the mass of lightest neutalino || *** #
            modificarLinea(inp, "  1000022 1.000000e+01 # Mneu1", "  1000022 " + str(num) + " # Mneu1 ")

            Mess(" :: Change mass of lightest neutalino to :: " + str(num), info)
            return True
        elif var == "Ma_DNeu":
            # *** || Change the mass of dark neutalino || *** #
            modificarLinea(inp, "  3000001 1.000000e+00 # MneuD", "  3000001 " + str(num) + " # MneuD ")

            Mess(" :: Change mass of dark neutalino to :: " + str(num), info)
            return True
        elif var == "events" or var == "Events":
            modificarLinea(inp, "  10000 = nevents ! Number of unweighted events requested",
                           "  " + str(num) + "  = nevents ! Number of unweighted events requested ")

            Mess(" :: Change Event to :: " + str(num), info)
            return True
        else:
            Mess(" :: ERROR :: var no incluide :: ", info)
            return False
    except:
        Mess(" :: ERROR :: Execution of :: " + var + "incorrect", info)
        return False


def file_set(inp, info=None):
    # Create file
    try:
        os.makedirs(inp)
        Mess(" :: Create file :: " + inp, info)
        return file_exists(inp)
    except:
        Mess(" :: ERROT :: Create file :: " + inp, info)
        return False


def file_copy(dir_in, dir_out, mode, info=None):
    try:
        if mode == "tt" or mode == "TT":
            os.system("cp -r " + dir_in + "/* " + dir_out)

            Mess(" :: Copy folder :: " + dir_in + " :: to folder:: " + dir_out, info)
            return True
        elif mode == "ft" or mode == "FT":
            os.system("cp -r " + dir_in + " " + dir_out)

            Mess(" :: Copy file :: " + dir_in + " :: to folder:: " + dir_out, info)
            return True
        elif mode == "ff" or mode == "FF":
            shutil.copy(dir_in, dir_out)

            Mess(" :: Copy file :: " + dir_in + " :: to file :: " + dir_out, info)
            return True
        else:

            Mess(" :: ERROR IN MODE :: Copy :: " + dir_in + " :: to folder:: " + dir_out, info)
            return False
    except:
        Mess(" :: ERROR IN EXECUTION :: Copy :: " + dir_in + " :: to folder:: " + dir_out, info)
        return False


def file_exists(inp, info=None):
    "Entra posible direccion, no importa si existe o es sintacticamente incorrecta"
    try:
        log = os.path.exists(inp)
        if log:
            Mess(" :: Exist file :: " + inp, info)
            return True
        else:
            Mess(" :: Not exist file :: " + inp, info)
            return False
    except:
        Mess(" :: NOT Exist file :: " + inp, info)
        return False


def file_clear(inp, mode, info=None):
    try:
        if mode is "Tree:" or mode is "tree:" or mode is "t:":
            os.system("rm --r -f " + inp)
        elif mode is "File" or mode is "file" or mode is "f":
            os.remove(inp)
        else:
            Mess(" :: Clear mode unknown :: ", info)
            return False

        if file_exists(inp):
            Mess(" :: Clear file :: " + inp, info)
            return True
        else:
            Mess(" :: Not posible clear file :: " + inp, info)
            return False
    except:
        Mess(" :: ERROR :: Clear file :: " + inp, info)
        return False


def execute(inp, info=None, position=None):
    if position is not None:
        os.chdir(position)  # Posicionarse en el lugar, es necesario por la salida param_card.dat
    try:
        g = os.system(inp)  # Execute the program
        Mess(" :: Execute correct :: " + str(g) + " :: " + inp, info)
        return True
    except:
        Mess(" :: ERROR :: Execute :: " + inp, info)
        return False


def activate(card, action, position_of_Card, position_of_Source=None, info=None, type=None):
    if action in ["ON", "On", "oN", "on"]:
        if card == "Pythia" or card == "pythia" or card == "Pythia8" or card == "pythia8":
            if file_exists(position_of_Card + "/pythia8_card_default.dat", info):
                file_copy(position_of_Card + "/pythia8_card_default.dat", position_of_Card + "/pythia8_card.dat", info)

                Mess(" :: Pythia8 Activate :: ", info)
                return True
            else:

                Mess(" :: ERROR :: Incorrect pythia8_card_default.dat not exist :: ", info)
                return False
        elif card == "Delphes" or card == "delphes":
            if type == "CMS":
                file_copy(position_of_Card + "/delphes_card_CMS.dat",
                          position_of_Card + "/delphes_card.dat", "ff", info)

                Mess(" :: Delphes CMS Activate :: ", info)
                return True
            elif type == "HL":
                if file_copy(position_of_Card + "/delphes_card_HL.dat",
                             position_of_Card + "/delphes_card.dat", "ff", info):

                    Mess(" :: Delphes HL Activate :: ", info)
                    return True
                elif file_copy(position_of_Card + "/delphes_card_HLLHC.dat",
                               position_of_Card + "/delphes_card.dat", "ff", info):

                    Mess(" :: Delphes HL Activate :: ", info)
                    return True
                elif file_copy(position_of_Source + "/delphes_card_HL.dat",
                               position_of_Source + "/delphes_card.dat", "ff", info):

                    Mess(" :: Delphes HL Activate :: ", info)
                    return True
                elif file_copy(position_of_Source + "/delphes_card_HLLHC.dat",
                               position_of_Source + "/delphes_card.dat", "ff", info):

                    Mess(" :: Delphes HL Activate :: ", info)
                    return True
                else:

                    Mess(" :: ERROR :: Incorrect delphes_card_HL*.dat not exist :: ", info)
                    return False
            elif type == "HL2":
                if file_copy(position_of_Card + "/delphes_card_HL2.dat",
                             position_of_Card + "/delphes_card.dat", "ff", info):

                    Mess(" :: Delphes HL2 Activate :: ", info)
                    return True
                elif file_copy(position_of_Card + "/delphes_card_HLLHC2.dat",
                               position_of_Card + "/delphes_card.dat", "ff", info):

                    Mess(" :: Delphes HL2 Activate :: ", info)
                    return True
                elif file_copy(position_of_Source + "/delphes_card_HL2.dat",
                               position_of_Source + "/delphes_card.dat", "ff", info):

                    Mess(" :: Delphes HL2 Activate :: ", info)
                    return True
                elif file_copy(position_of_Source + "/delphes_card_HLLHC2.dat",
                               position_of_Source + "/delphes_card.dat", "ff", info):

                    Mess(" :: Delphes HL2 Activate :: ", info)
                    return True
                else:

                    Mess(" :: ERROR :: Incorrect delphes_card_HL2*.dat not exist :: ", info)
                    return False
            else:

                Mess(" :: ERROR :: Incorrect type of card not include in program :: ", info)
                return False
        else:

            Mess(" :: ERROR :: Incorrect Position of Card for activate :: ", info)
            return True
    elif action in ["OFF", "Off", "oFF", "off"]:
        if file_exists(position_of_Card, info):
            if card == "Pythia" or card == "pythia" or card == "Pythia8" or card == "pythia8":
                file_clear(position_of_Card + "/pythia8_card.dat", "File", info)  # clear

                Mess(" :: Pythia8 Deactivate :: ", info)
                return True
            elif card == "Delphes" or card == "delphes":
                file_clear(position_of_Card + "/delphes_card.dat", "File", info)  # clear

                Mess(" :: Delphes Deactivate :: ", info)
                return True
            else:

                Mess(" :: ERROR :: Incorrect Card for deactivate :: ", info)
                return False
        else:
            Mess(" :: ERROR :: Incorrect Position of Card for deactivate :: ", info)
            return False


def Mess(inp, info=None):
    print(inp)
    if info is not None:
        try:
            info.write("\n" + " ::  Execution problems in madevent :: ")
        except:
            print(" :: ERROR in include messange in 'info' ::")


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
                tyout="lhe",  # condicion if save files -lhe- or -root-
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

        # *** || Borrar temporates Madgraph de previos calculos || *** #
        if Mode == "out":
            file_clear(Dir_temp_Madg + "/Process_" + NumberOfProcess, "Tree", info)
        return os.path.exists(DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe"), False

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
