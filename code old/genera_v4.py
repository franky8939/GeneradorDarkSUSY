from modules.mod_of_genera import *
import time

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

    # CONDITION
    if args.Ma_LNeu is None:
        Matrix_Ma_LNeu = [10]
    else:
        Matrix_Ma_LNeu = args.Ma_LNeu

    if args.Ma_DNeu is None:
        Matrix_Ma_DNeu = [.25, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    else:
        Matrix_Ma_DNeu = args.Ma_DNeu

    if args.Ma_DPho is None:
        Matrix_Ma_DPho = [.25, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    else:
        Matrix_Ma_DPho = args.Ma_DPho

    if args.Tc_DPho is None:
        Matrix_Tc_DPho = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    else:
        Matrix_Tc_DPho = args.Tc_DPho

    if type(args.Event) is not int or args.Event is 0 or args.Event is None:
        args.Event = 10000
        print(" :: Using default Event : 100")
    Event = args.Event

    if type(args.Mode) is not str or args.Mode not in ["in", "out"]:
        args.Mode = "out"
        print(" :: Input mode condition incorrect, using default || out || :: ")
    Mode = args.Mode

    if args.Card not in ["CMS", "HL", "ALL", "all", "all"]:
        args.Card = "CMS"
        print(" :: Input Card incorrect, using default || CMS || :: ")
    Card = args.Card

    if type(args.Name) is not str:
        args.Name = "DarkSUSY"
        print(" :: Input Name incorrect, using default || DarkSUSY || :: ")
        quit()
    Name = args.Name

    if type(args.Dir_Madg) is not str or not os.path.exists(args.Dir_Madg):
        print(" :: Directory of Madgraph not exist :: stop programs :: ")
        quit()

    if type(args.Dir_temp_Madg) is not str or not os.path.exists(args.Dir_temp_Madg):
        print(" :: Directory of temporal install Madgraph not exist :: stop programs ::  ")
        quit()

    if type(args.Dir_Source) is not str or not os.path.exists(args.Dir_Source):
        print(" :: Directory where source stay not exist :: stop programs ::  ")
        quit()

    if type(args.Dir_Out) is not str or not os.path.exists(args.Dir_Out):
        print(" :: Directory of result not exist :: stop programs ::  ")
        quit()

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

                            print(" ************************** CORRIDA NUEVA ************************** ")
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
                            ite = 1  # max number of iteration try to obtein info
                            time.sleep(random.random())  # desincronizar los procesos
                            if not os.path.exists(localization + "/lhe/run_01_decayed_1/unweighted_events.lhe") \
                                    and not os.path.exists(localization + "/" + NameLHE + ".txt") \
                                    and not os.path.exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt"):
                                f = open(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt", "w+")  # declarar corrida
                                f.write("\n" + " :: Correr programa para obtener lhe")
                                print(" :: Correr programa para obtener lhe")

                                lhe_log = False
                                root_log = False
                                while ite > 0:
                                    try:
                                        lhe_log, root_log = \
                                            genera_data(Event=Event,  # number of event simulate
                                                        Ma_DNeu=Ma_DNeu,  # value of mass of dark neutrino
                                                        Ma_LNeu=Ma_LNeu,  # value of mass of lightest neutrino
                                                        Ma_DPho=Ma_DPho,  # value of mass of dark photon
                                                        Tc_DPho=Tc_DPho,  # value of life time of dark photon
                                                        Dir_Madg=args.Dir_Madg,  # directory of install Madgraph
                                                        Dir_temp_Madg=args.Dir_temp_Madg,
                                                        # temp install Madgraph
                                                        Dir_Source=args.Dir_Source,
                                                        # directory where source stay
                                                        Dir_Out=args.Dir_Out,  # directory of output resolution
                                                        Card=args.Card,  # card using - CMS - or - HL -
                                                        Mode=args.Mode,  # condition using - in - or - out -
                                                        Pyt_bool="OFF",  # deactivation o no de Pythia8
                                                        Del_bool="OFF",  # deactivation o no de Delphes
                                                        tyout="lhe",  # condition save files -lhe- or -root-
                                                        Name=args.Name,  # name of root file output
                                                        info=f  # info of process
                                                        )
                                    except:
                                        f.write("\n" + " :: ERROR :: Problems in the execution of *.lhe :: ")
                                    if lhe_log:
                                        print(" :: genera lhe :: ")
                                        ite = 0
                                    else:
                                        print(" :: Not genera lhe :: ")
                                        ite -= 1
                                f.close()

                                if not lhe_log:
                                    file_copy(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt",
                                              localization + "/" + NameLHE + ".txt", "tt")  # declarar corrida
                                    file_exists(localization + "/" + NameLHE + ".txt")
                                # Remove file of RUN
                                file_clear(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt", "File")  # clear
                            else:
                                print(" :: File *.lhe exist or is runing :: ")

                            # File *.lhe verification in process
                            if file_exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt"):
                                count = True  # ciclo se repetira para buscar archivos pasados

                            # File *.root verification
                            ite = 1  # max number of iteration try to obtein info
                            if os.path.exists(localization + "/lhe/run_01_decayed_1/unweighted_events.lhe") \
                                    and not os.path.exists(localization + "/" + NameROOT + ".txt") \
                                    and not os.path.exists(localization + "/" + NameROOT + ".root") \
                                    and not os.path.exists(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt"):
                                # declarar corrida
                                f = open(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt", "w+")
                                f.write("\n" + " :: Correr programa para obtener root")

                                lhe_log = False
                                root_log = False
                                while ite > 0:
                                    try:
                                        lhe_log, root_log = \
                                            genera_data(Event=Event,  # number of event simulate
                                                        Ma_DNeu=Ma_DNeu,  # value of mass of dark neutrino
                                                        Ma_LNeu=Ma_LNeu,  # value of mass of lightest neutrino
                                                        Ma_DPho=Ma_DPho,  # value of mass of dark photon
                                                        Tc_DPho=Tc_DPho,  # value of life time of dark photon
                                                        Dir_Madg=args.Dir_Madg,  # directory of install Madgraph
                                                        Dir_temp_Madg=args.Dir_temp_Madg,
                                                        # temp install Madgraph
                                                        Dir_Source=args.Dir_Source,
                                                        # directory where source stay
                                                        Dir_Out=args.Dir_Out,  # directory of output solution
                                                        Card=args.Card,  # card using - CMS - or - HL -
                                                        Mode=args.Mode,  # condition using - in - or - out -
                                                        Pyt_bool="ON",  # deactivation o no de Pythia8
                                                        Del_bool="ON",  # deactivation o no de Delphes
                                                        tyout="root",  # condition save files -lhe- or -root-
                                                        Name=args.Name,  # name of root file output
                                                        info=f  # info of process
                                                        )
                                    except:
                                        f.write("\n" + " :: ERROR :: Problems in the execution of *.root :: ")
                                    if root_log:
                                        print(" :: genera root :: ")
                                        ite = 0
                                    else:
                                        print(" :: No genera root :: ")
                                        ite -= 1
                                f.close()
                                if not root_log:
                                    file_copy(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt",
                                              localization + "/" + NameROOT + ".txt", "ff")  # declarar corrida
                                    file_exists(localization + "/" + NameROOT + ".txt")
                                # Remove file of RUN
                                file_clear(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt", "File")  # borrar run
                                count = True  # ciclo se repetira para buscar archivos pasados
                            else:
                                print(" :: File *.root exist or is runing :: ")

                            # File *.lhe verification in process
                            if file_exists(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt"):
                                count = True  # ciclo se repetira para buscar archivos pasados

                            # *** || Convertir el root y seleccionar solo los eventos con 4 muones o mas || *** #
                            if os.path.exists(localization + "/" + NameROOT + ".root") \
                                    and not os.path.exists(localization + '/Mu_min4/Mu4_' + NameROOT + ".root"):
                                os.chdir(args.Dir_Source)  # se posiciona en el lugar donde esta SelectDark3
                                command = 'root -l SelectDark3.C\'("' + \
                                          localization + '/' + NameROOT + '.root" , "' + \
                                          localization + '/Mu_min4/Mu4_' + NameROOT + '.root" , "' + \
                                          localization + '/Mu_min4/LOG_Mu4_' + NameROOT + '.txt")\' <<< 0'
                                try:
                                    os.system(command)
                                    print(" :: Se creo el archivo Mu4_" + NameROOT + ".root")
                                except:
                                    print(" :: No se pudo crear el archivo Mu4_" + NameROOT + ".root")
                            else:
                                print(" :: File *.root reduction exist :: ")
