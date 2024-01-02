import math

from apps.dapp.models import Dapp, DappNetwork
from apps.quest.models import QuestAction
from apps.user.models import UserFavorite


async def filterDapps(user_id: int, tbd_token: bool, is_favorite: bool, network_ids: str, category_ids: str, quest: int, page: int, page_size: int):
    data = {
        "data": [],
        "total_page": 0,
    }
    dapps = await Dapp.all().order_by("-created_at").values()
    if len(dapps) == 0:
        return data

    if is_favorite:
        if user_id == 0:
            return [], 0
        userFavorites = await UserFavorite.filter(account_id=user_id, category="dapp", is_favorite=True).order_by("-created_at")
        if len(userFavorites) == 0:
            return [], 0
        dappFavorites = list()
        for userFavorite in userFavorites:
            for dapp in dapps:
                if userFavorite.dapp_id == dapp['id']:
                    dappFavorites.append(dapp)
                    break
        dapps = dappFavorites
    if len(dapps) == 0:
        return data

    questActions = []
    questDappIds = set()
    if quest != 0:
        questActions = await QuestAction.all()
    if quest == 1 and len(questActions) == 0:
        return [], 0
    for questAction in questActions:
        if len(questAction.dapps) == 0:
            continue
        questDappIds.update(questAction.dapps.split(','))

    filterNetworkIds = list()
    if network_ids:
        filterNetworkIds = network_ids.split(",")
    filterCategoryIds = list()
    if category_ids:
        filterCategoryIds = category_ids.split(",")

    dappsData = list()
    for dapp in dapps:
        if not is_favorite:
            if tbd_token and dapp['tbd_token'] != "Y":
                continue
            if not tbd_token and dapp['tbd_token'] != "N":
                continue
        if len(filterNetworkIds) > 0:
            if len(dapp['network_ids']) == 0:
                continue
            dappNetworkIds = dapp['network_ids'].split(",")
            match = any(elem in filterNetworkIds for elem in dappNetworkIds)
            if not match:
                continue
        if len(filterCategoryIds) > 0:
            if len(dapp['category_ids']) == 0:
                continue
            dappCategoryIds = dapp['category_ids'].split(",")
            match = any(elem in filterCategoryIds for elem in dappCategoryIds)
            if not match:
                continue
        if quest == 1 and str(dapp['id']) not in questDappIds:
            continue
        elif quest == 2 and str(dapp['id']) in questDappIds:
            continue
        dappsData.append(dapp)

    if len(dappsData) > 0:
        dappIds = list()
        for dapp in dappsData:
            dappIds.append(dapp['id'])
        dappNetworks = await DappNetwork.filter(dapp_id__in=dappIds).select_related("network").all()
        for dapp in dappsData:
            # if len(dapp['category_ids']) > 0:
            #     dappCategoryList = list()
            #     categoryIds = dapp['category_ids'].split(",")
            #     for id in categoryIds:
            #             dappCategoryList.append({
            #                 'dapp_id': dapp['id'],
            #                 'category_id': int(id),
            #             })
            #     dapp['dapp_category'] = dappCategoryList
            if len(dapp['network_ids']) > 0:
                dappNetworkList = list()
                networkIds = dapp['network_ids'].split(",")
                for id in networkIds:
                    dappSrc = ""
                    chain_id = None
                    for dappNetwork in dappNetworks:
                        if dappNetwork.dapp_id == dapp['id'] and dappNetwork.network_id == int(id):
                            dappSrc = dappNetwork.dapp_src
                            chain_id = dappNetwork.network.chain_id
                            break
                    dappNetworkList.append({
                        'dapp_id': dapp['id'],
                        'network_id': int(id),
                        'chain_id': chain_id,
                        'dapp_src': dappSrc,
                    })
                dapp['dapp_network'] = dappNetworkList

    data['total_page'] = math.ceil(len(dappsData)/page_size)
    offset = (page - 1) * page_size
    if offset >= len(dapps):
        return data
    to = offset+page_size
    if to > len(dappsData):
        to = len(dappsData)

    dappsResponseData = dappsData[offset:to]
    for dapp in dappsResponseData:
        if dapp['category_ids']:
            categoryIds = dapp['category_ids'].split(',')
            dapp['category_ids'] = []
            for categoryId in categoryIds:
                dapp['category_ids'].append(int(categoryId))
        else:
            dapp['category_ids'] = []
        if dapp['network_ids']:
            networkIds = dapp['network_ids'].split(',')
            dapp['network_ids'] = []
            for networkId in networkIds:
                dapp['network_ids'].append(int(networkId))
        else:
            dapp['network_ids'] = []

    data['data'] = dappsResponseData
    return data