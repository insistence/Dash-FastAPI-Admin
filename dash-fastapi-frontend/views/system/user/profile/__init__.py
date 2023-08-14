from dash import html
import feffery_utils_components as fuc
import feffery_antd_components as fac
from flask import session
from . import user_avatar, user_info, reset_pwd


def render(button_perms):

    return [
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdCard(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        user_avatar.render(),
                                        style={
                                            'textAlign': 'center',
                                            'marginBottom': '10px'
                                        }
                                    ),
                                    html.Ul(
                                        [
                                            html.Li(
                                                [
                                                    fac.AntdIcon(icon='antd-user'),
                                                    fac.AntdText('用户名称'),
                                                    html.Div(
                                                        session.get('user_info').get('user_name'),
                                                        id='profile_c-username',
                                                        className='pull-right'
                                                    )
                                                ],
                                                className='list-group-item'
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(icon='antd-mobile'),
                                                    fac.AntdText('手机号码'),
                                                    html.Div(
                                                        session.get('user_info').get('phonenumber'),
                                                        id='profile_c-phonenumber',
                                                        className='pull-right'
                                                    )
                                                ],
                                                className='list-group-item'
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(icon='antd-mail'),
                                                    fac.AntdText('用户邮箱'),
                                                    html.Div(
                                                        session.get('user_info').get('email'),
                                                        id='profile_c-email',
                                                        className='pull-right'
                                                    )
                                                ],
                                                className='list-group-item'
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(icon='antd-cluster'),
                                                    fac.AntdText('所属部门'),
                                                    html.Div(
                                                        session.get('dept_info').get('dept_name') + "/" + ','.join(
                                                            [item.get('post_name') for item in
                                                             session.get('post_info')]),
                                                        id='profile_c-dept',
                                                        className='pull-right'
                                                    )
                                                ],
                                                className='list-group-item'
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(icon='antd-team'),
                                                    fac.AntdText('所属角色'),
                                                    html.Div(
                                                        ','.join([item.get('role_name') for item in
                                                                  session.get('role_info')]),
                                                        id='profile_c-role',
                                                        className='pull-right'
                                                    )
                                                ],
                                                className='list-group-item'
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(icon='antd-schedule'),
                                                    fac.AntdText('创建日期'),
                                                    html.Div(
                                                        session.get('user_info').get('create_time'),
                                                        id='profile_c-create_time',
                                                        className='pull-right'
                                                    )
                                                ],
                                                className='list-group-item'
                                            ),
                                        ],
                                        className='list-group list-group-striped'
                                    ),
                                    fuc.FefferyStyle(
                                        rawStyle=
                                        '''
                                        .list-group-striped > .list-group-item {
                                            border-left: 0;
                                            border-right: 0;
                                            border-radius: 0;
                                            padding-left: 0;
                                            padding-right: 0;
                                        }
                                        
                                        .list-group {
                                            padding-left: 0px;
                                            list-style: none;
                                        }
                                        
                                        .list-group-item {
                                            border-bottom: 1px solid #e7eaec;
                                            border-top: 1px solid #e7eaec;
                                            margin-bottom: -1px;
                                            padding: 11px 0px;
                                            font-size: 13px;
                                        }
                                        
                                        .pull-right {
                                            float: right !important;
                                        }                    
                                        '''
                                    )
                                ],
                                style={
                                    'width': '100%'
                                }
                            ),
                        ],
                        title='个人信息',
                        size='small',
                        style={
                            'boxShadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px'
                        }
                    ),
                    span=10
                ),
                fac.AntdCol(
                    fac.AntdCard(
                        [
                            fac.AntdTabs(
                                items=[
                                    {
                                        'key': '基本资料',
                                        'label': '基本资料',
                                        'children': user_info.render()
                                    },
                                    {
                                        'key': '修改密码',
                                        'label': '修改密码',
                                        'children': reset_pwd.render()
                                    }
                                ],
                                style={
                                    'width': '100%'
                                }
                            )
                        ],
                        'size="small"',
                        title='基本资料',
                        size='small',
                        style={
                            'boxShadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px'
                        }
                    ),
                    span=14
                ),
            ],
            gutter=10
        ),
    ]
