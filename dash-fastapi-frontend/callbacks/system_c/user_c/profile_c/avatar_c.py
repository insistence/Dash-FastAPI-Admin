import dash
import feffery_utils_components as fuc
import time
import uuid
from dash.dependencies import Input, Output, State
from server import app

from api.user import change_user_avatar_api


@app.callback(
    [Output('avatar-cropper-modal', 'visible', allow_duplicate=True),
     Output('avatar-src-data', 'data', allow_duplicate=True)],
    Input('avatar-edit-click', 'n_clicks'),
    State('user-avatar-image-info', 'src'),
    prevent_initial_call=True
)
def avatar_cropper_modal_visible(n_clicks, user_avatar_image_info):
    if n_clicks:
        return [True, user_avatar_image_info]

    return dash.no_update, dash.no_update


@app.callback(
    Output('avatar-src-data', 'data', allow_duplicate=True),
    Input('avatar-upload-choose', 'listUploadTaskRecord'),
    prevent_initial_call=True
)
def upload_user_avatar(list_upload_task_record):
    if list_upload_task_record:

        return list_upload_task_record[-1].get('url')

    return dash.no_update


@app.callback(
    Output('avatar-cropper', 'jsString'),
    Input('avatar-src-data', 'data'),
    prevent_initial_call=True
)
def edit_user_avatar(src_data):

    return """
            // 创建新图像元素
            var newImage = document.createElement('img');
            newImage.id = 'user-avatar-image';
            newImage.src = '% s';
            newImage.onload = function() {
                // 删除旧图像元素
                var oldImage = document.getElementById('user-avatar-image');
                oldImage.parentNode.removeChild(oldImage);
                // 销毁旧的 Cropper.js 实例
                var oldCropper = oldImage.cropper;
                if (oldCropper) {
                    oldCropper.destroy();
                }
                // 将新图像添加到页面中
                var container = document.getElementById('avatar-cropper-container');
                container.appendChild(newImage);
                // var image = document.getElementById('user-avatar-image');
                var previewImage = document.getElementById('user-avatar-image-preview');
                // 创建新的 Cropper 实例
                var cropper = new Cropper(newImage, {
                  viewMode: 1,
                  dragMode: 'none',
                  initialAspectRatio: 1,
                  aspectRatio: 1,
                  preview: previewImage,
                  background: true,
                  autoCropArea: 0.6,
                  zoomOnWheel: true,
                  crop: function(event) {
                    // 当裁剪框的位置或尺寸发生改变时触发的回调函数
                    console.log(event.detail.x);
                    console.log(event.detail.y);
                    console.log(event.detail.width);
                    console.log(event.detail.height);
                    console.log(event.detail.rotate);
                    console.log(event.detail.scaleX);
                    console.log(event.detail.scaleY);
                    // 当需要获取裁剪后的数据时
                    var croppedDataUrl = cropper.getCroppedCanvas().toDataURL("image/jpeg", 1);
                    sessionStorage.setItem('cropper-avatar-base64', JSON.stringify({avatarBase64: croppedDataUrl}))
                  }
                });
                // 获取旋转按钮的引用
                var rotateLeftButton = document.getElementById('rotate-left');
                var rotateRightButton = document.getElementById('rotate-right');

                // 添加点击事件监听器
                rotateLeftButton.addEventListener('click', function() {
                  // 向左旋转图像90度
                  cropper.rotate(-90);
                });
                rotateRightButton.addEventListener('click', function() {
                  // 向右旋转图像90度
                  cropper.rotate(90);
                });
                // 获取缩小按钮和放大按钮的引用
                var zoomOutButton = document.getElementById('zoom-out');
                var zoomInButton = document.getElementById('zoom-in');

                // 添加点击事件监听器
                zoomOutButton.addEventListener('click', function() {
                  // 放大图像
                  cropper.zoom(0.1);
                });

                zoomInButton.addEventListener('click', function() {
                  // 缩小图像
                  cropper.zoom(-0.1);
                });
            }
        """ % src_data


@app.callback(
    [Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True),
     Output('avatar-cropper-modal', 'visible', allow_duplicate=True),
     Output('user-avatar-image-info', 'key'),
     Output('avatar-info', 'key')],
    Input('change-avatar-submit', 'nClicks'),
    State('cropper-avatar-base64', 'data'),
    prevent_initial_call=True
)
def change_user_avatar_callback(submit_click, avatar_data):

    if submit_click:
        params = dict(type='avatar', avatar=avatar_data['avatarBase64'])
        change_avatar_result = change_user_avatar_api(params)
        if change_avatar_result.get('code') == 200:

            return [
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('修改成功', type='success'),
                False,
                str(uuid.uuid4()),
                str(uuid.uuid4())
            ]

        return [
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('修改失败', type='error'),
            dash.no_update,
            dash.no_update,
            dash.no_update
        ]

    return [dash.no_update] * 5
