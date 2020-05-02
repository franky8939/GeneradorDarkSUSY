import argparse
import time
import itertools
from modules.all.modification_files import *
from modules.genera.variable_default import *
from modules.genera.ALL_genera import *

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
                        default=None)
    parser.add_argument("-Name", type=str, help="Name of root file out",
                        default="DarkSUSY")

    parser.add_argument("-Dir_Madg", type=str, help="Directory of Madgraph",
                        default="/LUSTRE/home/fmsanchez")
    parser.add_argument("-Dir_temp_Madg", type=str, help="Directory of temporal install Madgraph",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/temp")
    parser.add_argument("-Dir_Source", type=str, help="Directory where source stay",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/source")
    parser.add_argument("-Dir_Out", type=str, help="Directory of result",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/data")
    args = parser.parse_args()

    Event, Matrix_Card, Matrix_Ma_LNeu, Matrix_Ma_DNeu, Matrix_Ma_DPho, Matrix_Tc_DPho = \
        var_default(args.Event, args.Card, args.Ma_LNeu, args.Ma_DNeu, args.Ma_DPho, args.Tc_DPho)

    Name = args.Name
    # Card = args.Card
    count = True  # condition of loop
    ite = 1  # max number of iteration try to obtein info
    while count:
        count = False  # condition of break looprm --r -f temp/*
        for Ma_LNeu, Ma_DNeu, Ma_DPho, Tc_DPho, Card in \
                itertools.product(Matrix_Ma_LNeu, Matrix_Ma_DNeu, Matrix_Ma_DPho, Matrix_Tc_DPho, Matrix_Card):

            # Verificar que las masas se correspondan, en caso contrario no se generara file lhe
            if Ma_LNeu >= (Ma_DNeu + Ma_DPho):

                print(" ************************* CORRIDA NUEVA ************************* ")
                print(" :: Condiciones de Trabajo :: ")
                print(" :: Events :: " + str(Event) + " :: MneuL :: " + str(Ma_LNeu) + " :: MneuD :: " + str(Ma_DNeu) +
                      " :: MphoD :: " + str(Ma_DPho) + " :: TcPhoD :: " + str(Tc_DPho))
                localization = args.Dir_Out + "/Events_" + str(Event) + "/MneuL_" + str(Ma_LNeu) + \
                               "/MneuD_" + str(Ma_DNeu) + "/MphoD_" + str(Ma_DPho)
                NameLHE = Name + "_LHE" + "_Event_" + str(Event) + "_MNeuL_" + str(Ma_LNeu) + \
                          "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_"
                NameROOT = Name + "_" + Card + "_Event_" + str(Event) + "_MNeuL_" + str(Ma_LNeu) + \
                           "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_TcPhoD_" + str(Tc_DPho) + "_"

                # File *.lhe verification
                # Realizara el trabajo solo en 3 condiciones:
                #  - cuando exista lhe
                #  - cuando exista el file txt acreditando que se intento lhe y no converge
                #  - cuando el file RUN_lhe este activo
                time.sleep(random.random())  # desincronizar los procesos
                if not file_exists(localization + "/lhe/run_01_decayed_1/unweighted_events.lhe", local=True) \
                        and not file_exists(localization + "/" + NameLHE + ".txt", local=True) \
                        and not file_exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt", local=True):
                    info = open(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt", "w+")  # declarar corrida
                    printG(" :: CORRER PROGRAMA PARA OBTENER LHE ", info=info)
                    lhe_log = False
                    try:
                        lhe_log = genera(Event=Event,  # number of event simulate
                                         Ma_DNeu=Ma_DNeu,  # value of mass of dark neutrino
                                         Ma_LNeu=Ma_LNeu,  # value of mass of lightest neutrino
                                         Ma_DPho=Ma_DPho,  # value of mass of dark photon
                                         Tc_DPho=Tc_DPho,  # value of life time of dark photon
                                         Dir_Madg=args.Dir_Madg,  # directory of install Madgraph
                                         Dir_temp_Madg=args.Dir_temp_Madg,  # temp install Madgraph
                                         Dir_Source=args.Dir_Source,  # directory where source stay
                                         Dir_Out=args.Dir_Out,  # directory of out resolution
                                         Card=Card,  # card using - CMS - or - HL -
                                         Mode=args.Mode,  # condition using - in - or - out -
                                         tyout="lhe",  # condition save files -lhe- or -root-
                                         Name=args.Name,  # name of root file out
                                         info=info  # info of process
                                         )

                    except:
                        lhe_log = False
                        printG("\n" + " :: ERROR :: PROBLEMS IN THE EXECUTION OF *.lhe :: ", info=info)
                    # sys.exit()
                    if lhe_log:
                        printG(" :: SE GENERA LHE :: ", info=info)
                        #break
                    else:
                        printG(" :: NO GENERA LHE :: ", info=info)

                    # *** || Save info of Error || *** #
                    # if not lhe_log:
                    #    file_copy(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt",
                    #              localization + "/" + NameLHE + ".txt", "ff", info=info, local=True)
                    # Remove file of RUN
                    file_clear(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt", "File", info=info, local=True)
                    info.close()
                else:
                    printG(" :: FILE *.LHE EXIST OR IS RUNNING :: ")
                #sys.exit()
                # File *.lhe verification in process
                if file_exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt"):
                    count = True  # ciclo se repetira para generar despues los root del lhe cuando se genere

                # File *.root verification
                if file_exists(localization + "/lhe/run_01_decayed_1/unweighted_events.lhe", local=True) \
                        and not file_exists(localization + "/" + NameROOT + ".txt", local=True) \
                        and not file_exists(localization + "/" + NameROOT + ".root", local=True) \
                        and not file_exists(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt", local=True):
                    # DECLARE RUN
                    info = open(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt", "w+")
                    printG(" :: Run the programs for obtein root file", info=info)
                    root_log = False
                    try:
                        root_log = genera(Event=Event,  # number of event simulate
                                          Ma_DNeu=Ma_DNeu,  # value of mass of dark neutrino
                                          Ma_LNeu=Ma_LNeu,  # value of mass of lightest neutrino
                                          Ma_DPho=Ma_DPho,  # value of mass of dark photon
                                          Tc_DPho=Tc_DPho,  # value of life time of dark photon
                                          Dir_Madg=args.Dir_Madg,  # directory of install Madgraph
                                          Dir_temp_Madg=args.Dir_temp_Madg,  # temp install Madgraph
                                          Dir_Source=args.Dir_Source,  # directory where source stay
                                          Dir_Out=args.Dir_Out,  # directory of out solution
                                          Card=Card,  # card using - CMS - or - HL -
                                          Mode=args.Mode,  # condition using - in - or - out -
                                          tyout="root",  # condition save files -lhe- or -root-
                                          Name=args.Name,  # name of root file out
                                          info=info  # info of process
                                          )
                    except:
                        root_log = False
                        printG("\n" + " :: ERROR :: Problems in the execution of *.root :: ", info=info)
                    if root_log:
                        printG(" :: GENERA ROOT :: ", info=info)
                        #break
                    else:
                        printG(" :: NO GENERA ROOT :: ", info=info)
                    # if not root_log:
                    #    file_copy(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt",
                    #              localization + "/" + NameROOT + ".txt", "ff", info=info, local=True)
                    # Remove file of RUN
                    file_clear(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt", "File", local=True)
                    info.close()
                else:
                    printG(" :: FILE *.ROOT EXIST OR IS RUNNING :: ")

                # *** || Convertir el root y seleccionar solo los eventos con 4 muones o mas || *** #
                if file_exists(localization + '/Mu_min4/Mu4_' + NameROOT + ".root", local=True):
                    printG(" :: FILE Mu4*.root DE SELECCION EXISTE :: ")
                elif file_exists(localization + "/" + NameROOT + ".root") \
                        and not file_exists(localization + '/Mu_min4/Mu4_' + NameROOT + ".root", local=True):

                    command = 'root -l SelectDark3.C\'("' + \
                              localization + '/' + NameROOT + '.root" , "' + \
                              localization + '/Mu_min4/Mu4_' + NameROOT + '.root" , "' + \
                              localization + '/Mu_min4/LOG_Mu4_' + NameROOT + '.txt")\' <<< 0'
                    execute(command, position=args.Dir_Source, local=True)
                    file_exists(localization + '/Mu_min4/Mu4_' + NameROOT + '.root', local=True)

                elif file_exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt", local=True):
                    printG(" :: FILE *.LHE AND *.ROOT NOT EXIST :: RUNNING REDUCTION NOT POSIBLE ::")
                else:
                    printG(" :: FILE *.ROOT IS NOT RUNNING, GENERAL OPTION NO INCLUDE :: ")
