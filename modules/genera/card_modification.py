import random
from modules.all.modification_files import *
from modules.all.messange_info import printG  # include in modules.modification_files


#  FUNCION PARA CAMBIAR UNA LINEA DE UN ARCHIVO POR OTRA #
def changeLine(file, find, replace):
    with open(file, "r") as f:
        lines = (line.rstrip() for line in f)
        altered_lines = [replace if line == find else line for line in lines]

    with open(file, "w") as f:
        f.write('\n'.join(altered_lines) + '\n')


def lifetime(ct_mean_mm, inp="unweighted_events.lhe", out="unweighted_events_new.lhe"):
    """ function using in replace_lifetime_in_LHE.py, need stay in the folder of inp to work correct """
    # set inp file name
    # filename = "unweighted_events.lhe"
    f = open(inp, 'r')
    g = open(out, 'w')
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
        if event_begin and not event_end:
            word_n = 0
            for word in line.split():
                if word == '3000022' or word_n > 0:
                    word_n = word_n + 1
                    if word_n < 13:
                        if word_n == 12:
                            if ct_mean_mm is not 0:
                                ctau_mm = '%E' % random.expovariate(
                                    1.0 / float(ct_mean_mm))  # exponential distribution
                                # print "ctau (mm) mean: ", ct_mean_mm, " actual: ", ctau_mm
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


def change(inp, var, num, info=None):
    try:
        if var == "Ma_DPho":
            changeLine(inp, "  3000022 2.500000e-01 # MAD", "  3000022 " + str(num) + " # MAD ")

            printG(" :: Change mass of dark photon to :: " + str(num), info=info)
            return True
        elif var == "Ma_LNeu":
            # *** || Change the mass of lightest neutalino || *** #
            changeLine(inp, "  1000022 1.000000e+01 # Mneu1", "  1000022 " + str(num) + " # Mneu1 ")

            printG(" :: Change mass of lightest neutalino to :: " + str(num), info=info)
            return True
        elif var == "Ma_DNeu":
            # *** || Change the mass of dark neutalino || *** #
            changeLine(inp, "  3000001 1.000000e+00 # MneuD", "  3000001 " + str(num) + " # MneuD ")

            printG(" :: Change mass of dark neutalino to :: " + str(num), info=info)
            return True
        elif var == "events" or var == "Events":
            changeLine(inp, "  10000 = nevents ! Number of unweighted events requested",
                       "  " + str(num) + "  = nevents ! Number of unweighted events requested ")

            printG(" :: Change Event to :: " + str(num), info=info)
            return True
        else:
            printG(" :: ERROR :: var no incluide :: ", info=info)
            return False
    except:
        printG(" :: ERROR :: Execution of :: " + var + " incorrect", info=info)
        return False


def activate(card, action, position_of_Card, position_of_Source=None, info=None, typ=None):
    if action in ["ON", "On", "oN", "on"]:
        if card == "Pythia" or card == "pythia" or card == "Pythia8" or card == "pythia8":
            if file_exists(position_of_Card + "/pythia8_card_default.dat", info=info):
                file_copy(position_of_Card + "/pythia8_card_default.dat",
                          position_of_Card + "/pythia8_card.dat",
                          "ff",
                          info=info)

                printG(" :: Pythia8 Activate :: ", info=info)
                return True
            else:

                printG(" :: ERROR :: Incorrect pythia8_card_default.dat not exist :: ", info=info)
                return False
        elif card == "Delphes" or card == "delphes":
            if typ == "CMS":
                file_copy(position_of_Card + "/delphes_card_CMS.dat",
                          position_of_Card + "/delphes_card.dat", "ff", info=info)

                printG(" :: Delphes CMS Activate :: ", info=info)
                return True
            elif typ == "HL":
                # if file_copy(position_of_Card + "/delphes_card_HL.dat",
                #             position_of_Card + "/delphes_card.dat", "ff", info=info, local=True):

                #    printG(" :: Delphes HL Activate :: ", info=info)
                #    return True
                # elif file_copy(position_of_Card + "/delphes_card_HLLHC.dat",
                #               position_of_Card + "/delphes_card.dat", "ff", info=info, local=True):

                #    printG(" :: Delphes HL Activate :: ", info=info)
                #    return True
                if file_copy(position_of_Source + "/delphes_card_HL.dat",
                             position_of_Card + "/delphes_card.dat", "ff", info=info, local=True):

                    printG(" :: Delphes HL Activate :: ", info=info)
                    return True
                # elif file_copy(position_of_Source + "/delphes_card_HLLHC.dat",
                #               position_of_Card + "/delphes_card.dat", "ff", info=info, local=True):

                #    printG(" :: Delphes HL Activate :: ", info=info)
                #    return True
                else:

                    printG(" :: ERROR :: Incorrect delphes_card_HL*.dat not exist :: ", info=info)
                    return False
            elif typ == "HL2":
                # if file_copy(position_of_Card + "/delphes_card_HL2.dat",
                #             position_of_Card + "/delphes_card.dat", "ff", info=info, local=True):

                #    printG(" :: Delphes HL2 Activate :: ", info=info)
                #    return True
                # elif file_copy(position_of_Card + "/delphes_card_HLLHC2.dat",
                #               position_of_Card + "/delphes_card.dat", "ff", info=info, local=True):

                #    printG(" :: Delphes HL2 Activate :: ", info=info)
                #    return True
                if file_copy(position_of_Source + "/delphes_card_HL2.dat",
                             position_of_Card + "/delphes_card.dat", "ff", info=info, local=True):

                    printG(" :: Delphes HL2 Activate :: ", info=info)
                    return True
                # elif file_copy(position_of_Source + "/delphes_card_HLLHC2.dat",
                #               position_of_Source + "/delphes_card.dat", "ff", info=info, local=True):

                #    printG(" :: Delphes HL2 Activate :: ", info=info)
                #    return True
                else:

                    printG(" :: ERROR :: Incorrect delphes_card_HL2*.dat not exist :: ", info=info)
                    return False
            else:

                printG(" :: ERROR :: Incorrect typ of card not include in program :: ", info=info)
                return False
        else:

            printG(" :: ERROR :: Incorrect Position of Card for activate :: ", info=info)
            return True
    elif action in ["OFF", "Off", "oFF", "off"]:
        if file_exists(position_of_Card, info=info, local=True):
            if card == "Pythia" or card == "pythia" or card == "Pythia8" or card == "pythia8":
                file_clear(position_of_Card + "/pythia8_card.dat", "File", info=info, local=True)  # clear

                printG(" :: Pythia8 Deactivate :: ", info=info)
                return True
            elif card == "Delphes" or card == "delphes":
                file_clear(position_of_Card + "/delphes_card.dat", "File", info=info, local=True)  # clear

                printG(" :: Delphes Deactivate :: ", info=info)
                return True
            else:

                printG(" :: ERROR :: Incorrect Card for deactivate :: ", info=info)
                return False
        else:
            printG(" :: ERROR :: Incorrect Position of Card for deactivate :: ", info=info)
            return False
