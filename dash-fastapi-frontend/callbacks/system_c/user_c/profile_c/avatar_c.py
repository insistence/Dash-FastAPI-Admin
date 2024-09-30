import base64
import uuid
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from io import BytesIO
from api.system.user import UserApi
from server import app
from utils.feedback_util import MessageManager


@app.callback(
    [
        Output('avatar-cropper-modal', 'visible', allow_duplicate=True),
        Output('avatar-cropper', 'src', allow_duplicate=True),
    ],
    Input('avatar-edit-click', 'n_clicks'),
    State('user-avatar-image-info', 'src'),
    prevent_initial_call=True,
)
def avatar_cropper_modal_visible(n_clicks, user_avatar_image_info):
    """
    显示编辑头像弹窗回调
    """
    if n_clicks:
        return [True, user_avatar_image_info]

    raise PreventUpdate


@app.callback(
    Output('avatar-cropper', 'src', allow_duplicate=True),
    Input('avatar-upload-choose', 'contents'),
    prevent_initial_call=True,
)
def upload_user_avatar(contents):
    """
    上传用户头像获取后端url回调
    """
    if contents:
        return contents

    raise PreventUpdate


# 头像放大、缩小、逆时针旋转、顺时针旋转操作浏览器端回调
app.clientside_callback(
    """
    (zoomOut, zoomIn, rotateLeft, rotateRight) => {
            triggered_id = window.dash_clientside.callback_context.triggered[0].prop_id;
            if (triggered_id == 'zoom-out.nClicks') {
                return [{isZoom: true, ratio: 0.1}, window.dash_clientside.no_update];
            }
            else if (triggered_id == 'zoom-in.nClicks') {
                return [{isZoom: true, ratio: -0.1}, window.dash_clientside.no_update];
            }
            else if (triggered_id == 'rotate-left.nClicks') {
                return [window.dash_clientside.no_update, {isRotate: true, degree: -90}];
            }
            else if (triggered_id == 'rotate-right.nClicks') {
                return [window.dash_clientside.no_update, {isRotate: true, degree: 90}];
            }
            else {
                throw window.dash_clientside.PreventUpdate;
            }
        }
    """,
    [Output('avatar-cropper', 'zoom'), Output('avatar-cropper', 'rotate')],
    [
        Input('zoom-out', 'nClicks'),
        Input('zoom-in', 'nClicks'),
        Input('rotate-left', 'nClicks'),
        Input('rotate-right', 'nClicks'),
    ],
    prevent_initial_call=True,
)


@app.callback(
    [
        Output('avatar-cropper-modal', 'visible', allow_duplicate=True),
        Output('user-avatar-image-info', 'key'),
        Output('avatar-info', 'key'),
    ],
    Input('change-avatar-submit', 'nClicks'),
    State('avatar-cropper', 'croppedImageData'),
    running=[[Output('change-avatar-submit', 'loading'), True, False]],
    prevent_initial_call=True,
)
def change_user_avatar_callback(submit_click, avatar_data):
    """
    提交编辑完成头像数据回调，实现更新头像操作
    """

    if submit_click:
        params = dict(
            avatarfile=BytesIO(base64.b64decode(avatar_data.split(',', 1)[1]))
        )
        UserApi.upload_avatar(params)
        MessageManager.success(content='修改成功')

        return [
            False,
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        ]

    raise PreventUpdate
