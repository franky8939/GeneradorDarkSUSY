import os
import shutil
import random
import argparse
import random


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


def bashrc_Mad(Dir):
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
    except:
        print(" :: Problems include Bash")

def set_file(dir):
    # Create file
    os.system("mkdir " + dir)



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
                Name="DarkSUSY"  # name of root file output
                ):
    # *** MODE USING FOR SIMULATION *** #
    DirMadgraph = ""
    if Mode == "out":
        # create file in temp
        if not os.path.exists(Dir_temp_Madg):
            os.system("mkdir " + Dir_temp_Madg)
        NumberOfProcess = str(random.randint(0, 10000))  # NAME OF PROCESS
        while os.path.exists(Dir_temp_Madg + "/Process_" + NumberOfProcess):
            NumberOfProcess = str(random.randint(0, 10000))  # NAME OF PROCESS
        os.system("mkdir " + Dir_temp_Madg + "/Process_" + NumberOfProcess)
        os.system("mkdir " + Dir_temp_Madg + "/Process_" + NumberOfProcess + "/MG5_aMC")
        print(" :: Se crea la carpeta : Process_" + NumberOfProcess + "/MG5_aMC ::")

        DirMadgraph = Dir_temp_Madg + "/Process_" + NumberOfProcess + "/MG5_aMC"
        os.system("cp -r " + Dir_Madg + "/* " + DirMadgraph)  # shutil.copytree(Dir_Madg, DirMadgraph)
        print(" :: Se copio mg5 correctamente en la carpeta : " + DirMadgraph + " :: ")

        # INCLUDE BASH
        bashrc_Mad(DirMadgraph)

    elif Mode == "in":
        DirMadgraph = Dir_Madg
    else:
        print(" :: Error in the introduction of Mode :: ")
        quit()

    # *** || COPY MSSMD_UFO || # Go to the folder MG5_aMC_vXXX/models. Copy the UFO model there in to folder MSSMD_UFO:
    try:
        shutil.rmtree(DirMadgraph + "/models/MSSMD_UFO")  # Borrar el archivo con contenido
        print(" :: Se borro archivo MSSMD_UFO en Madg5 :: ")
    except:
        print(" :: No se encontro archivo MSSMD_UFO en Madg5 :: ")
        quit()

    # *** || copy info MSSMD_UFO || *** #
    try:
        shutil.copytree(Dir_Source + "/MSSMD_UFO", DirMadgraph + "/models/MSSMD_UFO")  # Copiar la info
        print(" :: Se copio el archivo MSSMD_UFO :: ")
    except:
        print(" :: Error en la copia del archivo MSSMD_UFO :: ")
        quit()

    # *** || Mass Dark Photon || *** # Go to the folder MSSMD_UFO and execute .py:
    try:
        os.chdir(
            DirMadgraph + "/models/MSSMD_UFO")  # Posicionarse en el lugar, es necesario por la salida param_card.dat
        os.system("python " + "write_param_card.py")  # Execute the program
        print(" :: Se ejecuto write_param_card.py:: ")
    except:
        print(" :: No se pudo ejecutar write_param_card.py:: ")
        quit()

    # *** || Change the mass of dark photon || *** #
    try:
        modificarLinea(DirMadgraph + "/models/MSSMD_UFO/param_card.dat",
                       "  3000022 2.500000e-01 # MAD", "  3000022 " + str(Ma_DPho) + " # MAD ")
        print(" :: Se cambio  mass of dark photon :: ")
    except:
        print(" :: Error al cambiar  mass of dark photon :: ")

    # *** || Change the mass of lightest neutalino || *** #
    try:
        modificarLinea(DirMadgraph + "/models/MSSMD_UFO/param_card.dat",
                       "  1000022 1.000000e+01 # Mneu1", "  1000022 " + str(Ma_LNeu) + " # Mneu1 ")
        print(" :: Se cambio  mass of lightest neutalino :: ")
    except:
        print(" :: Error al cambiar  mass of lightest neutalino :: ")

    # *** || Change the mass of dark neutalino || *** #
    try:
        modificarLinea(DirMadgraph + "/models/MSSMD_UFO/param_card.dat",
                       "  3000001 1.000000e+00 # MneuD", "  3000001 " + str(Ma_DNeu) + " # MneuD ")
        print(" :: Se cambio  mass of dark neutalino :: ")
    except:
        print(" :: Error al cambiar  mass of dark neutalino :: ")

    # *** || COPY proc_card.dat || *** # Remove the default proc_card.dat in the MG5_aMC_vXXX directory
    try:
        os.remove(DirMadgraph + "/proc_card.dat")
        print(" :: proc_card.dat fue borrado :: ")
    except:
        print(" :: proc_card.dat no existe en el directorio :: ")
        quit()
    # Copy the following proc_card.dat there:
    shutil.copy(Dir_Source + "/proc_card.dat", DirMadgraph)
    print(" :: Se copio correctamente el archivo proc_card.dat :: ")

    # *** || Generar MSSMD || *** # Run ./bin/mg5_aMC proc_card.dat and generate the folder called MSSMD.
    try:
        os.chdir(DirMadgraph)  # Posicionarse en el lugar, es necesario
        os.system("./bin/mg5_aMC proc_card.dat")  # EXECUTE
        print(" :: Generada la carpeta MSSMD :: ")
    except:
        print(" :: No fue generada la carpeta MSSMD :: ")
        quit()

    # *** || Copy madspin || *** # Copy the madspin card to the Cards directory /MadGraph5/MG5_aMC_vXXX/MSSMD/Cards
    try:
        shutil.copy(Dir_Source + "/madspin_card.dat", DirMadgraph + "/MSSMD/Cards")
        print(" :: Se copio el archivo madspin_card.dat ::")
    except:
        print(" :: No se pudo copiar el archivo madspin_card.dat ::")
        quit()

    # *** || Change Run_card || *** # Copiar el archivo Run_card en el lugar correspondiente
    try:
        shutil.copy(Dir_Source + "/run_card.dat", DirMadgraph + "/MSSMD/Cards")
        # realize the change correspondence in the file run_card.dat
        modificarLinea(DirMadgraph + "/MSSMD/Cards/run_card.dat",
                       "  10000 = nevents ! Number of unweighted events requested",
                       "  " + str(Event) + "  = nevents ! Number of unweighted events requested ")
        print(" :: Se cambio la Run_card :: ")
    except:
        print(" :: No se pudo cambiar la Run_card :: ")
        quit()

    # *** || Deactivate or activate Shower || *** #
    try:
        if Pyt_bool in ["ON", "On", "oN", "on"]:
            # activate
            shutil.copy(DirMadgraph + "/MSSMD/Cards/pythia8_card_default.dat",
                        DirMadgraph + "/MSSMD/Cards/pythia8_card.dat")
        elif Pyt_bool in ["OFF", "Off", "oFF", "off"]:
            # deactivate
            if os.path.exists(DirMadgraph + "/MSSMD/Cards/pythia8_card.dat"):
                os.remove(DirMadgraph + "/MSSMD/Cards/pythia8_card.dat")
            print(" :: pythia8_card.dat fue borrado para su desactivacion:: ")
        else:
            print(" :: pythia8_card.dat condicion sin cambios:: ")
    except:
        print(" :: pythia8_card.dat condicion con problemas:: ")
        quit()

    # *** || Desactiva or activate Delphes || *** #
    try:
        if Del_bool in ["OFF", "Off", "oFF", "off"]:
            # deactivate
            if os.path.exists(DirMadgraph + "/MSSMD/Cards/delphes_card.dat"):
                os.remove(DirMadgraph + "/MSSMD/Cards/delphes_card.dat")
                print(" :: delphes_card.dat fue borrado y desactivado:: ")
        elif Del_bool in ["ON", "On", "oN", "on"]:
            if Card == "CMS":
                shutil.copy(DirMadgraph + "/MSSMD/Cards/delphes_card_CMS.dat",
                            DirMadgraph + "/MSSMD/Cards/delphes_card.dat")
            elif Card == "HL":
                if os.path.exists(DirMadgraph + "/MSSMD/Cards/delphes_card_HL.dat"):
                    shutil.copy(DirMadgraph + "/MSSMD/Cards/delphes_card_HL.dat",
                                DirMadgraph + "/MSSMD/Cards/delphes_card.dat")
                elif os.path.exists(DirMadgraph + "/MSSMD/Cards/delphes_card_HLLHC.dat"):
                    shutil.copy(DirMadgraph + "/MSSMD/Cards/delphes_card_HLLHC.dat",
                                DirMadgraph + "/MSSMD/Cards/delphes_card.dat")
                elif os.path.exists(Dir_Source + "/delphes_card_HL.dat"):
                    shutil.copy(Dir_Source + "/delphes_card_HL.dat",
                                DirMadgraph + "/MSSMD/Cards/delphes_card.dat")
                elif os.path.exists(Dir_Source + "/delphes_card_HLLHC.dat"):
                    shutil.copy(Dir_Source + "/delphes_card_HLLHC.dat",
                                DirMadgraph + "/MSSMD/Cards/delphes_card.dat")
                else:
                    print(" :: No hay card de delphes para HL disponible, stop program")
                    quit()
        else:
            print(" :: delphes_card.dat sin cambios:: ")
    except:
        print(" :: delphes_card.dat condicion con problemas ::  ")
        quit()

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Mu_min4 || ***
    try:
        files = ["/Events_" + str(Event),
                 "/MneuL_" + str(Ma_LNeu),
                 "/MneuD_" + str(Ma_DNeu),
                 "/MphoD_" + str(Ma_DPho)]
        DirOutput = Dir_Out
        for name in files:
            DirOutput += name
            try:
                os.system("mkdir " + DirOutput)  # crea carpeta
                print(" :: Directorio :: " + DirOutput + " fue creado :: ")
            except:
                print(" :: Directorio :: " + DirOutput + " existe :: ")
                # quit()
    except:
        print(" :: Problemas en la creacion de directorios :: ")
        quit()

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/lhe || ***
    try:
        os.system("mkdir " + DirOutput + "/lhe")  # crea carpeta
        print(" :: Directorio :: " + DirOutput + "/lhe" + " fue creado :: ")
    except:
        print(" :: Directorio :: " + DirOutput + "/lhe" + " existe :: ")

    # *** || Create /Events_###/MneuL_###/MneuD_###/MphoD_###/Mu_min4 || ***
    try:
        os.system("mkdir " + DirOutput + "/Mu_min4")  # crea carpeta
        print(" :: Directorio :: " + DirOutput + "/Mu_min4" + " fue creado :: ")
    except:
        print(" :: Directorio :: " + DirOutput + "/Mu_min4" + " existe :: ")

    # *** || Genera datos || *** #
    lhe_log = False
    root_log = False
    try:
        if tyout == "lhe":
            # Genera
            os.chdir(DirMadgraph + "/MSSMD/")  # Posicionarse en el lugar, es necesario
            os.system("./bin/generate_events <<< 0 <<< 0 ")
            # directory of copy
            shutil.rmtree(DirOutput + "/lhe")  # clear directory
            print(" :: Dir " + DirOutput + "/lhe fue borrada ::")

            shutil.copytree(DirMadgraph + "/MSSMD/Events", DirOutput + "/lhe")  # Copy the info
            print(" :: Se copio *.lhe en el directorio: " + DirOutput + "/lhe ::")
            # descomprime
            os.system("gzip -d " + DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz")
            print(" :: Se descomprimio el archivo lhe en la carpeta de guardado::")

            lhe_log = os.path.exists(DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe")
            root_log = False

        elif tyout == "root":

            # *** || Preparando Madgraph de previos calculos || *** #
            shutil.rmtree(DirMadgraph + "/MSSMD/Events")  # borrar resultados
            print(" :: borrar resultados de directorio : ", DirMadgraph + "/MSSMD/Events")

            # *** || Copiar a Madgraph *.lhe || *** #
            # if os.path.exists(DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz"):
            os.system("gzip -d " + DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe.gz")  # decompiler
            print(" :: decompiler unweighted_events.lhe.gz en la posicion de guardado :: ")
            # copy file
            shutil.copytree(DirOutput + "/lhe/", DirMadgraph + "/MSSMD/Events")
            print(" :: copiar unweighted_events.lhe.gz en MSSMD/Event :: ")

            # *** || Change life time in lhe || *** #
            if Tc_DPho is not 0:
                lifetime(Tc_DPho,
                         input=DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe",
                         output=DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe")  # change Tc
                print(" :: Se cambio el life time por : " + str(Tc_DPho))
            else:
                print(" :: Se mantuvo el life time default : ")

            # *** || Comprise *.lhe in Madg || *** #
            os.system("gzip -1 " + DirMadgraph + "/MSSMD/Events/run_01_decayed_1/unweighted_events.lhe")  # comprime
            print(" :: Se comprimio unweighted_events.lhe.gz en la carpeta Eventos de Madgraph :: ")

            # *** || Obtein file root in Madg || *** #
            os.chdir(DirMadgraph + "/MSSMD/")  # Posicionarse en el lugar, es necesario
            os.system("./bin/madevent pythia8 run_01_decayed_1 <<< 0")  # genera root
            print(" :: Se genera el archivo *.root :: ")
            # *** || Encuentra archivo *.root creado || *** #
            outROOT = []
            for i in os.listdir(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/"):
                if i.find(".root") != -1:
                    outROOT = i

            NameOutput = Name + "_" + Card + "_Event_" + str(Event) + "_MNeuL_" + str(Ma_LNeu) + \
                         "_MNeuD_" + str(Ma_DNeu) + "_MPhoD_" + str(Ma_DPho) + "_TcPhoD_" + str(Tc_DPho) + "_"
            # if len(outROOT) > 0:
            os.rename(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + outROOT,
                      DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + NameOutput + ".root")  # rename root file
            print(" :: Se renombra el archivo root segun la codificacion recomendada:: ")

            shutil.copy(DirMadgraph + "/MSSMD/Events/run_01_decayed_1/" + NameOutput + ".root",
                        DirOutput)
            print(" :: Se copia el archivo root a su localidad de guardado :: ")
            '''            except:
                print(" :: No se pudo renombrar y copiar el root de salida")
                quit()'''
            # salida
            lhe_log = os.path.exists(DirOutput + "/lhe/run_01_decayed_1/unweighted_events.lhe")
            root_log = os.path.exists(DirOutput + "/" + NameOutput + ".root")

        else:
            lhe_log = False
            root_log = False
    except:
        print(" :: Problems in obtein output file of Madgraph")

    # *** || Borrar temporates Madgraph de previos calculos || *** #
    if Mode == "out":
        shutil.rmtree(Dir_temp_Madg + "/Process_" + NumberOfProcess)
    return lhe_log, root_log
