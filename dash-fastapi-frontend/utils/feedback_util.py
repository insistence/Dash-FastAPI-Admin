from dash import set_props
from typing import Dict, Literal, Optional, Union
from uuid import uuid4


class MessageManager:
    """
    全局提示管理器
    """

    @classmethod
    def default(
        cls,
        container_id: Optional[Union[str, Dict]] = 'global-message-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        className: Optional[str] = None,
        content: Optional[str] = '请求成功',
        duration: Optional[int] = 3,
        icon: Optional[str] = None,
        iconRenderer: Optional[Literal['AntdIcon', 'fontawesome']] = 'AntdIcon',
        key: Optional[str] = None,
        maxCount: Optional[int] = None,
        style: Optional[Dict] = None,
        top: Optional[int] = 8,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'className': className,
                        'content': content,
                        'duration': duration,
                        'icon': icon,
                        'iconRenderer': iconRenderer,
                        'key': key,
                        'maxCount': maxCount,
                        'style': style,
                        'top': top,
                        'type': 'default',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdMessage',
                    'namespace': 'feffery_antd_components',
                }
            },
        )

    @classmethod
    def info(
        cls,
        container_id: Optional[Union[str, Dict]] = 'global-message-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        className: Optional[str] = None,
        content: Optional[str] = '请求成功',
        duration: Optional[int] = 3,
        icon: Optional[str] = None,
        iconRenderer: Optional[Literal['AntdIcon', 'fontawesome']] = 'AntdIcon',
        key: Optional[str] = None,
        maxCount: Optional[int] = None,
        style: Optional[Dict] = None,
        top: Optional[int] = 8,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'className': className,
                        'content': content,
                        'duration': duration,
                        'icon': icon,
                        'iconRenderer': iconRenderer,
                        'key': key,
                        'maxCount': maxCount,
                        'style': style,
                        'top': top,
                        'type': 'info',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdMessage',
                    'namespace': 'feffery_antd_components',
                }
            },
            namespace='feffery_antd_components',
        )

    @classmethod
    def success(
        cls,
        container_id: Optional[Union[str, Dict]] = 'global-message-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        className: Optional[str] = None,
        content: Optional[str] = '请求成功',
        duration: Optional[int] = 3,
        icon: Optional[str] = None,
        iconRenderer: Optional[Literal['AntdIcon', 'fontawesome']] = 'AntdIcon',
        key: Optional[str] = None,
        maxCount: Optional[int] = None,
        style: Optional[Dict] = None,
        top: Optional[int] = 8,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'className': className,
                        'content': content,
                        'duration': duration,
                        'icon': icon,
                        'iconRenderer': iconRenderer,
                        'key': key,
                        'maxCount': maxCount,
                        'style': style,
                        'top': top,
                        'type': 'success',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdMessage',
                    'namespace': 'feffery_antd_components',
                }
            },
        )

    @classmethod
    def warning(
        cls,
        container_id: Optional[Union[str, Dict]] = 'global-message-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        className: Optional[str] = None,
        content: Optional[str] = '请求失败',
        duration: Optional[int] = 3,
        icon: Optional[str] = None,
        iconRenderer: Optional[Literal['AntdIcon', 'fontawesome']] = 'AntdIcon',
        key: Optional[str] = None,
        maxCount: Optional[int] = None,
        style: Optional[Dict] = None,
        top: Optional[int] = 8,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'className': className,
                        'content': content,
                        'duration': duration,
                        'icon': icon,
                        'iconRenderer': iconRenderer,
                        'key': key,
                        'maxCount': maxCount,
                        'style': style,
                        'top': top,
                        'type': 'warning',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdMessage',
                    'namespace': 'feffery_antd_components',
                }
            },
        )

    @classmethod
    def error(
        cls,
        container_id: Optional[Union[str, Dict]] = 'global-message-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        className: Optional[str] = None,
        content: Optional[str] = '请求异常',
        duration: Optional[int] = 3,
        icon: Optional[str] = None,
        iconRenderer: Optional[Literal['AntdIcon', 'fontawesome']] = 'AntdIcon',
        key: Optional[str] = None,
        maxCount: Optional[int] = None,
        style: Optional[Dict] = None,
        top: Optional[int] = 8,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'className': className,
                        'content': content,
                        'duration': duration,
                        'icon': icon,
                        'iconRenderer': iconRenderer,
                        'key': key,
                        'maxCount': maxCount,
                        'style': style,
                        'top': top,
                        'type': 'error',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdMessage',
                    'namespace': 'feffery_antd_components',
                }
            },
        )


