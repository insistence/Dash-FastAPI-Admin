import dash
import importlib
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac
from jsonpath_ng import parse

from server import app
import views  # noqa: F401
from utils.cache_util import CacheManager
from utils.tree_tool import find_href_by_key


@app.callback(
    [
        Output('tabs-container', 'items', allow_duplicate=True),
        Output('tabs-container', 'activeKey', allow_duplicate=True),
        Output('header-breadcrumb', 'items'),
    ],
    [
        Input('index-side-menu', 'currentKey'),
        Input('tabs-container', 'tabCloseCounts'),
    ],
    [
        State('index-side-menu', 'currentItem'),
        State('index-side-menu', 'currentItemPath'),
        State('tabs-container', 'latestDeletePane'),
        State('tabs-container', 'items'),
        State('tabs-container', 'activeKey'),
    ],
    prevent_initial_call=True,
)
def handle_tab_switch_and_create(
    currentKey,
    tabCloseCounts,
    currentItem,
    currentItemPath,
    latestDeletePane,
    origin_items,
    activeKey,
):
    """
    这个回调函数用于处理标签页子项的新建、切换及删除
    具体策略：
        1.当左侧某个菜单项被新选中，且右侧标签页子项尚未包含此项时，新建并切换
        2.当左侧某个菜单项被新选中，且右侧标签页子项已包含此项时，切换
        3.当右侧标签页子项某项被删除时，销毁对应标签页的同时切换回最后新增的标签页
    """

    trigger_id = dash.ctx.triggered_id

    # 基于jsonpath对各标签页子项中所有已有记录的nClicks参数重置为None
    # 以避免每次新的items返回给标签页重新渲染后，
    # 先前已更新为非None的按钮的nClicks误触发通知弹出回调
    parser = parse('$..nClicks')
    origin_items = parser.update(origin_items, None)
    new_items = dash.Patch()

    if trigger_id == 'index-side-menu':
        breadcrumb_items = [
            {'title': '首页', 'icon': 'antd-dashboard', 'href': '/'},
        ]
        if currentKey == '首页':
            pass
        elif currentKey == '个人资料':
            breadcrumb_items.append({'title': '个人资料'})
        else:
            breadcrumb_items = breadcrumb_items + [
                {'title': item.get('props').get('title')}
                for item in currentItemPath
            ]
        # 判断当前新选中的菜单栏项对应标签页是否已创建
        if currentKey in [item['key'] for item in origin_items]:
            return [dash.no_update, currentKey, breadcrumb_items]

        if currentKey == '个人资料':
            menu_title = '个人资料'
            menu_modules = 'system.user.profile'
            breadcrumb_items = [
                {'title': '首页', 'icon': 'antd-dashboard', 'href': '/'},
                {'title': menu_title},
            ]
        else:
            menu_title = currentItem.get('props').get('title')
            # 判断当前选中的菜单栏项是否存在module，如果有，则动态导入module，否则返回404页面
            menu_modules = currentItem.get('props').get('modules')

        for index, item in enumerate(origin_items):
            if {
                'key': '关闭右侧',
                'label': '关闭右侧',
                'icon': 'antd-arrow-right',
            } not in item['contextMenu']:
                item['contextMenu'].insert(
                    -1,
                    {
                        'key': '关闭右侧',
                        'label': '关闭右侧',
                        'icon': 'antd-arrow-right',
                    },
                )
            new_items[index]['contextMenu'] = item['contextMenu']
        context_menu = [
            {'key': '刷新页面', 'label': '刷新页面', 'icon': 'antd-reload'},
            {'key': '关闭当前', 'label': '关闭当前', 'icon': 'antd-close'},
            {
                'key': '关闭其他',
                'label': '关闭其他',
                'icon': 'antd-close-circle',
            },
            {
                'key': '全部关闭',
                'label': '全部关闭',
                'icon': 'antd-close-circle',
            },
        ]
        if len(origin_items) != 1:
            context_menu.insert(
                -1,
                {
                    'key': '关闭左侧',
                    'label': '关闭左侧',
                    'icon': 'antd-arrow-left',
                },
            )
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
                        'children': importlib.import_module(
                            'views.' + menu_modules
                        ).render(),
                        'contextMenu': context_menu,
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
                        style={'paddingBottom': 0, 'paddingTop': 0},
                    ),
                    'contextMenu': context_menu,
                }
            )

        return [new_items, currentKey, breadcrumb_items]

    elif trigger_id == 'tabs-container':
        # 如果删除的是当前标签页则回到最后新增的标签页，否则保持当前标签页不变
        for index, item in enumerate(origin_items):
            if item['key'] == latestDeletePane:
                context_menu = [
                    {
                        'key': '刷新页面',
                        'label': '刷新页面',
                        'icon': 'antd-reload',
                    },
                    {
                        'key': '关闭其他',
                        'label': '关闭其他',
                        'icon': 'antd-close-circle',
                    },
                    {
                        'key': '全部关闭',
                        'label': '全部关闭',
                        'icon': 'antd-close-circle',
                    },
                ]
                if index == 1:
                    if len(origin_items) == 2:
                        new_items[0]['contextMenu'] = context_menu
                    else:
                        origin_items[2]['contextMenu'].remove(
                            {
                                'key': '关闭左侧',
                                'label': '关闭左侧',
                                'icon': 'antd-arrow-left',
                            }
                        )
                        new_items[2]['contextMenu'] = origin_items[2][
                            'contextMenu'
                        ]
                elif index == 2:
                    if len(origin_items) == 3:
                        origin_items[1]['contextMenu'].remove(
                            {
                                'key': '关闭右侧',
                                'label': '关闭右侧',
                                'icon': 'antd-arrow-right',
                            }
                        )
                        new_items[1]['contextMenu'] = origin_items[1][
                            'contextMenu'
                        ]
                else:
                    if index == len(origin_items) - 1:
                        new_items[index - 1]['contextMenu'] = item[
                            'contextMenu'
                        ]
                del new_items[index]
                break
        new_origin_items = [
            item for item in origin_items if item['key'] != latestDeletePane
        ]

        return [
            new_items,
            new_origin_items[-1]['key']
            if activeKey == latestDeletePane
            else activeKey,
            dash.no_update,
        ]

    raise PreventUpdate


