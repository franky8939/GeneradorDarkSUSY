def var_default(Event, Card, Ma_LNeu, Ma_DNeu, Ma_DPho, Tc_DPho):
    if Ma_LNeu is None:
        Ma_LNeu = [10]

    if Card is None:
        Card = ["CMS", "HL", "HL2"]

    if Ma_DNeu is None:
        Ma_DNeu = [.25, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    if Ma_DPho is None:
        Ma_DPho = [.25, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:
        Ma_DPho = Ma_DPho

    if Tc_DPho is None:
        Tc_DPho = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    if Event is 0 or Event is None:
        Event = 10000

    return Event, Card, Ma_LNeu, Ma_DNeu, Ma_DPho, Tc_DPho
