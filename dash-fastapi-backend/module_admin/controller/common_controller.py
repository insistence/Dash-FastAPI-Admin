from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Query, Request, status, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from module_admin.service.common_service import CommonService
from module_admin.service.login_service import LoginService
from utils.log_util import logger
from utils.response_util import ResponseUtil

commonController = APIRouter(prefix='/common', dependencies=[Depends(LoginService.get_current_user)])


@commonController.post('/upload')
async def common_upload(request: Request, file: UploadFile = File(...)):
    upload_result = await CommonService.upload_service(request, file)
    logger.info('上传成功')

    return ResponseUtil.success(model_content=upload_result.result)


@commonController.post('/uploadForEditor', dependencies=[Depends(LoginService.get_current_user)])
async def editor_upload(request: Request, base_url: str = Form(), file: UploadFile = File(...)):
    try:
        upload_result = await CommonService.upload_service(request, file)
        logger.info('上传成功')
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {
                    'errno': 0,
                    'data': {'url': f'{base_url}{upload_result.result.file_name}'},
                }
            ),
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {
                    'errno': 1,
                    'message': str(e),
                }
            ),
        )


@commonController.get('/download')
async def common_download(
    request: Request,
    background_tasks: BackgroundTasks,
    file_name: str = Query(alias='fileName'),
    delete: bool = Query(),
):
    download_result = await CommonService.download_services(background_tasks, file_name, delete)
    logger.info(download_result.message)

    return ResponseUtil.streaming(data=download_result.result)


@commonController.get('/download/resource')
async def common_download_resource(request: Request, resource: str = Query()):
    download_resource_result = await CommonService.download_resource_services(resource)
    logger.info(download_resource_result.message)

    return ResponseUtil.streaming(data=download_resource_result.result)
