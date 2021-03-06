import os
import sys
from modules.all.messange_info import printG


def Mad_bashrc(Dir, info=None, local=False):
    printG(" :: ********** Generate Bash of Madgraph for using Dark Susy ********** :: ", info=info)
    if local:
        printG(" :: ** execute bash ** :: ", info=info)
    # Basic
    '''sys.path.insert(0, Dir)  # lib of Programs
    sys.path.insert(0, Dir + "/Delphes")  # lib of Programs
    sys.path.insert(0, Dir + "/Delphes/lib")  # lib of Programs
    sys.path.insert(0, Dir + "/Delphes/external")  # lib of Programs
    sys.path.insert(0, Dir + "/Delphes/external/ExRootAnalysis")  # lib of Programs
    sys.path.insert(0, Dir + "/Delphes/classes")  # lib of Programs
    sys.path.insert(0, Dir + "/HEPTools/bin")  # lib of Programs
    sys.path.insert(0, Dir + "/HEPTools/pythia8")  # lib of Programs
    sys.path.insert(0, Dir + "/HEPTools/pythia8/bin")  # lib of Programs
    sys.path.insert(0, Dir + "/HEPTools/pythia8/lib")  # lib of Programs
    sys.path.insert(0, Dir + "/HEPTools/lhapdf6/bin")  # lib of Programs\
    sys.path.insert(0, Dir + "/HEPTools/lhapdf6/lib")  # lib of Programs'''

    try:
        # Another Form
        os.environ["MADGRAPH5"] = Dir  # base
        os.environ["Delphes"] = os.environ["MADGRAPH5"] + "/Delphes"  # base

        os.environ["ExRoot"] = os.environ["Delphes"] + "/external" + ":" + \
                               os.environ["Delphes"] + "/external/ExRootAnalysis" + ":" + \
                               os.environ["Delphes"] + "/classes"

        os.environ["Pythia8"] = os.environ["MADGRAPH5"] + "/HEPTools/pythia8"

        os.environ["lhapdf6"] = os.environ["MADGRAPH5"] + "/HEPTools/lhapdf6"

        os.environ["PATH"] = os.environ["PATH"] + ":" + \
                             os.environ["MADGRAPH5"] + "/bin" + ":" + \
                             os.environ["ExRoot"] + ":" + \
                             os.environ["ExRoot"] + "/bin" + ":" + \
                             os.environ["Pythia8"] + "/bin" + ":" + \
                             os.environ["lhapdf6"] + "/bin" + ":" + \
                             os.environ["Heptools"] + "/bin"

        os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"] + ":" + \
                                        os.environ["ExRoot"] + ":" + \
                                        os.environ["ExRoot"] + "/lib" + ":" + \
                                        os.environ["Pythia8"] + "/lib" + ":" + \
                                        os.environ["lhapdf6"] + "/lib"

        os.environ["ROOT_INCLUDE_PATH"] = os.environ["ROOT_INCLUDE_PATH"] + ":" + \
                                          os.environ["ExRoot"]

        os.environ["PYTHONPATH"] = os.environ["PYTHONPATH"] + ":" + \
                                   os.environ["ExRoot"] + ":"
        '''os.environ["MAD_N"] = Dir  # base
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
                                   os.environ["ExRoot_N"] + ":"'''
        printG(" :: Bash execution :: ", info=info)
    except:
        printG(" :: ERROR :: Incorrect bash execution :: ", info=info)

    printG(" :: ********** Finally generate Bash of Madgraph for using Dark Susy ********** :: ", info=info)
    return True
