import os
from modules.messange_info import Mess


def Mad_bashrc(Dir, info=None):
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
        Mess(" :: Bash execution :: ", info)
    except:
        Mess(" :: ERROR :: Incorrect bash execution :: ", info)