@app.callback(
    [
        Output('tabs-container', 'items', allow_duplicate=True),
        Output('tabs-container', 'activeKey', allow_duplicate=True),
        Output('trigger-reload-output', 'reload', allow_duplicate=True),
    ],
    Input('tabs-container', 'clickedContextMenu'),
    [State('tabs-container', 'items'), State('tabs-container', 'activeKey')],
    prevent_initial_call=True,
)
def handle_via_context_menu(clickedContextMenu, origin_items, activeKey):
    """
    基于标签页标题右键菜单的额外标签页控制
    """
    if clickedContextMenu['menuKey'] == '刷新页面':
        return [dash.no_update, dash.no_update, True]

    if '关闭' in clickedContextMenu['menuKey']:
        new_items = dash.Patch()
        if clickedContextMenu['menuKey'] == '关闭当前':
            for index, item in enumerate(origin_items):
                if item['key'] == clickedContextMenu['tabKey']:
                    context_menu = [
                        {
                            'key': '刷新页面',
                            'label': '刷新页面',
                            'icon': 'antd-reload',
                        },
                        {
                            'key': '关闭其他',
                            'label': '关闭其他',
                            'icon': 'antd-close-circle',
                        },
                        {
                            'key': '全部关闭',
                            'label': '全部关闭',
                            'icon': 'antd-close-circle',
                        },
                    ]
                    if index == 1:
                        if len(origin_items) == 2:
                            new_items[0]['contextMenu'] = context_menu
                        else:
                            origin_items[2]['contextMenu'].remove(
                                {
                                    'key': '关闭左侧',
                                    'label': '关闭左侧',
                                    'icon': 'antd-arrow-left',
                                }
                            )
                            new_items[2]['contextMenu'] = origin_items[2][
                                'contextMenu'
                            ]
                    elif index == 2:
                        if len(origin_items) == 3:
                            origin_items[1]['contextMenu'].remove(
                                {
                                    'key': '关闭右侧',
                                    'label': '关闭右侧',
                                    'icon': 'antd-arrow-right',
                                }
                            )
                            new_items[1]['contextMenu'] = origin_items[1][
                                'contextMenu'
                            ]
                    else:
                        if index == len(origin_items) - 1:
                            new_items[index - 1]['contextMenu'] = item[
                                'contextMenu'
                            ]
                    del new_items[index]
                    break
            new_origin_items = [
                item
                for item in origin_items
                if item['key'] != clickedContextMenu['tabKey']
            ]

            return [
                new_items,
                new_origin_items[-1]['key']
                if activeKey == clickedContextMenu['tabKey']
                else activeKey,
                dash.no_update,
            ]

        elif clickedContextMenu['menuKey'] == '关闭其他':
            current_index = 0
            for index, item in enumerate(origin_items):
                if item['key'] == clickedContextMenu['tabKey']:
                    current_index = index
            for i in range(1, current_index):
                del new_items[1]
            for j in range(current_index + 1, len(origin_items) + 1):
                del new_items[2]
            context_menu = [
                {'key': '刷新页面', 'label': '刷新页面', 'icon': 'antd-reload'},
                {
                    'key': '关闭其他',
                    'label': '关闭其他',
                    'icon': 'antd-close-circle',
                },
                {
                    'key': '全部关闭',
                    'label': '全部关闭',
                    'icon': 'antd-close-circle',
                },
            ]
            if clickedContextMenu['tabKey'] == '首页':
                new_items[0]['contextMenu'] = context_menu
            else:
                context_menu.insert(
                    1,
                    {
                        'key': '关闭当前',
                        'label': '关闭当前',
                        'icon': 'antd-close',
                    },
                )
                new_items[1]['contextMenu'] = context_menu

            return [new_items, clickedContextMenu['tabKey'], dash.no_update]

        elif clickedContextMenu['menuKey'] == '关闭左侧':
            current_index = 0
            for index, item in enumerate(origin_items):
                if item['key'] == clickedContextMenu['tabKey']:
                    current_index = index
                    item['contextMenu'].remove(
                        {
                            'key': '关闭左侧',
                            'label': '关闭左侧',
                            'icon': 'antd-arrow-left',
                        }
                    )
                    new_items[index]['contextMenu'] = item['contextMenu']
                    break
            for i in range(1, current_index):
                del new_items[1]

            return [new_items, clickedContextMenu['tabKey'], dash.no_update]

        elif clickedContextMenu['menuKey'] == '关闭右侧':
            current_index = 0
            for index, item in enumerate(origin_items):
                if item['key'] == clickedContextMenu['tabKey']:
                    current_index = index
                    item['contextMenu'].remove(
                        {
                            'key': '关闭右侧',
                            'label': '关闭右侧',
                            'icon': 'antd-arrow-right',
                        }
                    )
                    new_items[index]['contextMenu'] = item['contextMenu']
                    break
            for i in range(current_index + 1, len(origin_items) + 1):
                del new_items[current_index + 1]

            return [new_items, clickedContextMenu['tabKey'], dash.no_update]

        for i in range(len(origin_items)):
            del new_items[1]
        new_items[0]['contextMenu'] = [
            {'key': '刷新页面', 'label': '刷新页面', 'icon': 'antd-reload'},
            {
                'key': '关闭其他',
                'label': '关闭其他',
                'icon': 'antd-close-circle',
            },
            {
                'key': '全部关闭',
                'label': '全部关闭',
                'icon': 'antd-close-circle',
            },
        ]
        # 否则则为全部关闭
        return [new_items, '首页', dash.no_update]

    raise PreventUpdate


# 标签页点击回调
@app.callback(
    Output('dcc-url', 'pathname', allow_duplicate=True),
    Input('tabs-container', 'activeKey'),
    prevent_initial_call=True,
)
def get_current_href(active_key):
    if active_key:
        if active_key == '首页':
            return '/'

        elif active_key == '个人资料':
            return '/user/profile'

        else:
            current_href = find_href_by_key(
                CacheManager.get('menu_info'), active_key
            )

            return current_href

    raise PreventUpdate
