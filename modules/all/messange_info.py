def printG(inp, info=None):
    print(inp)
    if info is not None:
        try:
            info.write("\n" + " ::  Execution problems in madevent :: ")
        except:
            print(" :: ERROR in include messange in 'info' ::")
