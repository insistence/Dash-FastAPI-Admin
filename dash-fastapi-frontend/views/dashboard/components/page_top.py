import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import html
from config.env import ApiConfig
from utils.cache_util import CacheManager


def render_page_top():
    return html.Div(
        [
            html.Div(
                fac.AntdAvatar(
                    id='dashboard-avatar-info',
                    mode='image',
                    src=f"{ApiConfig.BaseUrl}{CacheManager.get('user_info').get('avatar')}"
                    if CacheManager.get('user_info').get('avatar')
                    else '/assets/imgs/profile.jpg',
                    size='large',
                ),
                className='avatar',
            ),
            html.Div(
                [
                    html.Div(
                        fac.AntdText(
                            f"早安，{CacheManager.get('user_info').get('nick_name')}，祝你开心每一天！"
                        ),
                        className='content-title',
                    ),
                    html.Div(
                        '交互专家 |蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED'
                    ),
                ],
                className='content',
            ),
            html.Div(
                [
                    html.Div(
                        fac.AntdStatistic(title='项目数', value=56),
                        className='stat-item',
                    ),
                    html.Div(
                        fac.AntdStatistic(
                            title='团队内排名', value=8, suffix='/ 24'
                        ),
                        className='stat-item',
                    ),
                    html.Div(
                        fac.AntdStatistic(title='项目访问', value=2223),
                        className='stat-item',
                    ),
                ],
                className='extra-content',
            ),
            fuc.FefferyStyle(
                rawStyle="""
                    .page-header-content {
                        display: flex;
                    }

                    .page-header-content .avatar {
                        flex: 0 1 72px;
                    }

                    .page-header-content .avatar > span {
                        display: block;
                        width: 72px;
                        height: 72px;
                        border-radius: 72px;
                    }

                    .page-header-content .content {
                        position: relative;
                        top: 4px;
                        margin-left: 24px;
                        line-height: 22px;
                        color: rgba(0,0,0,.45);
                        flex: 1 1 auto;
                    }

                    .page-header-content .content .content-title {
                        margin-bottom: 12px;
                        font-size: 20px;
                        font-weight: 500;
                        line-height: 28px;
                        color: rgba(0,0,0,.85);
                    }

                    .extra-content {
                        float: right;
                        white-space: nowrap;
                    }

                    .extra-content .stat-item {
                        position: relative;
                        display: inline-block;
                        padding: 0 32px;
                    }

                    .extra-content .stat-item > p:first-child {
                        margin-bottom: 4px;
                        font-size: 14px;
                        line-height: 22px;
                        color: rgba(0,0,0,.45);
                    }

                    .extra-content .stat-item > p {
                        margin: 0;
                        font-size: 30px;
                        line-height: 38px;
                        color: rgba(0,0,0,.85);
                    }

                    .extra-content .stat-item > p > span {
                        font-size: 20px;
                        color: rgba(0,0,0,.45);
                    }

                    .extra-content .stat-item::after {
                        position: absolute;
                        top: 8px;
                        right: 0;
                        width: 1px;
                        height: 40px;
                        background-color: #e8e8e8;
                        content: '';
                    }

                    .extra-content .stat-item:last-child {
                        padding-right: 0;
                    }

                    .extra-content .stat-item:last-child::after {
                        display: none;
                    }
                    """
            ),
        ],
        className='page-header-content',
        style={
            'padding': '12px',
            'marginBottom': '24px',
            'boxShadow': 'rgba(0, 0, 0, 0.1) 0px 4px 12px',
        },
    )
