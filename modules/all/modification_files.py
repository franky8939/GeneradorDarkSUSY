import os
import subprocess
import shutil
from modules.all.messange_info import printG


def file_set(inp, info=None, local=False):
    if local:
        printG(" :: ** file_set ** :: ", info=info)
    # Create file
    try:
        os.makedirs(inp)
        printG(" :: Directory created :: " + inp, info=info)
        return True
    except OSError as error:
        printG(" :: ERROR :: Directory " + inp + " already exists. Directory not created  ", info=info)
        return False
    except AttributeError:
        printG(" :: ERROR :: Input must be string. Directory not created", info=info)
        return False
    except:
        printG(" :: ERROR :: Unknown error using file_set", info=info)
        return False


def file_copy(dir_in, dir_out, mode, info=None, local=False):
    if local:
        printG(" :: ** file_copy ** :: ", info=info)
    try:
        if mode.lower() in ["tt"]:
            os.system("cp -r " + dir_in + "/* " + dir_out)

            if file_exists(dir_out, mode="empty", info=info):
                printG(" :: Copy unsuccessful folder in the first intent :: " +
                       dir_in + "/* :: to folder:: " + dir_out, info=info)
                printG(" :: Try other form of copy folder :: ", info=info)
                shutil.copytree(dir_in, dir_out)

            if file_exists(dir_out, mode="empty", info=info):
                printG(" :: Copy unsuccessful folder :: " + dir_in + " :: to folder:: " + dir_out, info=info)
                return False
            else:
                printG(" :: Copy success folder :: " + dir_in + " :: to folder:: " + dir_out, info=info)
                return True
        elif mode.lower() in ["ft"]:
            os.system("cp -r " + dir_in + " " + dir_out)
            printG(" :: Copy file :: " + dir_in + " :: to folder:: " + dir_out, info=info)
            return True
        elif mode.lower() in ["ff"]:
            shutil.copy(dir_in, dir_out)
            printG(" :: Copy file :: " + dir_in + " :: to file :: " + dir_out, info=info)
            return True
        else:
            printG(" :: ERROR IN MODE :: Copy :: " + dir_in + " :: to folder:: " + dir_out, info=info)
            return False
    except:
        printG(" :: ERROR IN EXECUTION :: Copy :: " + dir_in + " :: to folder:: " + dir_out, info=info)
        return False


def file_exists(inp, mode=None, info=None, local=False):
    if local:
        printG(" :: ** file_exist ** :: ", info=info)
    "Entra posible direccion, no importa si existe o es sintacticamente incorrecta"
    try:

        if os.path.exists(inp):
            #printG(" :: File exists :: " + inp, info=info)

            if mode is None:
                printG(" :: File does exist :: " + inp, info=info)
                return True
            else:
                if type(mode) is str:
                    if mode.lower() in "empty":
                        if len(os.listdir(inp)) is 0:
                            printG(" :: File exists and is empty :: " + inp, info=info)
                            return True
                        else:
                            printG(" :: File exists and is not empty :: " + inp, info=info)
                            return False
                    elif mode.lower() in "not_empty":
                        if len(os.listdir(inp)) is 0:
                            printG(" :: File exists and is empty :: " + inp, info=info)
                            return False
                        else:
                            printG(" :: File exists and is not empty :: " + inp, info=info)
                            return True

                    else:
                        printG(" :: ERROR :: Input mode must be empty or None. Cannot check :: " + str(mode), info=info)
                        return False
                else:
                    printG(" :: ERROR :: Input mode typ must be str. Cannot check.", info=info)
                    return False

        else:
            printG(" :: File does not exist :: " + inp, info=info)
            return False
    except TypeError:
        printG(" :: ERROR :: Input must be string. Cannot check.", info=info)
        return False
        #raise
    except:
        printG(" :: ERROR :: Unknown error using file_exist", info=info)
        return False


def file_clear(inp, mode='f', info=None, local=False):
    if local:
        printG(" :: ** file_clear ** :: ", info=info)
    try:
        if file_exists(inp, info=info):
            if mode.lower() in ["tree", "t"]:
                os.system("rm --r -f " + inp)
            elif mode.lower() in ["file", "f"]:
                os.remove(inp)
            else:  # Unknown clear mode
                printG(" :: ERROR :: Unknown mode using file_clear", info=info)
                return False

            if file_exists(inp):
                printG(" :: Unsuccessful, object not cleared :: " + inp, info=info)
                return False
            else:
                printG(" :: Success, object cleared :: " + inp, info=info)
                return True
        else:
            printG(" :: Unsuccessful, , object not cleared because not exist :: " + inp, info=info)
            return True
    except TypeError:
        printG(" :: ERROR :: Clear mode typ unknown :: user inp: " + str(mode), info=info)
        raise
    except:
        printG(" :: ERROR :: Unknown error using file_clear", info=info)
        return False

        # return False
    # except FileExistsError:
    #     printG(" :: Unsuccessful. Something went wrong and object not cleared :: ", info=info)


def execute(inp, position=None, info=None, local=False):
    if local:
        printG(" :: ** execute ** :: ", info=info)
    if position is not None:
        os.chdir(position)  # Posicionarse en el lugar, es necesario por la salida param_card.dat
        printG(" :: Relocate directory to :: " + position, info=info)
        #printG(" :: Nos encontramos en  :: " + os.getcwd(), info=info)
    try:
        g = subprocess.call(inp, shell=True)
        #g = os.system(inp)  # Execute the program
        if g == 0:
            printG(" :: Execute correct :: " + str(g) + " :: " + inp, info=info)
            return True
        else:
            printG(" :: Execute not correct :: " + str(g) + " :: " + inp, info=info)
            return False
    except:
        printG(" :: ERROR :: Execute :: " + inp, info=info)
        return False
