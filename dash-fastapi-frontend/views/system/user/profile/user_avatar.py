from dash import html, dcc
import feffery_utils_components as fuc
import feffery_antd_components as fac
from flask import session

from config.global_config import ApiBaseUrlConfig
import callbacks.system_c.user_c.profile_c.avatar_c


def render():
    return [
        html.Div(
            [
                fac.AntdImage(
                    id='user-avatar-image-info',
                    src=f"{ApiBaseUrlConfig.BaseUrl}{session.get('user_info').get('avatar')}&token={session.get('Authorization')}",
                    preview=False,
                    height='120px',
                    width='120px',
                    style={
                        'borderRadius': '50%'
                    }
                )
            ],
            id='avatar-edit-click',
            className='user-info-head'
        ),
        fuc.FefferyStyle(
            rawStyle='''
            .user-info-head {
              position: relative;
              display: inline-block;
              height: 120px;
            }

            .user-info-head:hover:after {
              content: '+';
              position: absolute;
              left: 0;
              right: 0;
              top: 0;
              bottom: 0;
              color: #eee;
              background: rgba(0, 0, 0, 0.5);
              font-size: 24px;
              font-style: normal;
              -webkit-font-smoothing: antialiased;
              -moz-osx-font-smoothing: grayscale;
              cursor: pointer;
              line-height: 110px;
              border-radius: 50%;
            }
            '''
        ),
        fac.AntdModal(
            [
                fac.AntdRow(
                    [
                        fac.AntdCol(
                            [
                                html.Div(
                                    [

                                        fuc.FefferyImageCropper(
                                            id='avatar-cropper',
                                            alt='avatar',
                                            aspectRatio=1,
                                            dragMode='move',
                                            cropBoxMovable=False,
                                            cropBoxResizable=False,
                                            wheelZoomRatio=0.01,
                                            preview='#user-avatar-image-preview',
                                            style={
                                                'width': '100%',
                                                'height': '100%'
                                            }
                                        )
                                    ],
                                    id='avatar-cropper-container',
                                    style={
                                        'height': '350px',
                                        'width': '100%'
                                    }
                                ),
                            ],
                            span=12
                        ),
                        fac.AntdCol(
                            [
                                html.Div(
                                    id='user-avatar-image-preview',
                                    className='avatar-upload-preview'
                                ),
                                fuc.FefferyStyle(
                                    rawStyle="""
                                    .avatar-upload-preview {
                                        margin: 18% auto;
                                        width: 220px;
                                        height: 220px;
                                        border-radius: 50%;
                                        box-shadow: 0 0 4px #ccc;
                                        overflow: hidden;
                                    }
                                    """
                                )
                            ],
                            span=12
                        )
                    ]
                ),
                html.Br(),
                fac.AntdRow(
                    [
                        fac.AntdCol(
                            fac.AntdUpload(
                                id='avatar-upload-choose',
                                apiUrl=f'{ApiBaseUrlConfig.BaseUrl}/common/upload',
                                apiUrlExtraParams={'taskPath': 'avatarUpload'},
                                downloadUrl=f"{ApiBaseUrlConfig.BaseUrl}/common/caches",
                                downloadUrlExtraParams={'taskPath': 'avatarUpload', 'token': session.get('Authorization')},
                                headers={'Authorization': 'Bearer ' + session.get('Authorization')},
                                fileMaxSize=10,
                                showUploadList=False,
                                fileTypes=['jpeg', 'jpg', 'png'],
                                buttonContent='选择'
                            ),
                            span=4
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                id='zoom-out',
                                icon=fac.AntdIcon(
                                    icon='antd-plus'
                                )
                            ),
                            span=2
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                id='zoom-in',
                                icon=fac.AntdIcon(
                                    icon='antd-minus'
                                )
                            ),
                            span=2
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                icon=fac.AntdIcon(
                                    id='rotate-left',
                                    icon='antd-undo'
                                )
                            ),
                            span=2
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                icon=fac.AntdIcon(
                                    id='rotate-right',
                                    icon='antd-redo'
                                )
                            ),
                            span=7
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                '提交',
                                id='change-avatar-submit',
                                type='primary'
                            ),
                            span=7
                        ),
                    ],
                    gutter=10
                )
            ],
            id='avatar-cropper-modal',
            title='修改头像',
            width=850,
            mask=False
        )
    ]
