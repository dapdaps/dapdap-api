# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py
from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from apps.action.models import Action, ActionRecord
from fastapi_pagination import Page, add_pagination, paginate
from apps.action.schemas import ActionIn, DeleteActionIn, UpdateActionRecordIn, ActionRecordResultOut
from core.utils.base_util import get_limiter
import logging
import datetime
from tortoise.expressions import Q
from core.utils.tool_util import success, error
from tortoise.functions import Sum, Count
from fastapi_pagination.ext.tortoise import paginate
from core.base.db_provider import query_special_action

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/action")


@router.post('/add', tags=['action'])
async def add_action(request: Request, action_in: ActionIn):
    now_time = datetime.datetime.utcnow()
    timestamp = int(now_time.timestamp())

    # search ActionRecord table
    if action_in.tx_id:
        action_record_obj = await ActionRecord.get_or_none(tx_id = action_in.tx_id) # use get_or_none

        if action_record_obj:
            return action_record_obj.action_id
        else:
            raise HTTPException(400, f"this tx_id {action_in.tx_id} not exist")

    action_data_status = "1" if action_in.action_switch == 1 else "0"

    # search Action
    filter_q = Q(
        action_type=action_in.action_type,
        action_tokens=action_in.action_tokens,
        template=action_in.template,
        action_network_id=action_in.action_network_id,
    )
    if action_in.action_amount:
        filter_q.filters.update({"action_amount" : action_in.action_amount})
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
        
        action_obj = Action.all().order_by("-timestamp").first()
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

    await action_record.save()

    return action_id


@router.get('/get-action-by-account', tags=['get_action_by_account'])
async def get_action_by_account(account_id: str = "", account_info: str = "", action_network_id: str = ""):
    if account_id == "" and account_info == "":
        return success()
    filter_q = Q(account_id=account_id) | Q(account_info=account_info)
    filter_q_next = Q(action_network_id=action_network_id)
    result_data = await Action.filter(filter_q & filter_q_next).annotate(count_number=Sum("count_number")).group_by("action_title").order_by("-count_number").values("action_title", "count_number")
    return success(result_data)


@router.get('/get-hot-action', tags=['get_hot_action'])
async def get_hot_action(action_title: str = "", hot_number: int = 4, action_network_id: str = ""):
    filters = {"action_title": action_title}
    if action_network_id != "":
        filters.update({"action_network_id": action_network_id})
    result_data = await Action.filter(**filters).annotate(count_number=Sum("count_number")).group_by("action_title").order_by("-count_number").limit(hot_number).values("action_title", "count_number")
    return success(result_data)


@router.delete('/delete-action-by-id', tags=['delete_action_by_id'])
async def delete_action_by_id(delete_action: DeleteActionIn):
    action_data = await Action.filter(action_id=delete_action.action_id).first().values("action_title", "account_id", "action_network_id")
    update_data = {"action_title": action_data["action_title"], "account_id": action_data["account_id"], "action_network_id": action_data["action_network_id"]}
    await Action.filter(**update_data).update(status='0')
    return success(delete_action.action_id)


@router.delete('/batch-delete-action', tags=['batch_delete_action'])
async def batch_delete_action(delete_action: DeleteActionIn):
    for action_id in delete_action.action_id_list:
        action_data = await Action.filter(action_id=action_id).first().values("action_title", "account_id", "action_network_id")
        update_data = {"action_title": action_data["action_title"], "account_id": action_data["account_id"], "action_network_id": action_data["action_network_id"]}
        await Action.filter(**update_data).update(status='0')
    return success(delete_action.action_id_list)


@router.put('/update-action-by-id', tags=['update_action_by_id'])
async def update_action_by_id(update_action_record: UpdateActionRecordIn):
    update_data = {"id": update_action_record.action_record_id}
    await ActionRecord.filter(**update_data).update(action_status=update_action_record.action_status, tx_id=update_action_record.tx_id)
    return success(update_action_record.action_record_id)


@router.get('/get-action-records-by-account', tags=['get_action_records_by_account'], response_model=Page[ActionRecordResultOut])
async def get_action_records_by_account(action_network_id: str = "", account_id: str = "", account_info: str = "", action_type: str = "", template: str = "", action_status: str = ""):
    filters = {"action_network_id": action_network_id}
    if account_id != "":
        filters.update({"account_id": account_id})
    if account_info != "":
        filters.update({"account_info": account_info})
    if action_type != "":
        filters.update({"action_type": action_type})
    if template != "":
        filters.update({"template": template})
    if action_status != "":
        filters.update({"action_status": action_status})
    return await paginate(ActionRecord.filter(**filters).order_by("-id"))


@router.get('/get-special-action', tags=['get_special_action'])
async def get_special_action():
    return success(query_special_action())

