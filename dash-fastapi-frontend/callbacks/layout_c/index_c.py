import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
from jsonpath_ng import parse
from flask import json
from collections import OrderedDict

from server import app
import views
from utils.tree_tool import find_title_by_key, find_modules_by_key, find_href_by_key,  find_parents


@app.callback(
    [Output('tabs-container', 'items', allow_duplicate=True),
     Output('tabs-container', 'activeKey', allow_duplicate=True)],
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
    new_items = dash.Patch()

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

        for index, item in enumerate(origin_items):
            if {'key': '关闭右侧', 'label': '关闭右侧', 'icon': 'antd-arrow-right'} not in item['contextMenu']:
                item['contextMenu'].insert(-1, {
                    'key': '关闭右侧',
                    'label': '关闭右侧',
                    'icon': 'antd-arrow-right'
                })
            new_items[index]['contextMenu'] = item['contextMenu']
        context_menu = [
            {
                'key': '刷新页面',
                'label': '刷新页面',
                'icon': 'antd-reload'
            },
            {
                'key': '关闭当前',
                'label': '关闭当前',
                'icon': 'antd-close'
            },
            {
                'key': '关闭其他',
                'label': '关闭其他',
                'icon': 'antd-close-circle'
            },
            {
                'key': '全部关闭',
                'label': '全部关闭',
                'icon': 'antd-close-circle'
            }
        ]
        if len(origin_items) != 1:
            context_menu.insert(-1, {
                'key': '关闭左侧',
                'label': '关闭左侧',
                'icon': 'antd-arrow-left'
            })
        if menu_modules:
            if menu_modules == 'link':
                raise PreventUpdate
            else:
                # 否则追加子项返回
                # 其中若各标签页内元素类似，则推荐配合模式匹配构建交互逻辑
                new_items.append(
                    {
                        'label': menu_title,
                        'key': currentKey,
                        'children': eval('views.' + menu_modules + '.render(button_perms)'),
                        'contextMenu': context_menu
                    }
                )
        else:
            new_items.append(
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
                    'contextMenu': context_menu
                }
            )

        return [
            new_items,
            currentKey
        ]

    elif trigger_id == 'tabs-container':

        # 如果删除的是当前标签页则回到最后新增的标签页，否则保持当前标签页不变
        for index, item in enumerate(origin_items):
            if item['key'] == latestDeletePane:
                context_menu = [
                    {
                        'key': '刷新页面',
                        'label': '刷新页面',
                        'icon': 'antd-reload'
                    },
                    {
                        'key': '关闭其他',
                        'label': '关闭其他',
                        'icon': 'antd-close-circle'
                    },
                    {
                        'key': '全部关闭',
                        'label': '全部关闭',
                        'icon': 'antd-close-circle'
                    }
                ]
                if index == 1 and len(origin_items) == 2:
                    new_items[0]['contextMenu'] = context_menu
                elif len(origin_items) == 3:
                    context_menu.insert(1, {
                        'key': '关闭当前',
                        'label': '关闭当前',
                        'icon': 'antd-close'
                    })
                    if index == 1:
                        new_items[2]['contextMenu'] = context_menu
                    if index == 2:
                        new_items[1]['contextMenu'] = context_menu
                else:
                    if index == len(origin_items) - 1:
                        new_items[index - 1]['contextMenu'] = item['contextMenu']
                new_items.remove(item)
                break
        new_origin_items = [
            item for item in
            origin_items if item['key'] != latestDeletePane
        ]

        return [
            new_items,
            new_origin_items[-1]['key'] if activeKey == latestDeletePane else activeKey
        ]

    raise PreventUpdate


