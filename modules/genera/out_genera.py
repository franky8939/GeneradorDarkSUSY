from modules.genera.card_modification import *


def out_genera(Event,  # number of event simulate
               Ma_DNeu,  # value of mass of dark neutalino
               Ma_LNeu,  # value of mass of lightest neutalino
               Ma_DPho,  # value of mass of dark photon
               Dir_Out,  # directory of out resolution
               info=None  # out of info for the process
               ):
    printG(" :: ********** MODIFICATION OUTPUT RESOLUTION OF MADGRAPH FOR USING DARKSUSY ********** :: ", info=info)

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Mu_min4 || ***
    file_set(Dir_Out + "/Events_" + str(Event), info=info, local=True)

    file_set(Dir_Out + "/Events_" + str(Event) + "/MneuL_" + str(Ma_LNeu), info=info, local=True)
    file_set(Dir_Out + "/Events_" + str(Event) + "/MneuL_" + str(Ma_LNeu) + \
             "/MneuD_" + str(Ma_DNeu), info=info, local=True)
    file_set(Dir_Out + "/Events_" + str(Event) + "/MneuL_" + str(Ma_LNeu) + \
             "/MneuD_" + str(Ma_DNeu) + "/MphoD_" + str(Ma_DPho), info=info, local=True)
    DirOutput = Dir_Out + "/Events_" + str(Event) + "/MneuL_" + str(Ma_LNeu) + \
                "/MneuD_" + str(Ma_DNeu) + "/MphoD_" + str(Ma_DPho)  # new directory of out

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/lhe || ***
    file_set(DirOutput + "/lhe", info=info, local=True)

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Mu_min4 || ***
    file_set(DirOutput + "/Mu_min4", info=info, local=True)  # crea carpeta

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Bad_log || ***
    # file_set(DirOutput + "/Bad_log", info=info)  # crea carpeta

    printG(" :: ********** FINALLY MODIFICATION OUTPUT RESOLUTION OF MADGRAPH ********** :: ", info=info)
    return True