class NotificationManager:
    """
    通知提醒管理器
    """

    @classmethod
    def default(
        cls,
        container_id: Optional[
            Union[str, Dict]
        ] = 'global-notification-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        bottom: Optional[int] = 24,
        className: Optional[str] = None,
        closeable: Optional[bool] = True,
        closeButton: Optional[Dict] = None,
        description: Optional[str] = None,
        duration: Optional[Union[float, int]] = 4.5,
        key: Optional[str] = None,
        message: Optional[str] = '请求成功',
        placement: Optional[
            Literal[
                'top',
                'bottom',
                'topLeft',
                'topRight',
                'bottomLeft',
                'bottomRight',
            ]
        ] = 'topRight',
        style: Optional[Dict] = None,
        top: Optional[int] = 24,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'bottom': bottom,
                        'className': className,
                        'closeable': closeable,
                        'closeButton': closeButton,
                        'description': description,
                        'duration': duration,
                        'key': key,
                        'message': message,
                        'placement': placement,
                        'style': style,
                        'top': top,
                        'type': 'default',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdNotification',
                    'namespace': 'feffery_antd_components',
                }
            },
        )

    @classmethod
    def info(
        cls,
        container_id: Optional[
            Union[str, Dict]
        ] = 'global-notification-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        bottom: Optional[int] = 24,
        className: Optional[str] = None,
        closeable: Optional[bool] = True,
        closeButton: Optional[Dict] = None,
        description: Optional[str] = None,
        duration: Optional[Union[float, int]] = 4.5,
        key: Optional[str] = None,
        message: Optional[str] = '请求成功',
        placement: Optional[
            Literal[
                'top',
                'bottom',
                'topLeft',
                'topRight',
                'bottomLeft',
                'bottomRight',
            ]
        ] = 'topRight',
        style: Optional[Dict] = None,
        top: Optional[int] = 24,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'bottom': bottom,
                        'className': className,
                        'closeable': closeable,
                        'closeButton': closeButton,
                        'description': description,
                        'duration': duration,
                        'key': key,
                        'message': message,
                        'placement': placement,
                        'style': style,
                        'top': top,
                        'type': 'info',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdNotification',
                    'namespace': 'feffery_antd_components',
                }
            },
        )

    @classmethod
    def success(
        cls,
        container_id: Optional[
            Union[str, Dict]
        ] = 'global-notification-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        bottom: Optional[int] = 24,
        className: Optional[str] = None,
        closeable: Optional[bool] = True,
        closeButton: Optional[Dict] = None,
        description: Optional[str] = None,
        duration: Optional[Union[float, int]] = 4.5,
        key: Optional[str] = None,
        message: Optional[str] = '请求成功',
        placement: Optional[
            Literal[
                'top',
                'bottom',
                'topLeft',
                'topRight',
                'bottomLeft',
                'bottomRight',
            ]
        ] = 'topRight',
        style: Optional[Dict] = None,
        top: Optional[int] = 24,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'bottom': bottom,
                        'className': className,
                        'closeable': closeable,
                        'closeButton': closeButton,
                        'description': description,
                        'duration': duration,
                        'key': key,
                        'message': message,
                        'placement': placement,
                        'style': style,
                        'top': top,
                        'type': 'success',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdNotification',
                    'namespace': 'feffery_antd_components',
                }
            },
        )

    @classmethod
    def warning(
        cls,
        container_id: Optional[
            Union[str, Dict]
        ] = 'global-notification-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        bottom: Optional[int] = 24,
        className: Optional[str] = None,
        closeable: Optional[bool] = True,
        closeButton: Optional[Dict] = None,
        description: Optional[str] = None,
        duration: Optional[Union[float, int]] = 4.5,
        key: Optional[str] = None,
        message: Optional[str] = '请求失败',
        placement: Optional[
            Literal[
                'top',
                'bottom',
                'topLeft',
                'topRight',
                'bottomLeft',
                'bottomRight',
            ]
        ] = 'topRight',
        style: Optional[Dict] = None,
        top: Optional[int] = 24,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'bottom': bottom,
                        'className': className,
                        'closeable': closeable,
                        'closeButton': closeButton,
                        'description': description,
                        'duration': duration,
                        'key': key,
                        'message': message,
                        'placement': placement,
                        'style': style,
                        'top': top,
                        'type': 'warning',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdNotification',
                    'namespace': 'feffery_antd_components',
                }
            },
        )

    @classmethod
    def error(
        cls,
        container_id: Optional[
            Union[str, Dict]
        ] = 'global-notification-container',
        id: Optional[Union[str, Dict]] = str(uuid4()),
        bottom: Optional[int] = 24,
        className: Optional[str] = None,
        closeable: Optional[bool] = True,
        closeButton: Optional[Dict] = None,
        description: Optional[str] = None,
        duration: Optional[Union[float, int]] = 4.5,
        key: Optional[str] = None,
        message: Optional[str] = '请求异常',
        placement: Optional[
            Literal[
                'top',
                'bottom',
                'topLeft',
                'topRight',
                'bottomLeft',
                'bottomRight',
            ]
        ] = 'topRight',
        style: Optional[Dict] = None,
        top: Optional[int] = 24,
        underCompatibilityMode: Optional[bool] = False,
    ):
        set_props(
            container_id,
            {
                'children': {
                    'props': {
                        'id': id,
                        'bottom': bottom,
                        'className': className,
                        'closeable': closeable,
                        'closeButton': closeButton,
                        'description': description,
                        'duration': duration,
                        'key': key,
                        'message': message,
                        'placement': placement,
                        'style': style,
                        'top': top,
                        'type': 'error',
                        'underCompatibilityMode': underCompatibilityMode,
                    },
                    'type': 'AntdNotification',
                    'namespace': 'feffery_antd_components',
                }
            },
        )
