# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py
import math
from fastapi import APIRouter, Depends
from starlette.requests import Request
from tortoise.functions import Count
from web3 import Web3

from apps.action.models import Action, ActionRecord, ActionChain
from fastapi_pagination import Page
from apps.action.schemas import ActionIn, DeleteActionIn, UpdateActionRecordIn, ActionRecordResultOut
from apps.dapp.models import Dapp
from apps.invite.utils import is_w3_address
from core.auth.utils import get_current_user
from core.utils.base_util import get_limiter
import logging
import datetime
from tortoise.expressions import Q
from core.utils.tool_util import success
from fastapi_pagination.ext.tortoise import paginate
from core.base.db_provider import query_special_action

logger = logging.getLogger(__name__)
limiter = get_limiter()
# router = APIRouter(prefix="/api/action", dependencies=[Depends(get_current_user)],)
router = APIRouter(prefix="/api/action")


@router.post('/add', tags=['action'])
async def add_action(request: Request, action_in: ActionIn):
    now_time = datetime.datetime.utcnow()
    timestamp = int(now_time.timestamp())

    if is_w3_address(action_in.account_id):
        action_in.account_id = Web3.to_checksum_address(action_in.account_id)
    else:
        action_in.account_id = action_in.account_id.lower()

    dappId = 0
    if len(action_in.template) > 0:
        dapp = await Dapp.filter(name=action_in.template).first().values('id')
        if dapp:
            dappId = dapp['id']


    # search ActionRecord table
    if action_in.tx_id:
        action_record_obj = await ActionRecord.get_or_none(tx_id = action_in.tx_id) # use get_or_none

        if action_record_obj:
            return action_record_obj.action_id

    action_data_status = "1" if action_in.action_switch == 1 else "0"

    # search Action
    filter_q = Q(
        action_type=action_in.action_type,
        action_tokens=action_in.action_tokens,
        template=action_in.template,
        action_network_id=action_in.action_network_id,
    )
    if action_in.action_amount:
        filter_q = filter_q & Q(action_amount=action_in.action_amount)
    filter_q_next = Q(account_id=action_in.account_id if action_in.account_id else "") | Q(
        account_info=action_in.account_info if action_in.account_info else "")
    action_obj = await Action.filter(filter_q & filter_q_next).first()
    # if action_in.action_amount != "":
    #     action_obj = await Action.filter( Q(action_type=action_in.action_type) &
    #                                       Q(action_tokens=action_in.action_tokens) &
    #                                       Q(template=action_in.template) &
    #                                       Q(action_network_id=action_in.action_network_id) &
    #                                       Q(action_amount=action_in.action_amount) &
    #                                       (Q(account_id=action_in.account_id if action_in.account_id else "") | Q(account_info=action_in.account_info if action_in.account_info else ""))
    #                                     )
    # else:
    #     action_obj = await Action.filter( Q(action_type=action_in.action_type) &
    #                                       Q(action_tokens=action_in.action_tokens) &
    #                                       Q(template=action_in.template) &
    #                                       Q(action_network_id=action_in.action_network_id) &
    #                                       (Q(account_id=action_in.account_id if action_in.account_id else "") | Q(account_info=action_in.account_info if action_in.account_info else ""))
    #                                     )
    if action_obj:
        action_obj.count_number = action_obj.count_number + 1
        if action_in.action_switch == 1 or action_in.action_switch == "1":
            if action_obj.status == "0":
                action_obj.status = "1"  # update Status
        action_id = action_obj.action_id
        await action_obj.save()
    else:
        action_obj = Action()

        action_obj.action_title = action_in.action_title
        action_obj.action_type = action_in.action_type
        action_obj.action_tokens = action_in.action_tokens
        action_obj.action_amount = action_in.action_amount
        action_obj.account_id = action_in.account_id
        action_obj.account_info = action_in.account_info
        action_obj.template = action_in.template
        action_obj.status = action_data_status
        action_obj.count_number = 1
        action_obj.action_network_id = action_in.action_network_id
        action_obj.timestamp = timestamp
        action_obj.create_time = now_time
        await action_obj.save()

        action_obj = await Action.all().order_by("-timestamp").first()
        action_id = action_obj.action_id

    action_record = ActionRecord()

    action_record.action_id = action_id
    action_record.action_title = action_in.action_title
    action_record.action_type = action_in.action_type
    action_record.action_tokens = action_in.action_tokens
    action_record.action_amount = action_in.action_amount
    action_record.account_id = action_in.account_id
    action_record.account_info = action_in.account_info
    action_record.template = action_in.template
    action_record.status = action_data_status
    action_record.action_status = action_in.action_status
    action_record.tx_id = action_in.tx_id
    action_record.action_network_id = action_in.action_network_id
    action_record.gas = ""
    action_record.timestamp = timestamp
    action_record.create_time = now_time
    action_record.source = action_in.source
    action_record.chain_id = action_in.chain_id
    action_record.to_chain_id = action_in.to_chain_id
    action_record.dapp_id = dappId

    await action_record.save()

    return action_id


