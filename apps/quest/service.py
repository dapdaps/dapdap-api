
def init_dapps():
    pass


def actionDapps(actionDappIds:str, dapps:[]):
    if len(actionDappIds) == 0:
        return dapps
    actionDapps = list()
    actionDappIdArr = actionDappIds.split(",")
    for actionDappId in actionDappIdArr:
        for dapp in dapps:
            if dapp['id'] == actionDappId:
                actionDapps.append(dapp)
                break
    return actionDapps