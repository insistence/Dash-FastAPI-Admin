class CommonConstant:
    """
    常用常量

    WWW: www主域
    HTTP: http请求
    HTTPS: https请求
    """

    WWW = 'www.'
    HTTP = 'http://'
    HTTPS = 'https://'


class HttpStatusConstant:
    """
    返回状态码

    SUCCESS: 操作成功
    CREATED: 对象创建成功
    ACCEPTED: 请求已经被接受
    NO_CONTENT: 操作已经执行成功，但是没有返回数据
    MOVED_PERM: 资源已被移除
    SEE_OTHER: 重定向
    NOT_MODIFIED: 资源没有被修改
    BAD_REQUEST: 参数列表错误（缺少，格式不匹配）
    UNAUTHORIZED: 未授权
    FORBIDDEN: 访问受限，授权过期
    NOT_FOUND: 资源，服务未找到
    BAD_METHOD: 不允许的http方法
    CONFLICT: 资源冲突，或者资源被锁
    UNSUPPORTED_TYPE: 不支持的数据，媒体类型
    ERROR: 系统内部错误
    NOT_IMPLEMENTED: 接口未实现
    WARN: 系统警告消息
    """

    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    MOVED_PERM = 301
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    BAD_METHOD = 405
    CONFLICT = 409
    UNSUPPORTED_TYPE = 415
    ERROR = 500
    NOT_IMPLEMENTED = 501
    WARN = 601


class MenuConstant:
    """
    菜单常量

    TYPE_DIR: 菜单类型（目录）
    TYPE_MENU: 菜单类型（菜单）
    TYPE_BUTTON: 菜单类型（按钮）
    YES_FRAME: 是否菜单外链（是）
    NO_FRAME: 是否菜单外链（否）
    YES_CACHE: 是否缓存菜单（是）
    NO_CACHE: 是否缓存菜单（否）
    LAYOUT: Layout组件标识
    PARENT_VIEW: ParentView组件标识
    INNER_LINK: InnerLink组件标识
    SUB_MENU: 菜单类型（目录）标识
    ITEM: 菜单类型（菜单）标识
    """

    TYPE_DIR = 'M'
    TYPE_MENU = 'C'
    TYPE_BUTTON = 'F'
    YES_FRAME = 0
    NO_FRAME = 1
    YES_CACHE = 0
    NO_CACHE = 1
    LAYOUT = 'Layout'
    PARENT_VIEW = 'ParentView'
    INNER_LINK = 'InnerLink'
    SUB_MENU = 'SubMenu'
    ITEM = 'Item'


class SysJobStatusConstant:
    """
    任务状态常量

    NORMAL: 正常
    DISABLE: 暂停
    """

    NORMAL = '0'
    DISABLE = '1'


class SysNormalDisableConstant:
    """
    系统开关常量

    NORMAL: 正常
    DISABLE: 停用
    """

    NORMAL = '0'
    DISABLE = '1'


class SysNoticeStatusConstant:
    """
    通知状态常量

    NORMAL: 正常
    DISABLE: 关闭
    """

    NORMAL = '0'
    DISABLE = '1'


class SysNoticeTypeConstant:
    """
    通知类型常量

    NORMAL: 正常
    DISABLE: 关闭
    """

    NOTICE = '1'
    BULLETIN = '2'


class SysShowHideConstant:
    """
    菜单显隐常量

    SHOW: 正常
    HIDE: 暂停
    """

    SHOW = '0'
    HIDE = '1'


class SysYesNoConstant:
    """
    系统是否常量

    YES: 是
    NO: 否
    """

    YES = 'Y'
    NO = 'N'
