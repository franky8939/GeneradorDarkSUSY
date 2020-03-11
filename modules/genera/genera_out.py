from modules.modification_card import *


def genera_out(Event,  # number of event simulate
               Ma_DNeu,  # value of mass of dark neutalino
               Ma_LNeu,  # value of mass of lightest neutalino
               Ma_DPho,  # value of mass of dark photon
               Dir_Out,  # directory of output resolution
               info=None  # output of info for the process
               ):

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
    return True
