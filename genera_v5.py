import sys
import time
import argparse

# sys.path.insert(0, "/LUSTRE/home/fmsanchez/GDarkSUSY/")  # lib of Programs

from modules.genera.genera_ini import *
from modules.genera.var_default import *
from modules.all.modification_files import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-Event", type=int, help="Number of Event",
                        default=None)
    parser.add_argument("-Ma_DNeu", help="Mass of the Dark Neutralino",
                        default=None)
    parser.add_argument("-Ma_LNeu", help="Mass of the Lightest Neutalino",
                        default=None)
    parser.add_argument("-Ma_DPho", help="Mass of the Dark Photon",
                        default=None)
    parser.add_argument("-Tc_DPho", help="Life time of the Dark Photon",
                        default=None)

    parser.add_argument("-Mode", type=str, help="condition using - in - or - out -",
                        default="out")
    parser.add_argument("-Card", type=str, help="Card using - CMS - or - HL - or - HL2 -",
                        default="CMS")
    parser.add_argument("-Name", type=str, help="Name of root file output",
                        default="DarkSUSY")

    parser.add_argument("-Dir_Madg", type=str, help="Directory of Madgraph",
                        default="/LUSTRE/home/fmsanchez/MG5_aMC_v2_7_0")
    parser.add_argument("-Dir_temp_Madg", type=str, help="Directory of temporal install Madgraph",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/temp")
    parser.add_argument("-Dir_Source", type=str, help="Directory where source stay",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/source")
    parser.add_argument("-Dir_Out", type=str, help="Directory of result",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/data")
    args = parser.parse_args()

    Event, Matrix_Ma_LNeu, Matrix_Ma_DNeu, Matrix_Ma_DPho, Matrix_Tc_DPho = \
        var_default(args.Event, args.Ma_LNeu, args.Ma_DNeu, args.Ma_DPho, args.Tc_DPho)

    Name = args.Name
    Card = args.Card
    count = True  # condition of loop
    ite = 1  # max number of iteration try to obtein info
    while count:
        count = False  # condition of break looprm --r -f temp/*
        for Ma_LNeu in Matrix_Ma_LNeu:
            for Ma_DNeu in Matrix_Ma_DNeu:
                for Ma_DPho in Matrix_Ma_DPho:
                    for Tc_DPho in Matrix_Tc_DPho:

                        # Verificar que las masas se correspondan, en caso contrario no se generara archivo lhe
                        if Ma_LNeu >= (Ma_DNeu + Ma_DPho):

                            print(" ************************* CORRIDA NUEVA ************************* ")
                            print(" :: Condiciones de Trabajo :: ")
                            print(" :: Events :: " + str(Event) +
                                  " :: MneuL :: " + str(Ma_LNeu) +
                                  " :: MneuD :: " + str(Ma_DNeu) +
                                  " :: MphoD :: " + str(Ma_DPho) +
                                  " :: TcPhoD :: " + str(Tc_DPho))
                            localization = args.Dir_Out + \
                                           "/Events_" + str(Event) + \
                                           "/MneuL_" + str(Ma_LNeu) + \
                                           "/MneuD_" + str(Ma_DNeu) + \
                                           "/MphoD_" + str(Ma_DPho)
                            NameLHE = Name + "_LHE" + "_Event_" + str(Event) + "_MNeuL_" + str(Ma_LNeu) + \
                                      "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_"
                            NameROOT = Name + "_" + Card + "_Event_" + str(Event) + "_MNeuL_" + str(Ma_LNeu) + \
                                       "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_TcPhoD_" + str(
                                Tc_DPho) + "_"

                            # File *.lhe verification
                            # Realizara el trabajo solo en 3 condiciones:
                            #  - cuando exista lhe
                            #  - cuando exista el archivo txt acreditando que se intento lhe y no converge
                            #  - cuando el archivo RUN_lhe este activo
                            time.sleep(random.random())  # desincronizar los procesos
                            if not file_exists(localization + "/lhe/run_01_decayed_1/unweighted_events.lhe") \
                                    and not file_exists(localization + "/" + NameLHE + ".txt") \
                                    and not file_exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt"):
                                info = open(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt",
                                            "w+")  # declarar corrida
                                printG(" :: Correr programa para obtener lhe", info)
                                lhe_log = False
                                for i in range(ite):
                                    # try:
                                    lhe_log = \
                                        genera_ini(Event=Event,  # number of event simulate
                                                   Ma_DNeu=Ma_DNeu,  # value of mass of dark neutrino
                                                   Ma_LNeu=Ma_LNeu,  # value of mass of lightest neutrino
                                                   Ma_DPho=Ma_DPho,  # value of mass of dark photon
                                                   Tc_DPho=Tc_DPho,  # value of life time of dark photon
                                                   Dir_Madg=args.Dir_Madg,  # directory of install Madgraph
                                                   Dir_temp_Madg=args.Dir_temp_Madg,  # temp install Madgraph
                                                   Dir_Source=args.Dir_Source,  # directory where source stay
                                                   Dir_Out=args.Dir_Out,  # directory of output resolution
                                                   Card=args.Card,  # card using - CMS - or - HL -
                                                   Mode=args.Mode,  # condition using - in - or - out -
                                                   tyout="lhe",  # condition save files -lhe- or -root-
                                                   Name=args.Name,  # name of root file output
                                                   info=info  # info of process
                                                   )
                                    # except:
                                    #    f.write("\n" + " :: ERROR :: Problems in the execution of *.lhe :: ")
                                    if lhe_log:
                                        printG(" :: Se genera lhe :: ", info)
                                        break
                                    else:
                                        printG(" :: Not genera lhe :: ", info)

                                # *** || Save info of Error || *** #
                                if not lhe_log:
                                    file_copy(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt",
                                              localization + "/" + NameLHE + ".txt", "ff", info)  # declarar corrida
                                    file_exists(localization + "/" + NameLHE + ".txt", info)
                                # Remove file of RUN
                                file_clear(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt", "File", info)  # clear
                                info.close()
                            else:
                                printG(" :: File *.lhe exist or is running :: ")

                            # File *.lhe verification in process
                            if file_exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt") or \
                                    file_exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".root"):
                                count = True  # ciclo se repetira para buscar archivos pasados

                            # File *.root verification
                            if file_exists(localization + "/lhe/run_01_decayed_1/unweighted_events.lhe") \
                                    and not os.path.exists(localization + "/" + NameROOT + ".txt") \
                                    and not os.path.exists(localization + "/" + NameROOT + ".root") \
                                    and not os.path.exists(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt"):
                                # declarar corrida
                                info = open(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt", "w+")
                                printG(" :: Run the programs for obtein root file", info)
                                root_log = False
                                for i in range(ite):
                                    # try:
                                    root_log = \
                                        genera_ini(Event=Event,  # number of event simulate
                                                   Ma_DNeu=Ma_DNeu,  # value of mass of dark neutrino
                                                   Ma_LNeu=Ma_LNeu,  # value of mass of lightest neutrino
                                                   Ma_DPho=Ma_DPho,  # value of mass of dark photon
                                                   Tc_DPho=Tc_DPho,  # value of life time of dark photon
                                                   Dir_Madg=args.Dir_Madg,  # directory of install Madgraph
                                                   Dir_temp_Madg=args.Dir_temp_Madg,  # temp install Madgraph
                                                   Dir_Source=args.Dir_Source,  # directory where source stay
                                                   Dir_Out=args.Dir_Out,  # directory of output solution
                                                   Card=args.Card,  # card using - CMS - or - HL -
                                                   Mode=args.Mode,  # condition using - in - or - out -
                                                   tyout="root",  # condition save files -lhe- or -root-
                                                   Name=args.Name,  # name of root file output
                                                   info=info  # info of process
                                                   )
                                    if root_log:
                                        printG(" :: genera root :: ", info)
                                        break
                                    else:
                                        printG(" :: Not genera root :: ", info)
                                if not root_log:
                                    file_copy(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt",
                                              localization + "/" + NameROOT + ".txt", "ff", info)  # declarar corrida
                                    file_exists(localization + "/" + NameROOT + ".txt", info)
                                # Remove file of RUN
                                file_clear(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt", "File")  # borrar run
                                info.close()
                            else:
                                printG(" :: File *.root exist or is runing :: ")

                            # *** || Convertir el root y seleccionar solo los eventos con 4 muones o mas || *** #
                            if file_exists(localization + "/" + NameROOT + ".root") \
                                    and not file_exists(localization + '/Mu_min4/Mu4_' + NameROOT + ".root"):

                                command = 'root -l SelectDark3.C\'("' + \
                                          localization + '/' + NameROOT + '.root" , "' + \
                                          localization + '/Mu_min4/Mu4_' + NameROOT + '.root" , "' + \
                                          localization + '/Mu_min4/LOG_Mu4_' + NameROOT + '.txt")\' <<< 0'
                                execute(command, position=args.Dir_Source)
                                file_exists(localization + '/Mu_min4/Mu4_' + NameROOT + '.root')
                            else:
                                printG(" :: File *.root reduction exist :: ")
