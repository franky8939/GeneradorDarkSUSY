from mod_of_genera import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-Event", type=int, help="Number of Event",
                        default=100)
    parser.add_argument("-Ma_DNeu", help="Mass of the Dark Neutralino",
                        default={.25, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
    parser.add_argument("-Ma_LNeu", help="Mass of the Lightest Neutalino",
                        default={.25, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
    parser.add_argument("-Ma_DPho", help="Mass of the Dark Photon",
                        default={.25, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
    parser.add_argument("-Tc_DPho", help="Life time of the Dark Photon",
                        default={0})

    parser.add_argument("-Mode", type=str, help="condition using - in - or - out -",
                        default="out")
    parser.add_argument("-Card", type=str, help="Card using - CMS - or - HL -",
                        default="CMS")
    parser.add_argument("-Name", type=str, help="Name of root file output",
                        default="DarkSUSY")

    parser.add_argument("-Dir_Madg", type=str, help="Directory of Madgraph",
                        default="/LUSTRE/home/fmsanchez/MG5_aMC_v2_7_0")
    parser.add_argument("-Dir_temp_Madg", type=str, help="Directory of temporal install Madgraph",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/temp")
    parser.add_argument("-Dir_Source", type=str, help="Directory where source stay",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/source")
    parser.add_argument("-Dir_Orm --r -f temp/*ut", type=str, help="Directory of result",
                        default="/LUSTRE/home/fmsanchez/GDarkSUSY/data")
    args = parser.parse_args()

    # CONDITION
    if type(args.Event) is not int or args.Event is 0:
        args.Event = 100
        print(" :: Using default Event : 100")
    Event = args.Event

    if type(args.Mode) is not str or args.Mode not in ["in", "out"]:
        args.Mode = "out"
        print(" :: Input mode condition incorrect, using default || out || :: ")
    Mode = args.Mode

    if type(args.Card) is not str or args.Card not in ["CMS", "HL"]:
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

    count = 0  # condition of loop
    while count == 0:
        count = 1  # condition of break looprm --r -f temp/*
        for Ma_LNeu in args.Ma_LNeu:
            for Ma_DNeu in args.Ma_DNeu:
                for Ma_DPho in args.Ma_DPho:
                    for Tc_DPho in args.Tc_DPho:
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
                                   "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_TcPhoD_" + str(Tc_DPho) + "_"

                        # File *.lhe verification
                        if not os.path.exists(localization + "/lhe/run_01_decayed_1/unweighted_events.lhe") \
                                and not os.path.exists(localization + "/" + NameLHE + ".txt") \
                                and not os.path.exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt"):
                            open(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt", "w+")  # declarar corrida
                            print(" :: Correr programa para obtener lhe")

                            lhe_log, root_log = genera_data(Event=Event,  # number of event simulate
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
                                                            Pyt_bool="OFF",  # deactivation o no de Pythia8
                                                            Del_bool="OFF",  # deactivation o no de Delphes
                                                            tyout="lhe",  # condition save files -lhe- or -root-
                                                            Name=args.Name  # name of root file output
                                                            )
                            if not lhe_log:
                                open(localization + "/" + NameLHE + ".txt", "w+")  # declarar corrida
                            # Remove file of RUN
                            os.remove(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt")  # borrar declaracion de run
                            count = 0  # ciclo se repetira para buscar archivos pasados

                        # File *.lhe verification in process
                        if os.path.exists(args.Dir_Out + "/" + "RUN_lhe_" + NameLHE + ".txt"):
                            count = 0  # ciclo se repetira para buscar archivos pasados

                        # File *.root verification
                        if os.path.exists(localization + "/lhe/run_01_decayed_1/unweighted_events.lhe") \
                                and not os.path.exists(localization + "/" + NameROOT + ".txt") \
                                and not os.path.exists(localization + "/" + NameROOT + ".root") \
                                and not os.path.exists(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt"):
                            # declarar corrida
                            open(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt", "w+")
                            print(" :: Correr programa para obtener root")

                            lhe_log, root_log = genera_data(Event=Event,  # number of event simulate
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
                                                            Pyt_bool="ON",  # deactivation o no de Pythia8
                                                            Del_bool="ON",  # deactivation o no de Delphes
                                                            tyout="root",  # condition save files -lhe- or -root-
                                                            Name=args.Name  # name of root file output
                                                            )
                            if not root_log:
                                print(" :: Sin salida de ROOT :: ")
                                open(localization + "/" + NameROOT + ".txt", "w+")  # declarar corrida
                            # Remove file of RUN
                            os.remove(args.Dir_Out + "/" + "RUN_root_" + NameROOT + ".txt")  # borrar declaracion de run
                            count = 0  # ciclo se repetira para buscar archivos pasados

                        # *** || Convertir el root y seleccionar solo los eventos con 4 muones o mas || *** #
                        if os.path.exists(localization + "/" + NameROOT + ".root") and \
                                not os.path.exists(localization + '/Mu_min4/Mu4_' + NameROOT + ".root"):
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