@app.callback(
    [Output('tabs-container', 'items', allow_duplicate=True),
     Output('tabs-container', 'activeKey', allow_duplicate=True),
     Output('trigger-reload-output', 'reload', allow_duplicate=True)],
    Input('tabs-container', 'clickedContextMenu'),
    [State('tabs-container', 'items'),
     State('tabs-container', 'activeKey')],
    prevent_initial_call=True
)
def handle_via_context_menu(clickedContextMenu, origin_items, activeKey):
    """
    基于标签页标题右键菜单的额外标签页控制
    """
    if clickedContextMenu['menuKey'] == '刷新页面':

        return [
            dash.no_update,
            dash.no_update,
            True
        ]

    if '关闭' in clickedContextMenu['menuKey']:
        new_items = dash.Patch()
        if clickedContextMenu['menuKey'] == '关闭当前':
            for index, item in enumerate(origin_items):
                if item['key'] == clickedContextMenu['tabKey']:
                    context_menu = [
                        {
                            'key': '刷新页面',
                            'label': '刷新页面',
                            'icon': 'antd-reload'
                        },
                        {
                            'key': '关闭其他',
                            'label': '关闭其他',
                            'icon': 'antd-close-circle'
                        },
                        {
                            'key': '全部关闭',
                            'label': '全部关闭',
                            'icon': 'antd-close-circle'
                        }
                    ]
                    if index == 1 and len(origin_items) == 2:
                        new_items[0]['contextMenu'] = context_menu
                    elif len(origin_items) == 3:
                        context_menu.insert(1, {
                            'key': '关闭当前',
                            'label': '关闭当前',
                            'icon': 'antd-close'
                        })
                        if index == 1:
                            new_items[2]['contextMenu'] = context_menu
                        if index == 2:
                            new_items[1]['contextMenu'] = context_menu
                    else:
                        if index == len(origin_items) - 1:
                            new_items[index - 1]['contextMenu'] = item['contextMenu']
                    new_items.remove(item)
                    break
            new_origin_items = [
                item for item in
                origin_items if item['key'] != clickedContextMenu['tabKey']
            ]

            return [
                new_items,
                new_origin_items[-1]['key'] if activeKey == clickedContextMenu['tabKey'] else activeKey,
                dash.no_update
            ]

        elif clickedContextMenu['menuKey'] == '关闭其他':
            for item in origin_items:
                if item['key'] != clickedContextMenu['tabKey'] and item['key'] != '首页':
                    new_items.remove(item)
            context_menu = [
                {
                    'key': '刷新页面',
                    'label': '刷新页面',
                    'icon': 'antd-reload'
                },
                {
                    'key': '关闭其他',
                    'label': '关闭其他',
                    'icon': 'antd-close-circle'
                },
                {
                    'key': '全部关闭',
                    'label': '全部关闭',
                    'icon': 'antd-close-circle'
                }
            ]
            if clickedContextMenu['tabKey'] == '首页':
                new_items[0]['contextMenu'] = context_menu
            else:
                context_menu.insert(1, {
                    'key': '关闭当前',
                    'label': '关闭当前',
                    'icon': 'antd-close'
                })
                new_items[1]['contextMenu'] = context_menu

            return [
                new_items,
                clickedContextMenu['tabKey'],
                dash.no_update
            ]

        elif clickedContextMenu['menuKey'] == '关闭左侧':
            current_index = 0
            for index, item in enumerate(origin_items):
                if item['key'] == clickedContextMenu['tabKey']:
                    current_index = index
                    item['contextMenu'].remove({
                        'key': '关闭左侧',
                        'label': '关闭左侧',
                        'icon': 'antd-arrow-left'
                    })
                    new_items[index]['contextMenu'] = item['contextMenu']
                    break
            for item in origin_items[1:current_index]:
                new_items.remove(item)

            return [
                new_items,
                clickedContextMenu['tabKey'],
                dash.no_update
            ]

        elif clickedContextMenu['menuKey'] == '关闭右侧':
            current_index = 0
            for index, item in enumerate(origin_items):
                if item['key'] == clickedContextMenu['tabKey']:
                    current_index = index
                    item['contextMenu'].remove({
                        'key': '关闭右侧',
                        'label': '关闭右侧',
                        'icon': 'antd-arrow-right'
                    })
                    new_items[index]['contextMenu'] = item['contextMenu']
                    break
            for item in origin_items[current_index+1:]:
                new_items.remove(item)

            return [
                new_items,
                clickedContextMenu['tabKey'],
                dash.no_update
            ]

        for item in origin_items:
            if item['key'] != '首页':
                new_items.remove(item)
        new_items[0]['contextMenu'] = [
            {
                'key': '刷新页面',
                'label': '刷新页面',
                'icon': 'antd-reload'
            },
            {
                'key': '关闭其他',
                'label': '关闭其他',
                'icon': 'antd-close-circle'
            },
            {
                'key': '全部关闭',
                'label': '全部关闭',
                'icon': 'antd-close-circle'
            }
        ]
        # 否则则为全部关闭
        return [
            new_items,
            '首页',
            dash.no_update
        ]

    raise PreventUpdate


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

    raise PreventUpdate
