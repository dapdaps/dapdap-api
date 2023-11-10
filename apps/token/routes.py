from starlette.requests import Request
from fastapi import APIRouter, Depends, File, Form, UploadFile

from apps.token.models import Token
from apps.token.schemas import AddTokenIn
from core.auth.utils import get_current_user
from core.utils.base_util import get_limiter
import logging
from core.utils.tool_util import success,error
from typing import Annotated
import boto3
from settings.config import settings
from botocore.exceptions import ClientError
from web3 import Web3
from apps.invite.utils import is_w3_address


logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/token")


@router.post('/upload', tags=['token'], dependencies=[Depends(get_current_user)])
@limiter.limit('100/minute')
async def upload_icon(request: Request, file: Annotated[UploadFile, File()], address: Annotated[str, Form()]):
    contentType = file.content_type.lower()
    if contentType != 'image/png' and contentType != 'image/jpg' and contentType != 'image/jpeg':
        return error("image type only support png|jpg|jpeg")
    if not is_w3_address(address):
        return error("address is not web3")
    web3_address = Web3.to_checksum_address(address)
    filename = web3_address.lower()+".png"
    try:
        s3 = boto3.client('s3', region_name=settings.AWS_REGION_NAME, aws_access_key_id=settings.AWS_S3_AKI, aws_secret_access_key=settings.AWS_S3_SAK)
        s3.upload_fileobj(file.file, settings.AWS_BUCKET_NAME, "images/"+filename)
    except Exception as e:
        logger.error(f'upload token icon error: {e}')
        return error("error upload")
    return success({
        "url": settings.AWS_PATH+filename
    })

@router.post('/', tags=['token'], dependencies=[Depends(get_current_user)])
@limiter.limit('100/minute')
async def add_token(request: Request, token_in: AddTokenIn):
    if token_in.decimal < 0:
        return error("illegal decimals")
    if token_in.chain_id <= 0:
        return error("illegal chain_id")
    if not is_w3_address(token_in.address):
        return error("address is not web3")
    web3_address = Web3.to_checksum_address(token_in.address)
    hasAdd = await Token.filter(address=web3_address).exists()
    if hasAdd:
        return error("token already exist")
    await Token(
        address=web3_address,
        symbol=token_in.symbol,
        name=token_in.name,
        decimal=token_in.decimal,
        icon=token_in.icon
    ).save()
    return success()

@router.get('/', tags=['token'])
@limiter.limit('100/minute')
async def get_token(request: Request, address:str):
    token = await Token.filter(address=address)
    if len(token) > 0:
        return success(token[0])
    return success()

