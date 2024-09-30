import feffery_antd_components as fac
from dash import html
import callbacks.system_c.role_c.data_scope_c  # noqa: F401


def render():
    return [
        fac.AntdForm(
            [
                fac.AntdFormItem(
                    fac.AntdInput(
                        id={
                            'type': 'datascope-form-value',
                            'index': 'role_name',
                        },
                        placeholder='请输入角色名称',
                        allowClear=True,
                        disabled=True,
                        style={'width': 350},
                    ),
                    label='角色名称',
                    id={'type': 'datascope-form-label', 'index': 'role_name'},
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                ),
                fac.AntdFormItem(
                    fac.AntdInput(
                        id={
                            'type': 'datascope-form-value',
                            'index': 'role_key',
                        },
                        placeholder='请输入权限字符',
                        allowClear=True,
                        disabled=True,
                        style={'width': 350},
                    ),
                    label='权限字符',
                    id={'type': 'datascope-form-label', 'index': 'role_key'},
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                ),
                fac.AntdFormItem(
                    fac.AntdSelect(
                        id={
                            'type': 'datascope-form-value',
                            'index': 'data_scope',
                        },
                        options=[
                            {'label': '全部数据权限', 'value': '1'},
                            {'label': '自定义数据权限', 'value': '2'},
                            {'label': '本部门数据权限', 'value': '3'},
                            {'label': '本部门及以下数据权限', 'value': '4'},
                            {'label': '仅本人数据权限', 'value': '5'},
                        ],
                        placeholder='请选择权限范围',
                        style={'width': 350},
                    ),
                    label='权限范围',
                    id={'type': 'datascope-form-label', 'index': 'data_scope'},
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                ),
                html.Div(
                    fac.AntdFormItem(
                        [
                            fac.AntdRow(
                                [
                                    fac.AntdCol(
                                        fac.AntdCheckbox(
                                            id='role-dept-perms-radio-fold-unfold',
                                            label='展开/折叠',
                                        ),
                                        span=7,
                                    ),
                                    fac.AntdCol(
                                        fac.AntdCheckbox(
                                            id='role-dept-perms-radio-all-none',
                                            label='全选/全不选',
                                        ),
                                        span=8,
                                    ),
                                    fac.AntdCol(
                                        fac.AntdCheckbox(
                                            id='role-dept-perms-radio-parent-children',
                                            label='父子联动',
                                            checked=True,
                                        ),
                                        span=6,
                                    ),
                                ],
                                style={'paddingTop': '6px'},
                            ),
                            fac.AntdRow(
                                fac.AntdCol(
                                    html.Div(
                                        [
                                            fac.AntdTree(
                                                id='role-dept-perms',
                                                treeData=[],
                                                multiple=True,
                                                checkable=True,
                                                showLine=False,
                                                selectable=False,
                                            )
                                        ],
                                        style={
                                            'border': 'solid 1px rgba(0, 0, 0, 0.2)',
                                            'border-radius': '5px',
                                            'width': 350,
                                        },
                                    )
                                ),
                                style={'paddingTop': '6px'},
                            ),
                        ],
                        label='数据权限',
                        id='role-dept-perms-form-item',
                        labelCol={'span': 6},
                        wrapperCol={'span': 18},
                    ),
                    id='role-dept-perms-div',
                ),
            ]
        )
    ]
