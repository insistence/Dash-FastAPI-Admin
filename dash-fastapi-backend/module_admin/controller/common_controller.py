from fastapi import APIRouter, Request
from fastapi import Depends, UploadFile, File, Form
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


@commonController.post("/uploadForEditor", dependencies=[Depends(get_current_user), Depends(CheckUserInterfaceAuth('common'))])
async def editor_upload(request: Request, uploadId: str = Form(), file: UploadFile = File(...)):
    try:
        try:
            os.makedirs(os.path.join(CachePathConfig.PATH, uploadId))
        except FileExistsError:
            pass
        upload_service(CachePathConfig.PATH, uploadId, file)
        logger.info('上传成功')
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {
                    'errno': 0,
                    'data': {
                        'url': f'{request.base_url}common/{CachePathConfig.PATHSTR}?taskId={uploadId}&filename={file.filename}'
                    },
                }
            )
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                {
                    'errno': 1,
                    'message': str(e),
                }
            )
        )


@commonController.get(f"/{CachePathConfig.PATHSTR}")
def common_download(request: Request, taskId: str, filename: str):
    try:
        def generate_file():
            with open(os.path.join(CachePathConfig.PATH, taskId, filename), 'rb') as response_file:
                yield from response_file
        logger.info('获取成功')
        return streaming_response_200(data=generate_file())
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
