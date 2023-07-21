from fastapi import APIRouter, Request
from fastapi import Depends, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from config.env import CachePathConfig
from module_admin.service.login_service import get_current_user
from module_admin.service.common_service import *
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth


commonController = APIRouter()


@commonController.post("/upload", dependencies=[Depends(get_current_user), Depends(CheckUserInterfaceAuth('common'))])
async def common_upload(request: Request, uploadId: str = Form(), file: UploadFile = File(...)):
    try:
        try:
            os.makedirs(os.path.join(CachePathConfig.PATH, uploadId))
        except FileExistsError:
            pass
        upload_service(CachePathConfig.PATH, uploadId, file)
        logger.info('上传成功')
        return response_200(data={'filename': file.filename}, message="上传成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@commonController.get(f"/{CachePathConfig.PATHSTR}")
def common_download(request: Request, taskId: str, filename: str):
    try:
        def generate_file():
            with open(os.path.join(CachePathConfig.PATH, taskId, filename), 'rb') as response_file:
                yield from response_file
        logger.info('获取成功')
        return StreamingResponse(generate_file())
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
