from modules.mod_of_genera import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-Event", type=int, help="Number of Event", default=100)
    parser.add_argument("-Ma_DNeu", help="Mass of the Dark Neutralino", default=1)
    parser.add_argument("-Ma_LNeu", help="Mass of the Lightest Neutalino", default=10)
    parser.add_argument("-Ma_Pho", help="Mass of the Photon", default=None)
    parser.add_argument("-Tc_Pho", help="Mass of the Photon", default=None)
    parser.add_argument("-Dir_Madg", type=str, help="Directory of Madgraph", default="source/MG5_aMC_v2_6_7")
    parser.add_argument("-Dir_Out", type=str, help="Directory of Result", default="output/")
    parser.add_argument("-Modo", type=bool,
                        help=" 0 o False : Trabajar en el directorio de Madgraph; 1 o True Trabajar en directorio nuevo",
                        default=False)
    parser.add_argument("-Card", type=str, help="Card of Delphes using in the simulation ", default="CMS")

    args = parser.parse_args()
    # print(args.modo)
    if args.event == 100:
        print(" :: Using default Event : 100")
    else:
        print(" :: Using Event : " + str(args.event))
    if args.mphoton == None:
        args.mphoton = [.25, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        print(" :: Using default Photon Mass Default")
    if args.tcphoton == None:
        args.tcphoton = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        print(" :: Using default Photon Tc Default")

    genera_data(100,  # number of event simulate
                10,  # value of mass of dark neutalino
                1,  # value of mass of lightest neutalino
                1,  # value of mass of dark photon
                0,  # value of life time of dark photon
                "/LUSTRE/home/fmsanchez/MG5_aMC_v2_7_0",  # directory of install Madgraph
                "/LUSTRE/home/fmsanchez/GDarkSUSY/temp",  # directory of temporal install Madgraph
                "/LUSTRE/home/fmsanchez/GDarkSUSY/source",  # directory where source stay
                "/LUSTRE/home/fmsanchez/GDarkSUSY/data",  # directory of output resolution
                "CMS",  # card using - CMS - or - HL -
                "out",  # condicion using - in - or - out -
                "ON",  # desactivacion o no de Pythia
                "OFF",  # desactivacion o no de Delphes
                "lhe",  # condicion if save files -lhe- or -root-
                "DarkSUSY"  # name of root file output
                )

