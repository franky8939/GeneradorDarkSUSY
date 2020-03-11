import os
import shutil
from modules.all.messange_info import printG


def file_set(inp, info=None):
    # Create file
    try:
        os.makedirs(inp)
        printG(" :: Create file :: " + inp, info)
        return file_exists(inp)
    except:
        printG(" :: ERROT :: Create file :: " + inp, info)
        return False


def file_copy(dir_in, dir_out, mode, info=None):
    try:
        if mode == "tt" or mode == "TT":
            os.system("cp -r " + dir_in + "/* " + dir_out)

            printG(" :: Copy folder :: " + dir_in + " :: to folder:: " + dir_out, info)
            return True
        elif mode == "ft" or mode == "FT":
            os.system("cp -r " + dir_in + " " + dir_out)

            printG(" :: Copy file :: " + dir_in + " :: to folder:: " + dir_out, info)
            return True
        elif mode == "ff" or mode == "FF":
            shutil.copy(dir_in, dir_out)

            printG(" :: Copy file :: " + dir_in + " :: to file :: " + dir_out, info)
            return True
        else:

            printG(" :: ERROR IN MODE :: Copy :: " + dir_in + " :: to folder:: " + dir_out, info)
            return False
    except:
        printG(" :: ERROR IN EXECUTION :: Copy :: " + dir_in + " :: to folder:: " + dir_out, info)
        return False


def file_exists(inp, info=None):
    "Entra posible direccion, no importa si existe o es sintacticamente incorrecta"
    try:
        log = os.path.exists(inp)
        if log:
            printG(" :: Exist file :: " + inp, info)
            return True
        else:
            printG(" :: Not exist file :: " + inp, info)
            return False
    except:
        printG(" :: NOT Exist file :: " + inp, info)
        return False


def file_clear(inp, mode, info=None):
    try:
        if mode is "Tree:" or mode is "tree:" or mode is "t:":
            os.system("rm --r -f " + inp)
        elif mode is "File" or mode is "file" or mode is "f":
            os.remove(inp)
        else:
            printG(" :: Clear mode unknown :: ", info)
            return False

        if file_exists(inp):
            printG(" :: Clear file :: " + inp, info)
            return True
        else:
            printG(" :: Not posible clear file :: " + inp, info)
            return False
    except:
        printG(" :: ERROR :: Clear file :: " + inp, info)
        return False


def execute(inp, position=None, info=None):
    if position is not None:
        os.chdir(position)  # Posicionarse en el lugar, es necesario por la salida param_card.dat
        printG(" :: Relocalizarse en :: " + position == os.getcwd() + " :: " + position)
    try:
        g = os.system(inp)  # Execute the program
        printG(" :: Execute correct :: " + str(g) + " :: " + inp, info)
        return True
    except:
        printG(" :: ERROR :: Execute :: " + inp, info)
        return False
