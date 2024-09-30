import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import html
from api.system.user import UserApi
from utils.time_format_util import TimeFormatUtil
from . import reset_pwd, user_avatar, user_info


def render(*args, **kwargs):
    user_profile = UserApi.get_user_profile()

    return [
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdCard(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        user_avatar.render(
                                            user_profile.get('data').get(
                                                'avatar'
                                            )
                                        ),
                                        style={
                                            'textAlign': 'center',
                                            'marginBottom': '10px',
                                        },
                                    ),
                                    html.Ul(
                                        [
                                            html.Li(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-user'
                                                    ),
                                                    fac.AntdText('用户名称'),
                                                    html.Div(
                                                        user_profile.get(
                                                            'data'
                                                        ).get('user_name'),
                                                        id='profile_c-username',
                                                        className='pull-right',
                                                    ),
                                                ],
                                                className='list-group-item',
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-mobile'
                                                    ),
                                                    fac.AntdText('手机号码'),
                                                    html.Div(
                                                        user_profile.get(
                                                            'data'
                                                        ).get('phonenumber'),
                                                        id='profile_c-phonenumber',
                                                        className='pull-right',
                                                    ),
                                                ],
                                                className='list-group-item',
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-mail'
                                                    ),
                                                    fac.AntdText('用户邮箱'),
                                                    html.Div(
                                                        user_profile.get(
                                                            'data'
                                                        ).get('email'),
                                                        id='profile_c-email',
                                                        className='pull-right',
                                                    ),
                                                ],
                                                className='list-group-item',
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-cluster'
                                                    ),
                                                    fac.AntdText('所属部门'),
                                                    html.Div(
                                                        user_profile.get('data')
                                                        .get('dept')
                                                        .get('dept_name')
                                                        if user_profile.get(
                                                            'data'
                                                        ).get('dept')
                                                        else ''
                                                        + ' / '
                                                        + user_profile.get(
                                                            'post_group'
                                                        ),
                                                        id='profile_c-dept',
                                                        className='pull-right',
                                                    ),
                                                ],
                                                className='list-group-item',
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-team'
                                                    ),
                                                    fac.AntdText('所属角色'),
                                                    html.Div(
                                                        user_profile.get(
                                                            'role_group'
                                                        ),
                                                        id='profile_c-role',
                                                        className='pull-right',
                                                    ),
                                                ],
                                                className='list-group-item',
                                            ),
                                            html.Li(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-schedule'
                                                    ),
                                                    fac.AntdText('创建日期'),
                                                    html.Div(
                                                        TimeFormatUtil.format_time(
                                                            user_profile.get(
                                                                'data'
                                                            ).get('create_time')
                                                        ),
                                                        id='profile_c-create_time',
                                                        className='pull-right',
                                                    ),
                                                ],
                                                className='list-group-item',
                                            ),
                                        ],
                                        className='list-group list-group-striped',
                                    ),
                                    fuc.FefferyStyle(
                                        rawStyle="""
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
                                        """
                                    ),
                                ],
                                style={'width': '100%'},
                            ),
                        ],
                        title='个人信息',
                        size='small',
                        style={
                            'boxShadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px'
                        },
                    ),
                    span=10,
                ),
                fac.AntdCol(
                    fac.AntdCard(
                        [
                            fac.AntdTabs(
                                items=[
                                    {
                                        'key': '基本资料',
                                        'label': '基本资料',
                                        'children': user_info.render(
                                            nick_name=user_profile.get(
                                                'data'
                                            ).get('nick_name'),
                                            phonenumber=user_profile.get(
                                                'data'
                                            ).get('phonenumber'),
                                            email=user_profile.get('data').get(
                                                'email'
                                            ),
                                            sex=user_profile.get('data').get(
                                                'sex'
                                            ),
                                        ),
                                    },
                                    {
                                        'key': '修改密码',
                                        'label': '修改密码',
                                        'children': reset_pwd.render(),
                                    },
                                ],
                                style={'width': '100%'},
                            )
                        ],
                        'size="small"',
                        title='基本资料',
                        size='small',
                        style={
                            'boxShadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px'
                        },
                    ),
                    span=14,
                ),
            ],
            gutter=10,
        ),
    ]
