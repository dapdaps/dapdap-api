# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py
from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from apps.action.models import Action, ActionRecord
from apps.action.schemas import ActionIn
from core.utils.base_util import get_limiter
from settings.config import settings
import logging
import datetime
from tortoise.expressions import Q

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
        action_id =  action_obj.action_id
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
        action_id =  action_obj.action_id


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