@router.get('/get-action-by-account', tags=['action'])
async def get_action_by_account(account_id: str = "", account_info: str = "", action_network_id: str = ""):
    if account_id == "" and account_info == "":
        return success()
    if is_w3_address(account_id):
        account_id = Web3.to_checksum_address(account_id)
    else:
        account_id = account_id.lower()
    sql = "select (ARRAY_AGG(action_id))[1] as action_id, (ARRAY_AGG(account_id))[1] as account_id,action_title," \
          "(ARRAY_AGG(timestamp))[1] as timestamp,(ARRAY_AGG(template))[1] as template, " \
          "(ARRAY_AGG(account_info))[1] as account_info, sum(count_number) as count_number from t_action " \
          "where status = '1' and action_network_id = '%s' and (account_id = '%s' or account_info = '%s') " \
          "group by action_title order by count_number desc" % (action_network_id, account_id, account_info)
    result_data = await Action.raw(sql)
    return success(result_data)


@router.get('/get-hot-action', tags=['action'])
async def get_hot_action(action_title: str = "", hot_number: int = 4, action_network_id: str = ""):
    sql = "select (ARRAY_AGG(account_id))[1] as account_id,action_title, (ARRAY_AGG(action_type))[1] as action_type," \
          "(ARRAY_AGG(action_tokens))[1] as action_tokens,(ARRAY_AGG(action_amount))[1] as action_amount," \
          "(ARRAY_AGG(account_info))[1] as account_info,(ARRAY_AGG(timestamp))[1] as timestamp," \
          "(ARRAY_AGG(template))[1] as template,sum(count_number) as count_number from t_action " \
          "where action_title like '%%%s%%' and action_network_id = '%s' group by action_title " \
          "order by count_number desc limit %s" % (action_title, action_network_id, hot_number)
    result_data = await Action.raw(sql)
    return success(result_data)


@router.delete('/delete-action-by-id', tags=['action'])
async def delete_action_by_id(delete_action: DeleteActionIn):
    action_data = await Action.filter(action_id=delete_action.action_id).first().values("action_title", "account_id", "action_network_id")
    update_data = {"action_title": action_data["action_title"], "account_id": action_data["account_id"], "action_network_id": action_data["action_network_id"]}
    await Action.filter(**update_data).update(status='0')
    return success(delete_action.action_id)


@router.delete('/batch-delete-action', tags=['action'])
async def batch_delete_action(delete_action: DeleteActionIn):
    for action_id in delete_action.action_id_list:
        action_data = await Action.filter(action_id=action_id).first().values("action_title", "account_id", "action_network_id")
        update_data = {"action_title": action_data["action_title"], "account_id": action_data["account_id"], "action_network_id": action_data["action_network_id"]}
        await Action.filter(**update_data).update(status='0')
    return success(delete_action.action_id_list)


@router.put('/update-action-by-id', tags=['action'])
async def update_action_by_id(update_action_record: UpdateActionRecordIn):
    update_data = {"id": update_action_record.action_record_id}
    await ActionRecord.filter(**update_data).update(action_status=update_action_record.action_status, tx_id=update_action_record.tx_id)
    return success(update_action_record.action_record_id)


@router.get('/get-action-records-by-account', tags=['action'], response_model=Page[ActionRecordResultOut])
async def get_action_records_by_account(action_network_id: str = "", account_id: str = "", account_info: str = "", action_type: str = "", template: str = "", action_status: str = ""):
    if is_w3_address(account_id):
        account_id = Web3.to_checksum_address(account_id)
    else:
        account_id = account_id.lower()
    account_q = Q(account_id=account_id) | Q(account_info=account_info)
    action_network_id_q = Q(action_network_id=action_network_id)
    action_type_q = Q()
    if action_type != "":
        if action_type == "Lending":
            action_type_q_1 = Q(action_type="Supply") | Q(action_type="Repay")
            action_type_q_2 = action_type_q_1 | Q(action_type="Borrow")
            action_type_q = action_type_q_2 | Q(action_type="Lending Withdraw")
        elif action_type == "Liquidity":
            action_type_q = Q(action_type="Deposit") | Q(action_type="Liquidity Withdraw")
        else:
            action_type_q = Q(action_type=action_type)
    template_q = Q()
    if template != "":
        template_q = Q(template=template)
    action_status_q = Q()
    if action_status != "":
        action_status_q = Q(action_status=action_status)
    return await paginate(ActionRecord.filter(account_q & action_network_id_q & action_type_q & template_q & action_status_q).order_by("-id"))


@router.get('/get-special-action', tags=['action'])
async def get_special_action():
    return success(query_special_action())


@router.get('/get-popular-actions-by-network', tags=['action'])
async def get_actions_by_network(network_id: int, page: int = 1, page_size: int = 4):
    total = await ActionChain.filter(network_id=network_id).annotate(count=Count("id")).first().values('count')
    data = await ActionChain.filter(network_id=network_id).order_by("-count").offset((page-1)*page_size).limit(page_size)
    return success({
        'data': data,
        'total_page':  math.ceil(total['count']/page_size)
    })


@router.get('/get-actions-by-dapp', tags=['action'])
async def get_action_by_dapp(dapp_id: int, page: int = 1, page_size: int = 4):
    total = await ActionRecord.filter(dapp_id=dapp_id).annotate(count=Count("id")).first().values('count')
    data = await ActionRecord.filter(dapp_id=dapp_id).order_by('-id').offset((page-1)*page_size).limit(page_size)
    return success({
        'data': data,
        'total_page': math.ceil(total['count'] / page_size)
    })