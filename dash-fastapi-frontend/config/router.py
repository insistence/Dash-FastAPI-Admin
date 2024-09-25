class RouterConfig:
    """
    路由配置
    """

    WHITE_ROUTES_LIST = [
        {
            'path': '/login',
            'component': 'login',
        },
        {
            'path': '/forget',
            'component': 'forget',
        },
        {
            'path': '/register',
            'component': 'register',
        },
    ]

    CONSTANT_ROUTES = [
        {
            'path': '/login',
            'component': 'login',
            'name': 'Login',
            'hidden': True,
        },
        {
            'path': '/forget',
            'component': 'forget',
            'name': 'Forget',
            'hidden': True,
        },
        {
            'path': '/register',
            'component': 'register',
            'name': 'Register',
            'hidden': True,
        },
        {
            'path': '',
            'component': 'Layout',
            'name': '',
            'redirect': '/',
            'children': [
                {
                    'path': '/',
                    'component': 'dashboard',
                    'name': 'Index',
                    'meta': {
                        'title': '首页',
                        'icon': 'antd-dashboard',
                        'affix': True,
                    },
                }
            ],
        },
        {
            'path': 'user',
            'component': 'Layout',
            'hidden': True,
            'name': 'UserProfile',
            'redirect': 'noredirect',
            'children': [
                {
                    'path': 'profile',
                    'component': 'system.user.profile',
                    'name': 'Profile',
                    'meta': {'title': '个人资料'},
                }
            ],
        },
    ]
