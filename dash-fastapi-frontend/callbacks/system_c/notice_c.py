import dash
import time
import uuid
import re
import json
from dash import html
from flask import session
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc

from server import app
from config.global_config import ApiBaseUrlConfig
from api.notice import get_notice_list_api, add_notice_api, edit_notice_api, delete_notice_api, get_notice_detail_api
from api.dict import query_dict_data_list_api


@app.callback(
    [Output('notice-list-table', 'data', allow_duplicate=True),
     Output('notice-list-table', 'pagination', allow_duplicate=True),
     Output('notice-list-table', 'key'),
     Output('notice-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('notice-search', 'nClicks'),
     Input('notice-refresh', 'nClicks'),
     Input('notice-list-table', 'pagination'),
     Input('notice-operations-store', 'data')],
    [State('notice-notice_title-input', 'value'),
     State('notice-update_by-input', 'value'),
     State('notice-notice_type-select', 'value'),
     State('notice-create_time-range', 'value'),
     State('notice-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_notice_table_data(search_click, refresh_click, pagination, operations, notice_title, update_by, notice_type, create_time_range,
                          button_perms):
    create_time_start = None
    create_time_end = None
    if create_time_range:
        create_time_start = create_time_range[0]
        create_time_end = create_time_range[1]

    query_params = dict(
        notice_title=notice_title,
        update_by=update_by,
        notice_type=notice_type,
        create_time_start=create_time_start,
        create_time_end=create_time_end,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'notice-list-table':
        query_params = dict(
            notice_title=notice_title,
            update_by=update_by,
            notice_type=notice_type,
            create_time_start=create_time_start,
            create_time_end=create_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        option_table = []
        info = query_dict_data_list_api(dict_type='sys_notice_type')
        if info.get('code') == 200:
            data = info.get('data')
            option_table = [
                dict(label=item.get('dict_label'), value=item.get('dict_value'), css_class=item.get('css_class')) for
                item in data]
        option_dict = {item.get('value'): item for item in option_table}

        table_info = get_notice_list_api(query_params)
        if table_info['code'] == 200:
            table_data = table_info['data']['rows']
            table_pagination = dict(
                pageSize=table_info['data']['page_size'],
                current=table_info['data']['page_num'],
                showSizeChanger=True,
                pageSizeOptions=[10, 30, 50, 100],
                showQuickJumper=True,
                total=table_info['data']['total']
            )
            for item in table_data:
                if item['status'] == '0':
                    item['status'] = dict(tag='正常', color='blue')
                else:
                    item['status'] = dict(tag='关闭', color='volcano')
                item['notice_type'] = dict(
                    tag=option_dict.get(str(item.get('notice_type'))).get('label'),
                    color=json.loads(option_dict.get(str(item.get('notice_type'))).get('css_class')).get('color')
                )
                item['key'] = str(item['notice_id'])
                item['operation'] = [
                    {
                        'content': '修改',
                        'type': 'link',
                        'icon': 'antd-edit'
                    } if 'system:notice:edit' in button_perms else {},
                    {
                        'content': '删除',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'system:notice:remove' in button_perms else {},
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('notice-notice_title-input', 'value'),
     Output('notice-update_by-input', 'value'),
     Output('notice-notice_type-select', 'value'),
     Output('notice-create_time-range', 'value'),
     Output('notice-operations-store', 'data')],
    Input('notice-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_notice_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 5


@app.callback(
    [Output('notice-search-form-container', 'hidden'),
     Output('notice-hidden-tooltip', 'title')],
    Input('notice-hidden', 'nClicks'),
    State('notice-search-form-container', 'hidden'),
    prevent_initial_call=True
)
def hidden_notice_search_form(hidden_click, hidden_status):
    if hidden_click:

        return [not hidden_status, '隐藏搜索' if hidden_status else '显示搜索']
    return [dash.no_update] * 2


@app.callback(
    [Output('notice-edit', 'disabled'),
     Output('notice-delete', 'disabled')],
    Input('notice-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_notice_edit_delete_button_status(table_rows_selected):
    if table_rows_selected:
        if len(table_rows_selected) > 1:
            return [True, False]

        return [False, False]

    return [True, True]


@app.callback(
    Output('notice-init-editor', 'jsString'),
    Input('notice-written-editor-store', 'data'),
    prevent_initial_call=True
)
def init_render_editor(html_string):
    url = f'{ApiBaseUrlConfig.BaseUrl}/common/uploadForEditor'
    token = 'Bearer ' + session.get('Authorization')

    js_string = '''
            const { i18nChangeLanguage, createEditor, createToolbar } = window.wangEditor
            
            // 切换至中文
            i18nChangeLanguage('zh-CN')
            
            const editorConfig = {
                placeholder: '请输入...',
                onChange(editor) {
                  const html = editor.getHtml()
                  sessionStorage.setItem('notice-content', JSON.stringify({html: html}))
                },
                // 图片和视频上传参数配置
                MENU_CONF: {
                    uploadImage: {
                        server: '% s',
                        // form-data fieldName ，默认值 'editor-uploaded-file'
                        fieldName: 'file',
                        // 单个文件的最大体积限制，默认为 2M
                        maxFileSize: 10 * 1024 * 1024, // 10M
                        // 最多可上传几个文件，默认为 100
                        maxNumberOfFiles: 10,
                        // 选择文件时的类型限制，默认为 ['image/*'] 。如不想限制，则设置为 []
                        allowedFileTypes: ['image/*'],
                        // 自定义上传参数，例如传递验证的 token 等。参数会被添加到 formData 中，一起上传到服务端。
                        meta: {
                            uploadId: '% s',
                        },
                        // 将 meta 拼接到 url 参数中，默认 false
                        metaWithUrl: true,
                        // 自定义增加 http  header
                        headers: {
                            token: '% s'
                        },
                        // 跨域是否传递 cookie ，默认为 false
                        withCredentials: true,
                        // 超时时间，默认为 10 秒
                        timeout: 5 * 1000, // 5 秒
                        // 小于该值就插入 base64 格式（而不上传），默认为 0
                        base64LimitSize: 500 * 1024 // 500KB
                    },
                    uploadVideo: {
                        server: '% s',
                        // form-data fieldName ，默认值 'wangeditor-uploaded-video'
                        fieldName: 'file',
                        // 单个文件的最大体积限制，默认为 10M
                        maxFileSize: 100 * 1024 * 1024, // 100M
                        // 最多可上传几个文件，默认为 5
                        maxNumberOfFiles: 3,
                        // 选择文件时的类型限制，默认为 ['video/*'] 。如不想限制，则设置为 []
                        allowedFileTypes: ['video/*'],
                        // 自定义上传参数，例如传递验证的 token 等。参数会被添加到 formData 中，一起上传到服务端。
                        meta: {
                            uploadId: '% s',
                        },
                        // 将 meta 拼接到 url 参数中，默认 false
                        metaWithUrl: true,
                        // 自定义增加 http  header
                        headers: {
                            token: '% s'
                        },
                        // 跨域是否传递 cookie ，默认为 false
                        withCredentials: true,
                        // 超时时间，默认为 30 秒
                        timeout: 15 * 1000, // 15 秒
                    }
                }
            }
            
            
            const editor = createEditor({
                selector: '#notice-notice_content-editor-container',
                html: '% s',
                config: editorConfig,
                mode: 'default'
            })
            
            const toolbarConfig = {}
            
            const toolbar = createToolbar({
                editor,
                selector: '#notice-notice_content-toolbar-container',
                config: toolbarConfig,
                mode: 'default'
            })
            ''' % (url, f'notice_{uuid.uuid4()}', token, url, f'notice_{uuid.uuid4()}', token, html_string)

    return js_string


@app.callback(
    [Output('notice-modal', 'visible', allow_duplicate=True),
     Output('notice-modal', 'title'),
     Output('notice-notice_title', 'value'),
     Output('notice-notice_type', 'value'),
     Output('notice-status', 'value'),
     Output('notice-written-editor-store', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('notice-add', 'nClicks', allow_duplicate=True),
     Output('notice-edit', 'nClicks'),
     Output('notice-edit-id-store', 'data'),
     Output('notice-operations-store-bk', 'data')],
    [Input('notice-add', 'nClicks'),
     Input('notice-edit', 'nClicks'),
     Input('notice-list-table', 'nClicksButton')],
    [State('notice-list-table', 'selectedRowKeys'),
     State('notice-list-table', 'clickedContent'),
     State('notice-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_notice_modal(add_click, edit_click, button_click, selected_row_keys, clicked_content,
                          recently_button_clicked_row):
    if add_click or edit_click or button_click:
        if add_click:
            return [
                True,
                '新增通知公告',
                None,
                None,
                '0',
                '<p><br></p>',
                dash.no_update,
                None,
                None,
                None,
                {'type': 'add'}
            ]
        elif edit_click or (button_click and clicked_content == '修改'):
            if edit_click:
                notice_id = int(','.join(selected_row_keys))
            else:
                notice_id = int(recently_button_clicked_row['key'])
            notice_info_res = get_notice_detail_api(notice_id=notice_id)
            if notice_info_res['code'] == 200:
                notice_info = notice_info_res['data']
                notice_content = notice_info.get('notice_content')

                return [
                    True,
                    '编辑通知公告',
                    notice_info.get('notice_title'),
                    notice_info.get('notice_type'),
                    notice_info.get('status'),
                    re.sub(r"\n", "", notice_content),
                    {'timestamp': time.time()},
                    None,
                    None,
                    notice_info if notice_info else None,
                    {'type': 'edit'}
                ]

        return [dash.no_update] * 6 + [{'timestamp': time.time()}, None, None, None, None]

    return [dash.no_update] * 7 + [None, None, None, None]


@app.callback(
    [Output('notice-notice_title-form-item', 'validateStatus'),
     Output('notice-notice_type-form-item', 'validateStatus'),
     Output('notice-notice_title-form-item', 'help'),
     Output('notice-notice_type-form-item', 'help'),
     Output('notice-modal', 'visible'),
     Output('notice-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('notice-modal', 'okCounts'),
    [State('notice-operations-store-bk', 'data'),
     State('notice-edit-id-store', 'data'),
     State('notice-notice_title', 'value'),
     State('notice-notice_type', 'value'),
     State('notice-status', 'value'),
     State('notice-content', 'data')],
    prevent_initial_call=True
)
def notice_confirm(confirm_trigger, operation_type, cur_notice_info, notice_title, notice_type, status, notice_content):
    if confirm_trigger:
        if all([notice_title, notice_type]):
            params_add = dict(notice_title=notice_title, notice_type=notice_type, status=status,
                              notice_content=notice_content.get('html'))
            params_edit = dict(notice_id=cur_notice_info.get('notice_id') if cur_notice_info else None,
                               notice_title=notice_title,
                               notice_type=notice_type, status=status, notice_content=notice_content.get('html'))
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_notice_api(params_add)
            if operation_type == 'edit':
                api_res = edit_notice_api(params_edit)
            if api_res.get('code') == 200:
                if operation_type == 'add':
                    return [
                        None,
                        None,
                        None,
                        None,
                        False,
                        {'type': 'add'},
                        {'timestamp': time.time()},
                        fuc.FefferyFancyMessage('新增成功', type='success')
                    ]
                if operation_type == 'edit':
                    return [
                        None,
                        None,
                        None,
                        None,
                        False,
                        {'type': 'edit'},
                        {'timestamp': time.time()},
                        fuc.FefferyFancyMessage('编辑成功', type='success')
                    ]

            return [
                None,
                None,
                None,
                None,
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('处理失败', type='error')
            ]

        return [
            None if notice_title else 'error',
            None if notice_type else 'error',
            None if notice_title else '请输入公告标题！',
            None if notice_type else '请输入公告类型！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]

    return [dash.no_update] * 8


@app.callback(
    [Output('notice-delete-text', 'children'),
     Output('notice-delete-confirm-modal', 'visible'),
     Output('notice-delete-ids-store', 'data')],
    [Input('notice-delete', 'nClicks'),
     Input('notice-list-table', 'nClicksButton')],
    [State('notice-list-table', 'selectedRowKeys'),
     State('notice-list-table', 'clickedContent'),
     State('notice-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def notice_delete_modal(delete_click, button_click,
                        selected_row_keys, clicked_content, recently_button_clicked_row):
    if delete_click or button_click:
        trigger_id = dash.ctx.triggered_id

        if trigger_id == 'notice-delete':
            notice_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                notice_ids = recently_button_clicked_row['key']
            else:
                return dash.no_update

        return [
            f'是否确认删除序号为{notice_ids}的通知公告？',
            True,
            {'notice_ids': notice_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('notice-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('notice-delete-confirm-modal', 'okCounts'),
    State('notice-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def notice_delete_confirm(delete_confirm, notice_ids_data):
    if delete_confirm:

        params = notice_ids_data
        delete_button_info = delete_notice_api(params)
        if delete_button_info['code'] == 200:
            return [
                {'type': 'delete'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('删除成功', type='success')
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('删除失败', type='error')
        ]

    return [dash.no_update] * 3
