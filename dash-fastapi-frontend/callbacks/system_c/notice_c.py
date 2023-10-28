import dash
import time
import uuid
import re
import json
from flask import session
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from config.global_config import ApiBaseUrlConfig
from api.notice import get_notice_list_api, add_notice_api, edit_notice_api, delete_notice_api, get_notice_detail_api
from api.dict import query_dict_data_list_api


@app.callback(
    output=dict(
        notice_table_data=Output('notice-list-table', 'data', allow_duplicate=True),
        notice_table_pagination=Output('notice-list-table', 'pagination', allow_duplicate=True),
        notice_table_key=Output('notice-list-table', 'key'),
        notice_table_selectedrowkeys=Output('notice-list-table', 'selectedRowKeys'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        search_click=Input('notice-search', 'nClicks'),
        refresh_click=Input('notice-refresh', 'nClicks'),
        pagination=Input('notice-list-table', 'pagination'),
        operations=Input('notice-operations-store', 'data')
    ),
    state=dict(
        notice_title=State('notice-notice_title-input', 'value'),
        update_by=State('notice-update_by-input', 'value'),
        notice_type=State('notice-notice_type-select', 'value'),
        create_time_range=State('notice-create_time-range', 'value'),
        button_perms=State('notice-button-perms-container', 'data')
    ),
    prevent_initial_call=True
)
def get_notice_table_data(search_click, refresh_click, pagination, operations, notice_title, update_by, notice_type, create_time_range,
                          button_perms):
    """
    获取通知公告表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """
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

            return dict(
                notice_table_data=table_data,
                notice_table_pagination=table_pagination,
                notice_table_key=str(uuid.uuid4()),
                notice_table_selectedrowkeys=None,
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            notice_table_data=dash.no_update,
            notice_table_pagination=dash.no_update,
            notice_table_key=dash.no_update,
            notice_table_selectedrowkeys=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


# 重置通知公告搜索表单数据回调
app.clientside_callback(
    '''
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('notice-notice_title-input', 'value'),
     Output('notice-update_by-input', 'value'),
     Output('notice-notice_type-select', 'value'),
     Output('notice-create_time-range', 'value'),
     Output('notice-operations-store', 'data')],
    Input('notice-reset', 'nClicks'),
    prevent_initial_call=True
)


# 隐藏/显示通知公告搜索表单回调
app.clientside_callback(
    '''
    (hidden_click, hidden_status) => {
        if (hidden_click) {
            return [
                !hidden_status,
                hidden_status ? '隐藏搜索' : '显示搜索'
            ]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('notice-search-form-container', 'hidden'),
     Output('notice-hidden-tooltip', 'title')],
    Input('notice-hidden', 'nClicks'),
    State('notice-search-form-container', 'hidden'),
    prevent_initial_call=True
)


@app.callback(
    Output({'type': 'notice-operation-button', 'index': 'edit'}, 'disabled'),
    Input('notice-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_notice_edit_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制编辑按钮状态回调
    """
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1:
                return True

            return False

        return True

    raise PreventUpdate


@app.callback(
    Output({'type': 'notice-operation-button', 'index': 'delete'}, 'disabled'),
    Input('notice-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_notice_delete_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制删除按钮状态回调
    """
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:

            return False

        return True

    raise PreventUpdate


@app.callback(
    Output('notice-init-editor', 'jsString'),
    Input('notice-written-editor-store', 'data'),
    prevent_initial_call=True
)
def init_render_editor(html_string):
    """
    初始化富文本编辑器回调
    """
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
                            baseUrl: '% s',
                            uploadId: '% s',
                            taskPath: 'notice'
                        },
                        // 将 meta 拼接到 url 参数中，默认 false
                        metaWithUrl: true,
                        // 自定义增加 http  header
                        headers: {
                            Authorization: '% s'
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
                            baseUrl: '% s',
                            uploadId: '% s',
                            taskPath: 'notice'
                        },
                        // 将 meta 拼接到 url 参数中，默认 false
                        metaWithUrl: true,
                        // 自定义增加 http  header
                        headers: {
                            Authorization: '% s'
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
            ''' % (url, ApiBaseUrlConfig.BaseUrl, str(uuid.uuid4()), token, url, ApiBaseUrlConfig.BaseUrl, str(uuid.uuid4()), token, html_string)

    return js_string


@app.callback(
    output=dict(
        modal=dict(visible=Output('notice-modal', 'visible', allow_duplicate=True), title=Output('notice-modal', 'title')),
        form_value=dict(
            notice_title=Output('notice-notice_title', 'value'),
            notice_type=Output('notice-notice_type', 'value'),
            status=Output('notice-status', 'value'),
            editor_content=Output('notice-written-editor-store', 'data'),
        ),
        form_validate=[
            Output('notice-notice_title-form-item', 'validateStatus', allow_duplicate=True),
            Output('notice-notice_type-form-item', 'validateStatus', allow_duplicate=True),
            Output('notice-notice_title-form-item', 'help', allow_duplicate=True),
            Output('notice-notice_type-form-item', 'help', allow_duplicate=True)
        ],
        other=dict(
            api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
            edit_row_info=Output('notice-edit-id-store', 'data'),
            modal_type=Output('notice-operations-store-bk', 'data')
        )
    ),
    inputs=dict(
        operation_click=Input({'type': 'notice-operation-button', 'index': ALL}, 'nClicks'),
        button_click=Input('notice-list-table', 'nClicksButton')
    ),
    state=dict(
        selected_row_keys=State('notice-list-table', 'selectedRowKeys'),
        clicked_content=State('notice-list-table', 'clickedContent'),
        recently_button_clicked_row=State('notice-list-table', 'recentlyButtonClickedRow')
    ),
    prevent_initial_call=True
)
def add_edit_notice_modal(operation_click, button_click, selected_row_keys, clicked_content,
                          recently_button_clicked_row):
    """
    显示新增或编辑通知公告弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'add', 'type': 'notice-operation-button'} \
            or trigger_id == {'index': 'edit', 'type': 'notice-operation-button'} \
            or (trigger_id == 'notice-list-table' and clicked_content == '修改'):
        if trigger_id == {'index': 'add', 'type': 'notice-operation-button'}:
            return dict(
                modal=dict(visible=True, title='新增通知公告'),
                form_value=dict(notice_title=None, notice_type=None, status='0', editor_content='<p><br></p>'),
                form_validate=[None] * 4,
                other=dict(
                    api_check_token_trigger=dash.no_update,
                    edit_row_info=None,
                    modal_type={'type': 'add'}
                )
            )
        elif trigger_id == {'index': 'edit', 'type': 'notice-operation-button'} or (trigger_id == 'notice-list-table' and clicked_content == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'notice-operation-button'}:
                notice_id = int(','.join(selected_row_keys))
            else:
                notice_id = int(recently_button_clicked_row['key'])
            notice_info_res = get_notice_detail_api(notice_id=notice_id)
            if notice_info_res['code'] == 200:
                notice_info = notice_info_res['data']
                notice_content = notice_info.get('notice_content')

                return dict(
                    modal=dict(visible=True, title='编辑通知公告'),
                    form_value=dict(
                        notice_title=notice_info.get('notice_title'),
                        notice_type=notice_info.get('notice_type'),
                        status=notice_info.get('status'),
                        editor_content=re.sub(r"\n", "", notice_content)
                    ),
                    form_validate=[None] * 4,
                    other=dict(
                        api_check_token_trigger={'timestamp': time.time()},
                        edit_row_info=notice_info if notice_info else None,
                        modal_type={'type': 'edit'}
                    )
                )

        return dict(
            modal=dict(visible=dash.no_update, title=dash.no_update),
            form_value=dict(
                notice_title=dash.no_update,
                notice_type=dash.no_update,
                status=dash.no_update,
                editor_content=dash.no_update
            ),
            form_validate=[dash.no_update] * 4,
            other=dict(
                api_check_token_trigger={'timestamp': time.time()},
                edit_row_info=None,
                modal_type=None
            )
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        notice_title_form_status=Output('notice-notice_title-form-item', 'validateStatus', allow_duplicate=True),
        notice_type_form_status=Output('notice-notice_type-form-item', 'validateStatus', allow_duplicate=True),
        notice_title_form_help=Output('notice-notice_title-form-item', 'help', allow_duplicate=True),
        notice_type_form_help=Output('notice-notice_type-form-item', 'help', allow_duplicate=True),
        modal_visible=Output('notice-modal', 'visible'),
        operations=Output('notice-operations-store', 'data', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        confirm_trigger=Input('notice-modal', 'okCounts')
    ),
    state=dict(
        modal_type=State('notice-operations-store-bk', 'data'),
        edit_row_info=State('notice-edit-id-store', 'data'),
        notice_title=State('notice-notice_title', 'value'),
        notice_type=State('notice-notice_type', 'value'),
        status=State('notice-status', 'value'),
        notice_content=State('notice-content', 'data')
    ),
    prevent_initial_call=True
)
def notice_confirm(confirm_trigger, modal_type, edit_row_info, notice_title, notice_type, status, notice_content):
    """
    新增或编辑通知公告弹窗确认回调，实现新增或编辑操作
    """
    if confirm_trigger:
        if all([notice_title, notice_type]):
            params_add = dict(notice_title=notice_title, notice_type=notice_type, status=status,
                              notice_content=notice_content.get('html'))
            params_edit = dict(notice_id=edit_row_info.get('notice_id') if edit_row_info else None,
                               notice_title=notice_title,
                               notice_type=notice_type, status=status, notice_content=notice_content.get('html'))
            api_res = {}
            modal_type = modal_type.get('type')
            if modal_type == 'add':
                api_res = add_notice_api(params_add)
            if modal_type == 'edit':
                api_res = edit_notice_api(params_edit)
            if api_res.get('code') == 200:
                if modal_type == 'add':
                    return dict(
                        notice_title_form_status=None,
                        notice_type_form_status=None,
                        notice_title_form_help=None,
                        notice_type_form_help=None,
                        modal_visible=False,
                        operations={'type': 'add'},
                        api_check_token_trigger={'timestamp': time.time()},
                        global_message_container=fuc.FefferyFancyMessage('新增成功', type='success')
                    )
                if modal_type == 'edit':
                    return dict(
                        notice_title_form_status=None,
                        notice_type_form_status=None,
                        notice_title_form_help=None,
                        notice_type_form_help=None,
                        modal_visible=False,
                        operations={'type': 'edit'},
                        api_check_token_trigger={'timestamp': time.time()},
                        global_message_container=fuc.FefferyFancyMessage('编辑成功', type='success')
                    )

            return dict(
                notice_title_form_status=None,
                notice_type_form_status=None,
                notice_title_form_help=None,
                notice_type_form_help=None,
                modal_visible=dash.no_update,
                operations=dash.no_update,
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage('处理失败', type='error')
            )

        return dict(
            notice_title_form_status=None if notice_title else 'error',
            notice_type_form_status=None if notice_type else 'error',
            notice_title_form_help=None if notice_title else '请输入公告标题！',
            notice_type_form_help=None if notice_type else '请输入公告类型！',
            modal_visible=dash.no_update,
            operations=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()},
            global_message_container=fuc.FefferyFancyMessage('处理失败', type='error')
        )

    raise PreventUpdate


@app.callback(
    [Output('notice-delete-text', 'children'),
     Output('notice-delete-confirm-modal', 'visible'),
     Output('notice-delete-ids-store', 'data')],
    [Input({'type': 'notice-operation-button', 'index': ALL}, 'nClicks'),
     Input('notice-list-table', 'nClicksButton')],
    [State('notice-list-table', 'selectedRowKeys'),
     State('notice-list-table', 'clickedContent'),
     State('notice-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def notice_delete_modal(operation_click, button_click,
                        selected_row_keys, clicked_content, recently_button_clicked_row):
    """
    显示删除通知公告二次确认弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'notice-operation-button'} or (
            trigger_id == 'notice-list-table' and clicked_content == '删除'):
        trigger_id = dash.ctx.triggered_id

        if trigger_id == {'index': 'delete', 'type': 'notice-operation-button'}:
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

    raise PreventUpdate


@app.callback(
    [Output('notice-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('notice-delete-confirm-modal', 'okCounts'),
    State('notice-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def notice_delete_confirm(delete_confirm, notice_ids_data):
    """
    删除岗通知公告弹窗确认回调，实现删除操作
    """
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

    raise PreventUpdate
