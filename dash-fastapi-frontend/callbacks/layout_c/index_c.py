import dash
from dash import html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc
from jsonpath_ng import parse
from flask import session, json
from collections import OrderedDict

from server import app
import views
from utils.tree_tool import find_title_by_key, find_modules_by_key, find_href_by_key,  find_parents


@app.callback(
    [Output('tabs-container', 'items'),
     Output('tabs-container', 'activeKey')],
    [Input('index-side-menu', 'currentKey'),
     Input('tabs-container', 'latestDeletePane')],
    [State('tabs-container', 'items'),
     State('tabs-container', 'activeKey'),
     State('menu-info-store-container', 'data'),
     State('menu-list-store-container', 'data')],
    prevent_initial_call=True
)
def handle_tab_switch_and_create(currentKey, latestDeletePane, origin_items, activeKey, menu_info, menu_list):
    """
    这个回调函数用于处理标签页子项的新建、切换及删除
    具体策略：
        1.当左侧某个菜单项被新选中，且右侧标签页子项尚未包含此项时，新建并切换
        2.当左侧某个菜单项被新选中，且右侧标签页子项已包含此项时，切换
        3.当右侧标签页子项某项被删除时，销毁对应标签页的同时切换回主标签页
    """

    trigger_id = dash.ctx.triggered_id

    # 基于jsonpath对各标签页子项中所有已有记录的nClicks参数重置为None
    # 以避免每次新的items返回给标签页重新渲染后，
    # 先前已更新为非None的按钮的nClicks误触发通知弹出回调
    parser = parse('$..nClicks')
    origin_items = parser.update(origin_items, None)

    if trigger_id == 'index-side-menu':

        # 判断当前新选中的菜单栏项对应标签页是否已创建
        if currentKey in [item['key'] for item in origin_items]:
            return [
                dash.no_update,
                currentKey
            ]

        if currentKey == '个人资料':
            menu_title = '个人资料'
            button_perms = []
            menu_modules = 'system.user.profile'
        else:
            menu_title = find_title_by_key(menu_info.get('menu_info'), currentKey)
            button_perms = [item.get('perms') for item in menu_list.get('menu_list') if str(item.get('parent_id')) == currentKey]
            # 判断当前选中的菜单栏项是否存在module，如果有，则动态导入module，否则返回404页面
            menu_modules = find_modules_by_key(menu_info.get('menu_info'), currentKey)

        if menu_modules:
            if menu_modules == 'link':
                return [dash.no_update] * 2
            else:
                # 否则追加子项返回
                # 其中若各标签页内元素类似，则推荐配合模式匹配构建交互逻辑
                return [
                    [
                        *origin_items,
                        {
                            'label': menu_title,
                            'key': currentKey,
                            'children': eval('views.' + menu_modules + '.render(button_perms)'),
                        }
                    ],
                    currentKey
                ]

        return [
            [
                *origin_items,
                {
                    'label': menu_title,
                    'key': currentKey,
                    'children': fac.AntdResult(
                        status='404',
                        title='页面不存在',
                        subTitle='请先配置该路由的页面',
                        style={
                            'paddingBottom': 0,
                            'paddingTop': 0
                        }
                    ),
                }
            ],
            currentKey
        ]

    elif trigger_id == 'tabs-container':

        # 若要删除的是当前正激活的标签页
        if latestDeletePane == activeKey:
            return [
                [
                    item
                    for item in origin_items
                    if item['key'] != latestDeletePane
                ],
                '首页'
            ]

        # 否则保持当前激活的标签页子项不变，删去目标子项
        return [
            [
                item
                for item in origin_items
                if item['key'] != latestDeletePane
            ],
            dash.no_update
        ]


# 页首面包屑和hash回调
@app.callback(
    [Output('header-breadcrumb', 'items'),
     Output('dcc-url', 'pathname', allow_duplicate=True)],
    Input('tabs-container', 'activeKey'),
    State('menu-info-store-container', 'data'),
    prevent_initial_call=True
)
def get_current_breadcrumbs(active_key, menu_info):
    if active_key:

        if active_key == '首页':
            return [
                [
                    {
                        'title': '首页',
                        'icon': 'antd-dashboard',
                        'href': '/'
                    },
                ],
                '/'
            ]

        elif active_key == '个人资料':
            return [
                [
                    {
                        'title': '首页',
                        'icon': 'antd-dashboard',
                        'href': '/'
                    },
                    {
                        'title': '个人资料',
                    }
                ],
                '/user/profile'
            ]

        else:
            result = find_parents(menu_info.get('menu_info'), active_key)
            # 去除result的重复项
            parent_info = list(OrderedDict((json.dumps(d, ensure_ascii=False), d) for d in result).values())
            if parent_info:
                current_href = find_href_by_key(menu_info.get('menu_info'), active_key)

                return [
                    [
                        {
                            'title': '首页',
                            'icon': 'antd-dashboard',
                            'href': '/'
                        },
                    ] + parent_info,
                    current_href
                ]

    return dash.no_update
